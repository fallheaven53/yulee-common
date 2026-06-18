# -*- coding: utf-8 -*-
"""yulee_common.styles — 정적 자산 패키지 (main.css + Pretendard woff2).

코드는 없고 package_data 포함을 위한 패키지 마커. main.css 경로는
``importlib.resources`` 또는 ``os.path`` 로 참조한다.
"""

import os

STYLES_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_CSS = os.path.join(STYLES_DIR, "main.css")
FONTS_DIR = os.path.join(STYLES_DIR, "fonts")
