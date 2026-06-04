"""
投资简报 - 配置文件
"""
import os
from pathlib import Path

# 加载 .env 文件
_env_file = Path(__file__).resolve().parent.parent / ".env"
if _env_file.exists():
    for line in _env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip()
            if key and key not in os.environ:
                os.environ[key] = value

# ============ 微信推送配置 ============
SERVERCHAN_SENDKEY = os.getenv("SERVERCHAN_SENDKEY", "")

# ============ 定时配置 ============
MORNING_BRIEFING_TIME = os.getenv("MORNING_BRIEFING_TIME", "08:30")
AFTERNOON_BRIEFING_TIME = os.getenv("AFTERNOON_BRIEFING_TIME", "15:30")

# ============ 数据源配置 ============
# 新浪 - A股大盘指数
A_SHARE_INDICES = {
    "上证指数": "s_sh000001",
    "深证成指": "s_sz399001",
    "创业板指": "s_sz399006",
    "科创50": "s_sh000688",
}

# Yahoo Finance - 全球指数
GLOBAL_INDICES = {
    "道琼斯": "^DJI",
    "标普500": "^GSPC",
    "纳斯达克": "^IXIC",
    "恒生指数": "^HSI",
    "日经225": "^N225",
    "富时100": "^FTSE",
    "德国DAX": "^GDAXI",
}

# Yahoo Finance - 美股行业ETF
US_SECTOR_ETFS = {
    "科技": "XLK",
    "金融": "XLF",
    "医疗": "XLV",
    "可选消费": "XLY",
    "工业": "XLI",
    "能源": "XLE",
    "材料": "XLB",
    "公用事业": "XLU",
    "房地产": "XLRE",
    "通信": "XLC",
    "必需消费": "XLP",
}

# 新浪财经 - 新闻分类 lid
NEWS_CATEGORIES = {
    "财经要闻": "2516",
    "美股": "2518",
}

# ============ 请求配置 ============
REQUEST_TIMEOUT = 10
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://finance.sina.com.cn",
}
