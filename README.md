# yulee-common

율이공방 6개 Streamlit Cloud 앱(01W·09W·10W·12W·15W·18W)의 공통 GCP/Sheets/Secrets 유틸.

각 앱에 흩어져 있던 GCP 인증·스프레드시트 접근·secrets 처리 코드(약 1,200 lines)를
단일 모듈로 통합한다. 설계서 #2026-070 기반.

## 설치

requirements.txt에 한 줄 추가 (Private 레포 — PAT 필요):

```text
yulee-common @ git+https://${github_pat}@github.com/<user>/yulee-common@v0.1.0
```

로컬 개발:

```bash
pip install -e .
```

## 사용 예시

```python
from yulee_common import get_client, safe_write, get_secret

# Streamlit secrets로 인증된 클라이언트 (1회 캐시)
client = get_client(spreadsheet_key="spreadsheet_id")

# 워크시트 (없으면 생성)
ws = client.ws("발송기록")

# 읽기
rows = client.read_table(ws)
df = client.read_dataframe(ws)

# 안전 쓰기 (403/429 재시도 + 행 정리)
client.overwrite(ws, [["헤더1", "헤더2"], ["값1", "값2"]])

# 백업 후 쓰기 (18W sheets_safety 패턴)
safe_write(ws, data)

# secrets 헬퍼 — 09W 중첩 구조는 점 표기 지원
sid = get_secret("spreadsheet.spreadsheet_id", required=True)
```

## 모듈 구성

| 모듈 | 책임 |
|---|---|
| `gsheet.py` | `GSheetClient` · `get_client` 팩토리 · SCOPES 상수 |
| `secrets.py` | `st.secrets` 헬퍼 + 키 형식 검증 |
| `errors.py` | 공통 예외 + `retry` 데코레이터 + `safe_write` |
| `cache.py` | Streamlit cache 표준 래퍼 |

## 버전 정책

semver. 각 앱 requirements.txt는 정확한 태그(`@v0.1.0`)로 핀 — 자동 업데이트 금지.
변경 이력은 CHANGELOG.md 참고.
