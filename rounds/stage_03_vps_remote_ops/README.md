# Stage 03 · VPS 远程操作（VPS Remote Operations）

> 这是 `computer_study_plan` 主线之外的**实操支线**。
> 模块总纲请见 `docs/modules/vps_remote_ops.md`。
> 远程操作权限等级请见 `docs/governance/remote_operation_permissions.md`。

## 1. 阶段定位

VPS 实操支线服务于以下目的：

- 把 Linux / 网络 / GitHub / API / 部署等主线知识，**带到真实远程服务器环境中练习**。
- 建立"个人单节点基础设施闭环"的真实手感。
- 为未来 `VULTRagent`（独立项目仓库）留下规则与接口。
- 让编程 AI 在用户授权后，**按照文档**逐步操作远程服务器，而不是凭空臆测。

支线**不**追求一次完成全部部署，**也不**追求生产级稳定性，重点是建立 SOP 与权限边界。

## 2. Round 索引

| Round | 标题 | 默认权限等级 | 是否需要用户授权 |
|---|---|---|---|
| [VPS-00](round_vps_00_repo_scan.md) | 扫描仓库与生成治理报告 | Level 0 | 否 |
| [VPS-01](round_vps_01_repo_cleanup.md) | 执行仓库治理与文档合并 | Level 1 | 否（默认任务边界明确即可） |
| [VPS-02](round_vps_02_module_anchor.md) | 建立 VPS 模块总纲 | Level 1 | 否 |
| [VPS-03](round_vps_03_permission_levels.md) | 建立远程操作权限等级与安全规则 | Level 1 | 否 |
| [VPS-04](round_vps_04_ssh_basics.md) | SSH 与远程 Linux 基础任务文档 | 文档 Level 1，执行 Level 2/3 | 是（执行时） |
| [VPS-05](round_vps_05_first_readonly_check.md) | 首次远程服务器只读检查 | Level 2 | 是 |
| [VPS-06](round_vps_06_remote_dirs.md) | 远程学习目录与测试文件创建 | Level 3 | 是 |
| [VPS-07](round_vps_07_github_sync.md) | GitHub 仓库拉取与远程运行准备 | Level 3 | 是 |
| [VPS-08](round_vps_08_tmux_training.md) | tmux 后台任务训练 | Level 3 | 是 |
| [VPS-09](round_vps_09_network_check.md) | 网络连通性与端口检查 | Level 2/3 | 是 |
| [VPS-10](round_vps_10_remote_api_minimal.md) | 远程 API 调用最小实验 | Level 3 | 是 |
| [VPS-11](round_vps_11_minimal_service.md) | 最小 Web/API 服务部署实验 | Level 4 | 是 |
| [VPS-12](round_vps_12_sop_and_vultragent.md) | VPS 操作 SOP 与 VULTRagent 需求草案 | Level 1 | 否 |

## 3. 推荐执行顺序

```
VPS-00 → VPS-01 → VPS-02 → VPS-03  ←  纯文档与治理
                       ↓
                     VPS-04            ←  设计执行任务（仍是 Level 1）
                       ↓
                  VPS-05 (Level 2)     ←  首次真实只读连接
                       ↓
       VPS-06 / VPS-07 / VPS-08 (Level 3) ← 写入与同步训练
                       ↓
                     VPS-09            ←  网络与端口
                       ↓
                  VPS-10 (Level 3)     ←  API 调用
                       ↓
                  VPS-11 (Level 4)     ←  最小服务部署
                       ↓
                     VPS-12            ←  SOP 沉淀 + VULTRagent 需求草案
```

## 4. 安全约束（每个 Round 都默认遵守）

- 文档示例**只能用占位符**：`your_server_ip`、`your_user`、`your_repo_url`、`your_api_key_here`、`example.com`。
- 真实凭证**不写入仓库**。
- Level 2 及以上操作必须先走 `docs/templates/remote_operation_confirmation.md`。
- 高保护对象（Round 00 / 进度数据 / 主线 Round 概览）默认禁止删除。
- 任何 `rm -rf`、`reboot`、防火墙调整等操作均属 Level 5，需逐项确认。

## 5. 输出物索引（完成后回填）

随着 Round 推进，本目录会陆续沉淀：

- `outputs/server_check_record_template.md`（在 VPS-05 中给出）
- `outputs/remote_dir_record_template.md`（在 VPS-06 中给出）
- `outputs/github_sync_record_template.md`（在 VPS-07 中给出）
- `outputs/tmux_session_record_template.md`（在 VPS-08 中给出）
- `outputs/network_diag_record_template.md`（在 VPS-09 中给出）
- `outputs/remote_api_record_template.md`（在 VPS-10 中给出）
- `outputs/service_deploy_record_template.md`（在 VPS-11 中给出）
- `outputs/vps_sop.md`（在 VPS-12 中给出）
- `outputs/vultragent_mvp_requirements.md`（在 VPS-12 中给出）

> 当前阶段先给出 Round 文档；具体输出物模板会在对应 Round 第一次执行时生成。
