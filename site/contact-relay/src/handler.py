"""Contact relay for the SkyWays Architect site.

A browser posts JSON to this function's URL. The function validates the message, stores it in DynamoDB,
e-mails the owner through SES (with reply-to set to the visitor), and, if a GitHub secret exists, opens an
issue in a private repository so the message also lands somewhere it can be triaged.

Design notes
- No third-party packages: boto3 ships with the Lambda runtime; GitHub is called with urllib.
- Message bodies are never logged. CloudWatch sees ids, outcomes and error class names only.
- Preflight (OPTIONS) is answered by the Function URL's own CORS configuration, not by this code.
- Abuse limits: a per-address window inside each warm container, a global daily cap kept in DynamoDB,
  a honeypot field, and hard size limits.
- The message is stored before anything else is attempted, so a failed e-mail or mirror loses nothing.
"""
from __future__ import annotations

import base64
import json
import os
import re
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone

SITE = os.environ.get("SITE_NAME", "SkyWays Architect")
TABLE = os.environ.get("TABLE_NAME", "")
NOTIFY = os.environ.get("NOTIFY_EMAIL", "")
SECRET = os.environ.get("GITHUB_SECRET_NAME", "")
PER_IP = int(os.environ.get("PER_IP_LIMIT", "5"))
DAILY_CAP = int(os.environ.get("DAILY_CAP", "300"))
WINDOW_SECONDS = 600
MAX_BODY_BYTES = 16_000
LIMITS = {"name": 120, "email": 200, "topic": 40, "message": 4000, "page": 200}
TOPICS = ("idea", "question", "collaboration", "bug", "other")
EMAIL_RE = re.compile(r"^[^@\s]{1,64}@[^@\s]+\.[A-Za-z0-9-]{2,}$")

_seen: dict[str, list[float]] = {}          # per-address timestamps, per warm container
_clients: dict[str, object] = {}            # lazily created boto3 clients (tests inject fakes)
_github: dict | None = None                 # cached secret; {} once we know it is unavailable


def client(name: str):
    """boto3 is imported lazily so the module loads, and the tests run, without AWS."""
    if name not in _clients:
        import boto3  # pylint: disable=import-outside-toplevel

        _clients[name] = boto3.client(name)
    return _clients[name]


def reply(status: int, body: dict) -> dict:
    return {"statusCode": status, "headers": {"content-type": "application/json"}, "body": json.dumps(body)}


def clean(payload: object) -> tuple[dict | None, str | None]:
    """Return (message, None) or (None, reason). Reason 'spam' means the honeypot was filled."""
    if not isinstance(payload, dict):
        return None, "body must be a JSON object"
    if payload.get("website"):
        return None, "spam"
    out: dict[str, str] = {}
    for key, limit in LIMITS.items():
        value = payload.get(key, "")
        if not isinstance(value, str):
            return None, f"{key} must be text"
        value = value.strip()
        if len(value) > limit:
            return None, f"{key} is too long (at most {limit} characters)"
        out[key] = value
    if not out["name"]:
        return None, "a name is required"
    if not EMAIL_RE.match(out["email"]):
        return None, "a valid e-mail address is required"
    if len(out["message"]) < 10:
        return None, "the message is too short"
    out["topic"] = out["topic"].lower() if out["topic"].lower() in TOPICS else "other"
    return out, None


def throttled(ip: str, now: float | None = None) -> bool:
    now = now if now is not None else time.time()
    hits = [t for t in _seen.get(ip, []) if now - t < WINDOW_SECONDS]
    if len(hits) >= PER_IP:
        _seen[ip] = hits
        return True
    hits.append(now)
    _seen[ip] = hits
    return False


def under_daily_cap(day: str) -> bool:
    """Atomically count today's accepted messages; False once the cap is reached."""
    try:
        client("dynamodb").update_item(
            TableName=TABLE,
            Key={"id": {"S": f"quota#{day}"}},
            UpdateExpression="ADD n :one",
            ConditionExpression="attribute_not_exists(n) OR n < :cap",
            ExpressionAttributeValues={":one": {"N": "1"}, ":cap": {"N": str(DAILY_CAP)}},
        )
        return True
    except Exception as exc:  # noqa: BLE001 - boto3 raises generated exception classes
        if type(exc).__name__ == "ConditionalCheckFailedException":
            return False
        raise


def _attr(value: object) -> dict:
    return {"BOOL": value} if isinstance(value, bool) else {"S": str(value)}


def store(item: dict) -> None:
    client("dynamodb").put_item(TableName=TABLE, Item={k: _attr(v) for k, v in item.items()})


def flag(item_id: str, **fields: object) -> None:
    names = {f"#{k}": k for k in fields}
    values = {f":{k}": _attr(v) for k, v in fields.items()}
    client("dynamodb").update_item(
        TableName=TABLE,
        Key={"id": {"S": item_id}},
        UpdateExpression="SET " + ", ".join(f"#{k} = :{k}" for k in fields),
        ExpressionAttributeNames=names,
        ExpressionAttributeValues=values,
    )


def notify(item: dict) -> bool:
    if not NOTIFY:
        return False
    subject = f"[{SITE}] {item['topic']} from {item['name']}"
    text = (
        f"{item['message']}\n\n-- \n{item['name']} <{item['email']}>\n"
        f"topic: {item['topic']}\npage: {item['page'] or '-'}\nreceived: {item['ts']}\nid: {item['id']}\n"
    )
    try:
        client("sesv2").send_email(
            FromEmailAddress=NOTIFY,
            Destination={"ToAddresses": [NOTIFY]},
            ReplyToAddresses=[item["email"]],
            Content={"Simple": {
                "Subject": {"Data": subject, "Charset": "UTF-8"},
                "Body": {"Text": {"Data": text, "Charset": "UTF-8"}},
            }},
        )
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"notify failed id={item['id']} error={type(exc).__name__}")
        return False


def github_config() -> dict:
    """The mirror's settings, read once per warm container. Empty dict when the mirror is off."""
    global _github  # noqa: PLW0603
    if _github is None:
        _github = {}
        if SECRET:
            try:
                raw = client("secretsmanager").get_secret_value(SecretId=SECRET)["SecretString"]
                cfg = json.loads(raw)
                if cfg.get("token") and cfg.get("repo"):
                    _github = {"token": cfg["token"], "repo": cfg["repo"]}
            except Exception as exc:  # noqa: BLE001
                print(f"github mirror off: {type(exc).__name__}")
    return _github


def mirror(item: dict) -> str:
    """Open an issue in the private repository; returns its URL, or '' if the mirror is off or failed."""
    cfg = github_config()
    if not cfg:
        return ""
    body = (
        f"**From:** {item['name']} <{item['email']}>\n**Topic:** {item['topic']}\n"
        f"**Page:** {item['page'] or '-'}\n**Received:** {item['ts']}\n**Id:** `{item['id']}`\n\n---\n\n{item['message']}\n"
    )
    req = urllib.request.Request(
        f"https://api.github.com/repos/{cfg['repo']}/issues",
        data=json.dumps({"title": f"{item['topic']}: {item['name']}", "body": body,
                         "labels": ["contact-form", item["topic"]]}).encode(),
        headers={
            "Authorization": f"Bearer {cfg['token']}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "skyways-contact-relay",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=6) as resp:  # noqa: S310 - fixed https host
            return json.loads(resp.read().decode()).get("html_url") or ""
    except Exception as exc:  # noqa: BLE001
        print(f"mirror failed id={item['id']} error={type(exc).__name__}")
        return ""


def handler(event: dict, context: object = None) -> dict:  # noqa: ARG001
    http = (event.get("requestContext") or {}).get("http") or {}
    if http.get("method", "POST") != "POST":
        return reply(405, {"ok": False, "error": "POST only"})
    raw = event.get("body") or ""
    if event.get("isBase64Encoded"):
        raw = base64.b64decode(raw).decode("utf-8", "replace")
    if len(raw) > MAX_BODY_BYTES:
        return reply(413, {"ok": False, "error": "message too large"})
    try:
        payload = json.loads(raw or "{}")
    except ValueError:
        return reply(400, {"ok": False, "error": "body must be JSON"})

    data, err = clean(payload)
    if err == "spam":
        return reply(200, {"ok": True, "id": "spam"})  # bots learn nothing
    if err:
        return reply(400, {"ok": False, "error": err})

    ip = http.get("sourceIp", "?")
    if throttled(ip):
        return reply(429, {"ok": False, "error": "too many messages from this network right now; try again in ten minutes"})
    now = datetime.now(timezone.utc)
    if not under_daily_cap(now.strftime("%Y-%m-%d")):
        return reply(429, {"ok": False, "error": "the inbox is full for today; please try again tomorrow"})

    item = {
        "id": uuid.uuid4().hex,
        "ts": now.isoformat(timespec="seconds"),
        **data,
        "ip": ip,
        "ua": ((event.get("headers") or {}).get("user-agent") or "")[:200],
        "status": "new",
        "emailed": False,
        "issue": "",
    }
    store(item)                                   # durable first
    emailed = notify(item)
    issue = mirror(item)
    if emailed or issue:
        flag(item["id"], emailed=emailed, issue=issue)
    print(f"stored id={item['id']} topic={item['topic']} emailed={emailed} mirrored={bool(issue)}")
    return reply(200, {"ok": True, "id": item["id"], "emailed": emailed, "mirrored": bool(issue)})
