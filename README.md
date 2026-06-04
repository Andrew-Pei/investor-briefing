# 投资简报 - 个人投资趋势追踪工具

面向国内个人投资者的每日投资简报工具，自动追踪市场行情和热点新闻，定时推送到微信。

## 功能

- **大盘指数**: 上证、深证、创业板、科创50实时行情
- **行业板块**: 涨跌幅排行
- **北向资金**: 沪深港通资金流向
- **个股资金流**: 主力资金流入排行
- **财经热搜**: 实时财经热门话题
- **要闻速览**: 东方财富重要财经新闻
- **微信推送**: 通过 Server酱 推送到个人微信

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 Server酱

前往 [Server酱](https://sct.ftqq.com/) 注册并获取 SendKey，然后设置环境变量：

```bash
# Windows
set SERVERCHAN_SENDKEY=你的SendKey

# Linux/Mac
export SERVERCHAN_SENDKEY=你的SendKey
```

### 3. 运行

```bash
# 启动定时服务（上午08:30 + 下午15:30）
python main.py server

# 立即发送上午简报
python main.py now morning

# 立即发送下午简报
python main.py now afternoon
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SERVERCHAN_SENDKEY` | Server酱 SendKey（必填） | - |
| `MORNING_BRIEFING_TIME` | 上午简报时间 | 08:30 |
| `AFTERNOON_BRIEFING_TIME` | 下午简报时间 | 15:30 |

## 简报内容

### 上午简报（盘前）
- 大盘指数行情
- 财经热搜话题
- 重要财经新闻

### 下午简报（盘后）
- 收盘指数行情
- 领涨/领跌行业板块
- 北向资金流向
- 个股资金流入TOP5
- 重要财经新闻

## 数据来源

- [东方财富](https://www.eastmoney.com/) - 行情数据、新闻
- [Server酱](https://sct.ftqq.com/) - 微信推送

## 项目结构

```
investor-briefing/
├── main.py              # 主入口
├── requirements.txt     # 依赖
├── src/
│   └── config.py        # 配置
├── services/
│   ├── market.py        # 行情服务
│   ├── news.py          # 新闻服务
│   └── briefing.py      # 简报生成
└── utils/
    ├── wechat.py        # 微信推送
    ├── request.py       # HTTP工具
    └── date_utils.py    # 日期工具
```
