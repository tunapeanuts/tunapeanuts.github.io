#!/usr/bin/env python3
"""読点「，」の使い方を点検する。使い方: ./lint_commas.py [files...]（省略時は articles/*.html）

読点を打ってよいのは次の2つだけ。
  1. 話の切り出し: 「まず，」「例えば，」「ただし，」。「一方Xでは，」のように修飾が続く場合は後ろに打つ。
  2. 並列: 「A，B，C」「Xし，Yする」。
文を区切るだけの読点は不要。ここでは疑わしいものを機械的に拾う。最終判断は人が行う。
"""
import re, sys
from pathlib import Path

OPENERS = ["まず","次に","その後は","最後に","例えば","そこで","ただし","また","なお","つまり",
           "ちなみに","さらに","しかし","そのため","一方","もちろん","当然","かなりざっくり言えば",
           "これによって","これまでは"]
# 文を区切るだけになりやすい直前の語
SUSPECT = re.compile(r"(場合|ため|ように|ければ|れば|と|ば|は|が|に|を|で|も)$")

def text_of(src):
    src = re.sub(r"<(script|style|head).*?</\1>", "", src, flags=re.S)
    return re.sub(r"<[^>]+>", "\n", src)

def lint(path):
    n = 0
    for ln, line in enumerate(text_of(Path(path).read_text(encoding="utf-8")).split("\n"), 1):
        for sent in re.split(r"(?<=[．。])", line):
            parts = sent.split("，")
            if len(parts) < 2:
                continue
            notes = []
            if len(parts) > 3:
                notes.append(f"1文に読点{len(parts)-1}個")
            for i, p in enumerate(parts[:-1]):
                p = p.strip()
                if i == 0 and any(p.endswith(o) or p == o for o in OPENERS):
                    continue
                if SUSPECT.search(p) and not re.search(r"[A-Za-z0-9）)]$", p):
                    notes.append(f"「…{p[-8:]}，」は区切りだけでは？")
            if notes:
                n += 1
                print(f"{path}:{ln}: {'; '.join(notes)}\n    {sent.strip()}")
    return n

files = sys.argv[1:] or sorted(map(str, Path(__file__).parent.glob("articles/*.html")))
total = sum(lint(f) for f in files)
print(f"要確認: {total} 文")
