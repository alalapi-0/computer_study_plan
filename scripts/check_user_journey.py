#!/usr/bin/env python3
"""User-perspective consistency tests for README onboarding and daily use.

Runs scripted checks, writes docs/CONSISTENCY_AUDIT_REPORT.md, exits non-zero on failure.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REPORT_PATH = REPO / "docs" / "CONSISTENCY_AUDIT_REPORT.md"

sys.path.insert(0, str(REPO / "scripts"))
from round_status import scan_rounds, summary, task_id_to_round_id  # noqa: E402


@dataclass
class TestCase:
    id: str
    category: str
    title: str
    steps: str
    passed: bool = False
    detail: str = ""


@dataclass
class TestReport:
    cases: list[TestCase] = field(default_factory=list)

    def add(self, case: TestCase) -> None:
        self.cases.append(case)

    @property
    def failed(self) -> list[TestCase]:
        return [c for c in self.cases if not c.passed]


def run_cmd(cmd: list[str], cwd: Path = REPO) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out.strip()


def check_repo_root_identifiable(report: TestReport) -> None:
    case = TestCase(
        "TC-01",
        "首次进入",
        "确认仓库根目录可识别",
        "test -f progress.json && test -f mark_done.sh",
    )
    ok = (REPO / "progress.json").is_file() and (REPO / "mark_done.sh").is_file()
    case.passed = ok
    case.detail = "OK: 仓库根" if ok else "缺少 progress.json 或 mark_done.sh"
    report.add(case)


def check_workspace_doc(report: TestReport) -> None:
    case = TestCase(
        "TC-02",
        "首次进入",
        "WORKSPACE.md 存在且描述仓库根自检命令",
        "阅读 docs/WORKSPACE.md §1.1",
    )
    path = REPO / "docs" / "WORKSPACE.md"
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    ok = path.is_file() and "progress.json" in text and "mark_done.sh" in text
    case.passed = ok
    case.detail = "WORKSPACE.md 包含自检说明" if ok else "WORKSPACE.md 缺失或不完整"
    report.add(case)


def check_mark_done_list(report: TestReport) -> None:
    case = TestCase(
        "TC-03",
        "日常使用",
        "mark_done.sh 无参数可列出任务",
        "bash mark_done.sh | head",
    )
    code, out = run_cmd(["bash", "mark_done.sh"])
    ok = code == 0 and "总进度" in out
    case.passed = ok
    case.detail = out.split("\n")[0] if ok else out[:200]
    report.add(case)


def check_progress_json(report: TestReport) -> None:
    case = TestCase(
        "TC-04",
        "日常使用",
        "progress.json 结构合法（lanes + tasks）",
        "python3 -m json.tool progress.json",
    )
    try:
        data = json.loads((REPO / "progress.json").read_text(encoding="utf-8"))
        lanes = data.get("lanes")
        tasks = data.get("tasks")
        ok = isinstance(lanes, dict) and lanes and isinstance(tasks, dict) and tasks
        case.passed = ok
        case.detail = f"tasks={len(tasks) if isinstance(tasks, dict) else 0}"
    except Exception as exc:
        case.passed = False
        case.detail = str(exc)
    report.add(case)


def check_progress_data_js(report: TestReport) -> None:
    case = TestCase(
        "TC-05",
        "看进度",
        "progress_data.js 存在且含 PROGRESS_DATA",
        "grep PROGRESS_DATA progress_data.js",
    )
    path = REPO / "progress_data.js"
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    ok = path.is_file() and "window.PROGRESS_DATA" in text
    case.passed = ok
    case.detail = "progress_data.js OK" if ok else "缺少 progress_data.js"
    report.add(case)


def check_progress_rounds_sync(report: TestReport) -> None:
    case = TestCase(
        "TC-06",
        "看进度",
        "progress_rounds.json / .js 与轮次扫描一致",
        "python3 scripts/generate_progress_rounds.py && compare counts",
    )
    code, _ = run_cmd(["python3", "scripts/generate_progress_rounds.py"])
    json_path = REPO / "progress_rounds.json"
    js_path = REPO / "progress_rounds.js"
    statuses = scan_rounds(REPO)
    expected = sum(1 for s in statuses if s.scaffold_dir or s.overview_md)
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
        actual = len(data.get("rounds", []))
        ok = code == 0 and js_path.is_file() and actual == expected
        case.passed = ok
        case.detail = f"rounds in JSON={actual}, expected={expected}"
    except Exception as exc:
        case.passed = False
        case.detail = str(exc)
    report.add(case)


def check_round00_exercises(report: TestReport) -> None:
    case = TestCase(
        "TC-07",
        "Round 练习",
        "Round 00 练习脚本语法检查通过",
        "bash -n rounds/round_00/week1/exercises.sh 等",
    )
    scripts = list((REPO / "rounds" / "round_00").rglob("*.sh"))
    errors: list[str] = []
    for script in scripts:
        code, out = run_cmd(["bash", "-n", str(script)])
        if code != 0:
            errors.append(f"{script.name}: {out}")
    case.passed = not errors
    case.detail = "全部 bash -n 通过" if not errors else "; ".join(errors)
    report.add(case)


def check_progress_task_round_mapping(report: TestReport) -> None:
    case = TestCase(
        "TC-08",
        "进度一致性",
        "progress.json 任务 ID 可映射到 round_id",
        "task_id_to_round_id 全覆盖",
    )
    tasks = json.loads((REPO / "progress.json").read_text(encoding="utf-8")).get("tasks", {})
    unknown = [tid for tid in tasks if not task_id_to_round_id(tid)]
    case.passed = not unknown
    case.detail = f"未知映射: {unknown}" if unknown else f"全部 {len(tasks)} 个任务可映射"
    report.add(case)


def check_ui_tasks_in_progress(report: TestReport) -> None:
    case = TestCase(
        "TC-09",
        "看进度",
        "看板中已注册任务 ID 均存在于 progress.json",
        "比对 progress_rounds.json weeks.tasks 与 progress.json",
    )
    pr = json.loads((REPO / "progress_rounds.json").read_text(encoding="utf-8"))
    tasks = json.loads((REPO / "progress.json").read_text(encoding="utf-8")).get("tasks", {})
    missing: list[str] = []
    for rnd in pr.get("rounds", []):
        for week in rnd.get("weeks", []):
            for task in week.get("tasks", []):
                tid = task.get("id")
                if tid and tid not in tasks:
                    missing.append(tid)
    case.passed = not missing
    case.detail = f"缺失任务: {missing}" if missing else "看板任务与 progress.json 对齐"
    report.add(case)


def check_readme_no_false_claims(report: TestReport) -> None:
    case = TestCase(
        "TC-10",
        "文档准确",
        "README 不声称全部 Round 已接入进度看板（若实际未接入）",
        "比对 README 与 round_status summary",
    )
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    summ = summary(scan_rounds(REPO))
    ui_count = len(summ["ui_linked_rounds"])
    scaffold_only = len(summ["scaffold_only_rounds"])

    false_claim = False
    issues: list[str] = []
    if re.search(r"当前已展开 Round 00[–-]Round 21", readme) and ui_count < 22:
        false_claim = True
        issues.append("README 写「看板已展开 00–21」但实际 UI 仅覆盖部分轮次")
    if "round_00/" in readme and "← 终端入门（已完成）" in readme:
        issues.append("README 将 round_00 目录标注为「已完成」易误解为用户学完（应为「实操目录已建立」）")

    case.passed = not false_claim
    case.detail = (
        f"UI={ui_count}, scaffold_only={scaffold_only}; "
        + ("; ".join(issues) if issues else "未发现明显夸大表述")
    )
    report.add(case)


def check_governance_file_naming(report: TestReport) -> None:
    case = TestCase(
        "TC-11",
        "Agent 协作",
        "file_naming_rules 不与实际展开状态矛盾",
        "比对「仅 round_00 已展开」表述",
    )
    path = REPO / "docs" / "governance" / "file_naming_rules.md"
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    stale = "目前仅 `rounds/round_00/` 已展开" in text
    scaffold_count = summary(scan_rounds(REPO))["scaffold_complete_count"]
    case.passed = not stale
    case.detail = (
        f"file_naming_rules 仍写仅 round_00 已展开（实际完整骨架 {scaffold_count} 个）"
        if stale
        else "file_naming_rules 无过时「仅 round_00」表述"
    )
    report.add(case)


def check_validate_learning_data(report: TestReport) -> None:
    case = TestCase(
        "TC-12",
        "校验脚本",
        "validate_learning_data.py 通过",
        "python3 scripts/validate_learning_data.py",
    )
    code, out = run_cmd(["python3", "scripts/validate_learning_data.py"])
    case.passed = code == 0
    case.detail = out.split("\n")[-1] if out else str(code)
    report.add(case)


def check_protocol_sync(report: TestReport) -> None:
    case = TestCase(
        "TC-13",
        "校验脚本",
        "check_protocol_sync.py 通过",
        "python3 scripts/check_protocol_sync.py",
    )
    code, out = run_cmd(["python3", "scripts/check_protocol_sync.py"])
    case.passed = code == 0
    case.detail = out
    report.add(case)


def check_agent_gate_verify(report: TestReport) -> None:
    case = TestCase(
        "TC-14",
        "Agent 协作",
        "agent_gate --verify 通过",
        "python3 scripts/agent_gate.py --verify",
    )
    code, out = run_cmd(["python3", "scripts/agent_gate.py", "--verify"])
    case.passed = code == 0
    case.detail = out.split("\n")[0] if out else str(code)
    report.add(case)


def check_scaffold_rounds_exist(report: TestReport) -> None:
    case = TestCase(
        "TC-15",
        "仓库结构",
        "工程线 round_00–21 概览 md 与 rounds 目录齐全",
        "ls round_*.md rounds/round_*",
    )
    md_count = len(list(REPO.glob("round_[0-9][0-9].md")))
    dir_count = len([p for p in (REPO / "rounds").iterdir() if p.is_dir() and p.name.startswith("round_")])
    ok = md_count == 22 and dir_count >= 22
    case.passed = ok
    case.detail = f"md={md_count}, dirs={dir_count}"
    report.add(case)


def check_mark_done_round_resolver(report: TestReport) -> None:
    case = TestCase(
        "TC-16",
        "进度一致性",
        "progress_store 能正确解析各 round 的 task_id",
        "检查 resolve_round_id 逻辑",
    )
    from progress_store import resolve_round_id

    samples = {
        "w1-read": "round_00",
        "r04-w1-read": "round_04",
        "r02-w1-read": "round_02",
    }
    ok = all(resolve_round_id(k) == v for k, v in samples.items())
    case.passed = ok
    case.detail = "resolve_round_id 抽样通过" if ok else "resolve_round_id 抽样失败"
    report.add(case)


def check_learn_server_api(report: TestReport) -> None:
    case = TestCase(
        "TC-17",
        "网页学习",
        "learn_server 健康检查与网页打卡 API",
        "启动 learn_server 临时端口并 POST /api/tasks",
    )
    import subprocess
    import time
    import urllib.error
    import urllib.request

    port = 18080
    proc = subprocess.Popen(
        [sys.executable, "scripts/learn_server.py", "--port", str(port)],
        cwd=REPO,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        time.sleep(0.6)
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/health", timeout=3) as resp:
            health = json.loads(resp.read().decode())
        if not health.get("ok"):
            case.passed = False
            case.detail = "health not ok"
            report.add(case)
            return

        def post(path: str) -> dict:
            req = urllib.request.Request(
                f"http://127.0.0.1:{port}{path}",
                method="POST",
                headers={"Content-Type": "application/json"},
                data=b"{}",
            )
            with urllib.request.urlopen(req, timeout=3) as resp:
                return json.loads(resp.read().decode())

        post("/api/tasks/w1-read/undo")
        marked = post("/api/tasks/w1-read/done")
        post("/api/tasks/w1-read/undo")

        with urllib.request.urlopen(
            f"http://127.0.0.1:{port}/api/content?path=rounds/round_00/week1/notes.md",
            timeout=3,
        ) as resp:
            content = json.loads(resp.read().decode())

        ok = marked.get("done") is True and content.get("ok") and content.get("html")
        case.passed = ok
        case.detail = "health + mark + content OK" if ok else "API 响应不完整"
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        case.passed = False
        case.detail = str(exc)
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()
    report.add(case)


def write_report(report: TestReport) -> None:
    statuses = scan_rounds(REPO)
    summ = summary(statuses)
    today = date.today().isoformat()
    failed = report.failed
    passed = len(report.cases) - len(failed)

    lines = [
        "# 仓库描述一致性审计报告",
        "",
        f"> 生成日期：{today} · 脚本：`python3 scripts/check_user_journey.py`",
        "",
        "## 摘要",
        "",
        f"- 测试用例：{len(report.cases)} 项，通过 {passed}，失败 {len(failed)}",
        f"- 概览 md：{summ['overview_md_count']} · 完整实操骨架：{summ['scaffold_complete_count']}",
        f"- 进度已接入：{', '.join(summ['progress_linked_rounds']) or '无'}",
        f"- 进度闭环（脚本+看板+JSON）：{', '.join(summ['full_loop_rounds']) or '无'}",
        f"- 仅骨架（未接入进度）：{', '.join(summ['scaffold_only_rounds']) or '无'}",
        "",
        "## 用户旅程测试用例",
        "",
        "| ID | 类别 | 标题 | 结果 | 说明 |",
        "|----|------|------|------|------|",
    ]
    for c in report.cases:
        status = "✅" if c.passed else "❌"
        lines.append(f"| {c.id} | {c.category} | {c.title} | {status} | {c.detail} |")

    lines.extend(
        [
            "",
            "## 轮次状态（动态扫描，勿手工维护）",
            "",
            "运行 `python3 scripts/round_status.py --markdown` 获取最新表。",
            "",
            "```markdown",
        ]
    )
    from round_status import to_markdown_table

    lines.append(to_markdown_table(statuses))
    lines.extend(["```", "", "## 修复记录", "", "_本轮修复见对应 commit / PR。_"])

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    report = TestReport()
    check_repo_root_identifiable(report)
    check_workspace_doc(report)
    check_mark_done_list(report)
    check_progress_json(report)
    check_progress_data_js(report)
    check_progress_rounds_sync(report)
    check_round00_exercises(report)
    check_progress_task_round_mapping(report)
    check_ui_tasks_in_progress(report)
    check_readme_no_false_claims(report)
    check_governance_file_naming(report)
    check_validate_learning_data(report)
    check_protocol_sync(report)
    check_agent_gate_verify(report)
    check_scaffold_rounds_exist(report)
    check_mark_done_round_resolver(report)
    check_learn_server_api(report)

    write_report(report)

    failed = report.failed
    if failed:
        print("USER JOURNEY CHECK FAILED")
        for c in failed:
            print(f"- {c.id}: {c.title} — {c.detail}")
        print(f"Report: {REPORT_PATH}")
        return 1

    print("USER JOURNEY CHECK PASSED")
    print(f"Report: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
