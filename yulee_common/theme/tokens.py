# -*- coding: utf-8 -*-
"""디자인 토큰 — 단일 진실의 원천 (설계서 #2026-079 v0.4.0 확정값).

마스터 결정: 한국 전통색 라이트톤 + Pretendard 로컬 폰트.
청자(#2C5973)는 핵심 한두 곳, 단청 황금(#C9A046)은 Primary와 짝지어 위계 —
동시 강조 금지. v0.3.x의 미드나잇 다크톤은 폐기(아래 __getattr__ 소프트 폐기 참조).
"""

import warnings

# ── 라이트 토큰: 한국 전통색 11색 (설계서 [1.1] 확정값) ──
LIGHT_TOKENS = {
    "color.bg": "#F5EFE0",          # 한지 베이지 — 페이지 배경
    "color.surface": "#FFFEF9",     # 카드·헤더
    "color.surface_2": "#FAF4E8",   # 보조 표면·줄무늬
    "color.primary": "#2C5973",     # 청자 — 주버튼·핵심 수치
    "color.primary_lt": "#DCE6EE",  # 표 헤더 배경·뱃지
    "color.accent": "#C9A046",      # 단청 황금 — 뱃지·하이라이트
    "color.text": "#1F1F1F",
    "color.text_sub": "#6B6B6B",
    "color.border": "#E0D8C4",      # 카드·표 테두리
    "color.border_lt": "#ECE6D7",   # 표 줄무늬 구분선
    "color.danger": "#A04040",      # 오류·경고·삭제
}

# ── 여백: 8px 기반 7단계 (설계서 [1.3]) ──
SPACING = {
    "xs": "4px",    # 아이콘-텍스트
    "sm": "8px",    # 라벨-입력
    "md": "16px",   # 카드 패딩·항목간
    "lg": "24px",   # 섹션간·카드외부
    "xl": "32px",   # 페이지 좌우 패딩
    "2xl": "48px",  # 큰 섹션간
    "3xl": "64px",  # 페이지 상하 외곽
}

# ── 라운드: 4단계 (설계서 [1.4]) ──
RADIUS = {
    "xs": "4px",   # 작은 뱃지·인풋
    "sm": "6px",   # 버튼
    "md": "8px",   # 카드·표 기본
    "lg": "12px",  # 모달·강조 카드
}

# ── 그림자: 3단계, large 미사용 (설계서 [1.5]) ──
SHADOW = {
    "none": "none",
    "subtle": "0 1px 3px rgba(0,0,0,.08)",   # 카드 기본
    "medium": "0 4px 12px rgba(0,0,0,.10)",  # 모달·드롭다운·플로팅
}

# ── 타이포: Pretendard 위계 8단계 + KPI 2단계 (설계서 [1.2]) ──
# 본문 line-height 150%. KPI는 line 1.0 / 자간 -1.0px.
TYPO = {
    "display":  {"size": "32px", "weight": 700, "line_height": 1.25},
    "h1":       {"size": "26px", "weight": 700, "line_height": 1.3},
    "h2":       {"size": "20px", "weight": 600, "line_height": 1.35},
    "h3":       {"size": "16px", "weight": 600, "line_height": 1.4},
    "body_lg":  {"size": "16px", "weight": 500, "line_height": 1.5},
    "body":     {"size": "14px", "weight": 400, "line_height": 1.5},
    "body_sm":  {"size": "13px", "weight": 400, "line_height": 1.5},
    "caption":  {"size": "12px", "weight": 400, "line_height": 1.5},
    "kpi_lg":   {"size": "38px", "weight": 700, "line_height": 1.0,
                 "letter_spacing": "-1.0px"},
    "kpi_md":   {"size": "24px", "weight": 700, "line_height": 1.0,
                 "letter_spacing": "-1.0px"},
}

# ── 버튼 규격: 3단계 (높이/좌우 패딩/폰트, 설계서 [1.6]) ──
BUTTON_SIZE = {
    "sm": {"height": "32px", "padding_x": "12px", "font_size": "13px"},
    "md": {"height": "40px", "padding_x": "16px", "font_size": "14px"},
    "lg": {"height": "48px", "padding_x": "20px", "font_size": "15px"},
}

# ── 폰트 스택: Pretendard 로컬(main.css @font-face) + 시스템 폴백 ──
FONT_STACK = (
    "'Pretendard', -apple-system, BlinkMacSystemFont, "
    "'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif"
)

# ── 차트 팔레트: Primary·Accent 중심 (외부 시각화 톤 정합, 설계서 [7] 5-4) ──
CHART_SEQUENCE = [
    LIGHT_TOKENS["color.primary"],   # 청자
    LIGHT_TOKENS["color.accent"],    # 단청 황금
    "#5B8BA8",   # 청자 라이트
    "#A0793A",   # 단청 다크
    "#7BA05B",   # 보조 그린
    LIGHT_TOKENS["color.danger"],    # 단심 적
]

PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": LIGHT_TOKENS["color.surface"],
        "plot_bgcolor": LIGHT_TOKENS["color.surface"],
        "font": {"color": LIGHT_TOKENS["color.text"]},
        "colorway": CHART_SEQUENCE,
    }
}


def get_tokens(mode="light"):
    """컬러 토큰 반환. v0.4.0은 라이트 단일 — 모든 mode가 LIGHT_TOKENS.

    mode 인자는 v0.3.x 호환을 위해 유지(시그니처 불변). 'dark' 포함 어떤 값이든
    라이트 토큰을 돌려준다(다크톤 폐기, 6-1)."""
    return LIGHT_TOKENS


# ── Tkinter 전용 토큰 (v0.3.x 미드나잇/골드 유지) ──────────────────────
# #2026-079W는 web(Streamlit) 테마만 한국 전통색 라이트로 전환한다. Tkinter
# 재색상화는 주문서·설계서에 명세가 없으므로(윤실장 확인 대기) 기존 디자인을
# 그대로 보존한다. web LIGHT_TOKENS(11색)와 키 구성이 다르므로 분리 유지.
_TK_DARK = {
    "color.bg": "#1A1D2E",
    "color.surface": "#252937",
    "color.surface_alt": "#2F3344",
    "color.primary": "#FAFAF7",
    "color.accent": "#C9A961",
    "color.accent_hover": "#D6B775",
    "color.text_primary": "#FAFAF7",
    "color.text_secondary": "#B8B5AC",
    "color.border": "#3A3F52",
    "color.success": "#7BC47F",
    "color.warning": "#E0B248",
    "color.error": "#E07B7B",
}

_TK_LIGHT = {
    "color.bg": "#FAFAF7",
    "color.surface": "#FFFFFF",
    "color.surface_alt": "#F4F2EC",
    "color.primary": "#1A1D2E",
    "color.accent": "#C9A961",
    "color.accent_hover": "#B89952",
    "color.text_primary": "#2D2D2D",
    "color.text_secondary": "#6B6862",
    "color.border": "#E5E2DA",
    "color.success": "#3E8E47",
    "color.warning": "#B58B1F",
    "color.error": "#A33A3A",
}


def get_tk_tokens(mode="dark"):
    """Tkinter 전용 컬러 토큰. 기본 dark(미드나잇). 'light'면 라이트.

    web get_tokens()와 분리 — Tkinter 디자인은 v0.4.0에서 변경하지 않는다."""
    return _TK_LIGHT if mode == "light" else _TK_DARK


# ── v0.3.x 소프트 폐기 (설계서 [6-1], 옵션 A) ─────────────────────────
# DARK_TOKENS / PLOTLY_TEMPLATE_DARK 는 LIGHT 동등물로 alias 하되, 접근 시
# DeprecationWarning 을 1회 발생시킨다. v0.5.0 에서 완전 제거 예정(CHANGELOG).
_DEPRECATED = {
    "DARK_TOKENS": ("LIGHT_TOKENS", LIGHT_TOKENS),
    "PLOTLY_TEMPLATE_DARK": ("PLOTLY_TEMPLATE", PLOTLY_TEMPLATE),
}


def __getattr__(name):
    if name in _DEPRECATED:
        new_name, value = _DEPRECATED[name]
        warnings.warn(
            f"{name}는 v0.4.0에서 폐기 예정입니다. {new_name}(또는 새 라이트 토큰)을 "
            "사용해 주세요. v0.5.0에서 완전 제거됩니다.",
            DeprecationWarning,
            stacklevel=2,
        )
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
