# -*- coding: utf-8 -*-
"""theme smoke test — v0.4.0 토큰·CSS·폰트 생성 1회 확인 (#2026-079)."""

from yulee_common import __version__, LIGHT_TOKENS
from yulee_common.theme.css import build_css, inject_font

assert __version__ == "0.4.0", __version__
assert LIGHT_TOKENS["color.bg"] == "#F5EFE0"      # 한지 베이지
assert LIGHT_TOKENS["color.primary"] == "#2C5973"  # 청자

css = build_css()
assert ":root" in css
assert "--color-bg: #F5EFE0;" in css
assert ".yl-card" in css and ".yulee-badge--primary" in css

font = inject_font()
assert "@font-face" in font and "data:font/woff2;base64," in font
assert "cdn.jsdelivr.net" not in font             # 외부 CDN 의존 없음

print(f"yulee-common {__version__} - theme v0.4.0 OK (한국 전통색 + Pretendard 로컬)")
