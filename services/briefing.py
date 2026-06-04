"""
简报生成服务 - A股+全球市场
"""
from utils.date_utils import now_str, today_str
from services.market import (
    get_market_indices, get_global_indices,
    get_global_sectors, get_a_share_sectors,
)
from services.news import get_finance_news, get_us_news, get_global_news


def _fmt_chg(value) -> str:
    try:
        v = float(value)
        return f"+{v:.2f}%" if v > 0 else f"{v:.2f}%"
    except (TypeError, ValueError):
        return str(value)


def _news_link(title: str, url: str) -> str:
    if url:
        return f"- [{title}]({url})"
    return f"- {title}"


def _dedup_news(*news_lists: list[dict]) -> list[list[dict]]:
    seen = set()
    result = []
    for lst in news_lists:
        deduped = []
        for item in lst:
            t = item["title"]
            if t not in seen:
                seen.add(t)
                deduped.append(item)
        result.append(deduped)
    return result


def _render_sectors(top: list[dict], bottom: list[dict], label: str, lines: list[str]):
    """渲染行业板块涨跌"""
    if not top and not bottom:
        return
    if top:
        lines.append(f"### {label}领涨")
        for s in top:
            lead = f"（{s['lead_stock']}）" if s.get("lead_stock") else ""
            lines.append(f"- {s['name']} ({_fmt_chg(s['change_pct'])}){lead}")
        lines.append("")
    if bottom:
        lines.append(f"### {label}领跌")
        for s in bottom:
            lead = f"（{s['lead_stock']}）" if s.get("lead_stock") else ""
            lines.append(f"- {s['name']} ({_fmt_chg(s['change_pct'])}){lead}")
        lines.append("")


def generate_morning_briefing() -> tuple[str, str]:
    """生成上午简报（盘前/开盘）"""
    date_str = today_str()
    title = f"投资早报 {date_str}"

    indices = get_market_indices()
    global_idx = get_global_indices()
    g_top, g_bottom = get_global_sectors(3)
    a_top, a_bottom = get_a_share_sectors(3)
    news = get_finance_news(3)
    us_news = get_us_news(3)
    global_news = get_global_news(3)
    news, us_news, global_news = _dedup_news(news, us_news, global_news)

    lines = [f"## 投资早报 {date_str}\n"]

    lines.append("### 全球指数")
    if global_idx:
        for idx in global_idx:
            chg = _fmt_chg(idx["change_pct"])
            lines.append(f"- **{idx['name']}** {idx['price']:,.2f} ({chg})")
    else:
        lines.append("- 暂无数据")
    lines.append("")

    lines.append("### A股指数")
    if indices:
        for idx in indices:
            chg = _fmt_chg(idx["change_pct"])
            lines.append(f"- **{idx['name']}** {idx['price']:.2f} ({chg})")
    else:
        lines.append("- 暂无数据")
    lines.append("")

    _render_sectors(g_top, g_bottom, "美股行业", lines)
    _render_sectors(a_top, a_bottom, "A股行业", lines)

    if news:
        lines.append("### 要闻速览")
        for item in news:
            lines.append(_news_link(item["title"], item.get("url", "")))
        lines.append("")
    if us_news:
        lines.append("### 美股动态")
        for item in us_news:
            lines.append(_news_link(item["title"], item.get("url", "")))
        lines.append("")
    if global_news:
        lines.append("### 全球市场")
        for item in global_news:
            lines.append(_news_link(item["title"], item.get("url", "")))
        lines.append("")

    lines.append(f"> 生成时间: {now_str()}")
    return title, "\n".join(lines)


def generate_afternoon_briefing() -> tuple[str, str]:
    """生成下午简报（盘后/收盘）"""
    date_str = today_str()
    title = f"投资晚报 {date_str}"

    indices = get_market_indices()
    global_idx = get_global_indices()
    g_top, g_bottom = get_global_sectors(3)
    a_top, a_bottom = get_a_share_sectors(3)
    news = get_finance_news(3)
    us_news = get_us_news(3)
    global_news = get_global_news(3)
    news, us_news, global_news = _dedup_news(news, us_news, global_news)

    lines = [f"## 投资晚报 {date_str}\n"]

    lines.append("### 全球指数")
    if global_idx:
        for idx in global_idx:
            chg = _fmt_chg(idx["change_pct"])
            lines.append(f"- **{idx['name']}** {idx['price']:,.2f} ({chg})")
    else:
        lines.append("- 暂无数据")
    lines.append("")

    lines.append("### A股收盘")
    if indices:
        for idx in indices:
            chg = _fmt_chg(idx["change_pct"])
            lines.append(f"- **{idx['name']}** {idx['price']:.2f} ({chg})")
    else:
        lines.append("- 暂无数据")
    lines.append("")

    _render_sectors(g_top, g_bottom, "美股行业", lines)
    _render_sectors(a_top, a_bottom, "A股行业", lines)

    if news:
        lines.append("### 要闻速览")
        for item in news:
            lines.append(_news_link(item["title"], item.get("url", "")))
        lines.append("")
    if us_news:
        lines.append("### 美股动态")
        for item in us_news:
            lines.append(_news_link(item["title"], item.get("url", "")))
        lines.append("")
    if global_news:
        lines.append("### 全球市场")
        for item in global_news:
            lines.append(_news_link(item["title"], item.get("url", "")))
        lines.append("")

    lines.append(f"> 生成时间: {now_str()}")
    return title, "\n".join(lines)
