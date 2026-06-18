# -*- coding: utf-8 -*-
"""yulee_common.theme — 율이공방 디자인 시스템 v0.4.0 (설계서 #2026-079).

한국 전통색 라이트 토큰 + Pretendard 로컬 폰트. 공개 함수 시그니처 불변.
v0.3.x의 DARK_TOKENS·PLOTLY_TEMPLATE_DARK 는 소프트 폐기(접근 시 DeprecationWarning).
"""

from .apply import apply_style, toggle_mode, get_current_mode
from .components import (
    header, sidebar_brand, card, metric_row,
    kpi_card, badge, status_dot,
)
from .css import build_css, inject_font, inject_layout_helpers, font_face_css
from .tokens import (
    LIGHT_TOKENS, SPACING, RADIUS, SHADOW, TYPO, BUTTON_SIZE,
    FONT_STACK, CHART_SEQUENCE, PLOTLY_TEMPLATE, get_tokens,
)
# Tkinter (v0.3.0) — tk 서브패키지는 tkinter를 함수 내부에서만 import하므로
# tkinter 없는 환경(Streamlit Cloud 등)에서도 이 import는 안전하다.
from .tk import (
    apply_tk_style, toggle_tk_mode, get_current_tk_mode,
    resolve_font_family, get_tk_typo, install_check,
    header_tk, card_tk,
)

# v0.3.x 폐기 심볼 — eager import 하지 않고 접근 시점에만 경고 후 alias 반환.
_DEPRECATED_NAMES = {"DARK_TOKENS", "PLOTLY_TEMPLATE_DARK"}


def __getattr__(name):
    if name in _DEPRECATED_NAMES:
        from . import tokens
        return getattr(tokens, name)  # tokens.__getattr__ 가 DeprecationWarning 발생
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "apply_style", "toggle_mode", "get_current_mode",
    "header", "sidebar_brand", "card", "metric_row",
    "kpi_card", "badge", "status_dot",
    "build_css", "inject_font", "inject_layout_helpers", "font_face_css",
    "LIGHT_TOKENS", "SPACING", "RADIUS", "SHADOW", "TYPO", "BUTTON_SIZE",
    "FONT_STACK", "CHART_SEQUENCE", "PLOTLY_TEMPLATE", "get_tokens",
    "apply_tk_style", "toggle_tk_mode", "get_current_tk_mode",
    "resolve_font_family", "get_tk_typo", "install_check",
    "header_tk", "card_tk",
]
