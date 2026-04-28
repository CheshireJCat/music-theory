#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/nekos/daily/music-theory"
REMOTE_URL="https://github.com/CheshireJCat/music-theory"
BRANCH="main"

cd "$ROOT"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not a git repository: $ROOT" >&2
  exit 1
fi

current_branch="$(git branch --show-current || true)"
if [[ -z "$current_branch" ]]; then
  git checkout -B "$BRANCH"
elif [[ "$current_branch" != "$BRANCH" ]]; then
  git branch -M "$BRANCH"
fi

if git remote get-url origin >/dev/null 2>&1; then
  existing_remote="$(git remote get-url origin)"
  if [[ "$existing_remote" != "$REMOTE_URL" ]]; then
    git remote set-url origin "$REMOTE_URL"
  fi
else
  git remote add origin "$REMOTE_URL"
fi

git add README.md lessons assets scripts .gitignore .github-sync.md

if git diff --cached --quiet; then
  echo "No music-theory content changes to commit."
else
  commit_date="$(date '+%Y-%m-%d')"
  git commit -m "Add music theory lesson updates ${commit_date}"
fi

git fetch origin "$BRANCH" >/dev/null 2>&1 || true

if git show-ref --verify --quiet "refs/remotes/origin/$BRANCH"; then
  git branch --set-upstream-to="origin/$BRANCH" "$BRANCH" >/dev/null 2>&1 || true
  git pull --rebase origin "$BRANCH"
fi

git push -u origin "$BRANCH"
