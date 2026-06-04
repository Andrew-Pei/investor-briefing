"""
日期时间工具
"""
from datetime import datetime


def now_str(fmt: str = "%Y-%m-%d %H:%M") -> str:
    return datetime.now().strftime(fmt)


def today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def is_trading_day() -> bool:
    """简单判断是否为工作日（不包含节假日判断）"""
    return datetime.now().weekday() < 5
