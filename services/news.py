"""
新闻服务 - 获取财经热点新闻（国内+全球）
"""
import html
import random
import re

from src.config import NEWS_CATEGORIES


def _sina_news(lid: str, limit: int) -> list[dict]:
    """从新浪财经获取指定分类新闻"""
    url = "https://feed.mix.sina.com.cn/api/roll/get"
    params = {
        "pageid": "153",
        "lid": lid,
        "num": limit,
        "page": 1,
        "r": random.random(),
    }
    results = []
    try:
        import requests as rq
        resp = rq.get(url, params=params, timeout=10)
        data = resp.json()
        for item in data.get("result", {}).get("data", []):
            title = item.get("title", "")
            news_url = item.get("url", "")
            if title:
                results.append({"title": title, "url": news_url})
    except Exception as e:
        print(f"[新闻获取失败] lid={lid} {e}")
    return results[:limit]


def get_finance_news(limit: int = 10) -> list[dict]:
    """
    获取财经热点新闻（新浪财经）
    返回: [{title, url}, ...]
    """
    lid = NEWS_CATEGORIES.get("财经要闻", "2516")
    return _sina_news(lid, limit)


def get_us_news(limit: int = 10) -> list[dict]:
    """
    获取美股相关新闻（新浪财经美股频道）
    返回: [{title, url}, ...]
    """
    lid = NEWS_CATEGORIES.get("美股", "2518")
    return _sina_news(lid, limit)


def get_global_news(limit: int = 10) -> list[dict]:
    """
    获取全球财经新闻（CNBC RSS）
    返回: [{title, url}, ...]
    """
    url = "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100727362"
    results = []
    try:
        import requests as rq
        resp = rq.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        resp.encoding = "utf-8"
        titles = re.findall(r"<title><!\[CDATA\[(.*?)\]\]></title>", resp.text)
        if not titles:
            titles = re.findall(r"<title>(.*?)</title>", resp.text)
        links = re.findall(r"<link>(.*?)</link>", resp.text)
        for i, title in enumerate(titles):
            title = html.unescape(title.strip())
            if not title or "Top News" in title:
                continue
            link = links[i].strip() if i < len(links) else ""
            results.append({"title": title, "url": link})
            if len(results) >= limit:
                break
    except Exception as e:
        print(f"[全球新闻获取失败] {e}")
    return results[:limit]


def get_hot_topics(limit: int = 8) -> list[str]:
    """
    获取热搜话题（从百度热搜）
    返回: [topic1, topic2, ...]
    """
    url = "https://top.baidu.com/api/board"
    params = {
        "platform": "wise",
        "tab": "realtime",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
    }
    topics = []
    try:
        import requests as rq
        resp = rq.get(url, params=params, headers=headers, timeout=10)
        data = resp.json()
        for card in data.get("data", {}).get("cards", []):
            for group in card.get("content", []):
                if isinstance(group, dict):
                    inner = group.get("content", [])
                    if isinstance(inner, list):
                        for item in inner:
                            if isinstance(item, dict):
                                word = item.get("word", "")
                                if word:
                                    topics.append(word)
                if len(topics) >= limit:
                    break
            if len(topics) >= limit:
                break
    except Exception as e:
        print(f"[热搜获取失败] {e}")

    return topics[:limit]
