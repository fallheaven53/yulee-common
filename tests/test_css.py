# -*- coding: utf-8 -*-
from yulee_common.theme.css import build_css, inject_font, inject_layout_helpers
from yulee_common.theme.tokens import DARK_TOKENS, LIGHT_TOKENS


def test_build_css_contains_root_vars():
    css = build_css(mode="dark")
    assert ":root" in css
    assert "--yl-bg: #1A1D2E;" in css
    assert "--yl-accent: #C9A961;" in css
    assert "--yl-space-3: 16px;" in css
    assert "--yl-radius-md: 8px;" in css


def test_build_css_light_mode():
    css = build_css(mode="light")
    assert "--yl-bg: #FAFAF7;" in css
    assert "--yl-text-primary: #2D2D2D;" in css


def test_build_css_override_tokens():
    tokens = dict(DARK_TOKENS, **{"color.accent": "#FF0000"})
    css = build_css(tokens, mode="dark")
    assert "--yl-accent: #FF0000;" in css


def test_css_korean_readability():
    css = build_css(mode="dark")
    assert "line-height: 1.6" in css           # 본문 행간
    assert "tabular-nums" in css               # 숫자 정렬
    assert "Wanted Sans" in css                # 폰트 스택


def test_css_no_script_tags():
    # 7.4: <style>만, <script>·이벤트 핸들러 금지
    css = build_css(mode="dark")
    assert "<script" not in css.lower()
    assert "onclick" not in css.lower()
    font = inject_font()
    assert "<script" not in font.lower()


def test_inject_font_pins_version():
    font = inject_font()
    assert "cdn.jsdelivr.net" in font
    assert "@v" in font                        # @latest 아닌 버전 핀
    assert "preconnect" in font


def test_layout_helpers_components():
    helpers = inject_layout_helpers()
    for cls in (".yl-card", ".yl-metric", ".yl-header",
                ".yl-sidebar-brand", ".yl-msg"):
        assert cls in helpers, f"{cls} 누락"


def test_build_css_embeds_helpers():
    css = build_css(mode="dark")
    assert ".yl-card" in css                   # base.css 포함 확인
