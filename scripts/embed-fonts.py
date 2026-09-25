#!/usr/bin/env python3
"""Embed fonts/*.woff2 into theme.css as base64, between the FONTS:GENERATED markers.

The community installer only fetches theme.css and manifest.json, and Obsidian's
theme policy bans network requests, so the font has to live inside the stylesheet.
Usage: python3 scripts/embed-fonts.py
"""
import base64
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
FACES = [  # file, unicode-range
    ("nunito-latin-800.woff2", "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"),
    ("nunito-cyrillic-800.woff2", "U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116"),
]

blocks = []
for name, urange in FACES:
    data = base64.b64encode((ROOT / "fonts" / name).read_bytes()).decode()
    blocks.append(
        "@font-face {\n  font-family: Nunito;\n"
        f"  src: url(\"data:font/woff2;base64,{data}\") format(\"woff2\");\n"
        "  font-weight: 800;\n  font-style: normal;\n  font-display: swap;\n"
        f"  unicode-range: {urange};\n}}\n")

css = (ROOT / "theme.css").read_text()
start = "/* FONTS:GENERATED:START — produced by scripts/embed-fonts.py, do not hand-edit */"
end = "/* FONTS:GENERATED:END */"
css = re.sub(re.escape(start) + r".*?" + re.escape(end),
             lambda _: start + "\n" + "\n".join(blocks) + end, css, flags=re.S)
(ROOT / "theme.css").write_text(css)
print(f"embedded {len(FACES)} faces")
