# -*- coding: utf-8 -*-
import sys
import types

import pytest

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
    # 폰트 <style>@font-face 1회 + <style> 본문 1회 = 호출 2회
    assert len(fake_st.markdown_calls) == 2
    font, style = fake_st.markdown_calls
    assert "@font-face" in font and "Pretendard" in font
    assert "cdn.jsdelivr.net" not in font          # 외부 CDN 의존 없음
    assert "<style>" in style and "--color-bg: #F5EFE0;" in style

    # 같은 설정 재호출 → 중복 주입 없음 (가드)
    apply_style()
    assert len(fake_st.markdown_calls) == 2


def test_style_block_has_no_blank_lines(fake_st):
    # 빈 줄이 있으면 Streamlit markdown이 <style> 블록을 끊고
    # 이후 CSS가 본문 텍스트로 노출됨 (10W 실사고 회귀 테스트)
    apply_style()
    style = fake_st.markdown_calls[1]
    for line in style.splitlines():
        assert line.strip() != "", "스타일 블록에 빈 줄 존재 — CSS 텍스트 노출 위험"


def test_apply_style_mode_ignored(fake_st):
    # v0.4.0 라이트 단일 — mode="dark" 도 라이트, 같은 서명이라 재주입 없음
    apply_style(mode="dark")
    apply_style(mode="light")
    assert len(fake_st.markdown_calls) == 2
    assert "--color-bg: #F5EFE0;" in fake_st.markdown_calls[1]


def test_apply_style_override(fake_st):
    apply_style(override={"color.accent": "#123456"})
    assert "--color-accent: #123456;" in fake_st.markdown_calls[1]


def test_get_current_mode_is_light(fake_st):
    assert get_current_mode() == "light"


def test_components_escape_html(fake_st):
    from yulee_common.theme.components import card, header, metric_row

    header("<b>제목</b>", subtitle="<i>부제</i>")
    card("<script>alert(1)</script>", title="<x>")
    metric_row([("<라벨>", "<값>")])
    joined = "\n".join(fake_st.markdown_calls)
    assert "<script>" not in joined            # 이스케이프 확인 (7.4)
    assert "&lt;b&gt;제목&lt;/b&gt;" in joined


def test_new_components_escape_and_whitelist(fake_st):
    from yulee_common.theme.components import kpi_card, badge, status_dot

    kpi_card("<라벨>", "<값>", unit="<명>", color="#2C5973", note="<주석>")
    badge("<상태>", variant="javascript:alert(1)")   # 화이트리스트 외 → default
    status_dot("<라벨>", status="primary")
    joined = "\n".join(fake_st.markdown_calls)
    assert "<script>" not in joined
    assert "javascript:alert(1)" not in joined        # 클래스 주입 차단
    assert "yulee-badge--default" in joined
    assert "yulee-kpi-card" in joined


def test_kpi_card_rejects_bad_color(fake_st):
    from yulee_common.theme.components import kpi_card
    kpi_card("라벨", "값", color="red; background:url(x)")   # 화이트리스트 외 → 무시
    body = fake_st.markdown_calls[0]
    assert "background:url" not in body


def test_apply_style_prefers_st_html(monkeypatch):
    # st.html 지원 시 markdown 파서를 거치지 않음 (CSS 노출 근본 차단)
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
    sidebar_brand("관객", version="0.4.0")
    body = fake_st.markdown_calls[0]
    assert "율이공방" in body and "관객" in body
    assert "yulee-common v0.4.0" in body
