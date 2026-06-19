# -*- coding: utf-8 -*-
"""apply_style — 표준 1줄 호출 + 모드 상태 관리 (설계서 #2026-071 7·9절)."""

from .css import build_css, inject_font
from .tokens import get_tokens

_MODE_KEY = "yl_theme_mode"
_APPLIED_KEY = "yl_theme_applied"


def get_current_mode():
    """현재 모드. v0.4.0은 라이트 단일 — 항상 light (시그니처 유지)."""
    return "light"


def apply_style(mode=None, *, override=None):
    """디자인 토큰 CSS를 1회 주입. 각 앱 app.py 최상단에서 호출.

    Args:
        mode: v0.3.x 호환 인자. v0.4.0은 라이트 단일이라 무시되고 항상 라이트.
        override: 토큰 일부 덮어쓰기 dict (예: {"color.accent": "#..."}). 재배포 없는
            즉시 보정용 (롤백 안전망).
    """
    import streamlit as st

    mode = "light"  # v0.4.0 라이트 단일

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

    # 빈 줄이 있으면 Streamlit markdown 파서가 <style> HTML 블록을 끊고
    # 이후 CSS를 본문 텍스트로 렌더한다 — 반드시 제거 (v0.2.1 수정).
    css = build_css(tokens, mode=mode)
    css = "\n".join(line for line in css.splitlines() if line.strip())
    _inject_html(st, inject_font())
    _inject_html(st, f"<style>\n{css}\n</style>")


def _inject_html(st, html_str):
    """markdown 파서를 거치지 않는 HTML 주입 (v0.2.2).

    st.html(1.32+)은 markdown 파싱이 없어 <style> 블록이 절대 깨지지 않는다.
    구버전은 st.markdown 폴백 (빈 줄 제거 전제).
    """
    if hasattr(st, "html"):
        st.html(html_str)
    else:
        st.markdown(html_str, unsafe_allow_html=True)


def toggle_mode():
    """v0.4.0 단순화 — 라이트 단일 모드라 토글 위젯 없이 'light' 반환.

    v0.3.x에서 사이드바 다크/라이트 토글로 쓰이던 자리. 시그니처는 호환을 위해
    유지하되, 라이트 토큰만 존재하므로 항상 라이트를 보장하고 'light'를 돌려준다.
    """
    apply_style(mode="light")
    return "light"
