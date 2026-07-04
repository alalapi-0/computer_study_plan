# Round 09 · 仓库规范化与测试速查

## Web UI 完成路径

1. 点击 `r09-fin-comp` 的“运行”，确认输出显示布局、Git 工作流和测试均通过。
2. 打开本文件“阅读”，按下面的小抄检查自己是否能解释。
3. 能说清楚 README、`.gitignore`、分支、纯函数和测试后，手动完成 `r09-fin-sheet` 与 `r09-fin-acc1`。

## 建议顺序

1. 先规范目录与 README。
2. 再练习 feature/hotfix 分支工作流。
3. 最后补最小 pytest 思维与断言覆盖。

## 最小通过标准

- 项目目录可读，README 能说明用途与运行方式。
- `.gitignore` 已排除缓存、虚拟环境和输出副产物。
- 核心逻辑可用纯函数表达，并可用断言验证。

## 常用命令

```bash
git status
git checkout -b feature/readme-note
git add README.md
git commit -m feature-readme-note
git checkout main
git merge feature/readme-note
git branch -d feature/readme-note
python3 run_tests.py
```

## 验收自问

- README 是否能让陌生人 3 分钟内知道怎么运行？
- `.gitignore` 是否覆盖缓存、日志、输出和虚拟环境？
- 分支练习是否只发生在 `~/cli-lab/round9` 沙盒？
- 测试函数是否覆盖普通重复、空列表、顺序保持和无重复？
- 核心逻辑是否不直接读写文件？
