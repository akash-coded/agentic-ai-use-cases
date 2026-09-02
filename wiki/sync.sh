#!/usr/bin/env bash
# Seed or restore the GitHub wiki from wiki/*.md
#
# The wiki's git repo does not exist until the first page is created in the web
# UI. If this fails with "Repository not found", that is what has happened —
# create any page at the /wiki URL first, then re-run.
#
# This OVERWRITES the wiki. It is a seed/restore, not a sync.
set -euo pipefail

REPO="akash-coded/aws-bedrock-agentcore-strands"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

if ! command -v gh >/dev/null; then echo "needs the gh CLI"; exit 1; fi
TOKEN="$(gh auth token)"
URL="https://x-access-token:${TOKEN}@github.com/${REPO}.wiki.git"

echo "Cloning the wiki…"
if ! git clone --quiet "$URL" "$TMP/wiki" 2>/dev/null; then
  cat <<'MSG'

The wiki repository does not exist yet.

GitHub creates it only when the first page is saved in the web UI — there is no
API for this, and pushing to an unseeded wiki fails.

  1. Open  https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki
  2. Click "Create the first page", save anything at all
  3. Re-run this script

MSG
  exit 1
fi

# Scoreboard.md is owned by the Pulse workflow, not this seed — leave it alone
find "$TMP/wiki" -maxdepth 1 -name '*.md' ! -name 'Scoreboard.md' -delete
cp "$HERE"/*.md "$TMP/wiki/"
rm -f "$TMP/wiki/README.md"          # the seed README stays in the repo only

cd "$TMP/wiki"
if git diff --quiet && git diff --cached --quiet && [ -z "$(git status --porcelain)" ]; then
  echo "Wiki already matches the seed. Nothing to do."; exit 0
fi
git add -A
git commit --quiet -m "Seed wiki from repository wiki/ directory"
git push --quiet origin HEAD
echo "Pushed $(ls "$HERE"/*.md | grep -v README | wc -l | tr -d ' ') pages."
echo "https://github.com/${REPO}/wiki"
