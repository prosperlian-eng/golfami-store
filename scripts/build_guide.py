#!/usr/bin/env python3
"""articles/*.md から guide/*.html と guide/index.html を作る。
記事の書式: 先頭に --- で囲んだ項目(title,date,summary,product,price,video,relation,rakuten,amazon)、本文は ## 見出し・- 箇条書き・段落。
relation: provided=メーカー提供 / own=自分で購入 / tieup=タイアップ / none=なし(調べて紹介)"""
import glob, html, os, re

REL = {"provided": "メーカー提供", "own": "自分で購入", "tieup": "タイアップ", "none": "調べて紹介（使ってはいません）"}
CSS = """
:root{--cream:#FBF7F0;--ink:#33291F;--sub:#7A6E5F;--brown:#3E2B20;--terra:#C0603A;--terra-deep:#A84E2B;--sun:#E9B44C;--line:#EADFD0;--rakuten:#BF0000;--amazon:#232F3E}
*{box-sizing:border-box}body{margin:0;background:var(--cream);color:var(--ink);font:400 15px/2.0 "Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic",Meiryo,sans-serif;letter-spacing:.02em;-webkit-text-size-adjust:100%}
.pr{background:var(--sun);color:#3a2a10;font-size:13px;line-height:1.5;padding:8px 16px;text-align:center}.pr span{display:block}
.wrap{max-width:720px;margin:0 auto;padding:0 16px 56px}
header.top{padding:18px 0 8px}header.top a{color:var(--brown);font-weight:700;text-decoration:none}
h1{font-weight:700;font-size:22px;line-height:1.5;margin:20px 0 8px;color:var(--brown)}h2{font-weight:700;font-size:18px;margin:32px 0 8px;color:var(--brown);border-left:5px solid var(--terra);padding-left:10px}
.meta{color:var(--sub);font-size:13px}.chip{display:inline-block;background:#fff;border:1px solid var(--line);border-radius:99px;padding:2px 10px;font-size:12px;margin-right:6px}
.video{position:relative;padding-top:56.25%;margin:20px 0;background:#000;border-radius:12px;overflow:hidden}.video iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.card{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px;margin:24px 0}.card b{display:block;margin-bottom:4px}
.btns{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px}.btn{flex:1 1 140px;text-align:center;color:#fff;text-decoration:none;font-weight:700;border-radius:10px;padding:14px 8px}
.btn.rakuten{background:var(--rakuten)}.btn.amazon{background:var(--amazon)}
ul{padding-left:1.3em}li{margin:4px 0}
.verdict{background:#fff;border:2px solid var(--terra);border-radius:16px;padding:16px;margin:18px 0 8px}.verdict .lab{display:inline-block;background:var(--terra-deep);color:#fff;font-size:13px;border-radius:6px;padding:2px 10px;margin-bottom:6px}.verdict p{margin:4px 0 0;font-weight:700;color:var(--brown)}.verdict .pr2{color:var(--sub);font-size:14px;font-weight:500}
.pc{display:grid;grid-template-columns:1fr;gap:10px;margin:16px 0}.pc div{background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px 14px}.pc b{display:block;margin-bottom:2px}.pc .g b{color:#2E7D4F}.pc .bd b{color:var(--terra-deep)}.pc ul{margin:0}
@media(min-width:600px){.pc{grid-template-columns:1fr 1fr}}
.sticky{position:fixed;left:0;right:0;bottom:0;background:rgba(255,255,255,.97);border-top:1px solid var(--line);padding:8px 12px calc(8px + env(safe-area-inset-bottom));display:flex;gap:8px;align-items:center;z-index:9}.sticky span{flex:1;font-size:13px;line-height:1.4;font-weight:700;color:var(--brown)}.sticky a{flex:0 0 auto;padding:10px 14px;font-size:14px}
body.has-sticky{padding-bottom:72px}
.rel h2{margin-top:40px}
.list a{display:block;background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px;margin:12px 0;color:inherit;text-decoration:none}.list b{color:var(--brown)}
footer{border-top:1px solid var(--line);margin-top:40px;padding-top:16px;color:var(--sub);font-size:13px;line-height:1.8}
"""
PR = '<div class="pr"><span>広告・PR｜アフィリエイト広告を利用しています</span><span>メーカーから提供を受けた商品を含みます</span></div>'
FOOT = ('<footer><p><b>広告・PRについて</b><br>本ページはアフィリエイト広告（楽天アフィリエイト・Amazonアソシエイト）を利用しています。'
        '「メーカー提供」「タイアップ」と表示した商品は、メーカー等から商品の提供または対価を受けて紹介しています。'
        '「調べて紹介」と表示した商品は、私たちは使っていません。<br>'
        'Amazonのアソシエイトとして、GOLFAMIは適格販売により収入を得ています。<br>'
        '掲載の価格は紹介時点のおおよその目安です。最新の価格・在庫は各ショップの商品ページでご確認ください。<br>'
        '運営: GOLFAMI 親子ゴルフチャンネル</p></footer>')

def head(title, desc, path, ld=""):
    return (f'<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(title)}｜GOLFAMI</title><meta name="description" content="{html.escape(desc)}">'
            f'<link rel="canonical" href="https://www.golfami.jp/{path}"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:type" content="article"><meta property="og:url" content="https://www.golfami.jp/{path}"><meta property="og:image" content="https://www.golfami.jp/assets/ogp.jpg"><meta name="twitter:card" content="summary_large_image">{ld}<link rel="icon" href="../assets/logo-circle.jpg">'
            f'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap" rel="stylesheet">'
            f'<style>{CSS}</style></head><body>{PR}<div class="wrap"><header class="top"><a href="../">GOLFAMI オンラインストア</a> ／ <a href="./">紹介記事</a></header>')

def parse(path):
    t = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S)
    meta = dict(re.match(r"(\w+):\s*(.*)", l).groups() for l in m.group(1).splitlines() if ":" in l)
    return meta, m.group(2).strip()

def body_html(md):
    out, ul = [], False
    for line in md.splitlines():
        if line.startswith("- "):
            if not ul: out.append("<ul>"); ul = True
            out.append(f"<li>{html.escape(line[2:])}</li>"); continue
        if ul: out.append("</ul>"); ul = False
        if line.startswith("## "): out.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.strip(): out.append(f"<p>{html.escape(line)}</p>")
    if ul: out.append("</ul>")
    return "\n".join(out)

def buttons(m):
    b = []
    if m.get("rakuten"): b.append(f'<a class="btn rakuten" href="{html.escape(m["rakuten"])}" rel="nofollow sponsored">楽天で見る</a>')
    if m.get("amazon"): b.append(f'<a class="btn amazon" href="{html.escape(m["amazon"])}" rel="nofollow sponsored">Amazonで見る</a>')
    return '<div class="btns">' + "".join(b) + "</div>" if b else ""

os.makedirs("guide", exist_ok=True)
items = []
for p in sorted(glob.glob("articles/*.md")):
    slug = os.path.basename(p)[:-3]
    m, md = parse(p)
    rel = REL.get(m.get("relation", "none"), REL["none"])
    import json as _j
    ld = {"@context":"https://schema.org","@graph":[
      {"@type":"Article","headline":m["title"],"description":m.get("summary",""),"datePublished":m["date"],"dateModified":m["date"],
       "author":{"@type":"Organization","name":"GOLFAMI 親子ゴルフチャンネル","url":"https://www.youtube.com/@family_golf"},
       "publisher":{"@type":"Organization","name":"GOLFAMI","logo":{"@type":"ImageObject","url":"https://www.golfami.jp/assets/logo-circle.jpg"}},
       "image": f"https://i.ytimg.com/vi/{m['video']}/hqdefault.jpg" if m.get("video") else "https://www.golfami.jp/assets/ogp.jpg",
       "mainEntityOfPage": f"https://www.golfami.jp/guide/{slug}.html"},
      {"@type":"BreadcrumbList","itemListElement":[
       {"@type":"ListItem","position":1,"name":"GOLFAMI オンラインストア","item":"https://www.golfami.jp/"},
       {"@type":"ListItem","position":2,"name":"紹介記事","item":"https://www.golfami.jp/guide/"},
       {"@type":"ListItem","position":3,"name":m["product"],"item":f"https://www.golfami.jp/guide/{slug}.html"}]}]}
    page = head(m["title"], m.get("summary", ""), f"guide/{slug}.html", '<script type="application/ld+json">'+_j.dumps(ld,ensure_ascii=False)+'</script>')
    page = page.replace("<body>", '<body class="has-sticky">', 1)
    page += f'<h1>{html.escape(m["title"])}</h1><p class="meta"><span class="chip">{html.escape(rel)}</span>{html.escape(m["date"])}</p>'
    if m.get("verdict"):
        page += (f'<div class="verdict"><span class="lab">この記事の結論</span><p>{html.escape(m["verdict"])}</p>'
                 f'<span class="pr2">{html.escape(m["product"])}｜{html.escape(m.get("price",""))}</span>{buttons(m)}</div>')
    if m.get("good") or m.get("bad"):
        li = lambda k: "".join(f"<li>{html.escape(x)}</li>" for x in m.get(k, "").split("|") if x)
        page += f'<div class="pc"><div class="g"><b>良かった点</b><ul>{li("good")}</ul></div><div class="bd"><b>気になる点</b><ul>{li("bad")}</ul></div></div>'
    card = (f'<div class="card"><b>{html.escape(m["product"])}</b>{html.escape(m.get("price",""))}'
             f'<br><small>{html.escape(rel)}の商品です。価格と在庫は変わります。</small>{buttons(m)}</div>')
    bh = body_html(md)
    parts = bh.split("<h2>")
    if len(parts) > 3:  # 2つ目の見出しの後に1回目の購入カード（最後まで読まない人向け）
        bh = "<h2>".join(parts[:3]) + card + "<h2>" + "<h2>".join(parts[3:])
    page += bh
    if m.get("video"):
        page += f'<div class="video"><iframe src="https://www.youtube.com/embed/{html.escape(m["video"])}" loading="lazy" allowfullscreen title="紹介動画"></iframe></div>'
    page += card
    page += "<!--REL-->" + FOOT + "</div>"
    if m.get("rakuten"):
        page += f'<div class="sticky"><span>{html.escape(m["product"])}</span><a class="btn rakuten" href="{html.escape(m["rakuten"])}" rel="nofollow sponsored">楽天で見る</a></div>'
    page += "</body></html>"
    items.append((m["date"], slug, m, page))

items.sort(key=lambda x: (x[0], x[1]), reverse=True)
for d, slug, m, page in items:
    others = [x for x in items if x[1] != slug][:3]
    rel_html = '<div class="rel"><h2>ほかの紹介記事</h2><div class="list">' + "".join(f'<a href="{s}.html"><b>{html.escape(mm["title"])}</b></a>' for _, s, mm, _ in others) + "</div></div>"
    open(f"guide/{slug}.html", "w", encoding="utf-8").write(page.replace("<!--REL-->", rel_html))
items = [(d, s, m) for d, s, m, _ in items]
idx = head("紹介記事", "GOLFAMIが動画で紹介してきたゴルフ道具の紹介記事。", "guide/") + "<h1>紹介記事</h1><p class='meta'>買わせるためではなく、本当に役立つかを正直に書いています。</p><div class='list'>"
for d, slug, m in items:
    idx += f'<a href="{slug}.html"><b>{html.escape(m["title"])}</b><br><span class="meta">{html.escape(d)}｜{html.escape(REL.get(m.get("relation","none"),""))}</span><br>{html.escape(m.get("summary",""))}</a>'
idx += "</div>" + FOOT + "</div></body></html>"
open("guide/index.html", "w", encoding="utf-8").write(idx)
print("built", len(items), "articles")

# トップページの「紹介記事」欄（新しい順に3本）
import re as _re
top = open("index.html", encoding="utf-8").read()
cards = []
for d, slug, m in [x for x in items if x[2].get("video")][:3]:
    thumb = f'<img src="https://i.ytimg.com/vi/{html.escape(m["video"])}/hqdefault.jpg" alt="" width="480" height="360" loading="lazy">' if m.get("video") else '<img src="assets/logo-circle.jpg" alt="" width="480" height="360" loading="lazy">'
    cards.append(f'      <a class="latest-card reveal" href="guide/{slug}.html"><span class="latest-thumb">{thumb}</span><span class="latest-title">{html.escape(m["title"])}</span><span class="latest-date">{html.escape(REL.get(m.get("relation","none"),""))}</span></a>')
top = _re.sub(r"<!-- GUIDE-START -->.*?<!-- GUIDE-END -->", "<!-- GUIDE-START -->\n" + "\n".join(cards) + "\n<!-- GUIDE-END -->", top, flags=_re.S)
open("index.html", "w", encoding="utf-8").write(top)

# sitemap.xml と robots.txt
urls = ["https://www.golfami.jp/", "https://www.golfami.jp/guide/"] + [f"https://www.golfami.jp/guide/{s}.html" for _, s, _ in items]
lm = {f"https://www.golfami.jp/guide/{s}.html": d for d, s, _ in items}
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{u}</loc>" + (f"<lastmod>{lm[u]}</lastmod>" if u in lm else "") + "</url>\n" for u in urls) + "</urlset>\n"
open("sitemap.xml", "w").write(xml)
open("robots.txt", "w").write("User-agent: *\nAllow: /\nSitemap: https://www.golfami.jp/sitemap.xml\n")
