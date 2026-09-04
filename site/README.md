# The site: SkyWays Architect on GitHub Pages

**Live:** https://akash-coded.github.io/aws-bedrock-agentcore-strands/

SkyWays Architect is an interactive walk-through of one agentic feature, a disruption assistant for a
fictional airline, taken through the agentic PDLC: six architect decisions, thirty-eight scenarios, the
artefacts each team produces, and role-by-role deep dives (product manager, solution architect, engineering
and QA) from P0 to P3. It is an original work and the intellectual property of **Akash Das**, open-sourced
under the repository's [MIT Licence](../LICENSE) for knowledge and experience sharing.

## How the site is put together

| Path | What it is |
| --- | --- |
| [`app/SkyWays-Architect.html`](app/SkyWays-Architect.html) | **The tool, pristine.** A single self-contained file with no external dependencies. It is never edited here. |
| [`build.py`](build.py) | Copies the tool to `_site/index.html` and injects, at the document boundaries only, the metadata and the site frame. Refuses to build if the tool's own bytes changed. |
| [`frame/`](frame/) | The layer around the tool: [`config.js`](frame/config.js) (links, contact delivery), [`frame.js`](frame/frame.js) (attribution, licence and disclaimer, ideas invitation, contact drawer), [`frame.css`](frame/frame.css). Everything is prefixed `sw-` and appended to the end of `<body>`. |
| [`assets/`](assets/) | Favicon and the social preview image. |
| [`contact-relay/`](contact-relay/) | Optional AWS backend for the contact form: Lambda Function URL, DynamoDB, SES, and a private GitHub mirror. Infrastructure as code, one command to deploy. |
| [`404.html`](404.html) | Custom not-found page. |
| [`../.github/workflows/pages.yml`](../.github/workflows/pages.yml) | Builds and deploys on every push that touches `site/`. |

The frameless tool is also published, unchanged, at
[`app/SkyWays-Architect.html`](https://akash-coded.github.io/aws-bedrock-agentcore-strands/app/SkyWays-Architect.html)
for full-screen sessions and embedding.

## Updating the tool

Replace `site/app/SkyWays-Architect.html` with the new export and push. That is the whole procedure; the
frame, metadata and contact form are layered on at build time.

## Preview locally

```bash
python site/build.py
python -m http.server -d site/_site 8000
```

Then open http://localhost:8000/. Add `?contact` to the URL to open the contact drawer directly.

## The contact form

The form has three delivery modes, chosen in [`frame/config.js`](frame/config.js):

| `contact.endpoint` | What happens when a visitor presses Send |
| --- | --- |
| empty (default) | The visitor's own mail app opens with the message addressed and ready. Works everywhere, needs nothing. |
| the relay's Function URL | The message is e-mailed to the owner, stored in DynamoDB, and mirrored as an issue in the private `akash-coded/inbox` repository. See [`contact-relay/`](contact-relay/). |
| a Formspree or Web3Forms URL | The hosted service e-mails the owner. Set `accessKey` for Web3Forms. |

The visitor is told which mode is active, in the drawer's consent line. Messages are never published.

## Attribution and reuse

Keep the copyright notice and attribution when you reuse the tool or any part of it. Ideas, corrections and
disagreements belong in the [ideas thread](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/101);
the ones that ship are credited in the [changelog](../CHANGELOG.md).
