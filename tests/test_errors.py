# -*- coding: utf-8 -*-
import json
import os

import pytest

from yulee_common.errors import (
    GSheetTransientError, GSheetAuthError, retry, safe_write, is_transient,
)


class _FakeAPIError(Exception):
    """gspread APIError처럼 .response.status_code를 가진 가짜 예외."""
    def __init__(self, code):
        class R:
            status_code = code
        self.response = R()


def test_is_transient_codes():
    assert is_transient(_FakeAPIError(403))
    assert is_transient(_FakeAPIError(429))
    assert is_transient(_FakeAPIError(503))
    assert not is_transient(_FakeAPIError(404))
    assert is_transient(GSheetTransientError("x"))
    assert not is_transient(ValueError("x"))


def test_retry_succeeds_after_failures(monkeypatch):
    monkeypatch.setattr("time.sleep", lambda s: None)
    calls = []

    @retry(max_attempts=3, base_delay=0)
    def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise GSheetTransientError("일시 오류")
        return "ok"

    assert flaky() == "ok"
    assert len(calls) == 3


def test_retry_exhausts_and_raises(monkeypatch):
    monkeypatch.setattr("time.sleep", lambda s: None)

    @retry(max_attempts=2, base_delay=0)
    def always_fail():
        raise GSheetTransientError("계속 실패")

    with pytest.raises(GSheetTransientError):
        always_fail()


def test_retry_does_not_catch_other_errors():
    @retry(max_attempts=3, base_delay=0)
    def boom():
        raise ValueError("재시도 대상 아님")

    with pytest.raises(ValueError):
        boom()


def test_safe_write_backs_up_then_writes(fake_ws, tmp_path):
    new_data = [["h1", "h2"], ["x", "y"], ["z", "w"]]
    backup_path = safe_write(fake_ws, new_data, backup_dir=str(tmp_path))

    # 백업 파일에 이전 값이 저장됨
    assert os.path.exists(backup_path)
    with open(backup_path, encoding="utf-8") as f:
        backed_up = json.load(f)
    assert backed_up == [["h1", "h2"], ["a", "b"]]

    # 워크시트에 새 데이터가 반영됨
    assert fake_ws.get_all_values() == new_data


def test_safe_write_row_mismatch_raises(fake_ws, tmp_path, monkeypatch):
    # update가 데이터를 일부만 반영하는 상황 흉내 → 검증 실패해야 함
    original_update = fake_ws.update

    def bad_update(values=None, range_name="A1"):
        original_update(values=values[:-1], range_name=range_name)

    monkeypatch.setattr(fake_ws, "update", bad_update)
    with pytest.raises(RuntimeError, match="검증 실패"):
        safe_write(fake_ws, [["a"], ["b"], ["c"]], backup_dir=str(tmp_path))
