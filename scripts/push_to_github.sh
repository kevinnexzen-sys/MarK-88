#!/bin/bash
set -e
REPO_URL="$1"
if [ -z "$REPO_URL" ]; then
  echo "Usage: ./scripts/push_to_github.sh https://github.com/USER/REPO.git"
  exit 1
fi
git init
git add .
git commit -m "MARK v8.1 full system"
git remote add origin "$REPO_URL"
git branch -M main
git push -u origin main
