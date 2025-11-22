# 简易敏捷需求管理服务

这是一个最小的敏捷需求/缺陷管理 REST 服务示例，基于 Flask + SQLite。

功能：
- 需求（Story）管理：CRUD
- 缺陷（Bug）管理：CRUD
- 迭代（Iteration）和发布（Release）管理：CRUD

快速运行：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

API 根路径：`/api`

示例：创建需求

```bash
curl -X POST http://127.0.0.1:5000/api/stories -H "Content-Type: application/json" -d '{"title":"示例需求","description":"描述"}'
```
# demo