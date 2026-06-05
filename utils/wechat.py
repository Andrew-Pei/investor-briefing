"""
微信推送工具 - 通过 Server酱 推送消息到微信
注册地址: https://sct.ftqq.com/
"""
import requests
from src.config import SERVERCHAN_SENDKEY


def send_wechat(title: str, content: str) -> bool:
    """
    通过 Server酱 发送消息到微信

    Args:
        title: 消息标题
        content: 消息内容（支持 Markdown）

    Returns:
        是否发送成功
    """
    if not SERVERCHAN_SENDKEY:
        print("[警告] SERVERCHAN_SENDKEY 未配置，消息未发送")
        print(f"[预览] 标题: {title}")
        print(f"[预览] 内容:\n{content}")
        return False

    url = f"https://sctapi.ftqq.com/{SERVERCHAN_SENDKEY}.send"
    data = {
        "title": title,
        "desp": content,
    }

    try:
        s = requests.Session()
        s.trust_env = False
        resp = s.post(url, data=data, timeout=10)
        result = resp.json()
        if result.get("code") == 0:
            print(f"[微信推送] 发送成功: {title}")
            return True
        else:
            print(f"[微信推送] 发送失败: {result}")
            return False
    except Exception as e:
        print(f"[微信推送] 异常: {e}")
        return False
