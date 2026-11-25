#!/usr/bin/env python3
"""articles/*.html の <title> と meta description から index.html を生成する。"""
import html, re, datetime
from pathlib import Path

root = Path(__file__).parent
# 既存の日付は index.html から引き継ぐ（記事を編集しても変わらない）
old = re.findall(r'<a href="articles/([^"]+)">[^<]*</a><time>([^<]*)</time>',
                 (root / "index.html").read_text(encoding="utf-8")
                 if (root / "index.html").exists() else "")
dates = {n: d for n, d in old}
order = {n: i for i, (n, _) in enumerate(old)}
items = []
for p in (root / "articles").glob("*.html"):
    s = p.read_text(encoding="utf-8")
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    d = re.search(r'<meta\s+name="description"\s+content="(.*?)"', s, re.S)
    day = dates.get(p.name) or str(datetime.date.fromtimestamp(p.stat().st_mtime))
    items.append(((day, -order.get(p.name, -1)), p.name,
                  t.group(1).strip() if t else p.stem,
                  d.group(1).strip() if d else ""))
items.sort(reverse=True)  # 日付が新しい順（同日は新規が先，既存は元の順）

rows = "\n".join(
    f'<li><a href="articles/{n}">{t}</a>'
    f'<time>{m[0]}</time>'
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
a{{color:#254d77}}
.note{{margin-top:3em;font-size:.9rem;color:#444}}
.note h2{{font-size:1rem;margin:0 0 .3em}}
.note ul{{padding-left:1.2em;margin:0}}
.note li{{padding:0;border:0}}
li p{{margin:.3em 0 0;color:#666b73;font-size:.95rem}}
</style></head><body>
<h1>Tips</h1>
<ul>
{rows}
</ul>
<div class="note">
<h2>留意事項</h2>
<ul>
<li>これは筆者自身のメモであり，内容の正確性は保証しない．</li>
<li>予告なく内容を変更したり，公開をやめたりすることがある．</li>
<li>誤りや不備があれば，<a href="https://github.com/tunapeanuts/tunapeanuts.github.io/issues/new">GitHub の Issue</a> で教えてほしい（GitHub のアカウントが必要で，内容は公開される）．</li>
</ul>
</div>
</body></html>
""", encoding="utf-8")
print(f"index.html: {len(items)} articles")
