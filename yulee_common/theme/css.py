# -*- coding: utf-8 -*-
"""CSS 생성 — 토큰 → :root 변수 + 컴포넌트 규칙 (설계서 #2026-079 [3]).

주입 CSS는 본 패키지 코드만으로 생성한다. 사용자 입력 합성 절대 금지.
<style> 태그만 사용, <script>·이벤트 핸들러 금지.

v0.4.0: Wanted Sans CDN 제거 → Pretendard 로컬 woff2(내부망 무의존).
CSS 변수명 통일 --color-* / --space-* / --radius-* / --shadow-*.
"""

import base64
import functools
import os

from .tokens import FONT_STACK, RADIUS, SHADOW, SPACING, TYPO, get_tokens

_THEME_DIR = os.path.dirname(os.path.abspath(__file__))
_ASSETS_DIR = os.path.join(_THEME_DIR, "assets")
_FONTS_DIR = os.path.join(_THEME_DIR, os.pardir, "styles", "fonts")

# Pretendard 로컬 woff2 4종 (orioncactus/pretendard, OFL 1.1)
_FONT_WEIGHTS = {
    "Regular": 400,
    "Medium": 500,
    "SemiBold": 600,
    "Bold": 700,
}


def _font_path(name):
    return os.path.join(_FONTS_DIR, f"Pretendard-{name}.woff2")


@functools.lru_cache(maxsize=8)
def _font_b64(name):
    """woff2 → base64 (lru 캐시, 세션당 1회 디스크 읽기)."""
    with open(_font_path(name), "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def font_face_css(strategy="base64", base_url=""):
    """Pretendard @font-face 4블록 (font-display: swap).

    strategy:
      "base64" — woff2를 data URI로 인라인 (자기완결, 내부망 1순위 / 설계서 6-2).
      "static" — base_url 기준 정적 서빙 url() 참조 (용량 과대 시 폴백).
    """
    blocks = []
    for name, weight in _FONT_WEIGHTS.items():
        if strategy == "static":
            src = f"url('{base_url.rstrip('/')}/Pretendard-{name}.woff2')"
        else:
            src = f"url(data:font/woff2;base64,{_font_b64(name)})"
        blocks.append(
            "@font-face{font-family:'Pretendard';font-style:normal;"
            f"font-weight:{weight};font-display:swap;"
            f"src:{src} format('woff2');}}"
        )
    return "".join(blocks)


def inject_font(strategy="base64", base_url=""):
    """Pretendard 로컬 @font-face 주입용 <style> 블록.

    v0.3.x의 Wanted Sans CDN <link>를 대체. 외부 네트워크 의존 없음."""
    return f"<style>{font_face_css(strategy=strategy, base_url=base_url)}</style>"


def _css_var_block(tokens):
    """컬러·여백·라운드·그림자 토큰을 CSS 변수 선언으로 변환."""
    lines = []
    for key, val in tokens.items():
        name = key.replace("color.", "").replace("_", "-")
        lines.append(f"  --color-{name}: {val};")
    for k, val in SPACING.items():
        lines.append(f"  --space-{k}: {val};")
    for k, val in RADIUS.items():
        lines.append(f"  --radius-{k}: {val};")
    for k, val in SHADOW.items():
        lines.append(f"  --shadow-{k}: {val};")
    lines.append(f"  --font: {FONT_STACK};")
    return "\n".join(lines)


def inject_layout_helpers():
    """assets/base.css의 정적 컴포넌트 규칙 (yulee-card·yulee-table 등)."""
    path = os.path.join(_ASSETS_DIR, "base.css")
    with open(path, encoding="utf-8") as f:
        return f.read()


def build_css(tokens=None, mode="light"):
    """토큰 → 전체 CSS 문자열 (:root 변수 + 전역 + 위젯 오버라이드 + 컴포넌트).

    mode 인자는 v0.3.x 호환 유지(시그니처 불변). v0.4.0은 라이트 단일."""
    tokens = tokens or get_tokens(mode)
    body = TYPO["body"]
    h1, h2, h3 = TYPO["h1"], TYPO["h2"], TYPO["h3"]
    cap = TYPO["caption"]

    return f""":root {{
{_css_var_block(tokens)}
}}

/* ── 전역: 배경·본문 타이포 (한글 행간 1.5, tabular-nums) ── */
.stApp {{
  background-color: var(--color-bg);
  font-family: var(--font);
  color: var(--color-text);
  font-size: {body["size"]};
  line-height: {body["line_height"]};
  font-variant-numeric: tabular-nums;
}}
.stApp h1 {{ font-size: {h1["size"]}; font-weight: {h1["weight"]};
  line-height: {h1["line_height"]}; letter-spacing: -0.02em;
  color: var(--color-text); }}
.stApp h2 {{ font-size: {h2["size"]}; font-weight: {h2["weight"]};
  line-height: {h2["line_height"]}; letter-spacing: -0.02em;
  color: var(--color-text); }}
.stApp h3 {{ font-size: {h3["size"]}; font-weight: {h3["weight"]};
  line-height: {h3["line_height"]}; letter-spacing: -0.01em;
  color: var(--color-text); }}
.stApp .stCaption, .stApp small {{
  font-size: {cap["size"]}; color: var(--color-text-sub); }}

/* ── 사이드바 ── */
[data-testid="stSidebar"] {{
  background-color: var(--color-surface);
  border-right: 1px solid var(--color-border);
}}

/* ── 버튼 — Primary 청자, Secondary 표면, Danger 단심 ── */
.stApp button[kind="primary"] {{
  background-color: var(--color-primary); color: #FFFFFF;
  font-weight: 600; border-radius: var(--radius-sm);
  border: none; padding: 0 16px; min-height: 40px;
}}
.stApp button[kind="primary"]:hover {{ filter: brightness(1.08); }}
.stApp button[kind="secondary"] {{
  background-color: var(--color-surface); color: var(--color-text);
  border: 1px solid var(--color-border); border-radius: var(--radius-sm);
}}

/* ── 입력 — 포커스 시 청자 outline ── */
.stApp input, .stApp textarea, .stApp [data-baseweb="select"] > div {{
  background-color: var(--color-surface);
  border-color: var(--color-border);
  color: var(--color-text);
}}
.stApp input:focus, .stApp textarea:focus {{
  outline: 2px solid var(--color-primary); outline-offset: -1px;
}}

/* ── 표 — 헤더 청자라이트, 줄무늬 Surface 2, 구분선 Border Light ── */
[data-testid="stDataFrame"] {{
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}}
[data-testid="stDataFrame"] thead tr th {{
  background-color: var(--color-primary-lt);
  color: var(--color-text);
}}
[data-testid="stDataFrame"] tbody tr:nth-child(even) {{
  background-color: var(--color-surface-2);
}}

/* ── metric 위젯 오버라이드 (혼합 전략, 설계서 6-3) ── */
[data-testid="stMetricValue"] {{
  color: var(--color-primary); font-variant-numeric: tabular-nums;
}}
[data-testid="stMetricLabel"] {{ color: var(--color-text-sub); }}

{inject_layout_helpers()}"""
