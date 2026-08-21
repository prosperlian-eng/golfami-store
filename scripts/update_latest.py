#!/usr/bin/env python3
"""GOLFAMIチャンネルのRSSから最新動画を取得し assets/latest.json を更新する。
GitHub Actionsが毎日実行する。変更があった時だけコミットされる。"""
import json, re, urllib.request

RSS = "https://www.youtube.com/feeds/videos.xml?channel_id=UC2KiF7XifrmpRlvxrTpsZgg"
OUT = "assets/latest.json"

xml = urllib.request.urlopen(RSS, timeout=30).read().decode()
entries = re.findall(r"<entry>(.*?)</entry>", xml, re.S)
videos = []
for e in entries[:6]:
    vid = re.search(r"<yt:videoId>([^<]+)</yt:videoId>", e)
    title = re.search(r"<title>([^<]+)</title>", e)
    pub = re.search(r"<published>([^<]+)</published>", e)
    if vid and title and pub:
        videos.append({"id": vid.group(1), "title": title.group(1), "date": pub.group(1)[:10]})

if len(videos) >= 3:  # RSSが壊れている時は既存を守る
    json.dump(videos, open(OUT, "w"), ensure_ascii=False, indent=1)
    print(f"updated: {len(videos)} videos")
else:
    print("skip: rss too small")
