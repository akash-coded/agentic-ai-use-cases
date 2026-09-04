#!/usr/bin/env python3
"""Offline tests for the contact relay. No AWS, no network: the boto3 clients are replaced with fakes.

    python site/contact-relay/test_handler.py
"""
from __future__ import annotations

import base64
import json
import os
import sys
from pathlib import Path

os.environ.update(TABLE_NAME="messages", NOTIFY_EMAIL="owner@example.com",
                  GITHUB_SECRET_NAME="skyways-contact-relay/github", PER_IP_LIMIT="3", DAILY_CAP="5")
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
import handler as relay  # noqa: E402


class ConditionalCheckFailedException(Exception):
    pass


class FakeDynamo:
    def __init__(self):
        self.items: dict[str, dict] = {}
        self.counts: dict[str, int] = {}

    def put_item(self, TableName, Item):
        self.items[Item["id"]["S"]] = Item

    def update_item(self, TableName, Key, UpdateExpression, **kw):
        key = Key["id"]["S"]
        if UpdateExpression.startswith("ADD"):
            cap = int(kw["ExpressionAttributeValues"][":cap"]["N"])
            if self.counts.get(key, 0) >= cap:
                raise ConditionalCheckFailedException()
            self.counts[key] = self.counts.get(key, 0) + 1
        else:
            for k, v in kw["ExpressionAttributeValues"].items():
                self.items[key][k[1:]] = v


class FakeSes:
    def __init__(self, fail=False):
        self.sent, self.fail = [], fail

    def send_email(self, **kw):
        if self.fail:
            raise RuntimeError("MessageRejected")
        self.sent.append(kw)


class FakeSecrets:
    def get_secret_value(self, SecretId):
        raise LookupError("ResourceNotFoundException")


def post(body, ip="203.0.113.7", method="POST", b64=False):
    raw = json.dumps(body) if not isinstance(body, str) else body
    if b64:
        raw = base64.b64encode(raw.encode()).decode()
    ev = {"requestContext": {"http": {"method": method, "sourceIp": ip}},
          "headers": {"user-agent": "test"}, "body": raw, "isBase64Encoded": b64}
    r = relay.handler(ev, None)
    return r["statusCode"], json.loads(r["body"])


def fresh(ses_fail=False):
    relay._seen.clear()
    relay._github = None
    relay._clients.clear()
    relay._clients.update({"dynamodb": FakeDynamo(), "sesv2": FakeSes(ses_fail), "secretsmanager": FakeSecrets()})
    return relay._clients


GOOD = {"name": "Ada", "email": "ada@example.com", "topic": "idea", "message": "Scenario 12 undercounts the retry cost."}


def test_method_and_body_guards():
    fresh()
    assert post({}, method="GET")[0] == 405
    assert post("{not json")[0] == 400
    assert post({"name": "x"})[0] == 400
    assert post({**GOOD, "email": "nope"})[0] == 400
    assert post({**GOOD, "message": "short"})[0] == 400
    assert post({**GOOD, "message": "x" * 5000})[0] == 400
    assert post({**GOOD, "name": 42})[0] == 400


def test_honeypot_is_swallowed():
    c = fresh()
    status, body = post({**GOOD, "website": "http://spam"})
    assert (status, body["ok"], body["id"]) == (200, True, "spam")
    assert not c["dynamodb"].items and not c["sesv2"].sent


def test_happy_path_stores_emails_and_flags():
    c = fresh()
    status, body = post(GOOD)
    assert status == 200 and body["ok"] and body["emailed"] and not body["mirrored"]
    item = c["dynamodb"].items[body["id"]]
    assert item["message"]["S"] == GOOD["message"] and item["topic"]["S"] == "idea"
    assert item["emailed"]["BOOL"] is True and item["issue"]["S"] == ""
    sent = c["sesv2"].sent[0]
    assert sent["ReplyToAddresses"] == ["ada@example.com"]
    assert sent["Content"]["Simple"]["Subject"]["Data"] == "[SkyWays Architect] idea from Ada"


def test_unknown_topic_becomes_other_and_base64_bodies_decode():
    c = fresh()
    status, body = post({**GOOD, "topic": "Rant"}, b64=True)
    assert status == 200 and c["dynamodb"].items[body["id"]]["topic"]["S"] == "other"


def test_email_failure_still_stores():
    c = fresh(ses_fail=True)
    status, body = post(GOOD)
    assert status == 200 and body["emailed"] is False
    assert c["dynamodb"].items[body["id"]]["emailed"]["BOOL"] is False


def test_per_ip_throttle():
    fresh()
    codes = [post(GOOD, ip="198.51.100.1")[0] for _ in range(4)]
    assert codes == [200, 200, 200, 429]
    assert post(GOOD, ip="198.51.100.2")[0] == 200


def test_daily_cap():
    fresh()
    codes = [post(GOOD, ip=f"192.0.2.{i}")[0] for i in range(7)]
    assert codes == [200] * 5 + [429, 429]


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"{len(tests)} tests passed")
