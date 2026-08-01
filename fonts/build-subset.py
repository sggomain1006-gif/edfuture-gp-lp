#!/usr/bin/env python3
"""
LINE Seed JP / LINE Seed Sans をこのLPで実際に使う文字だけに絞る（サブセット化）。

なぜ必要か
    LINE Seed JP のフルセットは 1面あたり約 2.1MB（woff2）ある。
    日本語LPの転送量はほぼフォントで決まるため、ここを削るのが最も効く。

使い方
    index.html のテキストを書き換えたら、必ずこれを実行し直す。
        python3 fonts/build-subset.py

    実行すると fonts/*.subset.woff2 が再生成され、css/style.css の @font-face が
    参照しているファイルが更新される。原本（フルセット）は fonts/_full/ に残す。

含める文字
    ① index.html に出てくる全文字
    ② ひらがな・カタカナ全部（テキスト微修正で欠字にならないように）
    ③ ASCII と日本語で使う約物・記号
    ここに無い漢字を後から本文に足すと豆腐（□）になるので、必ず再実行すること。
"""
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "fonts"
FULL_DIR = FONT_DIR / "_full"
HTML = ROOT / "index.html"

FACES = [
    ("LINESeedJP_OTF_Rg.woff2", "LINESeedJP_OTF_Rg.subset.woff2"),
    ("LINESeedJP_OTF_Bd.woff2", "LINESeedJP_OTF_Bd.subset.woff2"),
    ("LINESeedSans_W_Bd.woff2", "LINESeedSans_W_Bd.subset.woff2"),
]

# ② かな全域 ③ ASCII・約物
ALWAYS = set()
ALWAYS |= {chr(c) for c in range(0x3041, 0x309F + 1)}   # ひらがな
ALWAYS |= {chr(c) for c in range(0x30A0, 0x30FF + 1)}   # カタカナ
ALWAYS |= {chr(c) for c in range(0x0020, 0x007F)}       # ASCII（U+0020 の空白を必ず含める）
ALWAYS |= set("　、。，．・：；？！゛゜´｀¨＾￣＿ヽヾゝゞ〃仝々〆〇ー―‐／＼〜‖｜…‥"
              "‘’“”（）〔〕［］｛｝〈〉《》「」『』【】＋－±×÷＝≠＜＞≦≧∞∴♂♀°′″"
              "℃￥＄￠￡％＃＆＊＠§☆★○●◎◇◆□■△▲▽▼※〒→←↑↓〓"
              "０１２３４５６７８９")


def used_chars() -> set:
    src = HTML.read_text(encoding="utf-8")
    # コメント・script・style を除去してから、タグを剥がす
    src = re.sub(r"<!--.*?-->", "", src, flags=re.S)
    src = re.sub(r"<script.*?</script>", "", src, flags=re.S)
    src = re.sub(r"<style.*?</style>", "", src, flags=re.S)
    # alt / title / content 属性の文言も描画されうるので拾っておく
    attrs = " ".join(re.findall(r'(?:alt|title|content|aria-label)="([^"]*)"', src))
    body = re.sub(r"<[^>]+>", " ", src)
    text = body + " " + attrs
    text = text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    return {c for c in text if not unicodedata.category(c).startswith("C")}


def main() -> int:
    try:
        from fontTools import subset  # noqa: F401
    except ImportError:
        print("fonttools が必要です:  pip3 install fonttools brotli", file=sys.stderr)
        return 1

    FULL_DIR.mkdir(exist_ok=True)
    charset = sorted(used_chars() | ALWAYS)
    unicodes = ",".join(f"U+{ord(c):04X}" for c in charset)
    print(f"対象文字数: {len(charset)}")

    total_before = total_after = 0
    for full_name, out_name in FACES:
        src = FULL_DIR / full_name
        if not src.exists():
            # 初回実行時はフルセットを _full/ へ退避する
            here = FONT_DIR / full_name
            if not here.exists():
                print(f"  !! {full_name} が見つかりません（fonts/ か fonts/_full/ に置いてください）")
                return 1
            here.replace(src)

        out = FONT_DIR / out_name
        cmd = [
            sys.executable, "-m", "fontTools.subset", str(src),
            f"--unicodes={unicodes}",
            "--flavor=woff2",
            "--layout-features=*",
            "--no-hinting",
            "--desubroutinize",
            "--name-IDs=*",
            f"--output-file={out}",
        ]
        subprocess.run(cmd, check=True)
        before, after = src.stat().st_size, out.stat().st_size
        total_before += before
        total_after += after
        print(f"  {full_name:28s} {before/1024:8.1f}KB -> {after/1024:7.1f}KB  ({after/before*100:.1f}%)")

    print(f"  {'合計':28s} {total_before/1024:8.1f}KB -> {total_after/1024:7.1f}KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
