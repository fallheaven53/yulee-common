# -*- coding: utf-8 -*-
"""setup_page — Streamlit 페이지 설정 + 디자인 시스템 1줄 부트스트랩 (설계서 #2026-079 [4]).

각 앱 app.py 최상단에서 setup_page("앱명") 한 번 호출하면
st.set_page_config + main.css(토큰·위젯·컴포넌트) + Pretendard 폰트가 주입된다.

폰트 서빙 (설계서 6-2 실측):
  font="base64"(기본) — woff2를 data URI로 인라인. 내부망 무의존, 앱 설정 0.
  font="static"       — main.css의 url('fonts/...') 정적 참조 유지. 앱이
                        styles/fonts 를 static 서빙으로 노출해야 함(용량 폴백).
"""

import os

from ..styles import MAIN_CSS
from ..theme.css import font_face_css

_TOKENS_MARKER = "/* ===== PART 2: TOKENS ===== */"


def _read_main_css():
    with open(MAIN_CSS, encoding="utf-8") as f:
        return f.read()


def _strip_blank_lines(text):
    # 빈 줄이 있으면 st.markdown 폴백 시 <style> 블록이 끊긴다 (apply.py와 동일 가드).
    return "\n".join(line for line in text.splitlines() if line.strip())


def _build_style(font, static_url):
    css = _read_main_css()
    idx = css.find(_TOKENS_MARKER)
    fonts_part, rest = (css[:idx], css[idx:]) if idx != -1 else ("", css)

    if font == "static":
        if static_url:
            css = css.replace("url('fonts/", f"url('{static_url.rstrip('/')}/")
        body = css
    else:  # base64 (기본): 정적 @font-face 블록 제거 후 인라인 폰트로 대체
        body = font_face_css(strategy="base64") + "\n" + rest

    return f"<style>\n{_strip_blank_lines(body)}\n</style>"


def _inject(st, html_str):
    if hasattr(st, "html"):
        st.html(html_str)
    else:
        st.markdown(html_str, unsafe_allow_html=True)


def inject_design(font="base64", static_url="app/static"):
    """set_page_config 없이 디자인만 주입 (이미 페이지 설정한 앱용)."""
    import streamlit as st
    _inject(st, _build_style(font, static_url))


def setup_page(title, icon="🎭", layout="wide", *,
               font="base64", static_url="app/static"):
    """st.set_page_config + 디자인 시스템 주입을 한 번에.

    Args:
        title: 페이지 타이틀(브라우저 탭).
        icon: 페이지 아이콘 이모지.
        layout: "wide" | "centered".
        font: "base64"(기본) | "static". 폰트 서빙 전략.
        static_url: static 전략일 때 woff2 베이스 URL.
    """
    import streamlit as st
    st.set_page_config(page_title=title, page_icon=icon, layout=layout)
    _inject(st, _build_style(font, static_url))
