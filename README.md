# 投资简报 - 全球市场每日推送

面向国内投资者的每日全球市场简报，覆盖 A股 + 美股 + 港股 + 全球主要指数，定时推送到微信。

## 功能

- **全球指数**: 道琼斯、标普500、纳斯达克、恒生、日经225、富时100、德国DAX（Yahoo Finance 实时数据）
- **美股行业**: 11个行业ETF涨跌排行（能源/科技/金融/医疗等）
- **A股指数**: 上证、深证、创业板、科创50
- **A股行业**: 行业涨跌排行+领涨股
- **要闻速览**: 新浪财经（带超链接，点击跳转原文）
- **美股动态**: 新浪财经美股频道
- **全球市场**: CNBC 国际新闻
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
- 美股行业涨跌排行
- A股行业涨跌排行
- 要闻速览 + 美股动态 + 全球市场

### 晚报（15:30）
- 全球指数行情
- A股收盘行情
- 美股行业涨跌排行
- A股行业涨跌排行
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

GitHub Actions 自动推送，零成本：
1. Fork 本仓库
2. 在 Settings -> Secrets -> Actions 添加 `SERVERCHAN_SENDKEY`
3. 每天自动推送早报(08:30) + 晚报(15:30)

也可手动触发：Actions 页面 -> Run workflow

## 项目现状

**做得还行**
- 功能闭环：数据采集 -> 简报生成 -> 微信推送 -> 定时调度，全链路打通
- 全球覆盖：7个全球指数 + 11个美股行业ETF + A股指数 + A股行业 + 三源新闻
- 新闻去重 + 超链接，用户体验细节有考虑

**已知短板**
- **新闻质量**：新浪财经推送的内容与投资相关性不强，CNBC 英文新闻未做主题筛选
- **无降级机制**：Yahoo Finance 限流/封IP 时全球指数和美股行业全部为空，无缓存无 fallback
- **早晚报差异小**：盘前和盘后用户关注点不同，目前结构几乎一样
- **Yahoo Finance 风险**：使用非官方 query1 API，无 API key，云服务器调用频率高可能触发限流

**待优化方向**
1. Yahoo Finance 备选方案（新浪 gb_ 美股代码等）
2. 新闻源质量提升（过滤投资无关内容，或换更专业的源）
3. 早晚报差异化内容

## License

MIT
