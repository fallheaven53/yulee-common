# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.font as tkfont

import pytest

from yulee_common.theme.tk.font import (
    resolve_font_family, get_tk_typo, install_check, _FALLBACK_ORDER,
)


@pytest.fixture
def tk_root(shared_tk_root):
    return shared_tk_root


def test_resolve_returns_known_family(tk_root):
    fam = resolve_font_family()
    assert fam in _FALLBACK_ORDER + ["TkDefaultFont"]


def test_typo_six_fonts(tk_root):
    typo = get_tk_typo()
    assert set(typo.keys()) == {"h1", "h2", "h3", "body", "body_strong", "caption"}
    for f in typo.values():
        assert isinstance(f, tkfont.Font)
    assert typo["h1"].cget("size") == 20
    assert typo["h1"].cget("weight") == "bold"
    assert typo["body"].cget("size") == 11


def test_install_check_keys(tk_root):
    info = install_check()
    assert set(info.keys()) == {"wanted_sans", "pretendard", "resolved"}
    assert isinstance(info["wanted_sans"], bool)
