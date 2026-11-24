#!/usr/bin/env python3
"""articles/*.html の <title> と meta description から index.html を生成する。"""
import html, re, datetime
from pathlib import Path

root = Path(__file__).parent
items = []
for p in (root / "articles").glob("*.html"):
    s = p.read_text(encoding="utf-8")
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    d = re.search(r'<meta\s+name="description"\s+content="(.*?)"', s, re.S)
    items.append((p.stat().st_mtime, p.name,
                  t.group(1).strip() if t else p.stem,
                  d.group(1).strip() if d else ""))
items.sort(reverse=True)  # 更新が新しい順

rows = "\n".join(
    f'<li><a href="articles/{n}">{t}</a>'
    f'<time>{datetime.date.fromtimestamp(m)}</time>'
    f'<p>{d}</p></li>'
    for m, n, t, d in items)

(root / "index.html").write_text(f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tips</title>
<style>
body{{margin:0 auto;max-width:760px;padding:48px 24px;font:16px/1.8 system-ui,"Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif;color:#202124}}
h1{{font-size:2rem;margin:0 0 1.5em}}
ul{{list-style:none;padding:0}}
li{{padding:1em 0;border-bottom:1px solid #dce0e4}}
li a{{font-size:1.2rem;font-weight:700;color:#254d77}}
time{{float:right;color:#666b73;font-size:.85rem}}
li p{{margin:.3em 0 0;color:#666b73;font-size:.95rem}}
</style></head><body>
<h1>Tips</h1>
<ul>
{rows}
</ul>
</body></html>
""", encoding="utf-8")
print(f"index.html: {len(items)} articles")
