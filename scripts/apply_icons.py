#!/usr/bin/env python3
"""Apply custom icons onto an apktool-decoded Meeye tree.

usage: apply_icons.py <decoded_dir> <icons_dir>

icons_dir is the repo icons/ folder: 192px PNGs plus appfilter_snippet.xml
and drawable_snippet.xml. SVG sources in that folder are not packed.
"""
from __future__ import annotations

import os
import re
import shutil
import sys

# Source PNG in icons/ -> drawable name written into res/drawable-nodpi.
PNG_MAP = {
    "grok": "grok",
    "grok_bot": "grok_bot",
    "x_twitter": "x_twitter",
    "feiniu": "feiniu",
    "philips_sonicare": "philips_sonicare",
    "termius": "termius",
    "pilinara": "pilinara",
    "venera": "venera",
    "hail": "hail",
    "senplayer": "senplayer",
    "bilibili_white": "bilibili_white",
    "nrfr": "nrfr",
    "eskimo": "eskimo",
    "samsung_game_booster_plus": "samsung_game_booster_plus",
    "deepseek": "deepseek",
    "disney_plus": "disney_plus",
    "meituan": "meituan",
    "meituan_alt": "meituan_alt",
    "google_gemini": "google_gemini",
    "deepseek_alt": "deepseek_alt",
    "genshin_a": "genshin_a",
    "genshin_b": "genshin_b",
    "genshin_c": "genshin_c",
    "v2rayng_new": "v2rayng_new",
    "droid_ify_alt": "droid_ify_alt",
    "samsung_expert_raw": "samsung_expert_raw",
    "nothing_x": "nothing_x",
    "canta": "canta",
    "resplash": "resplash",
    "tiktok": "tiktok",
    "chatgpt": "chatgpt",
    "shenmezhidemai": "shenmezhidemai",
}

# (label, pattern, replacement). Counts must be non-zero or the upstream XML
# changed shape and the icon would silently stay on the old drawable.
REPOINTS = (
    (
        "twitter",
        re.compile(
            r'(ComponentInfo\{com\.twitter\.android/[^"]*\}"\s+drawable=")twitter(")'
        ),
        r"\1x_twitter\2",
    ),
    (
        "genshin",
        re.compile(
            r'(ComponentInfo\{com\.miHoYo\.(?:Yuanshen|GenshinImpact)/[^"]*\}"\s+drawable=")genshin_impact(")'
        ),
        r"\1genshin_a\2",
    ),
    (
        "tiktok",
        re.compile(
            r'(ComponentInfo\{com\.(?:zhiliaoapp\.musically|ss\.android\.ugc\.trill)/com\.ss\.android\.ugc\.aweme\.splash\.SplashActivity\}"\s+drawable=")douyin(")'
        ),
        r"\1tiktok\2",
    ),
    (
        "bilibili",
        re.compile(
            r'(ComponentInfo\{com\.bilibili\.app\.in/[^"]*\}"\s+drawable=")bilibili(")'
        ),
        r"\1bilibili_white\2",
    ),
)


def die(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(1)


def read_text(path: str) -> str:
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def write_text(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def snippet_items(path: str) -> str:
    text = re.sub(r"<!--.*?-->", "", read_text(path), flags=re.S)
    return "\n".join(
        line for line in text.splitlines() if line.strip().startswith("<item")
    )


def main() -> None:
    if len(sys.argv) != 3:
        die("usage: apply_icons.py <decoded_dir> <icons_dir>")
    decoded, icons = sys.argv[1], sys.argv[2]
    drawable_dir = os.path.join(decoded, "res", "drawable-nodpi")
    if not os.path.isdir(drawable_dir):
        die(f"missing {drawable_dir} (apktool did not produce drawable-nodpi)")

    old_gemini = os.path.join(drawable_dir, "google_gemini.png")
    if not os.path.isfile(old_gemini):
        die(f"missing {old_gemini}; cannot keep the previous Gemini icon")
    shutil.copy(old_gemini, os.path.join(drawable_dir, "google_gemini_old.png"))

    # ChatGPT and 什么值得买 are replaced in place; keep the pack originals as
    # unmapped *_old alternates. Copy BEFORE the PNG_MAP loop overwrites them.
    for base in ("chatgpt", "shenmezhidemai"):
        orig = os.path.join(drawable_dir, base + ".png")
        if not os.path.isfile(orig):
            die(f"missing {orig}; cannot keep the previous {base} icon")
        shutil.copy(orig, os.path.join(drawable_dir, base + "_old.png"))

    for src, name in PNG_MAP.items():
        png = os.path.join(icons, src + ".png")
        if not os.path.isfile(png):
            die(f"missing icon {png}")
        shutil.copy(png, os.path.join(drawable_dir, name + ".png"))

    entries = snippet_items(os.path.join(icons, "appfilter_snippet.xml"))
    # Existing com.twitter.android rows are re-pointed below. Drop snippet rows
    # for that package so StartActivity is not inserted a second time.
    entries = "\n".join(
        line for line in entries.splitlines() if "com.twitter.android" not in line
    )
    if not entries.strip():
        die("appfilter snippet produced no <item> entries")
    drawable_items = snippet_items(os.path.join(icons, "drawable_snippet.xml"))
    if not drawable_items.strip():
        die("drawable snippet produced no <item> entries")

    for rel in ("assets/appfilter.xml", "res/xml/appfilter.xml"):
        path = os.path.join(decoded, rel)
        if not os.path.isfile(path):
            die(f"missing {path}")
        text = read_text(path)
        for label, pattern, repl in REPOINTS:
            text, count = pattern.subn(repl, text)
            print(f"{rel}: repoint {label} x{count}")
            if count == 0:
                die(f"{rel}: expected to repoint {label}, matched nothing")
        if text.count("</resources>") != 1:
            die(f"{path} should contain exactly one </resources>")
        text = text.replace("</resources>", entries + "\n</resources>")
        write_text(path, text)

    latest = '<category title="Latest">'
    for rel in ("assets/drawable.xml", "res/xml/drawable.xml"):
        path = os.path.join(decoded, rel)
        if not os.path.isfile(path):
            die(f"missing {path}")
        text = read_text(path)
        if latest not in text:
            die(f"{path} has no {latest}")
        text = text.replace(latest, latest + "\n" + drawable_items, 1)
        write_text(path, text)
        print(f"{rel}: inserted Latest entries")

    print(f"applied {len(PNG_MAP)} icons")


if __name__ == "__main__":
    main()
