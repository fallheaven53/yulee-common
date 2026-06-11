# -*- coding: utf-8 -*-
"""공용 fixture — 가짜 service account dict, 가짜 worksheet, secrets 주입."""

import pytest


@pytest.fixture
def fake_sa_dict():
    """형식만 갖춘 가짜 GCP 서비스계정 dict (실제 키 아님)."""
    return {
        "type": "service_account",
        "project_id": "test-project",
        "private_key_id": "0" * 40,
        "private_key": "-----BEGIN PRIVATE KEY-----\nFAKE\n-----END PRIVATE KEY-----\n",
        "client_email": "test@test-project.iam.gserviceaccount.com",
        "client_id": "123456789012345678901",
        "token_uri": "https://oauth2.googleapis.com/token",
    }


class FakeWorksheet:
    """update/delete_rows/get_all_values만 흉내내는 가짜 워크시트."""

    def __init__(self, title="시트1", values=None, row_count=200):
        self.title = title
        self._values = values or []
        self.row_count = row_count
        self.cleared = False
        self.deleted_ranges = []

    def get_all_values(self):
        return [row[:] for row in self._values]

    def update(self, values=None, range_name="A1"):
        self._values = [row[:] for row in values]
        self.row_count = max(self.row_count, len(values))

    def delete_rows(self, start, end):
        self.deleted_ranges.append((start, end))
        self.row_count = start - 1

    def clear(self):
        self._values = []
        self.cleared = True


@pytest.fixture
def fake_ws():
    return FakeWorksheet(values=[["h1", "h2"], ["a", "b"]])


@pytest.fixture
def fake_secrets(monkeypatch):
    """st.secrets를 일반 dict로 대체. 테스트가 내용을 직접 구성."""
    store = {}

    def _root():
        return store

    monkeypatch.setattr("yulee_common.secrets._secrets_root", _root)
    return store
