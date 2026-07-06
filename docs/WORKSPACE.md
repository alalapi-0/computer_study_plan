# 工作区与路径约定

> **单一事实源**：本文件定义「本仓库在磁盘上的位置」「IDE 应打开哪个目录」「练习沙盒与仓库如何区分」。  
> 若文档、Cursor 左下角路径、终端 `pwd` 三者不一致，以本文件为准并修正 IDE/终端，而不是再克隆第二份副本。

---

## 1. 唯一 Git 工作副本（仓库根）

| 项 | 值 |
|---|---|
| **推荐写法（`~`）** | `~/PycharmProjects/computer_study_plan` |
| **本机绝对路径** | `/Users/alalapi/PycharmProjects/computer_study_plan` |
| **目录名** | `computer_study_plan` |
| **远程仓库** | `https://github.com/alalapi-0/computer_study_plan`（以 `git remote -v` 为准） |

### 1.1 如何确认当前就在仓库根

在终端执行：

```bash
cd ~/PycharmProjects/computer_study_plan
test -f progress.json && test -f mark_done.sh && echo "OK: 仓库根"
git rev-parse --show-toplevel
```

最后一行应输出：`/Users/alalapi/PycharmProjects/computer_study_plan`。

### 1.2 IDE / Cursor / PyCharm

- **工作区根目录**必须打开上表中的文件夹（不是父级 `PycharmProjects`，也不是子目录 `rounds/`）。
- Cursor 窗口**左下角显示的路径**即工作区根；正常应为 `…/PycharmProjects/computer_study_plan`。
- 所有 `bash mark_done.sh`、`python3 scripts/progress_server.py`、阅读 `progress.html` 的操作，默认都在该根目录下执行。静态打开页面只用于只读布局 / 进度检查，不具备写 API、练习脚本、动作日志或浏览器终端能力。

### 1.3 不再使用的路径（避免混淆）

| 路径 | 说明 |
|---|---|
| `~/Desktop/computer_study_plan` | 历史上可能出现的解压/副本位置；**不是**当前主仓库 |
| `~/Desktop/computer_study_plan.zip` | 旧备份压缩包；已清理则忽略 |
| 任意第二份 `computer_study_plan` 克隆 | 容易造成「改了 A 目录、打开的是 B 目录」；应只保留 PyCharmProjects 下这一份 |

若曾在其他位置改过文件，请对比 `git remote -v` 与 `git log -1`，将 IDE 指回 **§1** 的路径，或把未推送的提交 cherry-pick / 复制到主副本后再删冗余目录。

---

## 2. 练习沙盒（与仓库分离）

Round 00 等终端练习在**用户主目录**下的沙盒进行，**不**放在 Git 仓库内：

| 用途 | 路径 |
|---|---|
| Round 00 终端练习 | `~/cli-lab/round0` |
| 其他 Round（按大纲） | `~/cli-lab/roundN` 等 |

这是**教学设计**：避免把临时 `mkdir`/`touch` 产物提交进 `computer_study_plan`。  
`rounds/round_00/week*/exercises.sh` 会通过脚本内的 `REPO_ROOT` 自动定位仓库根并调用 `mark_done.sh`，与 `~/cli-lab` 互不冲突。

---

## 3. 文档中的路径写法规范

| 场景 | 应写 |
|---|---|
| 进入本仓库、跑进度脚本、打开 Web UI 学习工作区 | `~/PycharmProjects/computer_study_plan` 或「仓库根」 |
| Round 00 手敲命令练习 | `~/cli-lab/round0`（保持现有 round 文档不变） |
| VPS 支线 clone 示例 | `~/study/<repo_name>`（见 `rounds/stage_03_vps_remote_ops/`） |
| 泛指「任意机器上的克隆目录」 | `cd <你的 computer_study_plan 仓库根>`，并注明需含 `progress.json` |

**禁止**在治理文档（README、`docs/`、`AGENTS.md`）中再写 `Desktop/computer_study_plan` 作为默认工作路径。

---

## 4. 与仓库内脚本的对应关系

| 机制 | 行为 |
|---|---|
| `mark_done.sh` | 必须在含 `progress.json` 的目录执行（即 §1 仓库根） |
| `rounds/round_00/**/exercises.sh` | `REPO_ROOT="$(cd …/../../.. && pwd)"` 动态解析，不硬编码用户名 |
| `progress.html` | 日常学习应通过 §1 仓库根启动 `python3 scripts/progress_server.py` 后访问 `http://127.0.0.1:8777/progress.html`；直接打开文件仅用于只读布局 / 进度检查，没有写 API、练习脚本、动作日志或浏览器终端能力 |

---

## 5. 变更记录

| 日期 | 说明 |
|---|---|
| 2026-05-28 | 建立本文件，统一文档 / IDE / 本机仓库路径为 `~/PycharmProjects/computer_study_plan` |
