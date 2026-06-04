"""
简报生成服务 - 将行情和新闻组装为简报内容
"""
from utils.date_utils import now_str, today_str
from services.market import (
    get_market_indices,
    get_top_sectors,
    get_bottom_sectors,
    get_northbound_flow,
    get_top_stock_flow,
)
from services.news import get_finance_news, get_hot_topics


def _format_change(value) -> str:
    """格式化涨跌幅"""
    try:
        v = float(value)
        if v > 0:
            return f"+{v:.2f}%"
        return f"{v:.2f}%"
    except (TypeError, ValueError):
        return str(value)


def _format_amount(value) -> str:
    """格式化金额（亿）"""
    try:
        v = float(value)
        if abs(v) >= 1e8:
            return f"{v / 1e8:.2f}亿"
        elif abs(v) >= 1e4:
            return f"{v / 1e4:.2f}万"
        return f"{v:.2f}"
    except (TypeError, ValueError):
        return str(value)


def generate_morning_briefing() -> tuple[str, str]:
    """
    生成上午简报（盘前/开盘）
    返回: (title, markdown_content)
    """
    date_str = today_str()
    title = f"投资早报 {date_str}"

    # 获取数据
    indices = get_market_indices()
    hot_topics = get_hot_topics(8)
    news = get_finance_news(6)

    # 组装内容
    lines = [f"## 投资早报 {date_str}\n"]

    # 大盘指数
    lines.append("### 大盘指数")
    if indices:
        for idx in indices:
            chg = _format_change(idx["change_pct"])
            lines.append(f"- **{idx['name']}** {idx['price']} ({chg})")
    else:
        lines.append("- 暂无数据")
    lines.append("")

    # 热搜话题
    lines.append("### 财经热搜")
    if hot_topics:
        for i, topic in enumerate(hot_topics, 1):
            lines.append(f"{i}. {topic}")
    else:
        lines.append("- 暂无数据")
    lines.append("")

    # 重要新闻
    lines.append("### 要闻速览")
    if news:
        for item in news[:6]:
            title_text = item["title"]
            lines.append(f"- {title_text}")
    else:
        lines.append("- 暂无数据")
    lines.append("")

    lines.append(f"> 生成时间: {now_str()}")

    return title, "\n".join(lines)


def generate_afternoon_briefing() -> tuple[str, str]:
    """
    生成下午简报（盘后/收盘）
    返回: (title, markdown_content)
    """
    date_str = today_str()
    title = f"投资晚报 {date_str}"

    # 获取数据
    indices = get_market_indices()
    top_sectors = get_top_sectors(5)
    bottom_sectors = get_bottom_sectors(5)
    northbound = get_northbound_flow()
    stock_flow = get_top_stock_flow(5)
    news = get_finance_news(6)

    # 组装内容
    lines = [f"## 投资晚报 {date_str}\n"]

    # 大盘指数
    lines.append("### 收盘指数")
    if indices:
        for idx in indices:
            chg = _format_change(idx["change_pct"])
            lines.append(f"- **{idx['name']}** {idx['price']} ({chg})")
    else:
        lines.append("- 暂无数据")
    lines.append("")

    # 行业板块
    lines.append("### 领涨行业")
    if top_sectors:
        for s in top_sectors:
            chg = _format_change(s["change_pct"])
            lines.append(f"- {s['name']} ({chg})")
    else:
        lines.append("- 暂无数据")
    lines.append("")

    lines.append("### 领跌行业")
    if bottom_sectors:
        for s in bottom_sectors:
            chg = _format_change(s["change_pct"])
            lines.append(f"- {s['name']} ({chg})")
    else:
        lines.append("- 暂无数据")
    lines.append("")

    # 北向资金
    lines.append("### 北向资金")
    lines.append(f"- 沪股通净流入: {northbound['sh_net']}")
    lines.append(f"- 深股通净流入: {northbound['sz_net']}")
    lines.append(f"- 合计净流入: {northbound['total']}")
    lines.append("")

    # 资金流入个股
    lines.append("### 资金流入TOP5")
    if stock_flow:
        for s in stock_flow:
            amt = _format_amount(s["net_amount"])
            lines.append(f"- {s['name']}({s['code']}) 净流入 {amt}")
    else:
        lines.append("- 暂无数据")
    lines.append("")

    # 新闻
    lines.append("### 要闻速览")
    if news:
        for item in news[:6]:
            lines.append(f"- {item['title']}")
    else:
        lines.append("- 暂无数据")
    lines.append("")

    lines.append(f"> 生成时间: {now_str()}")

    return title, "\n".join(lines)
