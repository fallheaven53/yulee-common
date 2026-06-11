# -*- coding: utf-8 -*-
"""apply_style — 표준 1줄 호출 + 모드 상태 관리 (설계서 #2026-071 7·9절)."""

from .css import build_css, inject_font
from .tokens import get_tokens

_MODE_KEY = "yl_theme_mode"
_APPLIED_KEY = "yl_theme_applied"


def get_current_mode():
    """현재 모드. session_state 없으면(테스트 등) dark."""
    try:
        import streamlit as st
        return st.session_state.get(_MODE_KEY, "dark")
    except Exception:
        return "dark"


def apply_style(mode=None, *, override=None):
    """디자인 토큰 CSS를 1회 주입. 각 앱 app.py 최상단에서 호출.

    Args:
        mode: "dark" | "light". 미지정 시 session_state["yl_theme_mode"], 없으면 dark.
        override: 토큰 일부 덮어쓰기 dict (예: {"color.accent": "#..."}). 재배포 없는
            즉시 보정용 (롤백 안전망 3).
    """
    import streamlit as st

    if mode is None:
        mode = get_current_mode()

    tokens = dict(get_tokens(mode))
    if override:
        tokens.update(override)

    # 같은 모드·설정으로 이미 주입했으면 재주입 생략 (rerun 중복 방지 — 7.3 가드).
    # 모드가 바뀌면 다시 주입해야 하므로 적용 서명을 함께 저장한다.
    signature = (mode, tuple(sorted(override.items())) if override else None)
    if st.session_state.get(_APPLIED_KEY) == signature:
        return
    st.session_state[_APPLIED_KEY] = signature
    st.session_state[_MODE_KEY] = mode

    css = build_css(tokens, mode=mode)
    st.markdown(f"{inject_font()}\n<style>\n{css}\n</style>",
                unsafe_allow_html=True)


def toggle_mode():
    """사이드바 다크/라이트 토글 위젯. 변경 시 session_state 갱신 후 재주입.

    Returns: 선택된 모드 문자열.
    """
    import streamlit as st

    current = get_current_mode()
    choice = st.radio(
        "화면 모드",
        options=["dark", "light"],
        format_func=lambda m: "🌙 다크" if m == "dark" else "☀ 라이트",
        index=0 if current == "dark" else 1,
        horizontal=True,
        key="yl_theme_toggle",
        label_visibility="collapsed",
    )
    if choice != current:
        st.session_state[_MODE_KEY] = choice
        apply_style(mode=choice)
    return choice
