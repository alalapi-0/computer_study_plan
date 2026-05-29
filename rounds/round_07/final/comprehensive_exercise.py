#!/usr/bin/env python3
"""Round 07 · Final: minimal ai_prep tool demo."""

import argparse
import logging
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI prep tool minimal demo")
    parser.add_argument("--input", required=True, help="Input txt path")
    parser.add_argument("--output", default="output/result.txt", help="Output txt path")
    parser.add_argument("--dedup", action="store_true", help="Enable deduplication")
    return parser.parse_args()


def load_lines(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def dump_lines(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def maybe_dedup(lines: list[str], enabled: bool) -> list[str]:
    if not enabled:
        return lines
    seen: set[str] = set()
    result: list[str] = []
    for line in lines:
        if line not in seen:
            seen.add(line)
            result.append(line)
    return result


def setup_logging() -> None:
    Path("logs").mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler("logs/round7_final.log", encoding="utf-8")],
    )


def main() -> None:
    setup_logging()
    args = parse_args()

    src = Path(args.input)
    dst = Path(args.output)

    lines = load_lines(src)
    processed = maybe_dedup(lines, args.dedup)
    dump_lines(dst, processed)

    logging.info("input=%s original=%d output=%s processed=%d dedup=%s", src, len(lines), dst, len(processed), args.dedup)
    print("Summary")
    print("- original:", len(lines))
    print("- processed:", len(processed))
    print("- output:", dst)


if __name__ == "__main__":
    main()
