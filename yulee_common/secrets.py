# -*- coding: utf-8 -*-
"""st.secrets 헬퍼 + 키 형식 검증.

값 평문을 로그·예외 메시지에 절대 노출하지 않는다 — 키 이름만 표기.
09W의 중첩 구조(st.secrets["spreadsheet"]["spreadsheet_id"])는 점 표기로 지원:
get_secret("spreadsheet.spreadsheet_id")
"""

import re

from .errors import GSheetAuthError

_MISSING = object()


def _secrets_root():
    import streamlit as st
    return st.secrets


def get_secret(key, default=None, required=False):
    """st.secrets 조회. 점 표기로 중첩 키 지원.

    required=True인데 키가 없으면 RuntimeError (키 이름만 노출, 값 노출 없음).
    """
    node = _secrets_root()
    for part in key.split("."):
        getter = getattr(node, "get", None)
        if getter is not None:
            node = getter(part, _MISSING)
        else:
            node = _MISSING
        if node is _MISSING:
            if required:
                raise RuntimeError(f"secrets 키 누락: {key}")
            return default
    return node


def get_gcp_credentials_dict(key="gcp_service_account"):
    """dict(st.secrets["gcp_service_account"]) 표준화. 없으면 GSheetAuthError."""
    raw = get_secret(key)
    if raw is None:
        raise GSheetAuthError(f"GCP 인증 정보 누락: secrets 키 '{key}' 없음")
    creds = dict(raw)
    for field in ("client_email", "private_key"):
        if not creds.get(field):
            raise GSheetAuthError(f"GCP 인증 정보 불완전: '{key}.{field}' 비어 있음")
    return creds


def get_spreadsheet_id(key="spreadsheet_id"):
    """스프레드시트 ID 조회. 앱별로 키 이름이 다양하므로 key 인자로 처리.

    예) "spreadsheet_id", "satisfaction_sheet_id", "audience_sheet_id",
        "spreadsheet.spreadsheet_id"(09W 중첩) 등
    """
    sid = get_secret(key)
    if not sid:
        raise RuntimeError(f"스프레드시트 ID 누락: secrets 키 '{key}' 없음 또는 빈 값")
    return str(sid)


# 키 형식 검증 패턴. 검증만 하고 값은 절대 노출하지 않는다.
_KEY_PATTERNS = {
    "anthropic": re.compile(r"^sk-ant-[A-Za-z0-9_-]{10,}$"),
    "gcp_private_key_id": re.compile(r"^[0-9a-f]{40}$"),
    "telegram": re.compile(r"^\d{8,10}:[A-Za-z0-9_-]{35}$"),
    "github_pat": re.compile(r"^(ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{22,})$"),
    "sheet_id": re.compile(r"^[A-Za-z0-9_-]{40,50}$"),
}


def validate_key_format(key, kind):
    """API 키 형식 검증. True/False만 반환 — 값·사유 평문 노출 금지.

    kind: anthropic | gcp_private_key_id | telegram | github_pat | sheet_id
    """
    pattern = _KEY_PATTERNS.get(kind)
    if pattern is None:
        raise ValueError(f"알 수 없는 키 종류: {kind}")
    return bool(key) and bool(pattern.match(str(key)))
