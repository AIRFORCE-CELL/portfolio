# 📦 客户交付文件夹

每个子文件夹 = 一个可直接打包发给客户的产品。

## 目录

```
deliverables/
├── discord-bot/          🤖 Discord 机器人 — 完整源码 + Docker + 教程
│   ├── bot/              Python 源码
│   ├── .env.example      配置模板
│   ├── requirements.txt  依赖
│   ├── Dockerfile        Docker 镜像
│   ├── docker-compose.yml
│   └── 使用说明.md        客户教程（含 Discord 注册步骤）
│
├── scraper-script/       🕷️ 网页采集 — 独立脚本，命令行即用
│   ├── scraper.py        采集脚本
│   └── 使用说明.md        客户教程
│
├── landing-page/         🌐 个人主页 — 一个 HTML 文件
│   ├── index.html        主页源码
│   └── 修改指南.md        客户自行修改教程
│
└── python-scripts/       🐍 Python 小工具
    ├── excel_merge.py    Excel 批量合并
    ├── file_rename.py    文件批量重命名
    └── 使用说明.md        客户教程
```

## 发货步骤

1. 根据客户需求微调对应文件夹里的代码
2. 右键文件夹 → 压缩为 zip
3. 闲鱼聊天发 zip 文件，或传百度网盘/蓝奏云发链接
4. 附言："使用说明在压缩包里的 README/使用说明.md，有问题随时找我"
