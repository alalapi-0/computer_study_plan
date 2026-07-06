# Round 14 · Week 1 笔记（HTTP 方法与状态码）

## Web UI 学习路径

1. 在 Round 14 页面先阅读本文。
2. 点击 `练习：生成 HTTP 方法与状态码矩阵` 的“运行脚本”按钮。
3. 在运行结果里确认 `http_report.json`、`method_matrix.json`、`status_matrix.json` 都已生成。
4. 点击 `自测：自己写 method_quiz.txt` 的“终端练习”按钮，手敲下面的自测命令。
5. 自测完成后，点击“记录并完成”记录 `r14-w1-self`。

## 你要建立的直觉

| 场景 | 优先想到 |
|---|---|
| 取列表、取详情、查状态 | `GET` |
| 提交一次处理任务、创建一条记录 | `POST` |
| 完整替换一个对象 | `PUT` |
| 只改对象的一部分 | `PATCH` |
| 删除资源 | `DELETE` |

状态码不用先背完，先记这几个判断：

- `200`：成功返回。
- `201`：创建成功。
- `400`：请求参数不合法。
- `404`：资源不存在。
- `500`：服务端内部错误。

## 自动练习会做什么

脚本会在 `~/cli-lab/round14/week1_auto/http_basics` 下生成：

- `method_matrix.json`：GET/POST/PUT/PATCH/DELETE 的语义、安全性和幂等性。
- `status_matrix.json`：常见 2xx/4xx/5xx 状态码的解释。
- `request_response_examples.json`：用 `ai_prep_tool` 场景写出的请求/响应例子。
- `http_report.json`：检查矩阵完整性和推荐下一步。

## 终端自测

在浏览器终端绑定 `r14-w1-self` 后执行：

```bash
pwd
mkdir week1_self
cd week1_self
printf 'GET means read data\nPOST means submit a new job\n404 means resource missing\n500 means server failed\n' > method_quiz.txt
cat method_quiz.txt
grep POST method_quiz.txt
```

本周不要在浏览器终端里执行 `curl https://...`。Web UI 终端会拦截 `curl` 和网络下载命令，本轮先把语义练稳。

## 完成标准

- 能说出 GET 和 POST 的语义区别。
- 能解释 200、201、400、404、500。
- 能把“提交一次 ai_prep_tool 处理任务”判断为 POST，而不是 GET。
