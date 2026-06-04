"""
通用HTTP请求工具
"""
import requests
from src.config import REQUEST_HEADERS, REQUEST_TIMEOUT


def http_get(url: str, params: dict = None, headers: dict = None) -> dict | None:
    """
    发送 GET 请求，返回 JSON 数据
    """
    try:
        resp = requests.get(
            url,
            params=params,
            headers=headers or REQUEST_HEADERS,
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[请求失败] {url}: {e}")
        return None


def http_get_text(url: str, params: dict = None, headers: dict = None) -> str | None:
    """
    发送 GET 请求，返回文本
    """
    try:
        resp = requests.get(
            url,
            params=params,
            headers=headers or REQUEST_HEADERS,
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"[请求失败] {url}: {e}")
        return None
