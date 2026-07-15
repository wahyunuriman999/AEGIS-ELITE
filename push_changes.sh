#!/usr/bin/env bash
# Bash script to initialize git, commit, and push changes
# Usage: ./push_changes.sh <remote-url> [branch]
set -e
REMOTE_URL="$1"
BRANCH="${2:-main}"
if [ -z "$REMOTE_URL" ]; then
  echo "Usage: $0 <remote-url> [branch]"
  exit 2
fi
if [ ! -d .git ]; then
  git init
  git add .
  git commit -m "CI: add Docker build/push, API hardening, tests, migrations, studio proxy"
  git branch -M "$BRANCH"
  git remote add origin "$REMOTE_URL"
else
  git add .
  git commit -m "CI: add Docker build/push, API hardening, tests, migrations, studio proxy" || echo "No changes to commit"
fi

echo "Pushing to $REMOTE_URL ($BRANCH)..."
git push -u origin "$BRANCH"
