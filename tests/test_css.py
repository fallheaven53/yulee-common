# -*- coding: utf-8 -*-
from yulee_common.theme.css import (
    build_css, inject_font, inject_layout_helpers, font_face_css,
)
from yulee_common.theme.tokens import LIGHT_TOKENS


def test_build_css_contains_root_vars():
    css = build_css()
    assert ":root" in css
    assert "--color-bg: #F5EFE0;" in css
    assert "--color-primary: #2C5973;" in css
    assert "--color-primary-lt: #DCE6EE;" in css
    assert "--space-md: 16px;" in css
    assert "--radius-md: 8px;" in css
    assert "--shadow-subtle: 0 1px 3px rgba(0,0,0,.08);" in css


def test_build_css_mode_ignored_is_light():
    # v0.4.0 라이트 단일 — mode="dark" 여도 라이트
    css = build_css(mode="dark")
    assert "--color-bg: #F5EFE0;" in css
    assert "--color-text: #1F1F1F;" in css


def test_build_css_override_tokens():
    tokens = dict(LIGHT_TOKENS, **{"color.accent": "#FF0000"})
    css = build_css(tokens)
    assert "--color-accent: #FF0000;" in css


def test_css_korean_readability():
    css = build_css()
    assert "line-height: 1.5" in css       # 본문 행간
    assert "tabular-nums" in css           # 숫자 정렬
    assert "Pretendard" in css             # 폰트 스택(--font)


def test_css_no_script_tags():
    css = build_css()
    assert "<script" not in css.lower()
    assert "onclick" not in css.lower()
    font = inject_font()
    assert "<script" not in font.lower()


def test_inject_font_local_pretendard():
    # v0.4.0: CDN 제거, 로컬 woff2 base64 인라인 @font-face
    font = inject_font()
    assert "@font-face" in font
    assert "Pretendard" in font
    assert "font-display:swap" in font
    assert "data:font/woff2;base64," in font
    assert "cdn.jsdelivr.net" not in font   # 외부 CDN 의존 없음


def test_font_face_static_strategy():
    css = font_face_css(strategy="static", base_url="app/static")
    assert "url('app/static/Pretendard-Regular.woff2')" in css
    assert "base64" not in css


def test_layout_helpers_components():
    helpers = inject_layout_helpers()
    for cls in (".yl-card", ".yl-metric", ".yl-header", ".yl-sidebar-brand",
                ".yl-msg", ".yulee-kpi-card", ".yulee-badge", ".yulee-status-dot"):
        assert cls in helpers, f"{cls} 누락"


def test_build_css_embeds_helpers():
    css = build_css()
    assert ".yl-card" in css               # base.css 포함 확인
    assert ".yulee-badge--primary" in css
