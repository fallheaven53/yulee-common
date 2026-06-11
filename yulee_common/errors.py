# -*- coding: utf-8 -*-
"""공통 예외 + 재시도 데코레이터 + 안전 쓰기 (18W sheets_safety.py 흡수)."""

import functools
import json
import os
import time
from datetime import datetime


class GSheetTransientError(Exception):
    """403/429/5xx 등 재시도 대상 일시 오류."""


class GSheetAuthError(Exception):
    """GCP 인증 실패 (secrets 누락·키 불량 등)."""


def _status_code(exc):
    """gspread APIError 등에서 HTTP 상태코드 추출. 못 찾으면 None."""
    resp = getattr(exc, "response", None)
    code = getattr(resp, "status_code", None)
    if code is not None:
        return code
    return getattr(exc, "code", None)


def is_transient(exc) -> bool:
    """재시도 가치가 있는 오류인지 판정 (403 rate / 429 / 5xx)."""
    if isinstance(exc, GSheetTransientError):
        return True
    code = _status_code(exc)
    return code in (403, 429) or (code is not None and 500 <= code < 600)


def retry(max_attempts=3, base_delay=1.0, on=(GSheetTransientError,)):
    """일시 오류 재시도 데코레이터. 지수 백오프(base_delay * 2^n).

    on에 든 예외 또는 is_transient 판정 오류만 재시도하고,
    마지막 시도 실패 시 원본 예외를 그대로 올린다.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if not (isinstance(e, on) or is_transient(e)):
                        raise
                    last = e
                    if attempt < max_attempts - 1:
                        time.sleep(base_delay * (2 ** attempt))
            raise last
        return wrapper
    return decorator


# 백업 JSON 기본 위치. 18W sheets_safety.py는 앱 폴더 기준이었으므로
# 마이그레이션 시 YULEE_BACKUP_DIR 환경변수로 기존 경로를 지정할 수 있다 (설계서 13절 5번).
DEFAULT_BACKUP_DIR = os.environ.get("YULEE_BACKUP_DIR", "sheet_backups")


def safe_write(ws, data, backup_dir=None):
    """백업 → 쓰기 → 검증 (18W sheets_safety.py 패턴).

    1) 현재 워크시트 전체 값을 JSON으로 로컬 백업
    2) clear 없이 update로 덮어쓰기 (남는 행은 정리)
    3) 행 수 검증 — 다르면 RuntimeError

    Returns: 백업 파일 경로
    """
    backup_dir = backup_dir or DEFAULT_BACKUP_DIR
    os.makedirs(backup_dir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    title = getattr(ws, "title", "sheet")
    backup_path = os.path.join(backup_dir, f"{title}_{stamp}.json")

    before = ws.get_all_values()
    with open(backup_path, "w", encoding="utf-8") as f:
        json.dump(before, f, ensure_ascii=False)

    _write_with_trim(ws, data)

    after = ws.get_all_values()
    if len(after) != len(data):
        raise RuntimeError(
            f"safe_write 검증 실패: 기대 {len(data)}행, 실제 {len(after)}행 "
            f"(백업: {backup_path})"
        )
    return backup_path


@retry(max_attempts=3, base_delay=1.0)
def _write_with_trim(ws, data):
    """clear() 없이 update + 남는 행 삭제. 09W·12W _overwrite_sheet 패턴."""
    if not data:
        ws.clear()
        return
    ws.update(values=data, range_name="A1")
    existing = ws.row_count
    if existing > len(data):
        ws.delete_rows(len(data) + 1, existing)
