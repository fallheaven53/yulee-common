# -*- coding: utf-8 -*-
"""CSS 생성 — 토큰 → :root 변수 + 컴포넌트 규칙 (설계서 #2026-071 4.3·5·6절).

주입 CSS는 본 패키지 코드만으로 생성한다. 사용자 입력 합성 절대 금지 (7.4).
<style> 태그만 사용, <script>·이벤트 핸들러 금지.
"""

import os

from .tokens import FONT_STACK, RADIUS, SPACING, TYPO, get_tokens

# CDN 경로 — 2026-06-11 검증 완료 (200 OK). @latest 대신 버전 핀으로 변동 차단.
WANTED_SANS_CSS_URL = (
    "https://cdn.jsdelivr.net/gh/wanteddev/wanted-sans@v1.0.3"
    "/packages/wanted-sans/fonts/webfonts/variable/complete/WantedSansVariable.css"
)

_ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def _css_var_block(tokens):
    """컬러·여백·반경 토큰을 CSS 변수 선언으로 변환."""
    lines = []
    for key, val in tokens.items():
        name = key.replace("color.", "").replace("_", "-")
        lines.append(f"  --yl-{name}: {val};")
    for n, val in SPACING.items():
        lines.append(f"  --yl-space-{n}: {val};")
    for n, val in RADIUS.items():
        lines.append(f"  --yl-radius-{n}: {val};")
    return "\n".join(lines)


def inject_font():
    """Wanted Sans CDN 로드 스니펫. font-display: swap은 Wanted Sans CSS에 포함."""
    return (
        '<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>\n'
        f'<link rel="stylesheet" href="{WANTED_SANS_CSS_URL}">'
    )


def inject_layout_helpers():
    """assets/base.css의 정적 컴포넌트 규칙 (yl-card·yl-table 등)."""
    path = os.path.join(_ASSETS_DIR, "base.css")
    with open(path, encoding="utf-8") as f:
        return f.read()


def build_css(tokens=None, mode="dark"):
    """토큰 → 전체 CSS 문자열 (:root 변수 + 전역 + 컴포넌트 규칙)."""
    tokens = tokens or get_tokens(mode)
    body = TYPO["body"]
    h1, h2, h3 = TYPO["h1"], TYPO["h2"], TYPO["h3"]
    cap = TYPO["caption"]
    shadow = ("0 1px 2px rgba(0,0,0,.06)" if mode == "light"
              else "0 1px 0 rgba(0,0,0,.3)")

    return f""":root {{
{_css_var_block(tokens)}
  --yl-card-shadow: {shadow};
}}

/* ── 전역: 배경·본문 타이포 (한글 행간 1.6, tabular-nums) ── */
.stApp {{
  background-color: var(--yl-bg);
  font-family: {FONT_STACK};
  color: var(--yl-text-primary);
  font-size: {body["size"]};
  line-height: {body["line_height"]};
  font-variant-numeric: tabular-nums;
}}
.stApp h1 {{ font-size: {h1["size"]}; font-weight: {h1["weight"]};
  line-height: {h1["line_height"]}; letter-spacing: -0.02em;
  color: var(--yl-primary); }}
.stApp h2 {{ font-size: {h2["size"]}; font-weight: {h2["weight"]};
  line-height: {h2["line_height"]}; letter-spacing: -0.02em;
  color: var(--yl-primary); }}
.stApp h3 {{ font-size: {h3["size"]}; font-weight: {h3["weight"]};
  line-height: {h3["line_height"]}; letter-spacing: -0.02em;
  color: var(--yl-primary); }}
.stApp .stCaption, .stApp small {{
  font-size: {cap["size"]}; color: var(--yl-text-secondary); }}

/* ── 사이드바 ── */
[data-testid="stSidebar"] {{
  background-color: var(--yl-surface);
  border-right: 1px solid var(--yl-border);
}}

/* ── 버튼 (6.6) — Primary 골드, Secondary 표면 ── */
.stApp button[kind="primary"] {{
  background-color: var(--yl-accent); color: var(--yl-bg);
  font-weight: 600; border-radius: var(--yl-radius-md);
  border: none; padding: 8px 16px;
}}
.stApp button[kind="primary"]:hover {{ background-color: var(--yl-accent-hover); }}
.stApp button[kind="secondary"] {{
  background-color: var(--yl-surface-alt); color: var(--yl-text-primary);
  border: 1px solid var(--yl-border); border-radius: var(--yl-radius-md);
}}

/* ── 입력 (6.5) — 포커스 시 골드 outline ── */
.stApp input, .stApp textarea, .stApp [data-baseweb="select"] > div {{
  background-color: var(--yl-surface);
  border-color: var(--yl-border);
  color: var(--yl-text-primary);
}}
.stApp input:focus, .stApp textarea:focus {{
  outline: 2px solid var(--yl-accent); outline-offset: -1px;
}}

/* ── 테이블 (6.4) ── */
[data-testid="stDataFrame"] {{
  border: 1px solid var(--yl-border);
  border-radius: var(--yl-radius-md);
}}

{inject_layout_helpers()}"""
