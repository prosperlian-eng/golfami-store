# GOLFAMI オンラインストア 引き継ぎ書

最終更新: 2026-08-21

## これは何か

親子ゴルフYouTube「GOLFAMI」(@family_golf) のアフィリエイト用オンラインストア。
「物を売る店」ではなく「**応援ページ**」がコンセプト。買う人が親子の夢のスポンサーになる構図。

- **正式URL（設定中）**: https://golfami.jp/
- **旧URL**: https://prosperlian-eng.github.io/golfami-store/
- **公開リポジトリ**: https://github.com/prosperlian-eng/golfami-store （public）
- **ソースの場所**: `/Users/yusuke/golfami-store/`

> ⚠️ **知識ベース本体（prosperlian-eng/YUSUKE）は絶対に公開しないこと。**
> works/legal/ に弁護士相談資料・医療情報が入っている。ストアは別リポジトリにしてある。

---

## 🔴 今すぐ知るべきこと（2026-08-21 時点で未完了）

### ドメイン切替が途中で、**サイトが一時的に見られない**

**状況**:
- golfami.jp のDNS設定（GitHub PagesのIP 4つ + www）は投入済み → Xserverの権威DNSでは正しく引ける
- ネームサーバーも `ns1〜3.xdomain.ne.jp` に変更済み（whoisには反映済み）
- **しかしJPレジストリ側の委任情報がまだ `ns1〜5.xserver.jp` のまま**＝一般のDNSからは名前が引けない
- GitHub PagesにCNAME(golfami.jp)を設定したため、**旧URLは golfami.jp へ301転送される**
- 結果: **golfami.jp も旧URLも、今は開けない**

**放置してよいか**: JPレジストリへの反映は通常数時間で完了する。完了すれば自動的に両方生きる。
バックグラウンドで見張りスクリプトを走らせてあり、浸透を検知したらHTTPS証明書の発行を待って
`https_enforced=true` まで自動で仕上げる設計（`scratchpad/domain_watch.sh`。ただしセッション終了で消える）。

**もし急いで復旧したいなら**（サイトを今すぐ見せたい場合の応急処置）:
```bash
# GitHub Pagesのカスタムドメインを一旦外す → 旧URLが復活する
gh api -X PUT repos/prosperlian-eng/golfami-store/pages -f cname=""
# DNS浸透後に戻す
gh api -X PUT repos/prosperlian-eng/golfami-store/pages -f cname=golfami.jp
```
※ 外した場合、リポジトリの `CNAME` ファイルも一旦消さないとpush時に再設定されるので注意。

**浸透確認コマンド**:
```bash
dig +short NS golfami.jp @a.dns.jp     # ns1-3.xdomain.ne.jp になれば委任OK
dig +short A golfami.jp @8.8.8.8       # 185.199.10x.153 が返ればDNS浸透OK
curl -sI https://golfami.jp/ | head -1 # 200になれば完了
gh api repos/prosperlian-eng/golfami-store/pages --jq '{cname:.cname,https:.https_enforced,cert:.https_certificate.state}'
```
証明書が `approved`/`issued` になったら:
```bash
gh api -X PUT repos/prosperlian-eng/golfami-store/pages -F https_enforced=true
```

---

## アカウント情報

| 用途 | 情報 |
|---|---|
| Googleアカウント | prosper.lian@gmail.com（**Chromeのプロファイル指定が毎回ハマる。迷ったら本人に聞く**） |
| GitHub | prosperlian-eng |
| Xserverドメイン | アカウントID phrs495744 / 契約者 村田佑輔 / golfami.jp は2027-07-31まで自動更新 |
| 楽天アフィリエイト | 楽天IDでログイン。今月実績: 売上22,878円・報酬1,269円・クリック124 |
| Amazonアソシエイト | **StoreID: golfami-22**。今月実績: クリック80・注文2・紹介料175円 |
| YouTube | @family_golf / channel_id UC2KiF7XifrmpRlvxrTpsZgg / 登録5,600人・動画1,303本 |

---

## 掲載商品と、その裏付け

| # | 商品 | 楽天 | Amazon(ASIN) | 紹介動画 | 関係 |
|---|---|---|---|---|---|
| 1位 | ボイスキャディ スイングスティック SS10 (19,800円) | a.r10.to/hgrf5z | B0H3YY2C1N | 革命的な素振り棒 `dfZsW1cBXao` **50万回** | メーカー提供 |
| 2位 | STEAD 冷感ポンチョ (5,478円・**料率20%**) | a.r10.to/hFef20 | B0FGCFJQZ3 | SNSで噂の冷感アイテム `hxsa6JwYJKI` | 自分で購入 |
| 3位 | ボイスキャディ T12 PRO (52,000円〜) | a.r10.to/hktj1U | B0G1LMCHT7 | 新型ゴルフナビT12PRO `3o0OgMpHcX4` | メーカー提供 |
| — | ボイスキャディ SL mini (41,800円〜) | a.r10.to/h5p7F2 | B0G4659MCZ | （専用回なし） | メーカー提供 |
| — | ボイスキャディ SC200+ (24,200円) | a.r10.to/h56J59 | B0GJ2X4RNG | トラックマン比較 `MtPev9FDZdk` | メーカー提供 |
| — | バランススティック | （販売準備中・動画のみ） | — | 日本未発売の素振り棒 `JeBiKIVcoG4` | タイアップ |
| — | テーラーメイド Qi4D (86,240円〜) | a.r10.to/hRilGO | B0G8FGXN8V | Qi4D試打 `W3OIcS67UVY` | — |
| — | ARGOLF アーサー（パター） | a.r10.to/h5nizs（一覧） | 取扱なし | 元シングル親父パター数激減 `santuCaaO_k` | — |
| — | 空調服 ファン付き (9,790円) | a.r10.to/hgIUCr | B0GRZMFWFX | EFFLORESCENCE空調服 `vH1iKxt0LZs` | ※代替品と明記 |

**空調服の注意**: 動画で着ているのはEFFLORESCENCE製だが現在販売がないため、代わりに人気の同タイプ
(BALANCEDESIGN)を紹介している。カードにその旨を明記済み。**提供/自腹のタグは未設定**（本人確認待ち）。

---

## 法令・規約対応（**勝手に消さないこと**）

一次情報を当たって実装済み。詳細は `dialogues/2026-07-30-GOLFAMIアフィリLP.md` の8/2追記。

1. **最上部の「広告・PR」帯**（山吹地・2行固定）
   - 消費者庁の運用基準Q13が「文字のサイズや色なども踏まえ明瞭であること」を要求
   - 楽天アフィリはファーストビューでの表示を必須としている
2. **商品ごとの関係性タグ**（メーカー提供／タイアップ／自分で購入）
   - 同Q13の「一部を見ただけでも明瞭に」への対応
3. **フッターの「広告・PRについて」一式**
   - **Amazonの定型文「Amazonのアソシエイトとして、GOLFAMIは適格販売により収入を得ています。」は規約上の義務**
4. **rel="nofollow sponsored"** を全アフィリリンクに付与

**注意**: 2026/4/20のAmazon規約改定で、**Amazonリンクへの有料広告・ブースト広告は不適格販売**になった。
インスタのリール広告等にAmazonリンクを使わないこと。楽天リンクを広告に使う件も規約確認が未了（ideas.mdのリマインド参照）。

---

## 自動で動いている仕組み

**新着動画の自動更新** — 新しい動画は何もしなくても翌朝ページに載る。
- `.github/workflows/update-videos.yml` が毎朝6時(JST)に実行
- `scripts/update_latest.py` がチャンネルRSSを読んで `assets/latest.json` を更新
- ページのJSがそれを読んで「新着動画」欄に最新3本を表示
- 手動実行: `gh workflow run update-videos.yml -R prosperlian-eng/golfami-store`

**自動化できないもの**: 新商品のアフィリリンク作成（本人アカウントでの操作が必要）。
新しいギア紹介動画が出たら、楽天アフィリにログインしたChromeを開いてもらえば5分で追加できる。

---

## 直し方

```bash
cd /Users/yusuke/golfami-store
# index.html を編集
git add -A && git commit -m "..." && git push
# 1〜2分で公開に反映される
```

画像は `assets/` に入っている（全て自サイト内。外部依存なし）。
動画サムネは `assets/t-<動画ID>.jpg` の命名。新しく足すときは:
```bash
curl -sf -o assets/t-<ID>.jpg "https://i.ytimg.com/vi/<ID>/maxresdefault.jpg"
sips -s format jpeg -s formatOptions 78 -Z 720 assets/t-<ID>.jpg --out assets/t-<ID>.jpg
```

---

## 残っている宿題

1. **ドメイン切替の完了確認**（上記🔴参照）— 最優先
2. **空調服の提供/自腹の区分**を本人に確認してタグを付ける
3. **アクセス解析が未設置**（GA4等）。どの商品のどのボタンが押されたか取れていない＝改善の材料がない
4. **日焼け止め・氷嚢・キャディバッグ**は専用の紹介動画がなく未掲載。撮れば追加できる
5. インスタのプロフィール／YouTube概要欄へのURL掲載（ドメイン確定後）

---

## 設計の意図（変えるときは読んで）

- **商品を絞る**のが売りの構造。「動画で紹介した物だけ」という制約が信頼の source になっている
- **楽天/Amazonのボタン色は固定**（#BF0000 / #232F3E）。認知色なので変えると押される率が落ちる
- **「先に、正直な話」ブロック**がこのページの心臓。本人の言葉「同じ買い物なら応援になるので、
  もし気になった商品があれば、ここから購入してもらえたら嬉しいです」から作った
- 夢セクション（親父をセントアンドリュースへ）が感情の山場。ここだけ明朝体
- デザインは3案作って3視点で審査した結果の「雑誌風」ベース。経緯は dialogues/2026-07-30 参照
