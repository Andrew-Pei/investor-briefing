"""
市场行情服务 - 获取大盘指数、板块排行、北向资金等
"""
from src.config import MARKET_INDICES, SECTOR_RANK_URL, NORTHBOUND_URL, STOCK_FLOW_URL
from utils.request import http_get


def get_market_indices() -> list[dict]:
    """
    获取主要大盘指数行情
    返回: [{name, price, change_pct}, ...]
    """
    results = []
    secids = ",".join(MARKET_INDICES.values())
    url = "https://push2.eastmoney.com/api/qt/ulist.np/get"
    params = {
        "secids": secids,
        "fields": "f2,f3,f12,f14",
        "_": "1",
    }
    data = http_get(url, params=params)
    if data and data.get("data"):
        for item in data["data"].get("diff", []):
            results.append({
                "name": item.get("f14", ""),
                "price": item.get("f2", 0),
                "change_pct": item.get("f3", 0),
            })
    return results


def get_top_sectors(limit: int = 5) -> list[dict]:
    """
    获取行业板块涨幅排行
    返回: [{name, change_pct}, ...]
    """
    params = {
        "pn": 1,
        "pz": limit,
        "po": 1,
        "np": 1,
        "fltt": 2,
        "invt": 2,
        "fid": "f3",
        "fs": "m:90+t:2+f:!50",
        "fields": "f2,f3,f12,f14",
    }
    data = http_get(SECTOR_RANK_URL, params=params)
    results = []
    if data and data.get("data"):
        for item in data["data"].get("diff", []):
            results.append({
                "name": item.get("f14", ""),
                "change_pct": item.get("f3", 0),
            })
    return results


def get_bottom_sectors(limit: int = 5) -> list[dict]:
    """
    获取行业板块跌幅排行
    返回: [{name, change_pct}, ...]
    """
    params = {
        "pn": 1,
        "pz": limit,
        "po": 0,
        "np": 1,
        "fltt": 2,
        "invt": 2,
        "fid": "f3",
        "fs": "m:90+t:2+f:!50",
        "fields": "f2,f3,f12,f14",
    }
    data = http_get(SECTOR_RANK_URL, params=params)
    results = []
    if data and data.get("data"):
        for item in data["data"].get("diff", []):
            results.append({
                "name": item.get("f14", ""),
                "change_pct": item.get("f3", 0),
            })
    return results


def get_northbound_flow() -> dict:
    """
    获取北向资金净流入
    返回: {sh_net: 沪股通净流入, sz_net: 深股通净流入, total: 合计}
    """
    data = http_get(NORTHBOUND_URL)
    if data and data.get("data"):
        try:
            d = data["data"]
            return {
                "sh_net": d.get("hsv2", "N/A"),
                "sz_net": d.get("ssv2", "N/A"),
                "total": d.get("ht2", "N/A"),
            }
        except (KeyError, TypeError):
            pass
    return {"sh_net": "N/A", "sz_net": "N/A", "total": "N/A"}


def get_top_stock_flow(limit: int = 5) -> list[dict]:
    """
    获取个股资金流入排行
    返回: [{name, code, net_amount}, ...]
    """
    params = {
        "pn": 1,
        "pz": limit,
        "po": 1,
        "np": 1,
        "fltt": 2,
        "invt": 2,
        "fid": "f62",
        "fs": "b:BK0800,f:!50",
        "fields": "f2,f3,f12,f14,f62",
    }
    data = http_get(STOCK_FLOW_URL, params=params)
    results = []
    if data and data.get("data"):
        for item in data["data"].get("diff", []):
            results.append({
                "name": item.get("f14", ""),
                "code": item.get("f12", ""),
                "net_amount": item.get("f62", 0),
            })
    return results
