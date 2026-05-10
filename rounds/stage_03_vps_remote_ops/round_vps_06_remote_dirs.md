# Round VPS-06 · 远程学习目录与测试文件创建

## 概览

| 项目 | 内容 |
|---|---|
| 主题 | 在 VPS 上建立学习目录结构与第一个测试文件 |
| 操作权限等级 | **Level 3** |
| 是否需要用户授权 | **是**（必须） |
| 前置 | [VPS-05](round_vps_05_first_readonly_check.md) |
| 下一轮 | [VPS-07](round_vps_07_github_sync.md) |

## 目标

- 在用户家目录下建立**学习专用**目录结构。
- 创建若干测试文件，验证写入权限与 Linux 基本操作。
- 不安装任何软件。
- 不动系统目录、不动其他用户目录。

## 用户授权请求范例

```
本轮将进行 Level 3 远程低风险写入操作。
仅会在 ~/study/ 下创建目录与测试文件，不会动系统目录、不会安装软件。
计划创建：
- ~/study/
- ~/study/logs/
- ~/study/tests/
- ~/study/tests/hello_vps.txt
请确认是否执行。
```

## 涉及文件

- 远程：用户主目录下的 `~/study/`、`~/study/logs/`、`~/study/tests/`、`~/study/tests/hello_vps.txt`
- 本地：`rounds/stage_03_vps_remote_ops/outputs/remote_dir_record_template.md`（建议建立）

## 操作权限等级

- 等级：**Level 3**

## 具体任务

1. 用户使用 `docs/templates/remote_operation_confirmation.md` 走完确认，明确：
   - 目标服务器（占位）
   - 目标用户（占位）
   - 目标目录（确切路径）
   - 是否允许创建文件
2. SSH 登录服务器。
3. 顺序执行写入命令（见下），每步验证。
4. 退出后填写"远程目录建立记录"。

## 命令示例

```bash
ssh your_user@your_server_alias

# 先确认身份与位置（防止误操作到错误目录）
whoami
hostname
pwd

# 建立学习目录
mkdir -p ~/study
mkdir -p ~/study/logs
mkdir -p ~/study/tests

# 验证目录已创建
ls -la ~/study

# 写入测试文件
cd ~/study/tests
touch hello_vps.txt
echo "hello vps" > hello_vps.txt

# 读回验证
cat hello_vps.txt
ls -la

exit
```

## 远程目录建立记录模板（建议字段）

```markdown
# Remote Dir Record · YYYY-MM-DD

- 服务器别名：your_server_alias
- 登录用户：your_user
- 当前家目录（脱敏）：______
- 已建立目录：
  - ~/study/
  - ~/study/logs/
  - ~/study/tests/
- 已建立文件：
  - ~/study/tests/hello_vps.txt
- 内容验证：cat hello_vps.txt → "hello vps"
- 是否触碰系统目录：[ ] 否（默认必勾）
- 回滚方式：rm -rf ~/study（仅在用户授权下执行）
```

## 验收标准

- [ ] 学习目录三层结构 (`~/study/` / `~/study/logs/` / `~/study/tests/`) 已建立。
- [ ] 测试文件已建立并能读回。
- [ ] 操作过程未写入系统目录、未修改任何已有文件。
- [ ] 远程目录建立记录已写入仓库（脱敏）。
- [ ] 安全 checklist + 远程操作 checklist 已逐项打勾。

## 风险与禁止事项

- 不在 `/`、`/etc/`、`/var/`、`/usr/` 等系统目录下创建测试文件。
- 不修改 `sshd_config`、`bashrc` 等配置文件。
- 不安装任何软件。
- 不开放任何端口。
- 不写入真实 API Key。
- `rm -rf ~/study` **不在本轮自动执行**，需单独授权。

## 输出物

- 一份脱敏后的"远程目录建立记录"。

## 下一轮接口

VPS-07 将在 `~/study/` 下 clone 一个公开的 GitHub 仓库，理解本地 ↔ GitHub ↔ VPS 三角同步。
