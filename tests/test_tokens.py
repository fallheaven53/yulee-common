# -*- coding: utf-8 -*-
from yulee_common.theme.tokens import (
    DARK_TOKENS, LIGHT_TOKENS, SPACING, RADIUS, TYPO,
    PLOTLY_TEMPLATE_DARK, get_tokens,
)


def test_master_decision_colors():
    # 마스터 결정 2: 미드나잇 + 골드
    assert DARK_TOKENS["color.bg"] == "#1A1D2E"
    assert DARK_TOKENS["color.accent"] == "#C9A961"
    assert LIGHT_TOKENS["color.accent"] == "#C9A961"
    assert LIGHT_TOKENS["color.bg"] == "#FAFAF7"


def test_dark_light_same_keys():
    # 모드 전환 시 누락 토큰이 없어야 CSS 변수가 정확히 덮어쓰임
    assert set(DARK_TOKENS.keys()) == set(LIGHT_TOKENS.keys())


def test_all_colors_are_hex():
    for tokens in (DARK_TOKENS, LIGHT_TOKENS):
        for key, val in tokens.items():
            assert val.startswith("#") and len(val) in (4, 7), f"{key}={val}"


def test_spacing_radius_typo():
    assert SPACING[3] == "16px"
    assert RADIUS["md"] == "8px"
    assert TYPO["body"]["line_height"] == 1.6   # 한글 가독성 행간
    assert TYPO["h1"]["weight"] == 700


def test_get_tokens_mode():
    assert get_tokens("dark") is DARK_TOKENS
    assert get_tokens("light") is LIGHT_TOKENS
    assert get_tokens("없는모드") is DARK_TOKENS  # 안전 기본값


def test_plotly_template():
    layout = PLOTLY_TEMPLATE_DARK["layout"]
    assert layout["paper_bgcolor"] == DARK_TOKENS["color.bg"]
    assert layout["colorway"][0] == DARK_TOKENS["color.accent"]


def _luminance(hex_color):
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def _contrast(c1, c2):
    l1, l2 = sorted((_luminance(c1), _luminance(c2)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def test_wcag_aa_contrast():
    # 본문 대비비 >= 4.5:1 (설계서 4.4)
    assert _contrast(DARK_TOKENS["color.text_primary"],
                     DARK_TOKENS["color.bg"]) >= 4.5
    assert _contrast(LIGHT_TOKENS["color.text_primary"],
                     LIGHT_TOKENS["color.bg"]) >= 4.5
