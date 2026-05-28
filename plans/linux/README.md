# plans/linux/ · 工程实操线下的 Linux 专项

> 所属 lane：`engineering`
> 关联 Stage：Stage 1（Linux + Git + Shell + 网络基础）

---

## 1. 这条线的角色

- 服务于"工程实操 + 软考广度入门 + 长期 AI 工程素养"
- 在仓库中**已经存在大量素材**：Round 00–02、Round 06、VPS 支线
- 本目录不复制那些内容，而是把它们**串成一条可执行的学习路径**

---

## 2. 关联资产清单

| 资产 | 位置 | 角色 |
|---|---|---|
| Round 00 完整闭环 | `rounds/round_00/` | 入门：终端 + pwd/ls/cd/mkdir/cat/man |
| Round 01 概览 | `round_01.md` | 文件系统与基本命令 |
| Round 02 概览 | `round_02.md` | Shell + 管道 + Git |
| Round 06 概览 | `round_06.md` | Linux 进阶与自动化 |
| VPS 远程实操支线 | `rounds/stage_03_vps_remote_ops/` | 远程操作 13 篇 Round 文档 |

---

## 3. 推进顺序建议

1. **Round 00**（如未完成）→ `rounds/round_00/week1/`
2. Round 02 Git / Shell 基础（按 `round_02.md` 展开实操）
3. Round 06 Linux 进阶（按 `round_06.md` 展开实操）
4. VPS 支线：先 VPS-04（SSH 文档）→ VPS-05（首次只读）→ 按需推进

---

## 4. 软考广度对照（按需补）

| Linux 知识 | 软考相关模块 | 笔记位置 |
|---|---|---|
| 文件系统、权限 | 操作系统模块（概念广度） | `plans/soft_exam/os.md` |
| 进程管理（ps/kill/jobs） | 操作系统模块（进程） | `plans/soft_exam/os.md` |
| 网络命令（ping/curl/ss） | 计算机网络模块 | `plans/soft_exam/network.md` |

---

## 5. 笔记骨架（按需建）

按节奏建立以下笔记，每份按 `docs/CONVERSION_PROTOCOL.md` 的 md 写作风格（清晰、不啰嗦、有命令示例）：

- `cli_basics.md`：命令行基础（合并 Round 00 学到的命令小抄）
- `shell_scripting.md`：Shell 编程
- `git_workflow.md`：Git 工作流
- `linux_admin.md`：Linux 用户 / 进程 / 服务管理
- `networking.md`：网络命令与排查
- `vps_practice.md`：VPS 实操经验沉淀（对接 `rounds/stage_03_vps_remote_ops/`）

> 这些文件**当前都不预先创建**。按真实学习节奏在需要时新建即可。
