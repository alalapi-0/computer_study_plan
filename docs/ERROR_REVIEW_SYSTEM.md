# Error Review System · Linux 练习复盘

> 更新日期：2026-07-18
> 本文件定义 Linux 单课程的错误复盘机制，不再服务考试 lane。

## 1. 归档目录

```text
records/
├─ error_notes/
│  └─ linux-foundations/
│     ├─ terminal/
│     ├─ filesystem/
│     ├─ shell/
│     ├─ automation/
│     └─ remote/
└─ weekly_reviews/
```

## 2. 复盘卡片最小字段

- 任务 / 模块
- 现象（命令输出或失败表现）
- 原因（概念误解 / 路径错误 / 权限 / 语法 / 粗心）
- 正确做法
- 下次如何避免
- 证据路径（可选）

## 3. 回流规则

- 同一错误出现 2 次以上 → 回到对应 Module overview 重读
- 与权限 / 路径相关 → 优先复盘 Module 01
- 与管道 / 脚本相关 → 优先复盘 Module 02
- 与远程操作相关 → 先重读 VPS 权限等级文档，再动手

## 4. 禁止事项

- 不缓存具体考题或考点
- 不把复盘系统重新绑回软考 / 考研主线
