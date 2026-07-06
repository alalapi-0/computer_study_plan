# Round VPS-02 · 建立 VPS 模块总纲

## 概览

| 项目 | 内容 |
|---|---|
| 主题 | 把 VPS 模块写入总控路线 |
| 操作权限等级 | **Level 1** |
| 是否需要用户授权 | 否 |
| 前置 | [VPS-01](round_vps_01_repo_cleanup.md) |
| 下一轮 | [VPS-03](round_vps_03_permission_levels.md) |

## 目标

- 在仓库内建立**VPS 模块总纲**：`docs/modules/vps_remote_ops.md`。
- 在 `README.md` 全局路线图中，让 VPS 模块作为**实操支线**可见。
- 明确 VPS 与 Linux / 网络 / GitHub / API / 部署的关系。

## 背景

主线 Round 00–21 是"工程能力 + 服务化 + AI/ML"路线，但**没有专门承载"在真实远程服务器上跑项目"这件事**。
VPS 模块作为支线接入，让用户可以在主线之外按节奏推进真实远程实操。

## 涉及文件

- 新增 / 维护：`docs/modules/vps_remote_ops.md`
- 更新：`README.md` 全局路线图与项目结构段落
- 更新：`docs/PROJECT_STATE.md`、`docs/NEXT_ACTIONS.md`

## 操作权限等级

- 等级：**Level 1**
- 行为限制：仅修改文档；不连接远程服务器。

## 具体任务

1. 撰写或维护 `docs/modules/vps_remote_ops.md`：
   - 模块定位
   - 与主线模块的连接
   - 学习目的
   - 模块硬约束（占位符 / 不写真实凭证 / 不默认公网）
   - 阶段拆分（Stage VPS-0 ~ Stage VPS-8）
   - 模块输出物清单
   - 与 VULTRagent 的关系
   - 模块级验收标准
2. 在 `README.md` 中：
   - 在"全局路线图"段落补充 VPS 实操支线说明（不破坏主线）。
   - 在"项目结构"中加入 `docs/modules/`、`docs/governance/`、`docs/checklists/`、`docs/templates/`、`rounds/stage_03_vps_remote_ops/` 的位置。
3. 在 `docs/PROJECT_STATE.md` 中追加"VPS 模块接入"段落。

## 命令示例

```bash
git status --short --branch
# 修改 README.md / docs/modules/vps_remote_ops.md / docs/PROJECT_STATE.md
git add README.md docs/modules/vps_remote_ops.md docs/PROJECT_STATE.md docs/NEXT_ACTIONS.md
bash mark_done.sh
python3 -m json.tool progress.json
git commit -m "VPS-02: anchor VPS module into long-term roadmap"
git push origin main
```

## 验收标准

- [ ] `docs/modules/vps_remote_ops.md` 存在且可读。
- [ ] `README.md` 中能找到 VPS 模块的入口或路线图体现。
- [ ] VPS 模块与 Linux / 网络 / GitHub / API / 部署的关系被写明。
- [ ] 模块文档使用占位符，不含真实 IP / Key。
- [ ] Round 00 闭环未被破坏。

## 风险与禁止事项

- 不修改 `progress.json`、`progress_data.js`、`rounds_data.js`、`progress.html`、`progress_ui.js`、`scripts/progress_server.py`、`mark_done.sh`、`records/action_logs/`、`records/feedback/`。
- 不动主线 Round 概览。
- 不在 `README.md` 中引入大段重写；仅最小必要补充。

## 输出物

- 维护好的 VPS 模块总纲。
- README 入口与路线图同步。

## 下一轮接口

VPS-03 将正式落地"远程操作权限等级 + 安全 checklist + 确认模板"。
