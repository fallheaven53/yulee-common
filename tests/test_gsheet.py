# -*- coding: utf-8 -*-
import gspread
import pytest

import yulee_common.gsheet as gs
from yulee_common.errors import GSheetAuthError
from yulee_common.gsheet import GSheetClient, SCOPES_FULL, SCOPES_SLIM

from conftest import FakeWorksheet


class FakeSpreadsheet:
    def __init__(self, worksheets=None):
        self.title = "테스트시트"
        self._wss = worksheets or {}
        self.added = []

    def worksheet(self, title):
        if title not in self._wss:
            raise gspread.WorksheetNotFound(title)
        return self._wss[title]

    def add_worksheet(self, title, rows, cols):
        ws = FakeWorksheet(title=title, row_count=rows)
        self._wss[title] = ws
        self.added.append(title)
        return ws

    def worksheets(self):
        return list(self._wss.values())


class FakeGC:
    def __init__(self, sheet):
        self._sheet = sheet
        self.opened_keys = []

    def open_by_key(self, key):
        self.opened_keys.append(key)
        return self._sheet


@pytest.fixture
def patched_client(monkeypatch, fake_sa_dict):
    """실제 GCP 호출 없이 GSheetClient를 만드는 fixture."""
    sheet = FakeSpreadsheet({"기존시트": FakeWorksheet("기존시트", [["h"], ["v"]])})
    fake_gc = FakeGC(sheet)

    monkeypatch.setattr(gs.Credentials, "from_service_account_info",
                        classmethod(lambda cls, info, scopes: ("creds", tuple(scopes))))
    monkeypatch.setattr(gs.gspread, "authorize", lambda creds: fake_gc)

    client = GSheetClient(credentials_dict=fake_sa_dict, spreadsheet_id="SID")
    return client, sheet, fake_gc


def test_init_requires_credentials():
    with pytest.raises(GSheetAuthError, match="필수"):
        GSheetClient(spreadsheet_id="SID")


def test_init_requires_spreadsheet_id(monkeypatch, fake_sa_dict):
    monkeypatch.setattr(gs.Credentials, "from_service_account_info",
                        classmethod(lambda cls, info, scopes: "creds"))
    monkeypatch.setattr(gs.gspread, "authorize", lambda creds: FakeGC(FakeSpreadsheet()))
    with pytest.raises(GSheetAuthError, match="spreadsheet_id"):
        GSheetClient(credentials_dict=fake_sa_dict, spreadsheet_id="")


def test_slim_scope_selects_scopes(monkeypatch, fake_sa_dict):
    captured = {}

    def fake_from_info(cls, info, scopes):
        captured["scopes"] = list(scopes)
        return "creds"

    monkeypatch.setattr(gs.Credentials, "from_service_account_info",
                        classmethod(fake_from_info))
    monkeypatch.setattr(gs.gspread, "authorize", lambda creds: FakeGC(FakeSpreadsheet()))

    GSheetClient(credentials_dict=fake_sa_dict, spreadsheet_id="S", slim_scope=True)
    assert captured["scopes"] == SCOPES_SLIM
    GSheetClient(credentials_dict=fake_sa_dict, spreadsheet_id="S", slim_scope=False)
    assert captured["scopes"] == SCOPES_FULL


def test_sh_lazy_open_and_alias(patched_client):
    client, sheet, fake_gc = patched_client
    assert fake_gc.opened_keys == []          # 아직 안 열림 (지연 연결)
    assert client.sh is sheet
    assert client.spreadsheet is sheet         # 별칭 동일 객체
    assert fake_gc.opened_keys == ["SID"]     # 1회만 open


def test_ws_returns_existing_and_caches(patched_client):
    client, sheet, _ = patched_client
    ws1 = client.ws("기존시트")
    ws2 = client.ws("기존시트")
    assert ws1 is ws2
    assert sheet.added == []


def test_ws_creates_when_missing(patched_client):
    client, sheet, _ = patched_client
    ws = client.ws("새시트", rows=50, cols=5)
    assert ws.title == "새시트"
    assert sheet.added == ["새시트"]


def test_ws_create_if_missing_false_raises(patched_client):
    client, _, _ = patched_client
    with pytest.raises(gspread.WorksheetNotFound):
        client.ws("없는시트", create_if_missing=False)


def test_read_table_and_dataframe(patched_client):
    client, _, _ = patched_client
    assert client.read_table("기존시트") == [["h"], ["v"]]
    df = client.read_dataframe("기존시트")
    assert list(df.columns) == ["h"]
    assert df.iloc[0, 0] == "v"


def test_overwrite_writes_and_trims(patched_client):
    client, _, _ = patched_client
    ws = client.ws("기존시트")
    ws.row_count = 100
    client.overwrite(ws, [["h"], ["1"], ["2"]])
    assert ws.get_all_values() == [["h"], ["1"], ["2"]]
    assert ws.deleted_ranges == [(4, 100)]


def test_overwrite_retries_on_transient(patched_client, monkeypatch):
    client, _, _ = patched_client
    monkeypatch.setattr("time.sleep", lambda s: None)
    ws = client.ws("기존시트")
    attempts = []
    original_update = ws.update

    def flaky_update(values=None, range_name="A1"):
        attempts.append(1)
        if len(attempts) < 2:
            class R:
                status_code = 429
            e = Exception("rate limited")
            e.response = R()
            raise e
        original_update(values=values, range_name=range_name)

    monkeypatch.setattr(ws, "update", flaky_update)
    client.overwrite(ws, [["x"]])
    assert len(attempts) == 2


def test_backward_compat_aliases(patched_client):
    client, _, _ = patched_client
    ws = client._ws("기존시트")
    assert ws is client.ws("기존시트")
    ws2 = client._get_or_create_sheet("별칭시트")
    assert ws2.title == "별칭시트"
    client._overwrite_sheet(ws, [["a"]])
    assert ws.get_all_values() == [["a"]]


def test_get_client_uses_secrets(monkeypatch, fake_secrets, fake_sa_dict):
    fake_secrets["gcp_service_account"] = fake_sa_dict
    fake_secrets["satisfaction_sheet_id"] = "SHEET44"

    sheet = FakeSpreadsheet()
    monkeypatch.setattr(gs.Credentials, "from_service_account_info",
                        classmethod(lambda cls, info, scopes: "creds"))
    monkeypatch.setattr(gs.gspread, "authorize", lambda creds: FakeGC(sheet))

    client = gs.get_client(spreadsheet_key="satisfaction_sheet_id")
    assert isinstance(client, GSheetClient)
    assert client.spreadsheet_id == "SHEET44"
