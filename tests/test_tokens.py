# -*- coding: utf-8 -*-
import pytest

from yulee_common.theme import tokens as T
from yulee_common.theme.tokens import (
    LIGHT_TOKENS, SPACING, RADIUS, SHADOW, TYPO, BUTTON_SIZE,
    CHART_SEQUENCE, PLOTLY_TEMPLATE, get_tokens,
)


def test_korean_traditional_colors():
    # 설계서 [1.1] 확정값 (1차 OCR 정정 반영)
    assert LIGHT_TOKENS["color.bg"] == "#F5EFE0"        # 한지 베이지
    assert LIGHT_TOKENS["color.surface"] == "#FFFEF9"   # 옵션 A
    assert LIGHT_TOKENS["color.primary"] == "#2C5973"   # 청자
    assert LIGHT_TOKENS["color.accent"] == "#C9A046"    # 단청 황금 (1차 #C5AD46 정정)
    assert LIGHT_TOKENS["color.text_sub"] == "#6B6B6B"  # 1차 #686868 정정
    assert LIGHT_TOKENS["color.border"] == "#E0D8C4"    # 1차 #ECD8C4 정정
    assert LIGHT_TOKENS["color.border_lt"] == "#ECE6D7"  # 신규
    assert LIGHT_TOKENS["color.danger"] == "#A04040"    # 1차 #AD4040 정정


def test_eleven_colors_all_hex():
    assert len(LIGHT_TOKENS) == 11
    for key, val in LIGHT_TOKENS.items():
        assert val.startswith("#") and len(val) in (4, 7), f"{key}={val}"


def test_spacing_radius_shadow():
    # 여백 7단계 / 라운드 4단계 / 그림자 3단계(large 미사용)
    assert SPACING["md"] == "16px" and SPACING["xl"] == "32px"
    assert len(SPACING) == 7
    assert RADIUS == {"xs": "4px", "sm": "6px", "md": "8px", "lg": "12px"}
    assert SHADOW["subtle"] == "0 1px 3px rgba(0,0,0,.08)"
    assert "large" not in SHADOW


def test_typo_and_kpi():
    assert TYPO["body"]["line_height"] == 1.5      # 한글 본문 행간
    assert TYPO["h1"]["weight"] == 700
    assert TYPO["kpi_md"]["size"] == "24px"        # KPI Medium 확정
    assert TYPO["kpi_md"]["weight"] == 700
    assert TYPO["kpi_md"]["letter_spacing"] == "-1.0px"


def test_button_sizes():
    assert BUTTON_SIZE["sm"]["height"] == "32px"
    assert BUTTON_SIZE["md"]["height"] == "40px"
    assert BUTTON_SIZE["lg"]["height"] == "48px"


def test_get_tokens_always_light():
    # v0.4.0 라이트 단일 — 어떤 mode든 LIGHT_TOKENS
    assert get_tokens("light") is LIGHT_TOKENS
    assert get_tokens("dark") is LIGHT_TOKENS
    assert get_tokens() is LIGHT_TOKENS


def test_plotly_template_light():
    layout = PLOTLY_TEMPLATE["layout"]
    assert layout["paper_bgcolor"] == LIGHT_TOKENS["color.surface"]
    assert layout["colorway"][0] == LIGHT_TOKENS["color.primary"]
    assert CHART_SEQUENCE[1] == LIGHT_TOKENS["color.accent"]


def test_dark_tokens_soft_deprecated():
    # 옵션 A 폐기: 접근 시 DeprecationWarning + LIGHT 동등 alias
    with pytest.warns(DeprecationWarning):
        dark = T.DARK_TOKENS
    assert dark == LIGHT_TOKENS
    with pytest.warns(DeprecationWarning):
        tmpl = T.PLOTLY_TEMPLATE_DARK
    assert tmpl == PLOTLY_TEMPLATE


def _luminance(hex_color):
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def _contrast(c1, c2):
    l1, l2 = sorted((_luminance(c1), _luminance(c2)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def test_wcag_aa_contrast():
    # 본문 텍스트 대비 >= 4.5:1, 주색(청자) 표면 위 대비 >= 4.5:1
    assert _contrast(LIGHT_TOKENS["color.text"], LIGHT_TOKENS["color.bg"]) >= 4.5
    assert _contrast(LIGHT_TOKENS["color.primary"], LIGHT_TOKENS["color.surface"]) >= 4.5
