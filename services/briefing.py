"""
简报生成服务 - A股+全球市场
"""
from utils.date_utils import now_str, today_str
from services.market import (
    get_market_indices, get_global_indices,
    get_top_sectors, get_bottom_sectors,
)
from services.news import get_finance_news, get_hot_topics, get_us_news, get_global_news


def _fmt_chg(value) -> str:
    try:
        v = float(value)
        return f"+{v:.2f}%" if v > 0 else f"{v:.2f}%"
    except (TypeError, ValueError):
        return str(value)


def generate_morning_briefing() -> tuple[str, str]:
    """生成上午简报（盘前/开盘）"""
    date_str = today_str()
    title = f"投资早报 {date_str}"

    indices = get_market_indices()
    global_idx = get_global_indices()
    hot_topics = get_hot_topics(8)
    news = get_finance_news(3)
    us_news = get_us_news(3)
    global_news = get_global_news(3)

    lines = [f"## 投资早报 {date_str}\n"]

    # 全球指数（放在最前面）
    lines.append("### 全球指数")
    if global_idx:
        for idx in global_idx:
            chg = _fmt_chg(idx["change_pct"])
            lines.append(f"- **{idx['name']}** {idx['price']:,.2f} ({chg})")
    else:
        lines.append("- 暂无数据")
    lines.append("")

    # A股指数
    lines.append("### A股指数")
    if indices:
        for idx in indices:
            chg = _fmt_chg(idx["change_pct"])
            lines.append(f"- **{idx['name']}** {idx['price']:.2f} ({chg})")
    else:
        lines.append("- 暂无数据")
    lines.append("")

    # 热搜
    lines.append("### 财经热搜")
    if hot_topics:
        for i, topic in enumerate(hot_topics, 1):
            lines.append(f"{i}. {topic}")
    else:
        lines.append("- 暂无数据")
    lines.append("")

    # 新闻
    lines.append("### 要闻速览")
    for item in news:
        lines.append(f"- {item['title']}")
    if us_news:
        lines.append("")
        lines.append("### 美股动态")
        for item in us_news:
            lines.append(f"- {item['title']}")
    if global_news:
        lines.append("")
        lines.append("### 全球市场")
        for item in global_news:
            lines.append(f"- {item['title']}")
    lines.append("")

    lines.append(f"> 生成时间: {now_str()}")
    return title, "\n".join(lines)


def generate_afternoon_briefing() -> tuple[str, str]:
    """生成下午简报（盘后/收盘）"""
    date_str = today_str()
    title = f"投资晚报 {date_str}"

    indices = get_market_indices()
    global_idx = get_global_indices()
    top_sectors = get_top_sectors(5)
    bottom_sectors = get_bottom_sectors(5)
    news = get_finance_news(3)
    us_news = get_us_news(3)
    global_news = get_global_news(3)

    lines = [f"## 投资晚报 {date_str}\n"]

    # 全球指数
    lines.append("### 全球指数")
    if global_idx:
        for idx in global_idx:
            chg = _fmt_chg(idx["change_pct"])
            lines.append(f"- **{idx['name']}** {idx['price']:,.2f} ({chg})")
    else:
        lines.append("- 暂无数据")
    lines.append("")

    # A股收盘
    lines.append("### A股收盘")
    if indices:
        for idx in indices:
            chg = _fmt_chg(idx["change_pct"])
            lines.append(f"- **{idx['name']}** {idx['price']:.2f} ({chg})")
    else:
        lines.append("- 暂无数据")
    lines.append("")

    # 行业板块
    lines.append("### 领涨行业")
    for s in top_sectors:
        chg = _fmt_chg(s["change_pct"])
        lead = f"（{s['lead_stock']}）" if s.get("lead_stock") else ""
        lines.append(f"- {s['name']} ({chg}){lead}")
    lines.append("")

    lines.append("### 领跌行业")
    for s in bottom_sectors:
        chg = _fmt_chg(s["change_pct"])
        lead = f"（{s['lead_stock']}）" if s.get("lead_stock") else ""
        lines.append(f"- {s['name']} ({chg}){lead}")
    lines.append("")

    # 新闻
    lines.append("### 要闻速览")
    for item in news:
        lines.append(f"- {item['title']}")
    if us_news:
        lines.append("")
        lines.append("### 美股动态")
        for item in us_news:
            lines.append(f"- {item['title']}")
    if global_news:
        lines.append("")
        lines.append("### 全球市场")
        for item in global_news:
            lines.append(f"- {item['title']}")
    lines.append("")

    lines.append(f"> 生成时间: {now_str()}")
    return title, "\n".join(lines)
