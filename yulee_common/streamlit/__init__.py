# -*- coding: utf-8 -*-
"""yulee_common.streamlit — Streamlit 부트스트랩 헬퍼 (v0.4.0).

주의: 이 패키지명은 yulee_common 내부 하위 모듈이며, 절대 import 규칙에 따라
``import streamlit`` 은 항상 최상위 Streamlit 패키지를 가리킨다(충돌 없음).
"""

from .page_config import setup_page, inject_design

__all__ = ["setup_page", "inject_design"]
