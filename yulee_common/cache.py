# -*- coding: utf-8 -*-
"""Streamlit cache 표준 래퍼.

Streamlit 런타임 밖(테스트·스크립트)에서도 동작하도록,
streamlit 캐시 적용 실패 시 원함수를 그대로 쓴다.
"""

import functools
import logging

logger = logging.getLogger("yulee_common")


def cache_resource(func):
    """@st.cache_resource 래퍼 + 최초 생성 시 로깅."""
    @functools.wraps(func)
    def logged(*args, **kwargs):
        logger.info("cache_resource 생성: %s", func.__name__)
        return func(*args, **kwargs)

    try:
        import streamlit as st
        return st.cache_resource(logged)
    except Exception:
        # Streamlit 밖 — functools 캐시도 걸지 않고 그대로 (테스트 예측 가능성)
        return logged


def cache_data(ttl=300, show_spinner=False):
    """@st.cache_data 표준 설정 래퍼 (기본 ttl 5분, 스피너 끔)."""
    def decorator(func):
        try:
            import streamlit as st
            return st.cache_data(ttl=ttl, show_spinner=show_spinner)(func)
        except Exception:
            return func
    return decorator
