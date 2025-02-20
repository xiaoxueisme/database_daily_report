# 数据库资讯日报系统

一个自动化的数据库相关新闻和资讯聚合系统，支持从多个来源收集信息并通过企业微信机器人推送日报。

## 功能特点

- 自动从多个来源收集数据库相关新闻和资讯
- 支持的信息来源：
  - 主流云服务商的数据库公众号
  - 云服务商官网数据库频道
  - 行业专家博客和技术社区
- 智能分类和整理新闻内容
- 生成结构化的日报，包含内容总结和详细信息
- 通过企业微信机器人自动推送日报
- 支持Markdown格式的报告
- 定时任务，每天固定时间推送

## 系统要求

- Python 3.8+
- 企业微信群聊机器人

## 安装

1. 克隆代码库：
```bash
git clone [repository-url]
cd database-daily-report
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置企业微信机器人：
   - 进入企业微信群聊
   - 点击右上角的群设置图标
   - 选择"群机器人" -> "添加机器人"
   - 设置机器人名称并获取Webhook地址

4. 配置Webhook：
可以选择以下两种方式之一：

a. 环境变量方式：创建 `.env` 文件并添加：
```
WECHAT_WEBHOOK_URL=your_webhook_url
```

b. 配置文件方式：编辑 `config/config.yaml` 文件：
```yaml
wechat:
  webhook_url: "your_webhook_url"  # 从企业微信群机器人获取的webhook地址
```

## 使用方法

1. 启动服务：
```bash
python src/main.py
```

2. 服务将在配置的时间（默认每天10:00）自动推送日报

## 日报格式

日报包含以下部分：
1. 内容总结
   - 新闻总数
   - 涉及领域
2. 详细内容
   - 按类别分组的新闻列表
   - 每条新闻包含标题、来源、链接和日期
3. 信息来源汇总

## 开发说明

### 项目结构
```
database_daily_report/
├── src/
│   ├── __init__.py
│   ├── crawler.py      # 新闻爬取模块
│   ├── processor.py    # 内容处理模块
│   ├── wechat_pusher.py# 企业微信推送模块
│   └── main.py         # 主程序
├── config/
│   └── config.yaml     # 配置文件
├── logs/               # 日志目录
├── requirements.txt    # 依赖列表
└── README.md          # 项目文档
```

### 主要模块说明

- `crawler.py`: 负责从各个来源收集新闻信息
- `processor.py`: 处理和格式化新闻内容
- `wechat_pusher.py`: 处理企业微信机器人消息推送
- `main.py`: 协调各个模块工作，处理定时任务

## 注意事项

1. 确保webhook地址配置正确
2. 检查网络连接是否正常
3. 定期检查日志文件
4. 注意机器人消息发送频率限制
5. webhook地址不要泄露或直接提交到代码仓库

## 常见问题

1. Q: 如何修改推送时间？
   A: 在 `config.yaml` 中修改 `report.schedule_time` 配置项

2. Q: 如何添加新的信息来源？
   A: 在 `config.yaml` 中的相应部分添加新的来源配置

3. Q: 日志在哪里查看？
   A: 查看 `logs/daily_report.log` 文件

4. Q: 消息发送失败怎么办？
   A: 检查webhook地址是否正确，网络是否正常，查看日志获取详细错误信息

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证

MIT License
