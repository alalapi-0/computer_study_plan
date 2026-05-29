#!/usr/bin/env python3
"""Round 08 · Week 3 exercises: API shape rehearsal."""


def build_health() -> dict[str, str]:
    return {"status": "ok"}


def build_run_response(input_file: str, dedup: bool) -> dict[str, object]:
    return {
        "status": "accepted",
        "input_file": input_file,
        "dedup": dedup,
    }


def main() -> None:
    print("health:", build_health())
    print("run:", build_run_response("input/demo.txt", True))


if __name__ == "__main__":
    main()
