"""
投资简报 - 主入口
支持两种运行模式:
1. 定时服务模式: python main.py server  (后台定时发送简报)
2. 即时发送模式: python main.py now morning|afternoon  (立即生成并发送)
"""
import sys
from apscheduler.schedulers.blocking import BlockingScheduler
from src.config import MORNING_BRIEFING_TIME, AFTERNOON_BRIEFING_TIME
from services.briefing import generate_morning_briefing, generate_afternoon_briefing
from utils.wechat import send_wechat
from utils.date_utils import is_trading_day


def send_morning():
    """生成并发送上午简报"""
    print("=" * 40)
    print("[早报] 开始生成上午简报...")
    title, content = generate_morning_briefing()
    print(content)
    send_wechat(title, content)
    print("[早报] 发送完成")


def send_afternoon():
    """生成并发送下午简报"""
    print("=" * 40)
    print("[晚报] 开始生成下午简报...")
    title, content = generate_afternoon_briefing()
    print(content)
    send_wechat(title, content)
    print("[晚报] 发送完成")


def run_server():
    """启动定时调度服务"""
    scheduler = BlockingScheduler()

    # 上午简报 - 默认08:30
    h_m = MORNING_BRIEFING_TIME.split(":")
    scheduler.add_job(
        send_morning,
        "cron",
        hour=int(h_m[0]),
        minute=int(h_m[1]),
        id="morning_briefing",
        name="上午简报",
    )

    # 下午简报 - 默认15:30
    h_m = AFTERNOON_BRIEFING_TIME.split(":")
    scheduler.add_job(
        send_afternoon,
        "cron",
        hour=int(h_m[0]),
        minute=int(h_m[1]),
        id="afternoon_briefing",
        name="下午简报",
    )

    print(f"投资简报服务已启动")
    print(f"  上午简报: 每日 {MORNING_BRIEFING_TIME}")
    print(f"  下午简报: 每日 {AFTERNOON_BRIEFING_TIME}")
    print("按 Ctrl+C 退出\n")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\n服务已停止")


def run_now(briefing_type: str):
    """立即生成并发送简报"""
    if briefing_type == "morning":
        send_morning()
    elif briefing_type == "afternoon":
        send_afternoon()
    else:
        print(f"未知的简报类型: {briefing_type}")
        print("用法: python main.py now morning|afternoon")
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("投资简报 - 个人投资趋势追踪工具")
        print()
        print("用法:")
        print("  python main.py server                    启动定时服务")
        print("  python main.py now morning               立即发送上午简报")
        print("  python main.py now afternoon             立即发送下午简报")
        print()
        print("环境变量:")
        print("  SERVERCHAN_SENDKEY       Server酱 SendKey（必填）")
        print("  MORNING_BRIEFING_TIME    上午简报时间，默认 08:30")
        print("  AFTERNOON_BRIEFING_TIME  下午简报时间，默认 15:30")
        sys.exit(0)

    command = sys.argv[1]

    if command == "server":
        run_server()
    elif command == "now":
        if len(sys.argv) < 3:
            print("请指定简报类型: python main.py now morning|afternoon")
            sys.exit(1)
        run_now(sys.argv[2])
    else:
        print(f"未知命令: {command}")
        print("可用命令: server, now")
        sys.exit(1)


if __name__ == "__main__":
    main()
