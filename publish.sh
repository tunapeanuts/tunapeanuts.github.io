#!/usr/bin/env bash
# 使い方: ./publish.sh ["コミットメッセージ"]
set -e
cd "$(dirname "$0")"
python3 build_index.py
git add -A
git commit -m "${1:-Update articles}" || { echo "変更なし"; exit 0; }
git push
