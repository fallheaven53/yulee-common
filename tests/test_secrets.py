# -*- coding: utf-8 -*-
import pytest

from yulee_common.errors import GSheetAuthError
from yulee_common.secrets import (
    get_secret, get_gcp_credentials_dict, get_spreadsheet_id, validate_key_format,
)


def test_get_secret_flat(fake_secrets):
    fake_secrets["app_password"] = "pw"
    assert get_secret("app_password") == "pw"


def test_get_secret_default_when_missing(fake_secrets):
    assert get_secret("없는키") is None
    assert get_secret("없는키", default="기본") == "기본"


def test_get_secret_required_raises(fake_secrets):
    with pytest.raises(RuntimeError, match="없는키"):
        get_secret("없는키", required=True)


def test_get_secret_nested_dot_notation(fake_secrets):
    # 09W 중첩 구조: st.secrets["spreadsheet"]["spreadsheet_id"]
    fake_secrets["spreadsheet"] = {"spreadsheet_id": "SID123"}
    assert get_secret("spreadsheet.spreadsheet_id") == "SID123"
    assert get_secret("spreadsheet.없는키") is None


def test_get_gcp_credentials_dict(fake_secrets, fake_sa_dict):
    fake_secrets["gcp_service_account"] = fake_sa_dict
    creds = get_gcp_credentials_dict()
    assert creds["client_email"] == fake_sa_dict["client_email"]
    assert isinstance(creds, dict)


def test_get_gcp_credentials_dict_missing(fake_secrets):
    with pytest.raises(GSheetAuthError):
        get_gcp_credentials_dict()


def test_get_gcp_credentials_dict_incomplete(fake_secrets, fake_sa_dict):
    broken = dict(fake_sa_dict, private_key="")
    fake_secrets["gcp_service_account"] = broken
    with pytest.raises(GSheetAuthError, match="private_key"):
        get_gcp_credentials_dict()


def test_get_spreadsheet_id(fake_secrets):
    fake_secrets["satisfaction_sheet_id"] = "S" * 44
    assert get_spreadsheet_id("satisfaction_sheet_id") == "S" * 44


def test_get_spreadsheet_id_nested(fake_secrets):
    fake_secrets["spreadsheet"] = {"spreadsheet_id": "N" * 44}
    assert get_spreadsheet_id("spreadsheet.spreadsheet_id") == "N" * 44


def test_get_spreadsheet_id_missing(fake_secrets):
    with pytest.raises(RuntimeError, match="spreadsheet_id"):
        get_spreadsheet_id()


def test_validate_key_format():
    assert validate_key_format("0" * 40, "gcp_private_key_id")
    assert not validate_key_format("0" * 39, "gcp_private_key_id")
    assert validate_key_format("A" * 44, "sheet_id")
    assert not validate_key_format("짧음", "sheet_id")
    assert validate_key_format("ghp_" + "a" * 36, "github_pat")
    assert validate_key_format("github_pat_" + "a" * 30, "github_pat")
    assert not validate_key_format("plain-token", "github_pat")
    with pytest.raises(ValueError):
        validate_key_format("x", "unknown_kind")
