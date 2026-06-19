# -*- coding: utf-8 -*-
"""yulee-common — 율이공방 공통 GCP/Sheets/Secrets/Theme 유틸 (설계서 #2026-070)."""

from .gsheet import GSheetClient, get_client, SCOPES_FULL, SCOPES_SLIM
from .secrets import get_secret, get_gcp_credentials_dict, get_spreadsheet_id
from .errors import GSheetTransientError, GSheetAuthError, retry, safe_write
from .cache import cache_resource, cache_data
from .theme import (
    apply_style, toggle_mode, get_current_mode,
    LIGHT_TOKENS, SPACING, RADIUS, SHADOW, TYPO, BUTTON_SIZE,
    FONT_STACK, CHART_SEQUENCE, PLOTLY_TEMPLATE,
    header, sidebar_brand, card, metric_row,
    kpi_card, badge, status_dot,
    apply_tk_style, toggle_tk_mode, get_current_tk_mode,
    resolve_font_family, get_tk_typo, install_check,
)
from .streamlit import setup_page, inject_design

__version__ = "0.4.1"

# v0.3.x 폐기 심볼 호환 — 접근 시 DeprecationWarning (theme 경유).
_DEPRECATED_NAMES = {"DARK_TOKENS", "PLOTLY_TEMPLATE_DARK"}


def __getattr__(name):
    if name in _DEPRECATED_NAMES:
        from . import theme
        return getattr(theme, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "GSheetClient", "get_client", "SCOPES_FULL", "SCOPES_SLIM",
    "get_secret", "get_gcp_credentials_dict", "get_spreadsheet_id",
    "GSheetTransientError", "GSheetAuthError", "retry", "safe_write",
    "cache_resource", "cache_data",
    "apply_style", "toggle_mode", "get_current_mode",
    "LIGHT_TOKENS", "SPACING", "RADIUS", "SHADOW", "TYPO", "BUTTON_SIZE",
    "FONT_STACK", "CHART_SEQUENCE", "PLOTLY_TEMPLATE",
    "header", "sidebar_brand", "card", "metric_row",
    "kpi_card", "badge", "status_dot",
    "setup_page", "inject_design",
    "apply_tk_style", "toggle_tk_mode", "get_current_tk_mode",
    "resolve_font_family", "get_tk_typo", "install_check",
    "__version__",
]
