#!/usr/bin/env python3
"""Round 12 · Week 1 exercises: batch scan input directory."""

from pathlib import Path


def scan_inputs(input_dir: Path) -> list[Path]:
    if not input_dir.is_dir():
        return []
    return sorted(p for p in input_dir.iterdir() if p.is_file())


def main() -> None:
    base = Path.home() / "cli-lab" / "round12" / "week1"
    input_dir = base / "input"
    output_dir = base / "output"
    fail_log = base / "failures.log"

    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    files = scan_inputs(input_dir)
    processed = 0
    failures: list[str] = []

    for src in files:
        try:
            dst = output_dir / src.name
            dst.write_text(src.read_text(encoding="utf-8").strip() + "\n", encoding="utf-8")
            processed += 1
        except OSError as exc:
            failures.append(f"{src.name}: {exc}")

    if failures:
        fail_log.write_text("\n".join(failures) + "\n", encoding="utf-8")

    print(f"扫描 {len(files)} 个文件，成功 {processed}，失败 {len(failures)}")
    print("沙盒目录:", base)


if __name__ == "__main__":
    main()
