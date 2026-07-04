# Round 10 · Week 2 笔记（配置与日志）

## 本周目标

- 用 `config.ini` 保存可调整参数。
- 区分用户可见输出与排查用日志。

## Web UI 学习路径

1. 打开本文件，先确认配置和日志分别解决什么问题：
   - 配置：用户不改代码也能调参数。
   - 日志：程序出问题时能追踪发生过什么。
2. 点击 `r10-w2-ex2` 的“运行”。脚本会在 `~/cli-lab/round10/week2_auto/ai_prep_tool` 生成：
   - `config.ini`
   - `config.py`
   - `log_utils.py`
   - `core.py`
   - `app.py`
   - `output/result.txt`
   - `logs/app.log`
3. 运行结果会验证 `min_length = 3` 生效，短记录被过滤，日志里能看到 `filter_records` 和 `dedup_records`。
4. 点击 `r10-w2-self` 的“终端”，自己读取一个 `config.ini` 并初始化日志。

## 配置最小规则

- 读取配置时要有 fallback，避免配置缺失导致程序直接崩。
- 配置只放“用户可能调整的值”，不要把代码逻辑写进配置。
- `config.py` 负责把字符串配置转成程序真正需要的类型，例如 int / bool。

## 日志最小规则

- 给用户看的摘要可以 `print()`。
- 给自己排查的过程信息用 `logging.info()`、`logging.warning()`、`logging.error()`。
- 日志文件放进 `logs/`，不要提交运行副产物。

## 浏览器终端自测命令

在 `r10-w2-self` 的终端里逐条运行：

```bash
mkdir week2_self
cd week2_self
printf '[defaults]\nlog_dir = logs\nmin_length = 2\n' > config.ini
printf 'import configparser\n\nconfig = configparser.ConfigParser()\nconfig.read("config.ini")\nprint(config.getint("defaults", "min_length", fallback=1))\nprint(config.get("defaults", "log_dir", fallback="logs"))\n' > read_config.py
python3 read_config.py
```

看到 `2` 和 `logs` 后，回到任务行手动点“记录 / 完成”。

## 本周自查

- [ ] 能解释 `configparser` 读取配置的最小流程
- [ ] 能说出 logging 中 INFO 与 DEBUG 的典型用途
- [ ] 能说明为什么配置缺失时要使用 fallback
