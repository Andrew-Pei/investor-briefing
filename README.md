# 投资简报 - 全球市场每日推送

面向国内投资者的每日全球市场简报，覆盖 A股 + 美股 + 港股 + 全球主要指数，定时推送到微信。

## 功能

- **全球指数**: 道琼斯、标普500、纳斯达克、恒生、日经225、富时100、德国DAX（Yahoo Finance 实时数据）
- **A股指数**: 上证、深证、创业板、科创50
- **行业板块**: A股行业涨跌幅排行
- **美股动态**: 新浪财经美股频道
- **全球市场**: CNBC 国际新闻
- **财经热搜**: 实时热门话题
- **微信推送**: Server酱 推送到微信

## 快速开始

### 1. 安装依赖

```bash
pip install requests APScheduler
```

或使用 uv：

```bash
uv run --with requests --with APScheduler python main.py server
```

### 2. 配置

在项目根目录创建 `.env` 文件：

```
SERVERCHAN_SENDKEY=你的SendKey
```

SendKey 在 [Server酱](https://sct.ftqq.com/) 注册获取。

### 3. 运行

```bash
# 启动定时服务（08:30 早报 + 15:30 晚报）
python main.py server

# 立即发送
python main.py now morning
python main.py now afternoon
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SERVERCHAN_SENDKEY` | Server酱 SendKey | - |
| `MORNING_BRIEFING_TIME` | 早报时间 | 08:30 |
| `AFTERNOON_BRIEFING_TIME` | 晚报时间 | 15:30 |

## 简报内容

### 早报（08:30）
- 全球指数行情
- A股指数行情
- 财经热搜话题
- 要闻速览 + 美股动态 + 全球市场

### 晚报（15:30）
- 全球指数行情
- A股收盘行情
- 领涨/领跌行业
- 要闻速览 + 美股动态 + 全球市场

## 数据来源

- [Yahoo Finance](https://finance.yahoo.com/) - 全球指数实时数据
- [新浪财经](https://finance.sina.com.cn/) - A股行情、行业板块、新闻
- [CNBC](https://www.cnbc.com/) - 全球市场新闻
- [Server酱](https://sct.ftqq.com/) - 微信推送

## 项目结构

```
investor-briefing/
├── main.py              # 主入口
├── .env                 # 配置（不入库）
├── src/
│   └── config.py        # 配置定义
├── services/
│   ├── market.py        # 行情服务（A股+全球指数+板块）
│   ├── news.py          # 新闻服务（国内+美股+全球）
│   └── briefing.py      # 简报生成
└── utils/
    ├── wechat.py        # 微信推送
    ├── request.py       # HTTP工具
    └── date_utils.py    # 日期工具
```

## 部署

支持部署到 Render、Railway、Fly.io 等免费平台，配置 `SERVERCHAN_SENDKEY` 环境变量即可自动每日推送。

## License

MIT
