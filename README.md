# グローバルプロジェクト 2026 LP（CROSS BRIDGE デザイン版）

NPO法人EdFuture のオンライン探究プログラム「グローバルプロジェクト」のLP。
レイアウト体系は [crossfields.jp/crossbridge/](https://crossfields.jp/crossbridge/) を実測して起こしたものを踏襲し、
中身は `edfuture_gp_upload_server` と [edfuture.jp/global-page/](https://edfuture.jp/global-page/) の内容に全面差し替えしている。

## 見る

```bash
python3 -m http.server 8953 --directory ~/Desktop/EdFuture/edfuture-gp-crossbridge
# → http://localhost:8953/
```

`file://` で直接開くと動画とフォントが読めないので必ずサーバー経由で。

## 構成

```
index.html          全セクション（1ページ完結）
css/style.css       全スタイル（依存ゼロ）
js/common.js        依存ゼロJS：FAQ開閉／動画のクリック再生／アンカースクロール／タブレットviewport切替
fonts/              LINE Seed JP・LINE Seed Sans のサブセット（SIL OFL 1.1）
  _full/            サブセット化の元データ。★サーバーへのアップロード不要
  build-subset.py   文字を書き換えたら実行し直すスクリプト（後述）
img/                写真・アイコン・地球シルエットSVG
video/              紹介動画・ワールド寺子屋動画（faststart 済み）
.htaccess           圧縮・キャッシュ・_full/ の遮断
```

## セクション構成と原本の対応

| このLP | 原本（CROSS BRIDGE）の同型コンポーネント |
|---|---|
| KV | KV（水色地＋斜めの紺帯＋縦組み黄コピー＋写真コラージュ） |
| グローバルプロジェクトとは | intro（リード＋動画＋主催団体ボックス） |
| 3 KEY POINTS | 3 SESSIONS（左見出し＋黄チップ＋右写真） |
| FEATURES | FEATURES（水色カード2×2） |
| GOLDEN TICKET（ワールド寺子屋） | schedule の `koukai` カード（丸バッジ付き） |
| こんな人におすすめ | 6色カード＋丸型の顔写真 |
| GUEST（ゲスト講師） | ENCOUNTER（円形写真＋色付き見出し＋プロフィール） |
| VOICE（参加者の声） | ENCOUNTER と同型（見出し色のみ変更） |
| プログラム概要と応募方法 | outline_table |
| SCHEDULE | schedule（番号丸＋縦線タイムライン） |
| SCHOLARSHIP（奨学金） | FEATURES の水色カードを3列で流用 |
| まずはオンライン無料説明会へ | event ＋ entry（黄枠のENTRYブロック） |
| よくあるご質問 | FAQ（アコーディオン） |
| フッター | footer（白地・主催団体＋パートナー列） |

デザイントークンは原本の実測値そのまま。
`#30334f`（セクション地）／`#4b4e69`（ページ地・サブカード）／`#a0d8e5`（KV地・特徴カード）／
`#f7ee12`（アクセント黄）／`#fa8700`（CTAオレンジ）／角丸 7px／本文コンテンツ幅 810px／セクション幅 1100px。

## テキストを書き換えたときにやること（重要）

日本語フォントは **このLPで使う文字だけに絞ってある**（4.17MB → 408KB）。
本文に新しい漢字を足すとその字が豆腐（□）になるので、**必ず**次を実行する。

```bash
python3 fonts/build-subset.py
```

ひらがな・カタカナ・ASCII・約物は全部入れてあるので、かな書きの修正だけなら再実行は不要。

## 差し替えた素材

すべて `edfuture_gp_upload_server/images/` 由来。切り抜き写真は透明部分の外接矩形でトリミングし、
表示サイズの2倍を上限に縮小した（1319KB → 336KB）。

| ファイル | 用途 | 元 |
|---|---|---|
| `cut-p2085.webp` | KV中央の人物 | `IMG_2085.webp` |
| `cut-arata / chocho / zenji` | 参加者の声・おすすめカード | `Arata / Chocho / Zenji.webp` |
| `cut-p7777 / p9999` | おすすめカード | `IMG_7777 / IMG_9999.webp` |
| `guest-nakamura / shiba / norimoto / tanaka` | ゲスト講師 | `nakamura_sho` / `2026 GP Step 2,4,5` |
| `GP1 / GP2 / GP3` | KVコラージュ・セッション | 同名 |
| `point1 / point2 / point3` | FEATURES・セッション | 同名 |
| `video/gp-intro.mp4` | 紹介動画 | `LP GP.mp4` |
| `video/gp-terakoya.mp4` | ワールド寺子屋 | `優秀者セクション.mp4` |

動画は `ffmpeg -c copy -movflags +faststart` で moov を先頭に移動済み（再生開始が速くなる）。
初期表示ではポスター画像だけを出し、再生ボタンを押したときに mp4 を読み込む。

## フォント

原本は LINE Seed JP（本文・見出し）＋ arboria（英字ディスプレイ）の組み合わせ。
arboria は Adobe Fonts の有償書体のため、**LINE Seed Sans Bold** で代替した（字幅・ウェイトともほぼ一致）。
LINE Seed は SIL OFL 1.1 で商用利用・自己ホストとも可（`fonts/OFL-LINESeed.txt`）。

## 検証結果（2026-08-01）

| 幅 | 横スクロール | console | 404 | はみ出し要素 |
|---|---|---|---|---|
| 375 (SE) | 0 | 0 | 0 | 0 |
| 390 (iPhone 14) | 0 | 0 | 0 | 0 |
| 430 (Pro Max) | 0 | 0 | 0 | 0 |
| 768 / 820 (iPad) | 0 | 0 | 0 | 0 |
| 1280 (PC) | 0 | 0 | 0 | 0 |
| 1920 (PC) | 0 | 0 | 0 | 0 |

- 実描画フォント: LINE Seed JP Regular / Bold / LINE Seed Sans のみ。**フォールバック 0件**（CDP `CSS.getPlatformFontsForNode` で全テキスト要素を実測）
- 初期表示: **854.7KB / 20リクエスト**（フォント408KB・画像364KB・CSS44KB・HTML35KB・JS3KB）

### タブレットの扱い

原本と同じ2ブレークポイント設計（SP ≤480px ／ PC ≥1100px）のため、その中間幅は
`js/common.js` が viewport meta を `width=1200` に差し替えてPCレイアウトを縮小表示する（原本と同じ手法）。
**PCブラウザのウィンドウを1100px未満に狭めた場合だけは横スクロールが出る**（原本も同じ挙動）。

## 公開前に確認すること

1. **日程・締切が2026年度のまま**。募集期間 5/15〜7/12、説明会 6/18、実施 7/19〜10/25 は
   すべて元の `edfuture_gp_upload_server` と `edfuture.jp/global-page/` の記載をそのまま移したもの。
   次期の募集で使うなら日付・年度・人数の更新が要る。
2. **中村柾さんの英字表記「Sho Nakamura」は画像ファイル名 `nakamura_sho.webp` からの推定**。
   正式表記を確認して直すこと。他3名（Yutaro Shiba / Nana Norimoto / Yuki Tanaka）はファイル名に明記あり。
3. **公開URLが決まったら** `index.html` の `canonical` / `og:url` / `og:image` を実URLに差し替える。
   現在は `https://edfuture.jp/gp/` を仮置きしている。
4. **GA4 / Clarity の計測タグが未挿入**。必要なら `</head>` 直前に追加する。
5. 説明会・申込の遷移先は現行LPと同じ `https://forms.gle/VC6EL6qB272KM8mZ9`。公式LINEは `https://lin.ee/e29aXVo`。
6. `fonts/_full/` はアップロード不要（4.1MB）。`.htaccess` でも遮断しているが、
   FTPで上げるときは除外したほうが早い。

## 制作の出自

デザイン再現の元になった学習用の再現習作は
`~/Desktop/Web制作/サイト再現・クローン/crossbridge-study/` にある（原本スクショ・実測値・比較検証つき）。
