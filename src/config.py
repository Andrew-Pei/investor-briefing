"""
投资简报 - 配置文件
"""
import os

# ============ 微信推送配置 ============
# Server酱 SendKey，在 https://sct.ftqq.com/ 获取
SERVERCHAN_SENDKEY = os.getenv("SERVERCHAN_SENDKEY", "")

# ============ 定时配置 ============
# 上午简报时间
MORNING_BRIEFING_TIME = os.getenv("MORNING_BRIEFING_TIME", "08:30")
# 下午简报时间
AFTERNOON_BRIEFING_TIME = os.getenv("AFTERNOON_BRIEFING_TIME", "15:30")

# ============ 数据源配置 ============
# 东方财富 - 大盘指数
MARKET_INDICES = {
    "上证指数": "1.000001",
    "深证成指": "0.399001",
    "创业板指": "0.399006",
    "科创50": "1.000688",
}

# 东方财富 - 北向资金
NORTHBOUND_URL = "https://push2.eastmoney.com/api/qt/kamtbs.wss"

# 东方财富 - 板块排行
SECTOR_RANK_URL = "https://push2.eastmoney.com/api/qt/clist/get"

# 新浪财经 - 热搜新闻
NEWS_URL = "https://tophub.today/n/KqndgxeLl9"

# 东方财富 - 个股资金流
STOCK_FLOW_URL = "https://push2.eastmoney.com/api/qt/clist/get"

# ============ 请求配置 ============
REQUEST_TIMEOUT = 10
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.eastmoney.com/",
}
