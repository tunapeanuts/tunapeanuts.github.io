#!/usr/bin/env bash
# 使い方: ./publish.sh ["コミットメッセージ"]
set -e
cd "$(dirname "$0")"
./lint_commas.py || true   # 読点の警告（止めはしない）
python3 build_index.py
git add -A
git commit -m "${1:-Update articles}" || { echo "変更なし"; exit 0; }
git push
