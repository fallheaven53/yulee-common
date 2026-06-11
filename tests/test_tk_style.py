# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

import pytest

from yulee_common.theme.tokens import DARK_TOKENS, LIGHT_TOKENS
from yulee_common.theme.tk import (
    apply_tk_style, toggle_tk_mode, get_current_tk_mode, header_tk,
)


@pytest.fixture
def root(shared_tk_root):
    return shared_tk_root


def test_apply_sets_root_bg(root):
    apply_tk_style(root)
    assert root.cget("background") == DARK_TOKENS["color.bg"]
    assert get_current_tk_mode(root) == "dark"


def test_ttk_button_accent(root):
    apply_tk_style(root)
    style = ttk.Style(root)
    assert style.lookup("TButton", "background") == DARK_TOKENS["color.accent"]
    assert style.lookup("Treeview.Heading", "background") == \
        DARK_TOKENS["color.surface_alt"]


def test_light_mode(root):
    apply_tk_style(root, mode="light")
    assert root.cget("background") == LIGHT_TOKENS["color.bg"]
    assert get_current_tk_mode(root) == "light"


def test_toggle(root):
    apply_tk_style(root, mode="dark")
    new = toggle_tk_mode(root)
    assert new == "light"
    assert root.cget("background") == LIGHT_TOKENS["color.bg"]
    assert toggle_tk_mode(root) == "dark"


def test_override(root):
    apply_tk_style(root, override={"color.bg": "#000000"})
    assert root.cget("background") == "#000000"


def test_header_tk(root):
    apply_tk_style(root)
    frame = header_tk(root, "테스트 도구", subtitle="2026 시즌")
    labels = [w for w in frame.winfo_children() if isinstance(w, ttk.Label)]
    assert len(labels) == 2           # 타이틀 + 서브타이틀
