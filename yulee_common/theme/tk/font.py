# -*- coding: utf-8 -*-
"""Tkinter 폰트 탐지·매핑 (설계서 #2026-073 5절).

Wanted Sans 시스템 설치 가정 + Pretendard·시스템 한글 폴백.
"""

_FALLBACK_ORDER = [
    "Wanted Sans Variable",
    "Wanted Sans",
    "Pretendard Variable",
    "Pretendard",
    "맑은 고딕",               # Windows
    "Apple SD Gothic Neo",     # macOS
    "Noto Sans CJK KR",        # Linux
]


def _families():
    """설치 폰트 패밀리 집합. Tk root가 없으면 임시 root를 만들어 조회."""
    import tkinter as tk
    import tkinter.font as tkfont
    try:
        return set(tkfont.families())
    except RuntimeError:                  # no default root window
        r = tk.Tk()
        r.withdraw()
        try:
            return set(tkfont.families(r))
        finally:
            r.destroy()


def resolve_font_family():
    """시스템 설치 폰트에서 폴백 순서대로 첫 발견 패밀리 반환."""
    families = _families()
    for fam in _FALLBACK_ORDER:
        if fam in families:
            return fam
    return "TkDefaultFont"


def install_check():
    """Wanted Sans·Pretendard 설치 여부 (도구·운영 진단용)."""
    families = _families()
    return {
        "wanted_sans": any(f in families for f in
                           ("Wanted Sans Variable", "Wanted Sans")),
        "pretendard": any(f in families for f in
                          ("Pretendard Variable", "Pretendard")),
        "resolved": resolve_font_family(),
    }


def get_tk_typo(family=None):
    """TYPO 토큰 → tkfont.Font 매핑. Streamlit px → pt 환산 (약 0.75배)."""
    import tkinter.font as tkfont
    family = family or resolve_font_family()
    return {
        "h1": tkfont.Font(family=family, size=20, weight="bold"),
        "h2": tkfont.Font(family=family, size=16, weight="bold"),
        "h3": tkfont.Font(family=family, size=13, weight="bold"),
        "body": tkfont.Font(family=family, size=11),
        "body_strong": tkfont.Font(family=family, size=11, weight="bold"),
        "caption": tkfont.Font(family=family, size=9),
    }
