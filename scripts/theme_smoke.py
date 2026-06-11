# -*- coding: utf-8 -*-
"""theme smoke test (설계서 #2026-071 11.4) — 토큰·CSS 생성 1회 확인."""

from yulee_common import DARK_TOKENS, __version__
from yulee_common.theme.css import build_css

assert DARK_TOKENS["color.bg"] == "#1A1D2E"
assert DARK_TOKENS["color.accent"] == "#C9A961"
css = build_css(mode="dark")
assert ":root" in css and ".yl-card" in css
print(f"yulee-common {__version__} - theme tokens OK")
