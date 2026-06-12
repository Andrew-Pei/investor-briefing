"""
市场行情服务 - A股用新浪，全球指数+美股行业用Yahoo Finance，A股行业用新浪
"""
import json
import re

import requests

from src.config import A_SHARE_INDICES, GLOBAL_INDICES, US_SECTOR_ETFS

SINA_HEADERS = {
    "Referer": "https://finance.sina.com.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}

YF_HEADERS = {"User-Agent": "Mozilla/5.0"}


def _yf_change_pct(symbol: str) -> float | None:
    """从 Yahoo Finance 获取单只标的涨跌幅"""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=1d&interval=1d"
    resp = requests.get(url, headers=YF_HEADERS, timeout=10)
    data = resp.json()
    meta = data["chart"]["result"][0]["meta"]
    price = meta.get("regularMarketPrice", 0)
    prev = meta.get("chartPreviousClose", meta.get("previousClose", 0))
    if prev:
        return round((price - prev) / prev * 100, 2)
    return None


def get_market_indices() -> list[dict]:
    """获取A股主要大盘指数行情（新浪接口）"""
    codes = ",".join(A_SHARE_INDICES.values())
    code_to_name = {v: k for k, v in A_SHARE_INDICES.items()}
    results = []
    try:
        url = f"https://hq.sinajs.cn/list={codes}"
        resp = requests.get(url, headers=SINA_HEADERS, timeout=10)
        resp.encoding = "gbk"
        pattern = re.compile(r'var hq_str_(\w+)="(.+?)"')
        for match in pattern.finditer(resp.text):
            code, content = match.group(1), match.group(2)
            if not content:
                continue
            parts = content.split(",")
            try:
                name = code_to_name.get(code, parts[0])
                price = float(parts[1])
                change = float(parts[2])
                change_pct = float(parts[3])
                results.append({
                    "name": name, "price": price,
                    "change": change, "change_pct": change_pct,
                })
            except (IndexError, ValueError):
                continue
    except Exception as e:
        print(f"[A股指数获取失败] {e}")
    return results


def get_global_indices() -> list[dict]:
    """获取全球主要指数行情（Yahoo Finance）"""
    results = []
    for name, symbol in GLOBAL_INDICES.items():
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=1d&interval=1d"
            resp = requests.get(url, headers=YF_HEADERS, timeout=10)
            data = resp.json()
            meta = data["chart"]["result"][0]["meta"]
            price = meta.get("regularMarketPrice", 0)
            prev = meta.get("chartPreviousClose", meta.get("previousClose", 0))
            change_pct = round((price - prev) / prev * 100, 2) if prev else 0
            change = round(price - prev, 2) if prev else 0
            results.append({
                "name": name, "price": price,
                "change": change, "change_pct": change_pct,
            })
        except Exception:
            continue
    return results


def get_global_sectors(limit: int = 3) -> tuple[list[dict], list[dict]]:
    """
    获取美股行业板块涨跌幅排行（Yahoo Finance ETF）
    返回: (top_sectors, bottom_sectors)
    """
    results = []
    for name, symbol in US_SECTOR_ETFS.items():
        try:
            chg = _yf_change_pct(symbol)
            if chg is not None:
                results.append({"name": f"美股{name}", "change_pct": chg})
        except Exception:
            continue
    results.sort(key=lambda x: x["change_pct"], reverse=True)
    return results[:limit], results[-limit:]


def get_a_share_sectors(limit: int = 3) -> tuple[list[dict], list[dict]]:
    """
    获取A股行业板块涨跌幅排行（新浪接口）
    返回: (top_sectors, bottom_sectors)
    """
    sectors = _fetch_sina_sectors()
    sectors.sort(key=lambda x: x["change_pct"], reverse=True)
    return sectors[:limit], list(reversed(sectors[-limit:]))


def _fetch_sina_sectors() -> list[dict]:
    """从新浪获取全部行业板块数据"""
    url = "https://vip.stock.finance.sina.com.cn/q/view/newSinaHy.php"
    try:
        resp = requests.get(url, headers=SINA_HEADERS, timeout=10)
        resp.encoding = "gbk"
        match = re.search(
            r'var S_Finance_bankuai_sinaindustry\s*=\s*(\{.*\})', resp.text, re.DOTALL,
        )
        if not match:
            return []
        data = json.loads(match.group(1))
        sectors = []
        for key, val in data.items():
            parts = val.split(",")
            try:
                name = parts[1]
                change_pct = float(parts[5])
                lead_stock = parts[12] if len(parts) > 12 else ""
                lead_code = parts[8] if len(parts) > 8 else ""
                sectors.append({
                    "name": name, "change_pct": change_pct,
                    "lead_stock": lead_stock, "lead_code": lead_code,
                })
            except (IndexError, ValueError):
                continue
        return sectors
    except Exception as e:
        print(f"[行业板块获取失败] {e}")
        return []
