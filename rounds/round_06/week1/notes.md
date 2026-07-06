# Round 06 · Week 1 笔记（find/xargs/sed/awk）

## 本周目标

- 掌握文件批量定位与基础文本处理。
- 能把 `find` 与 `xargs` 组合成自动化流水。

## 在 Web UI 中怎么学

1. 点“练习：find/xargs/sed/awk 日志清洗”的“运行脚本”，查看自动生成的 `log_clean_demo.sh`、`logs/` 和 `reports/`。
2. 点“自测：自己写 find_text_report.sh”的“终端练习”，浏览器终端会进入 `~/cli-lab/round6`。
3. 自己写一个批量统计脚本：

```bash
mkdir week1_self
cd week1_self
printf 'alpha error\nbeta ok\ngamma error\n' > app.log
printf 'delta ok\n' > worker.log
printf '#!/bin/bash\nset -e\nfind . -name "*.log" -print0 | xargs -0 grep -n "error"\nfind . -name "*.log" -print0 | xargs -0 wc -l\n' > find_text_report.sh
chmod +x find_text_report.sh
bash find_text_report.sh
```

4. 能解释为什么 `-print0 | xargs -0` 更安全后，再点击“记录并完成”保存自测记录。

## 命令直觉

- `find`：负责“找哪些文件”。
- `xargs`：负责“把找到的文件喂给下一条命令”。
- `sed`：适合替换、删除行、把文本改成另一种样子。
- `awk`：适合按列提取、筛选、统计。

## 本周自查

- [ ] 能写出一个 `find ... | xargs ...` 的批处理命令
- [ ] 能用 `sed` 或 `awk` 做最小日志清洗
- [ ] 能解释 `find -print0 | xargs -0` 的意义
