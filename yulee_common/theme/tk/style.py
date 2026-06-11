# -*- coding: utf-8 -*-
"""Tkinter 스타일 적용 — apply_tk_style (설계서 #2026-073 6절).

apply_style(Streamlit)과 API 일관: mode 기본 dark, override로 토큰 일부 보정.
"""

from ..tokens import get_tokens
from .font import get_tk_typo, resolve_font_family

_MODE_VAR = "yl_tk_theme_mode"


def get_current_tk_mode(root):
    """현재 모드. 미설정이면 dark."""
    try:
        return root.tk.getvar(_MODE_VAR)
    except Exception:
        return "dark"


def apply_tk_style(root, mode="dark", *, override=None):
    """Tkinter 루트에 율이공방 디자인 시스템 적용 (미드나잇+골드).

    Args:
        root: tk.Tk 또는 tk.Toplevel
        mode: "dark"(기본) | "light"
        override: 색 토큰 일부 덮어쓰기 (앱별 강조 색 등)
    """
    from tkinter import ttk

    tokens = dict(get_tokens(mode))
    if override:
        tokens.update(override)

    bg = tokens["color.bg"]
    surface = tokens["color.surface"]
    surface_alt = tokens["color.surface_alt"]
    accent = tokens["color.accent"]
    accent_hover = tokens["color.accent_hover"]
    text = tokens["color.text_primary"]
    text2 = tokens["color.text_secondary"]
    border = tokens["color.border"]

    typo = get_tk_typo()
    body_font = typo["body"]

    # ── 루트·전역 옵션 (tk.* 위젯 기본값) ──
    root.configure(bg=bg)
    root.option_add("*Background", bg)
    root.option_add("*Foreground", text)
    root.option_add("*Font", body_font)
    root.option_add("*selectBackground", accent)
    root.option_add("*selectForeground", bg)
    root.option_add("*insertBackground", text)       # tk.Text·Entry 커서
    root.option_add("*Menu.activeBackground", accent)
    root.option_add("*Menu.activeForeground", bg)

    # ── ttk 스타일 (clam 기반 — Windows 기본 테마는 색이 안 먹음) ──
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure(".", background=bg, foreground=text,
                    bordercolor=border, font=body_font)
    style.configure("TFrame", background=surface)
    style.configure("TLabel", background=bg, foreground=text)
    style.configure("TButton", background=accent, foreground=bg,
                    bordercolor=border, focuscolor=accent)
    style.map("TButton",
              background=[("active", accent_hover), ("pressed", accent_hover)],
              foreground=[("active", bg)])
    style.configure("TEntry", fieldbackground=surface, foreground=text,
                    insertcolor=text, bordercolor=border)
    style.configure("TCombobox", fieldbackground=surface, foreground=text,
                    background=surface, arrowcolor=text)
    style.configure("Treeview", background=surface, fieldbackground=surface,
                    foreground=text, bordercolor=border)
    style.configure("Treeview.Heading", background=surface_alt,
                    foreground=text, font=typo["body_strong"])
    style.map("Treeview",
              background=[("selected", accent)],
              foreground=[("selected", bg)])
    style.configure("TNotebook", background=bg, bordercolor=border)
    style.configure("TNotebook.Tab", background=surface_alt, foreground=text2)
    style.map("TNotebook.Tab",
              background=[("selected", surface)],
              foreground=[("selected", text)])
    style.configure("TCheckbutton", background=bg, foreground=text)
    style.configure("TRadiobutton", background=bg, foreground=text)

    # 헤더 헬퍼용 명명 스타일 (components.py)
    style.configure("Header.TFrame", background=bg)
    style.configure("HeaderTitle.TLabel", background=bg,
                    foreground=tokens["color.primary"], font=typo["h2"])
    style.configure("HeaderSub.TLabel", background=bg,
                    foreground=text2, font=typo["caption"])

    root.tk.setvar(_MODE_VAR, mode)


def toggle_tk_mode(root):
    """다크↔라이트 토글. 도구별 메뉴바 '보기' 항목에 연결 권장."""
    new = "light" if get_current_tk_mode(root) == "dark" else "dark"
    apply_tk_style(root, mode=new)
    return new
