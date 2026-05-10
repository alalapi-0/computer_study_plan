# Round VPS-09 · 网络连通性与端口检查

## 概览

| 项目 | 内容 |
|---|---|
| 主题 | 远程网络排查：能否出网 / 端口监听 / 防火墙状态 |
| 操作权限等级 | **Level 2 / Level 3**（不修改防火墙；如需测试出站，单条 `ping/curl` 属 Level 2） |
| 是否需要用户授权 | **是**（必须） |
| 前置 | [VPS-08](round_vps_08_tmux_training.md) |
| 下一轮 | [VPS-10](round_vps_10_remote_api_minimal.md) |

## 目标

- 区分三种"访问失败"：本地访问失败 / 服务器访问失败 / API 访问失败。
- 检查服务器外网访问能力（DNS / HTTP）。
- 检查服务器上有哪些端口在监听。
- 查看防火墙状态（**不修改**）。
- 识别 401 / 403 / 429 / 500 的不同含义。

## 用户授权请求范例

```
本轮将进行 Level 2/3 网络与端口检查。
仅会执行 ping、curl、ss、ufw status 等只读 / 信息查询命令。
不会修改防火墙、不会开放新端口、不会安装软件。
请确认是否执行。
```

## 涉及文件

- 远程：无写入
- 本地：`rounds/stage_03_vps_remote_ops/outputs/network_diag_record_template.md`

## 操作权限等级

- 等级：**Level 2** 为主；某些命令可能落到 **Level 3**（仅当 `curl -X POST` 之类涉及写入时，本轮**禁止**这种方式）。

## 学习内容

- IP / 端口 / DNS 的关系
- 入站 vs 出站
- 监听地址：`127.0.0.1` vs `0.0.0.0` vs `::` 的区别
- 工具：`ping`、`curl -I`、`wget --spider`、`ss -tulpn`、`ufw status`
- HTTP 状态码：
  - 401 Unauthorized：身份未认证
  - 403 Forbidden：身份认证了，但没权限
  - 429 Too Many Requests：被限流
  - 500 Internal Server Error：服务端崩了
  - 502/503/504：网关 / 上游问题

## 命令示例（只读）

```bash
ssh your_user@your_server_alias

# 出站连通性
ping -c 3 example.com
curl -I https://example.com
curl -I https://api.openai.com 2>/dev/null | head -n 1

# 当前监听端口
ss -tulpn 2>/dev/null

# 防火墙状态（仅查看）
sudo ufw status 2>/dev/null || echo "ufw 未安装或未启用 / 无 sudo 权限"
# 仅当用户授权 sudo 查询时才执行

# DNS
cat /etc/resolv.conf
getent hosts example.com

exit
```

> 上面的 `sudo ufw status` 仍属于"信息查询"，但需要 sudo 权限。如服务器未配置 sudo 或用户不希望使用，应直接跳过。

## 网络排查记录模板（建议字段）

```markdown
# Network Diag Record · YYYY-MM-DD

- 服务器别名：your_server_alias
- 出站：
  - ping example.com: [ ] 通 / [ ] 不通（loss: __）
  - curl -I https://example.com: HTTP ___
- 监听端口（去除真实 PID 与用户名）：
  - 22 / tcp / 0.0.0.0 / sshd
  - ___
- 防火墙：[ ] 未启用 / [ ] 启用（默认策略：______）
- DNS：______
- 状态码理解练习：
  - 401: ______
  - 403: ______
  - 429: ______
  - 500: ______
- 备注：______
```

## 验收标准

- [ ] 能判断服务器是否能访问外网。
- [ ] 能列出监听端口与监听地址（区分 127.0.0.1 / 0.0.0.0）。
- [ ] 能解释 401 / 403 / 429 / 500 的差别。
- [ ] 网络排查记录已写入仓库（脱敏）。
- [ ] **未**修改任何防火墙规则、**未**开放任何端口。

## 风险与禁止事项

- 不修改 `ufw` / `iptables` / `firewalld` 规则。
- 不开放公网端口。
- 不执行 `curl -X POST` 等写入型请求。
- 不让 sudo 查询泄漏密码。

## 输出物

- 一份脱敏后的网络排查记录。

## 下一轮接口

VPS-10 将在 VPS 上跑通最小 API 调用，并把本轮学到的状态码理解直接用上。
