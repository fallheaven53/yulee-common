# -*- coding: utf-8 -*-
"""yulee_common.theme — 율이공방 디자인 시스템 (설계서 #2026-071)."""

from .apply import apply_style, toggle_mode, get_current_mode
from .components import header, sidebar_brand, card, metric_row
from .css import build_css, inject_font, inject_layout_helpers
from .tokens import (
    DARK_TOKENS, LIGHT_TOKENS, SPACING, RADIUS, TYPO,
    PLOTLY_TEMPLATE_DARK, get_tokens,
)
# Tkinter (v0.3.0) — tk 서브패키지는 tkinter를 함수 내부에서만 import하므로
# tkinter 없는 환경(Streamlit Cloud 등)에서도 이 import는 안전하다.
from .tk import (
    apply_tk_style, toggle_tk_mode, get_current_tk_mode,
    resolve_font_family, get_tk_typo, install_check,
    header_tk, card_tk,
)

__all__ = [
    "apply_style", "toggle_mode", "get_current_mode",
    "header", "sidebar_brand", "card", "metric_row",
    "build_css", "inject_font", "inject_layout_helpers",
    "DARK_TOKENS", "LIGHT_TOKENS", "SPACING", "RADIUS", "TYPO",
    "PLOTLY_TEMPLATE_DARK", "get_tokens",
    "apply_tk_style", "toggle_tk_mode", "get_current_tk_mode",
    "resolve_font_family", "get_tk_typo", "install_check",
    "header_tk", "card_tk",
]
