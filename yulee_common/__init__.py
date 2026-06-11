# -*- coding: utf-8 -*-
"""yulee-common — 율이공방 공통 GCP/Sheets/Secrets 유틸 (설계서 #2026-070)."""

from .gsheet import GSheetClient, get_client, SCOPES_FULL, SCOPES_SLIM
from .secrets import get_secret, get_gcp_credentials_dict, get_spreadsheet_id
from .errors import GSheetTransientError, GSheetAuthError, retry, safe_write
from .cache import cache_resource, cache_data
from .theme import (
    apply_style, toggle_mode, get_current_mode,
    DARK_TOKENS, LIGHT_TOKENS, SPACING, RADIUS, TYPO, PLOTLY_TEMPLATE_DARK,
    header, sidebar_brand, card, metric_row,
    apply_tk_style, toggle_tk_mode, get_current_tk_mode,
    resolve_font_family, get_tk_typo, install_check,
)

__version__ = "0.3.1"
__all__ = [
    "GSheetClient", "get_client", "SCOPES_FULL", "SCOPES_SLIM",
    "get_secret", "get_gcp_credentials_dict", "get_spreadsheet_id",
    "GSheetTransientError", "GSheetAuthError", "retry", "safe_write",
    "cache_resource", "cache_data",
    "apply_style", "toggle_mode", "get_current_mode",
    "DARK_TOKENS", "LIGHT_TOKENS", "SPACING", "RADIUS", "TYPO",
    "PLOTLY_TEMPLATE_DARK",
    "header", "sidebar_brand", "card", "metric_row",
    "apply_tk_style", "toggle_tk_mode", "get_current_tk_mode",
    "resolve_font_family", "get_tk_typo", "install_check",
    "__version__",
]
