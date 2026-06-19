# -*- coding: utf-8 -*-
"""컴포넌트 헬퍼 — st.markdown thin wrapper (설계서 #2026-079 [3-3]).

unsafe_allow_html에 들어가는 문자열은 html.escape로 정제한다 —
사용자 입력이 그대로 합성되는 일이 없도록 (7.4).
variant·status·color 등 클래스/스타일에 들어가는 값은 화이트리스트로만 허용한다.
"""

import html
import re

# 뱃지·상태점 variant 화이트리스트 (클래스 주입 차단)
_VARIANTS = ("primary", "accent", "danger", "default")
_HEX_OR_VAR = re.compile(r"^(#[0-9A-Fa-f]{3,8}|var\(--[a-z0-9-]+\))$")


def _safe_variant(variant):
    return variant if variant in _VARIANTS else "default"


def header(title, subtitle=None, logo_emoji="🌙"):
    """일관된 헤더: 로고 이모지 + 타이틀 + (선택) 서브타이틀 + 골드 구분선."""
    import streamlit as st
    sub = (f'<span class="yl-header-subtitle">{html.escape(subtitle)}</span>'
           if subtitle else "")
    st.markdown(
        f'<div class="yl-header">'
        f'<span>{html.escape(logo_emoji)}</span>'
        f'<span class="yl-header-title">{html.escape(title)}</span>{sub}'
        f"</div>",
        unsafe_allow_html=True,
    )


def sidebar_brand(app_name, version=None):
    """사이드바 상단 앱명 + '공통모듈: yulee-common v{version}' 캡션 (8.4 표준)."""
    import streamlit as st
    if version is None:
        from .. import __version__ as version
    st.markdown(
        f'<div class="yl-sidebar-brand">'
        f'<div class="yl-brand-name">율이공방 — {html.escape(app_name)}</div>'
        f'<div class="yl-brand-caption">공통모듈: yulee-common v{html.escape(str(version))}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )


def card(content, *, title=None):
    """박스 카드. content는 텍스트(이스케이프됨)."""
    import streamlit as st
    head = f'<div class="yl-card-title">{html.escape(title)}</div>' if title else ""
    st.markdown(
        f'<div class="yl-card">{head}<div>{html.escape(str(content))}</div></div>',
        unsafe_allow_html=True,
    )


def metric_row(items):
    """한 줄에 N개 지표 카드. items: [(라벨, 값), ...]"""
    import streamlit as st
    cells = "".join(
        f'<div class="yl-metric">'
        f'<div class="yl-metric-value">{html.escape(str(value))}</div>'
        f'<div class="yl-metric-label">{html.escape(str(label))}</div>'
        f"</div>"
        for label, value in items
    )
    st.markdown(f'<div class="yl-metric-row">{cells}</div>',
                unsafe_allow_html=True)


def kpi_card(label, value, unit="", color=None, note=None):
    """단일 KPI 카드 — 라벨 + 큰 수치(+단위) + (선택) 보조 설명.

    color: 수치 색 오버라이드(hex 또는 var(--...)). 화이트리스트 외 값은 무시."""
    import streamlit as st
    style = ""
    if color and _HEX_OR_VAR.match(str(color)):
        style = f' style="color:{color}"'
    unit_html = (f'<span class="yulee-kpi-unit">{html.escape(str(unit))}</span>'
                 if unit else "")
    note_html = (f'<div class="yulee-kpi-note">{html.escape(str(note))}</div>'
                 if note else "")
    st.markdown(
        f'<div class="yulee-kpi-card">'
        f'<div class="yulee-kpi-label">{html.escape(str(label))}</div>'
        f'<div class="yulee-kpi-value"{style}>{html.escape(str(value))}{unit_html}</div>'
        f"{note_html}</div>",
        unsafe_allow_html=True,
    )


def badge(label, variant="default"):
    """상태 뱃지. variant: primary | accent | danger | default."""
    import streamlit as st
    v = _safe_variant(variant)
    st.markdown(
        f'<span class="yulee-badge yulee-badge--{v}">{html.escape(str(label))}</span>',
        unsafe_allow_html=True,
    )


def status_dot(label, status="default"):
    """색 점 + 라벨. status: primary | accent | danger | default."""
    import streamlit as st
    v = _safe_variant(status)
    st.markdown(
        f'<span class="yulee-status-dot yulee-status-dot--{v}">'
        f"{html.escape(str(label))}</span>",
        unsafe_allow_html=True,
    )
