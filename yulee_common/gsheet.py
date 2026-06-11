# -*- coding: utf-8 -*-
"""GCP 인증된 스프레드시트 클라이언트 + 캐시 팩토리."""

import time

import gspread
from google.oauth2.service_account import Credentials

from .cache import cache_resource
from .errors import GSheetAuthError, is_transient
from .secrets import get_gcp_credentials_dict, get_spreadsheet_id

SCOPES_FULL = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
SCOPES_SLIM = [
    "https://www.googleapis.com/auth/spreadsheets",
]


class GSheetClient:
    """GCP 인증된 스프레드시트 핸들 + 헬퍼 메서드.

    인증 1회 + worksheet 캐시 + 403 방어를 포함한 안전 쓰기.
    """

    def __init__(
        self,
        credentials_dict: dict | None = None,
        credentials_path: str | None = None,
        spreadsheet_id: str = "",
        slim_scope: bool = False,
    ) -> None:
        scopes = SCOPES_SLIM if slim_scope else SCOPES_FULL
        try:
            if credentials_dict is not None:
                creds = Credentials.from_service_account_info(
                    credentials_dict, scopes=scopes)
            elif credentials_path is not None:
                creds = Credentials.from_service_account_file(
                    credentials_path, scopes=scopes)
            else:
                raise GSheetAuthError(
                    "credentials_dict 또는 credentials_path 중 하나는 필수")
            self.gc = gspread.authorize(creds)
        except GSheetAuthError:
            raise
        except Exception as e:
            raise GSheetAuthError(f"GCP 인증 실패: {type(e).__name__}") from e

        if not spreadsheet_id:
            raise GSheetAuthError("spreadsheet_id가 비어 있음")
        self.spreadsheet_id = spreadsheet_id
        self._sh = None
        self._ws_cache: dict[str, "gspread.Worksheet"] = {}

    # ── 스프레드시트 핸들 ──

    @property
    def sh(self) -> "gspread.Spreadsheet":
        """기본 별칭. 최초 접근 시 open(지연 연결)."""
        if self._sh is None:
            self._sh = self.gc.open_by_key(self.spreadsheet_id)
        return self._sh

    @property
    def spreadsheet(self) -> "gspread.Spreadsheet":
        """self.sh와 동일 객체 (12W·09W 호환)."""
        return self.sh

    # ── worksheet ──

    def ws(
        self,
        title: str,
        rows: int = 200,
        cols: int = 20,
        create_if_missing: bool = True,
    ) -> "gspread.Worksheet":
        """worksheet 반환. 없으면 생성(create_if_missing=True일 때)."""
        if title in self._ws_cache:
            return self._ws_cache[title]
        try:
            ws = self.sh.worksheet(title)
        except gspread.WorksheetNotFound:
            if not create_if_missing:
                raise
            ws = self.sh.add_worksheet(title=title, rows=rows, cols=cols)
        self._ws_cache[title] = ws
        return ws

    def _resolve_ws(self, ws_or_title):
        if isinstance(ws_or_title, str):
            return self.ws(ws_or_title)
        return ws_or_title

    # ── 읽기 ──

    def read_table(self, ws_or_title) -> list[list[str]]:
        """get_all_values 래핑."""
        return self._resolve_ws(ws_or_title).get_all_values()

    def read_dataframe(self, ws_or_title, header_row: int = 1):
        """첫 행(header_row)을 헤더로 한 DataFrame. pandas optional import."""
        import pandas as pd
        rows = self.read_table(ws_or_title)
        if len(rows) < header_row:
            return pd.DataFrame()
        header = rows[header_row - 1]
        body = rows[header_row:]
        return pd.DataFrame(body, columns=header)

    # ── 쓰기 ──

    def overwrite(
        self,
        ws_or_title,
        data: list[list],
        max_retries: int = 3,
        trim_extra_rows: bool = True,
    ) -> None:
        """clear() 없이 update + delete_rows 정리 + 재시도(403/429).

        09W·12W의 _overwrite_sheet(403 방어 + 재시도) 흡수.
        """
        ws = self._resolve_ws(ws_or_title)
        last = None
        for attempt in range(max_retries):
            try:
                if not data:
                    ws.clear()
                    return
                ws.update(values=data, range_name="A1")
                if trim_extra_rows and ws.row_count > len(data):
                    ws.delete_rows(len(data) + 1, ws.row_count)
                return
            except Exception as e:
                if not is_transient(e):
                    raise
                last = e
                if attempt < max_retries - 1:
                    time.sleep(1.0 * (2 ** attempt))
        raise last

    # ── 후방 호환 별칭 (fallback 1개월, 이후 제거 — 설계서 4.4) ──

    def _ws(self, title, *args, **kwargs):
        return self.ws(title)

    def _get_or_create_sheet(self, title, rows: int = 200, cols: int = 20):
        return self.ws(title, rows=rows, cols=cols)

    def _overwrite_sheet(self, ws, data):
        return self.overwrite(ws, data)


@cache_resource
def get_client(
    spreadsheet_key: str = "spreadsheet_id",
    slim_scope: bool = False,
    credentials_secret_key: str = "gcp_service_account",
) -> GSheetClient:
    """Streamlit 환경에서 secrets로 인증된 GSheetClient 1회 캐시.

    Args:
        spreadsheet_key: st.secrets에서 스프레드시트 ID를 찾을 키
            예) "spreadsheet_id"(기본), "satisfaction_sheet_id", "audience_sheet_id",
                "spreadsheet.spreadsheet_id"(09W 중첩) 등
        slim_scope: True면 SCOPES_SLIM(spreadsheets만), False면 SCOPES_FULL(+drive)
        credentials_secret_key: 인증 dict가 들어있는 st.secrets 키 (기본 gcp_service_account)
    """
    creds_dict = get_gcp_credentials_dict(credentials_secret_key)
    sid = get_spreadsheet_id(spreadsheet_key)
    return GSheetClient(
        credentials_dict=creds_dict,
        spreadsheet_id=sid,
        slim_scope=slim_scope,
    )
