# Changelog

## v0.3.1 — 2026-06-11

버그 수정 (patch).

- font._families: Tk root 없이 resolve_font_family/install_check 단독 호출 시 RuntimeError("no default root window") — 임시 root 생성으로 해결. 진단 스크립트에서 단독 사용 가능.

## v0.3.0 — 2026-06-11

feat: theme.tk submodule for Tkinter color/font token sharing (설계서 #2026-073). minor — 기존 API 전부 하위 호환.

- `theme/tk/style.py`: apply_tk_style(root, mode, override) — clam 기반 ttk.Style 매핑(TButton 골드·Treeview·TNotebook 등) + tk.* 전역 option_add. toggle_tk_mode·get_current_tk_mode
- `theme/tk/font.py`: resolve_font_family(Wanted Sans → Pretendard → 시스템 한글 폴백), get_tk_typo(px→pt 환산 6종), install_check(설치 진단)
- `theme/tk/components.py`: header_tk(골드 구분선)·card_tk
- v0.2.x theme.tokens 100% 재사용 (SSoT, 별도 색 정의 0)
- tkinter import는 전부 함수 내부 지연 — tkinter 없는 환경(Streamlit Cloud)에서도 패키지 import 안전
- 단위 테스트 9건 추가 (총 61건). 같은 프로세스 Tk 재생성 TclError 회피를 위해 session-scope 공유 root 사용

영향: Streamlit 6개 앱 0 (v0.3.0 핀 갱신은 선택). Tkinter 도구 8개 적용 가능.

## v0.2.2 — 2026-06-11

버그 수정 (patch) — CSS 텍스트 노출 근본 차단.

- apply_style: HTML 주입을 st.html(1.32+)로 전환 — markdown 파서를 아예 거치지 않아 <style> 블록 깨짐이 구조적으로 불가능. 구버전 Streamlit은 st.markdown 폴백 (v0.2.1 빈 줄 제거 유지).
- 토글 재주입(사이드바 컨텍스트 포함)도 동일 경로 — 호출 위치와 무관하게 안전.
- 참고: components.v1.html은 iframe이라 CSS가 부모 문서에 적용되지 않아 채택 안 함.

영향 앱: 10W (requirements @v0.2.2 갱신).

## v0.2.1 — 2026-06-11

버그 수정 (patch) — 10W 프로토타입 실사고 대응.

- apply_style: 주입 CSS의 빈 줄 제거 + 폰트 `<link>`와 `<style>` 블록을 별도 markdown 호출로 분리. Streamlit markdown 파서가 `<style>` 블록 안 빈 줄에서 HTML 블록을 끊어 이후 CSS가 본문에 텍스트로 노출되던 문제 해결.
- 회귀 테스트 추가 (스타일 블록 빈 줄 금지).

영향 앱: 10W (requirements @v0.2.1 갱신 필요).

## v0.2.0 — 2026-06-11

theme 서브패키지 추가 (설계서 #2026-071). minor — v0.1.0 API 전부 하위 호환.

- `theme/tokens.py`: DARK/LIGHT 토큰(미드나잇 #1A1D2E + 골드 #C9A961), SPACING·RADIUS·TYPO(한글 행간 1.6·tabular-nums), PLOTLY_TEMPLATE_DARK
- `theme/css.py`: build_css(:root 변수 + 컴포넌트 규칙), inject_font(Wanted Sans CDN @v1.0.3 핀 — 2026-06-11 검증 200 OK, Pretendard·시스템 한글 폴백 스택), inject_layout_helpers
- `theme/apply.py`: apply_style(mode·override, session_state 가드로 중복 주입 방지), toggle_mode, get_current_mode
- `theme/components.py`: header·sidebar_brand·card·metric_row (html.escape 정제)
- `theme/assets/`: base.css(yl-card·yl-metric·yl-header·yl-msg), config.toml.template
- 단위 테스트 21건 추가 (총 50건): WCAG AA 대비비 검증, XSS 이스케이프, CSS 주입 가드 포함
- pyproject v0.2.0 + package-data(assets)

영향 앱: 10W(프로토타입 적용 예정) → 이후 #2026-070 순서 동기화.

## v0.1.0 — 2026-06-11

최초 릴리스 (설계서 #2026-070).

- `gsheet.py`: `GSheetClient`(인증·worksheet 캐시·overwrite 재시도·read_table/read_dataframe), `get_client` 캐시 팩토리, `SCOPES_FULL`/`SCOPES_SLIM`
- `secrets.py`: `get_secret`(점 표기 중첩 지원 — 09W), `get_gcp_credentials_dict`, `get_spreadsheet_id`, `validate_key_format`
- `errors.py`: `GSheetTransientError`/`GSheetAuthError`, `retry` 데코레이터, `safe_write`(18W sheets_safety 흡수)
- `cache.py`: `cache_resource`/`cache_data` 표준 래퍼
- 후방 호환 별칭(fallback 1개월): `client.spreadsheet`, `client._ws`, `client._get_or_create_sheet`, `client._overwrite_sheet`

영향 앱: (마이그레이션 전) 없음 — 12W부터 순차 적용 예정.
