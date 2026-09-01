#!/usr/bin/env bash
# Runs once, when the container is created.
#
# Deliberately minimal: every L.A.B. lab is stdlib-only and offline, so the
# environment is usable the moment the container starts. The heavy curriculum
# dependencies (boto3, langchain, strands, litellm …) are opt-in via `lab deps`,
# because most people want to start with a lab, not wait for a wheel to build.
set -euo pipefail

echo "▸ Installing the 'lab' command…"
sudo tee /usr/local/bin/lab >/dev/null <<'EOF'
#!/usr/bin/env bash
# Thin wrapper so you can type `lab next` instead of the full path.
ROOT="$(git -C "${PWD}" rev-parse --show-toplevel 2>/dev/null || echo /workspaces/aws-bedrock-agentcore-strands)"
case "${1:-}" in
  deps)
    echo "Installing the full curriculum dependencies (a few minutes)…"
    pip install --quiet --upgrade pip
    pip install --quiet -r "$ROOT/requirements.txt"
    echo "Done. Notebooks under modules/ will now run."
    ;;
  ""|help|-h|--help)
    python3 "$ROOT/labs/runner/labctl.py" --help
    ;;
  *)
    exec python3 "$ROOT/labs/runner/labctl.py" "$@"
    ;;
esac
EOF
sudo chmod +x /usr/local/bin/lab

# Tab-completion for lab ids and subcommands
sudo tee /etc/bash_completion.d/lab >/dev/null <<'EOF'
_lab_complete() {
  local cur prev root
  cur="${COMP_WORDS[COMP_CWORD]}"; prev="${COMP_WORDS[COMP_CWORD-1]}"
  root="$(git rev-parse --show-toplevel 2>/dev/null || echo /workspaces/aws-bedrock-agentcore-strands)"
  if [ "$COMP_CWORD" -eq 1 ]; then
    COMPREPLY=($(compgen -W "list next show start run break submit progress grade verify index deps" -- "$cur"))
  elif [[ "$prev" =~ ^(show|start|run|break|submit)$ ]]; then
    COMPREPLY=($(compgen -W "$(ls "$root"/labs/catalog/*/ -d 2>/dev/null | xargs -n1 basename | tr '\n' ' ')" -- "$cur"))
  fi
}
complete -F _lab_complete lab
EOF

echo "▸ Verifying the lab catalog…"
python3 labs/runner/labctl.py verify

echo "▸ Ready. Nothing else to install for the labs."
