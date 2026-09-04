# Contact relay

The backend for the site's contact form: a Lambda Function URL that stores each message, e-mails it to you,
and mirrors it into a private GitHub repository. Infrastructure as code, one command to deploy, nothing to
keep running, and comfortably inside the AWS free tier at contact-form volumes.

```
visitor's browser ── POST JSON ──▶ Lambda Function URL (CORS locked to the site's origin)
                                        │
                                        ├─▶ DynamoDB      every message, first, so nothing is lost
                                        ├─▶ SES           e-mail to you, reply-to set to the visitor
                                        └─▶ GitHub        issue in the private inbox repo (optional)
```

| File | Purpose |
| --- | --- |
| [`template.yaml`](template.yaml) | The stack: table, SES identity, log group, function, URL, least-privilege policy |
| [`src/handler.py`](src/handler.py) | The function. Standard library plus boto3; no packages to install |
| [`test_handler.py`](test_handler.py) | Offline tests with fake AWS clients: `python site/contact-relay/test_handler.py` |
| [`deploy.sh`](deploy.sh) | Package and deploy with the AWS CLI |

## Deploy

Sign the AWS CLI in to **your own** account, then:

```bash
cd site/contact-relay
NOTIFY_EMAIL=mfs.akash@gmail.com ALLOWED_ORIGIN=https://akash-coded.github.io ./deploy.sh
```

Then, in order:

1. **Verify the sender.** SES e-mails a verification link to `NOTIFY_EMAIL` when the identity is created.
   Click it. Until you do, messages are stored but not e-mailed, and the log says `notify failed … MessageRejected`.
2. **Point the site at the relay.** Copy the `FunctionUrl` output into `contact.endpoint` in
   [`../frame/config.js`](../frame/config.js) and push. Pages rebuilds in about a minute.
3. **Send yourself a test message** from the live site. It should arrive within seconds, with the visitor's
   address in reply-to, and appear as a row in the DynamoDB table.

Re-running `deploy.sh` updates the stack in place. To remove it: `aws cloudformation delete-stack --stack-name
skyways-contact-relay`. The table is kept on delete (it holds your messages); drop it yourself when you are sure.

## The private GitHub mirror

Messages can also become issues in **`akash-coded/inbox`**, a private repository that already exists with the
labels the relay uses (`contact-form` plus the topic). Issues give you threads, labels, closing, search, and
a place a private project board can auto-add from (board → Workflows → Auto-add → this repository).

The relay needs one secret to do this, and it must be **yours to create**:

1. GitHub → Settings → Developer settings → Personal access tokens → **Fine-grained tokens** → Generate.
   Repository access: *Only select repositories* → `inbox`. Permissions: *Issues → Read and write*. Nothing else.
   Expiry: a year is reasonable; the relay simply stops mirroring when it lapses and keeps e-mailing.
2. Store it in Secrets Manager in the relay's region under the name the stack expects (default
   `skyways-contact-relay/github`), as JSON with two keys. Use the console, or write the JSON to a file so the
   token never lands in shell history:

   ```bash
   printf '{"token":"%s","repo":"akash-coded/inbox"}' "$(cat token.txt)" > github.json
   aws secretsmanager create-secret --name skyways-contact-relay/github --secret-string file://github.json
   rm -P github.json token.txt
   ```

3. Nothing to redeploy. The function reads the secret on its next cold start (or within a few minutes).

Why not a GitHub Action in the public repository? Because anything the site could trigger there without a
secret is public, and a workflow that receives the message would print it into public run logs. A private
repository written to by a token that lives only in your AWS account keeps the message private end to end.

## What is stored, and where

Each accepted message is one DynamoDB item: id, timestamp, name, e-mail, topic, message, the page it was
sent from, the visitor's network address and user agent (for abuse tracing), whether the e-mail went out,
and the mirrored issue URL. Nothing is written to CloudWatch Logs except ids, outcomes and error class names.
Delete a message by deleting the item; the table has point-in-time recovery for the other direction.

## Abuse controls

- CORS on the Function URL admits one origin: the site's.
- Honeypot field: bots that fill it get a cheerful 200 and nothing is stored.
- Size limits: 16 KB body, 4,000-character message, validated e-mail address.
- Per-address window: five messages per ten minutes per warm container.
- Global daily cap (default 300, below the SES sandbox limit of 200 e-mails a day plus headroom for
  stored-only messages), counted atomically in DynamoDB. Beyond it the relay answers 429 and stores nothing.
- Optional reserved concurrency (`ReservedConcurrency` parameter) if your account's Lambda limit allows it.

## Cost

Lambda, DynamoDB on-demand, SES and Secrets Manager together cost a few cents a month at the volume a contact
form sees, and the first several thousand requests fall inside the always-free tier. The only fixed cost is
the Secrets Manager secret if you create it (about $0.40 a month). There is no server to leave running.

## Prefer a hosted form?

Set `contact.endpoint` in [`../frame/config.js`](../frame/config.js) to a Formspree form URL, or to
`https://api.web3forms.com/submit` with `accessKey` filled in. The form sends the same JSON fields either way.
You lose the private log and the reply-to header, and gain not having an AWS account in the loop.
