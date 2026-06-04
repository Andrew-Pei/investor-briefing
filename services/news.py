"""
新闻服务 - 获取财经热点新闻
"""
import re
from utils.request import http_get_text


def get_finance_news(limit: int = 10) -> list[dict]:
    """
    获取财经热点新闻（从东方财富要闻）
    返回: [{title, url}, ...]
    """
    url = "https://np-listapi.eastmoney.com/comm/web/getNewsByColumn"
    params = {
        "client": "web",
        "biz": "web_news_col",
        "column": "350",
        "order": "1",
        "needInteractData": "0",
        "page_index": 1,
        "page_size": limit,
    }
    data = None
    try:
        import requests as rq
        resp = rq.get(url, params=params, timeout=10)
        data = resp.json()
    except Exception as e:
        print(f"[新闻获取失败] {e}")

    results = []
    if data and data.get("data"):
        for item in data["data"].get("list", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
            })
    return results


def get_hot_topics(limit: int = 8) -> list[str]:
    """
    获取财经热搜话题
    返回: [topic1, topic2, ...]
    """
    url = "https://searchapi.eastmoney.com/api/suggest/gethot"
    params = {
        "type": "0",
        "pagesize": limit,
    }
    topics = []
    try:
        import requests as rq
        resp = rq.get(url, params=params, timeout=10)
        data = resp.json()
        if data.get("Data"):
            for item in data["Data"]:
                title = item.get("Title", "")
                if title:
                    topics.append(title)
    except Exception as e:
        print(f"[热搜获取失败] {e}")

    return topics[:limit]
