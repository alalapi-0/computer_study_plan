# Round 08 · Week 3 笔记（FastAPI 最小服务）

## 本周目标

- 理解“本地脚本”到“本地服务”的最小迁移。
- 跑通 `health` 与 `run` 两类接口。

## Web UI 学习路径

1. 先点击本文件“打开”，理解服务化先从接口形状开始。
2. 点击 `r08-w3-ex3` 的“运行”。脚本会在 `~/cli-lab/round8/week3_auto` 生成：
   - `api_contract.py`
   - `api_demo_output.json`
   - `fastapi_next_steps.md`
3. 本轮 Web UI 不安装 FastAPI、不启动真实后端服务；自动练习用标准库模拟 `GET /health`、`POST /run`、`GET /runs` 三个响应。
4. 点击 `r08-w3-self` 的“终端”，自己写一个 `api_contract.py` 并运行。

## 接口形状先行

服务化不是一上来就部署服务器，而是先把三个问题说清楚：

- 请求是什么：例如 `{"input_file": "input/demo.txt", "dedup": true}`。
- 响应是什么：例如 `{"status": "accepted", "run_id": 1}`。
- 状态存在哪里：例如 Week 2 的 SQLite `runs` 表。

等接口形状稳定后，后续 Round 再把这些函数包进 FastAPI 路由。

## 浏览器终端自测命令

在 `r08-w3-self` 的终端里逐条运行：

```bash
mkdir week3_self
cd week3_self
printf 'def health():\n    return {"status": "ok"}\n\ndef run(req):\n    return {"status": "accepted", "input_file": req["input_file"], "dedup": bool(req.get("dedup"))}\n\ndef list_runs():\n    return {"runs": [], "count": 0}\nprint("GET /health", health())\nprint("POST /run", run({"input_file": "input/demo.txt", "dedup": True}))\nprint("GET /runs", list_runs())\n' > api_contract.py
python3 api_contract.py
```

能解释三个接口的入参、响应和下一步如何接 SQLite 后，回到任务行手动点“记录 / 完成”。

## 本周自查

- [ ] 能说明接口入参与响应的最小设计
- [ ] 能本地启动服务并验证健康检查
- [ ] 能说明为什么本轮只做接口排练、不在仓库引入真实后端服务
