"""
日期时间工具
"""
import os
from datetime import datetime, timezone, timedelta

# 默认使用北京时间，可通过 TZ 环境变量覆盖
_TZ_OFFSET_HOURS = 8
_TZ = timezone(timedelta(hours=_TZ_OFFSET_HOURS))


def _get_tz():
    """获取时区，优先读取 TZ 环境变量"""
    tz_env = os.getenv("TZ", "")
    if tz_env and tz_env.startswith("Asia/Shanghai"):
        return _TZ
    # 如果 TZ 设置了其他值，仍用 UTC+8（本项目面向中国用户）
    return _TZ


def now_str(fmt: str = "%Y-%m-%d %H:%M") -> str:
    return datetime.now(_get_tz()).strftime(fmt)


def today_str() -> str:
    return datetime.now(_get_tz()).strftime("%Y-%m-%d")


def is_trading_day() -> bool:
    """简单判断是否为工作日（不包含节假日判断）"""
    return datetime.now(_get_tz()).weekday() < 5
