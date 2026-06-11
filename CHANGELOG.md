# Changelog

## v0.1.0 — 2026-06-11

최초 릴리스 (설계서 #2026-070).

- `gsheet.py`: `GSheetClient`(인증·worksheet 캐시·overwrite 재시도·read_table/read_dataframe), `get_client` 캐시 팩토리, `SCOPES_FULL`/`SCOPES_SLIM`
- `secrets.py`: `get_secret`(점 표기 중첩 지원 — 09W), `get_gcp_credentials_dict`, `get_spreadsheet_id`, `validate_key_format`
- `errors.py`: `GSheetTransientError`/`GSheetAuthError`, `retry` 데코레이터, `safe_write`(18W sheets_safety 흡수)
- `cache.py`: `cache_resource`/`cache_data` 표준 래퍼
- 후방 호환 별칭(fallback 1개월): `client.spreadsheet`, `client._ws`, `client._get_or_create_sheet`, `client._overwrite_sheet`

영향 앱: (마이그레이션 전) 없음 — 12W부터 순차 적용 예정.
