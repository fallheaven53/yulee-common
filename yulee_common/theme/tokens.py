# -*- coding: utf-8 -*-
"""디자인 토큰 — 단일 진실의 원천 (설계서 #2026-071 4·5절).

마스터 결정: 모던 / 미드나잇(#1A1D2E)+골드(#C9A961) / Wanted Sans.
골드는 핵심 포인트(버튼·강조·로고·구분선)에만 — 1화면 5건 이하.
"""

DARK_TOKENS = {
    "color.bg": "#1A1D2E",            # Midnight — 앱 배경
    "color.surface": "#252937",       # 카드·박스·테이블
    "color.surface_alt": "#2F3344",   # 보조 표면 (헤더 배경 등)
    "color.primary": "#FAFAF7",       # 헤더·강조 (텍스트 대비)
    "color.accent": "#C9A961",        # Muted Gold — 액션·강조·로고·구분선
    "color.accent_hover": "#D6B775",
    "color.text_primary": "#FAFAF7",
    "color.text_secondary": "#B8B5AC",
    "color.border": "#3A3F52",
    "color.success": "#7BC47F",
    "color.warning": "#E0B248",
    "color.error": "#E07B7B",
}

LIGHT_TOKENS = {
    "color.bg": "#FAFAF7",            # Cream
    "color.surface": "#FFFFFF",
    "color.surface_alt": "#F4F2EC",
    "color.primary": "#1A1D2E",       # Midnight
    "color.accent": "#C9A961",
    "color.accent_hover": "#B89952",
    "color.text_primary": "#2D2D2D",
    "color.text_secondary": "#6B6862",
    "color.border": "#E5E2DA",
    "color.success": "#3E8E47",
    "color.warning": "#B58B1F",
    "color.error": "#A33A3A",
}

SPACING = {1: "4px", 2: "8px", 3: "16px", 4: "24px", 5: "32px", 6: "48px"}

RADIUS = {"sm": "4px", "md": "8px", "lg": "12px", "xl": "16px"}

TYPO = {
    "h1": {"size": "28px", "weight": 700, "line_height": 1.3},
    "h2": {"size": "22px", "weight": 600, "line_height": 1.35},
    "h3": {"size": "18px", "weight": 600, "line_height": 1.4},
    "body": {"size": "15px", "weight": 400, "line_height": 1.6},
    "body_strong": {"size": "15px", "weight": 600, "line_height": 1.6},
    "caption": {"size": "13px", "weight": 400, "line_height": 1.5},
    "code": {"family": "Menlo, Consolas, monospace", "size": "13px"},
}

FONT_STACK = (
    '"Wanted Sans Variable", "Wanted Sans", '
    "-apple-system, BlinkMacSystemFont, "
    '"Pretendard Variable", "Pretendard", '
    '"Apple SD Gothic Neo", "Malgun Gothic", '
    '"Helvetica Neue", Arial, sans-serif'
)

PLOTLY_TEMPLATE_DARK = {
    "layout": {
        "paper_bgcolor": DARK_TOKENS["color.bg"],
        "plot_bgcolor": DARK_TOKENS["color.surface"],
        "font": {"color": DARK_TOKENS["color.text_primary"]},
        "colorway": [
            DARK_TOKENS["color.accent"], "#8FB8DE", "#7BC47F",
            "#E0B248", "#E07B7B", "#B58CE0",
        ],
    }
}


def get_tokens(mode="dark"):
    """모드별 컬러 토큰. 알 수 없는 모드는 다크로."""
    return LIGHT_TOKENS if mode == "light" else DARK_TOKENS
