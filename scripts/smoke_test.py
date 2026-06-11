# -*- coding: utf-8 -*-
"""마이그레이션 직후 각 앱에서 1회 실행하는 smoke test (설계서 11.2).

read만 수행 — write 없음, 안전. 앱별로 spreadsheet_key 인자만 다르게:
    python scripts/smoke_test.py
    python scripts/smoke_test.py satisfaction_sheet_id
"""

import sys

from yulee_common import get_client, __version__


def main(spreadsheet_key="spreadsheet_id"):
    print(f"yulee-common {__version__}")
    client = get_client(spreadsheet_key=spreadsheet_key)
    print(f"spreadsheet: {client.sh.title}")
    ws_titles = [ws.title for ws in client.sh.worksheets()]
    print(f"worksheets: {ws_titles[:5]}...")
    if not ws_titles:
        raise RuntimeError("워크시트 0건 — secrets·권한 확인")
    # 첫 워크시트에서 read만 (write 없음, 안전)
    ws = client.ws(ws_titles[0])
    rows = client.read_table(ws)
    print(f"first ws rows: {len(rows)}")
    print("OK")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "spreadsheet_id")
