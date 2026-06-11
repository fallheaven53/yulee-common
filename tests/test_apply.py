# -*- coding: utf-8 -*-
import sys
import types

import pytest

from yulee_common.theme import apply as apply_mod
from yulee_common.theme.apply import apply_style, get_current_mode


class FakeSt(types.ModuleType):
    """session_state + markdown 기록만 흉내내는 가짜 streamlit."""

    def __init__(self):
        super().__init__("streamlit")
        self.session_state = {}
        self.markdown_calls = []

    def markdown(self, body, unsafe_allow_html=False):
        self.markdown_calls.append(body)


@pytest.fixture
def fake_st(monkeypatch):
    st = FakeSt()
    monkeypatch.setitem(sys.modules, "streamlit", st)
    return st


def test_apply_style_injects_once(fake_st):
    apply_style()
    # 폰트 <link> 1회 + <style> 1회 = 호출 2회 (별도 주입 — v0.2.1)
    assert len(fake_st.markdown_calls) == 2
    font, style = fake_st.markdown_calls
    assert "cdn.jsdelivr.net" in font
    assert "<style>" in style and "--yl-bg: #1A1D2E;" in style

    # 같은 모드 재호출 → 중복 주입 없음 (7.3 가드)
    apply_style()
    assert len(fake_st.markdown_calls) == 2


def test_style_block_has_no_blank_lines(fake_st):
    # 빈 줄이 있으면 Streamlit markdown이 <style> 블록을 끊고
    # 이후 CSS가 본문 텍스트로 노출됨 (10W 실사고, v0.2.1 회귀 테스트)
    apply_style()
    style = fake_st.markdown_calls[1]
    for line in style.splitlines():
        assert line.strip() != "", "스타일 블록에 빈 줄 존재 — CSS 텍스트 노출 위험"


def test_apply_style_reinjects_on_mode_change(fake_st):
    apply_style(mode="dark")
    apply_style(mode="light")                  # 모드 변경 → 재주입
    assert len(fake_st.markdown_calls) == 4
    assert "--yl-bg: #FAFAF7;" in fake_st.markdown_calls[3]
    assert fake_st.session_state["yl_theme_mode"] == "light"


def test_apply_style_override(fake_st):
    apply_style(override={"color.accent": "#123456"})
    assert "--yl-accent: #123456;" in fake_st.markdown_calls[1]


def test_get_current_mode_defaults_dark(fake_st):
    assert get_current_mode() == "dark"
    fake_st.session_state["yl_theme_mode"] = "light"
    assert get_current_mode() == "light"


def test_components_escape_html(fake_st):
    from yulee_common.theme.components import card, header, metric_row

    header("<b>제목</b>", subtitle="<i>부제</i>")
    card("<script>alert(1)</script>", title="<x>")
    metric_row([("<라벨>", "<값>")])
    joined = "\n".join(fake_st.markdown_calls)
    assert "<script>" not in joined            # 이스케이프 확인 (7.4)
    assert "&lt;b&gt;제목&lt;/b&gt;" in joined


def test_apply_style_prefers_st_html(monkeypatch):
    # st.html 지원 시 markdown 파서를 거치지 않음 (v0.2.2 — CSS 노출 근본 차단)
    st = FakeSt()
    st.html_calls = []
    st.html = lambda body: st.html_calls.append(body)
    monkeypatch.setitem(sys.modules, "streamlit", st)

    apply_style()
    assert len(st.html_calls) == 2             # 폰트 + 스타일
    assert len(st.markdown_calls) == 0         # markdown 미사용
    assert "<style>" in st.html_calls[1]


def test_sidebar_brand_shows_version(fake_st):
    from yulee_common.theme.components import sidebar_brand
    sidebar_brand("관객", version="0.2.0")
    body = fake_st.markdown_calls[0]
    assert "율이공방" in body and "관객" in body
    assert "yulee-common v0.2.0" in body
