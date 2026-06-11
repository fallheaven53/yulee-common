# -*- coding: utf-8 -*-
"""Tkinter 컴포넌트 헬퍼 (선택 — 설계서 #2026-073 7.4절)."""

from ..tokens import get_tokens
from .style import get_current_tk_mode


def header_tk(parent, title, subtitle=None):
    """헤더: 타이틀 + (선택) 서브타이틀 + 하단 골드 1px 구분선."""
    import tkinter as tk
    from tkinter import ttk

    frame = ttk.Frame(parent, style="Header.TFrame")
    ttk.Label(frame, text=title, style="HeaderTitle.TLabel").pack(side="left")
    if subtitle:
        ttk.Label(frame, text=subtitle,
                  style="HeaderSub.TLabel").pack(side="left", padx=12)
    frame.pack(fill="x", padx=12, pady=(10, 4))

    tokens = get_tokens(get_current_tk_mode(parent))
    sep = tk.Frame(parent, height=1, bg=tokens["color.accent"])
    sep.pack(fill="x", padx=12, pady=(0, 8))
    return frame


def card_tk(parent, *, title=None):
    """카드 프레임 (surface 배경 + 패딩). 반환된 프레임에 위젯 배치."""
    import tkinter as tk
    from tkinter import ttk

    tokens = get_tokens(get_current_tk_mode(parent))
    outer = tk.Frame(parent, bg=tokens["color.border"], padx=1, pady=1)
    inner = ttk.Frame(outer, style="TFrame", padding=12)
    if title:
        ttk.Label(inner, text=title, style="HeaderSub.TLabel").pack(anchor="w")
    inner.pack(fill="both", expand=True)
    return outer, inner
