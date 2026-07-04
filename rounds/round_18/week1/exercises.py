#!/usr/bin/env python3
"""Round 18 · Week 1: generate NumPy array concept exercises."""

from __future__ import annotations

import ast
import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round18" / "week1_auto" / "numpy_arrays"

NUMPY_BASICS = '''"""NumPy array basics: shape, dtype, ndim, and constructors."""

import numpy as np


def main() -> None:
    a = np.array([1, 2, 3, 4, 5])
    b = np.array([[1, 2, 3], [4, 5, 6]])
    zeros = np.zeros((3, 4))
    ones = np.ones((2, 3))
    range_arr = np.arange(0, 10, 2)
    linspace_arr = np.linspace(0, 1, 5)

    print("a.shape:", a.shape)
    print("b.shape:", b.shape)
    print("b.dtype:", b.dtype)
    print("b.ndim:", b.ndim)
    print("zeros:", zeros.shape)
    print("ones:", ones.shape)
    print("range:", range_arr)
    print("linspace:", linspace_arr)


if __name__ == "__main__":
    main()
'''

VECTORIZE_DEMO = '''"""Vectorization demo: same intent, Python loop vs array operation."""

import time

import numpy as np


def square_with_loop(values):
    result = []
    for value in values:
        result.append(value ** 2)
    return result


def square_with_numpy(values):
    return values ** 2


def main() -> None:
    data = np.random.default_rng(42).normal(size=100_000)

    start = time.time()
    result_loop = square_with_loop(data)
    loop_seconds = time.time() - start

    start = time.time()
    result_np = square_with_numpy(data)
    numpy_seconds = time.time() - start

    print("loop_len:", len(result_loop))
    print("numpy_shape:", result_np.shape)
    print("speedup:", round(loop_seconds / max(numpy_seconds, 0.000001), 1))


if __name__ == "__main__":
    main()
'''

SLICE_BROADCAST = '''"""Slicing, broadcasting, and axis examples."""

import numpy as np


def main() -> None:
    matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    row = np.array([1, 2, 3])

    first_row = matrix[0]
    last_column = matrix[:, -1]
    submatrix = matrix[0:2, 1:3]
    broadcasted = matrix + row
    column_sums = matrix.sum(axis=0)
    row_sums = matrix.sum(axis=1)

    print("first_row:", first_row)
    print("last_column:", last_column)
    print("submatrix:", submatrix)
    print("broadcasted:", broadcasted)
    print("axis0_column_sums:", column_sums)
    print("axis1_row_sums:", row_sums)


if __name__ == "__main__":
    main()
'''

CONCEPTS = {
    "round": 18,
    "week": 1,
    "concepts": [
        {"name": "ndarray", "why": "stores same-type numeric data in shaped arrays"},
        {"name": "shape", "why": "tells how many dimensions and cells an array has"},
        {"name": "dtype", "why": "controls memory layout and numeric precision"},
        {"name": "axis", "why": "selects the direction for reduction or aggregation"},
        {"name": "broadcasting", "why": "aligns compatible shapes without manual loops"},
        {"name": "vectorization", "why": "moves repeated numeric work out of Python loops"},
    ],
    "axis_example": {
        "matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        "axis_0_result": [12, 15, 18],
        "axis_1_result": [6, 15, 24],
    },
}

STATIC_CHECK = '''#!/usr/bin/env python3
"""Static checks for Round 18 Week 1 generated NumPy examples."""

from __future__ import annotations

import ast
import json
from pathlib import Path


base = Path(__file__).resolve().parent
sources = {
    name: (base / name).read_text(encoding="utf-8")
    for name in ("numpy_basics.py", "vectorize_demo.py", "slice_broadcast.py")
}
for source in sources.values():
    ast.parse(source)

concepts = json.loads((base / "array_concepts.json").read_text(encoding="utf-8"))
basic = sources["numpy_basics.py"]
vector = sources["vectorize_demo.py"]
slice_src = sources["slice_broadcast.py"]

checks = {
    "imports_numpy": all("import numpy as np" in source for source in sources.values()),
    "array_basics": all(text in basic for text in ("np.array", "np.zeros", "np.ones", "np.arange", "np.linspace")),
    "shape_dtype_ndim": all(text in basic for text in ("a.shape", "b.shape", "b.dtype", "b.ndim")),
    "vectorization_pair": "for value in values" in vector and "values ** 2" in vector,
    "slicing_examples": all(text in slice_src for text in ("matrix[0]", "matrix[:, -1]", "matrix[0:2, 1:3]")),
    "broadcasting": "matrix + row" in slice_src,
    "axis_examples": "axis=0" in slice_src and "axis=1" in slice_src,
    "concept_inventory": len(concepts.get("concepts", [])) >= 6 and concepts["axis_example"]["axis_0_result"] == [12, 15, 18],
}
report = {"ok": all(checks.values()), "checks": checks, "files": sorted(sources)}
(base / "static_check_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
raise SystemExit(0 if report["ok"] else 1)
'''


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    LAB.mkdir(parents=True)


def main() -> None:
    reset_lab()
    (LAB / "numpy_basics.py").write_text(NUMPY_BASICS, encoding="utf-8")
    (LAB / "vectorize_demo.py").write_text(VECTORIZE_DEMO, encoding="utf-8")
    (LAB / "slice_broadcast.py").write_text(SLICE_BROADCAST, encoding="utf-8")
    (LAB / "array_concepts.json").write_text(json.dumps(CONCEPTS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    check = LAB / "static_check.py"
    check.write_text(STATIC_CHECK, encoding="utf-8")
    check.chmod(0o755)
    proc = subprocess.run(["python3", str(check)], cwd=LAB, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    print("Round 18 Week 1 NumPy 数组基础")
    print("sandbox:", LAB)
    print("concepts:", LAB / "array_concepts.json")
    print("report:", LAB / "static_check_report.json")
    mark("r18-w1-ex1")


if __name__ == "__main__":
    main()
