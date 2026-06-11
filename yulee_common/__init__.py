# -*- coding: utf-8 -*-
"""yulee-common — 율이공방 공통 GCP/Sheets/Secrets 유틸 (설계서 #2026-070)."""

from .gsheet import GSheetClient, get_client, SCOPES_FULL, SCOPES_SLIM
from .secrets import get_secret, get_gcp_credentials_dict, get_spreadsheet_id
from .errors import GSheetTransientError, GSheetAuthError, retry, safe_write
from .cache import cache_resource, cache_data

__version__ = "0.1.0"
__all__ = [
    "GSheetClient", "get_client", "SCOPES_FULL", "SCOPES_SLIM",
    "get_secret", "get_gcp_credentials_dict", "get_spreadsheet_id",
    "GSheetTransientError", "GSheetAuthError", "retry", "safe_write",
    "cache_resource", "cache_data",
    "__version__",
]
