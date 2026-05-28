# Protocol Sync Checklist

> 适用场景：当仓库发生治理规则、目录骨架、阶段结构或关键流程变更时，用于确保机器协议与人类文档同步。

## 1) 触发判定

- [ ] 新增 / 删除 / 重命名了治理关键文件（`governance/*.yaml`、`project.yaml` 等）。
- [ ] 调整了 Stage / Round 骨架、lane 归属或推进规则。
- [ ] 修改了 AGENT 读取顺序、安全边界、停止条件或验证命令。
- [ ] 在 Markdown 文档中新增了可复用的治理规则（需回写机器协议）。

## 2) 同步执行

- [ ] 更新 `governance/repo_protocol_standard.yaml`。
- [ ] 同步 `project.yaml` 的协议版本与当前 focus。
- [ ] 同步 `governance/round_state.yaml`（含本轮范围、验证、后续任务）。
- [ ] 同步 `governance/file_role_map.yaml`（新增/删除的权威文件映射）。
- [ ] 必要时同步 `governance/agent_policy.yaml`、`model_policy.yaml`、`data_policy.yaml`。
- [ ] 同步 `AGENTS.md` 与 `README.md` 的入口和引用。
- [ ] 同步 `docs/PROJECT_STATE.md` 与 `docs/NEXT_ACTIONS.md`。
- [ ] 生成或更新 `docs/reports/*_report.md` 治理报告。

## 3) 校验与留痕

- [ ] 运行：`python3 scripts/check_protocol_sync.py`。
- [ ] 若涉及进度文件，运行：`python3 -m json.tool progress.json`。
- [ ] 记录校验结果与遗留问题到 `docs/reports/`。
- [ ] 确认本轮未破坏 Round 00 最小闭环与 `records/` 历史记录。

## 4) 责任边界

- [ ] 执行代理负责本轮同步落地与校验。
- [ ] 用户负责策略方向确认与高风险删除授权。
- [ ] 未经用户明确要求，不执行 commit / push。
