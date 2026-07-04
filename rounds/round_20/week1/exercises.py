#!/usr/bin/env python3
"""Round 20 · Week 1: generate tensor, Dataset, and DataLoader examples."""

from __future__ import annotations

import ast
import csv
import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round20" / "week1_auto" / "tensor_dataloader"

TENSOR_BASICS = '''"""Tensor basics for Round 20 Week 1."""

import numpy as np
import torch


def main() -> None:
    x = torch.tensor([1.0, 2.0, 3.0], dtype=torch.float32)
    matrix = torch.ones((2, 3), dtype=torch.float32)
    random_batch = torch.rand((4, 3))

    arr = np.array([1, 2, 3], dtype=np.float32)
    from_numpy = torch.from_numpy(arr)
    back_to_numpy = from_numpy.numpy()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    x_on_device = x.to(device)

    print("x:", x)
    print("x dtype:", x.dtype)
    print("matrix shape:", matrix.shape)
    print("random batch shape:", random_batch.shape)
    print("numpy array:", arr)
    print("from numpy:", from_numpy)
    print("back to numpy:", back_to_numpy)
    print("device:", device)
    print("x device:", x_on_device.device)


if __name__ == "__main__":
    main()
'''

DATASET_DATALOADER = '''"""Custom Dataset and DataLoader example for Round 20 Week 1."""

from __future__ import annotations

import csv
from pathlib import Path

import torch
from torch.utils.data import Dataset, DataLoader


class ToyTabularDataset(Dataset):
    def __init__(self, path: Path) -> None:
        with path.open("r", encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        self.X = torch.tensor(
            [[float(row["feature_a"]), float(row["feature_b"]), float(row["feature_c"])] for row in rows],
            dtype=torch.float32,
        )
        self.y = torch.tensor([int(row["label"]) for row in rows], dtype=torch.long)

    def __len__(self) -> int:
        return len(self.X)

    def __getitem__(self, index: int):
        return self.X[index], self.y[index]


def main() -> None:
    dataset = ToyTabularDataset(Path("toy_tabular.csv"))
    loader = DataLoader(dataset, batch_size=4, shuffle=True)
    for batch_index, (X_batch, y_batch) in enumerate(loader):
        print("batch:", batch_index, "X:", tuple(X_batch.shape), "y:", tuple(y_batch.shape))
        if batch_index == 1:
            break


if __name__ == "__main__":
    main()
'''

STDLIB_BATCH_DEMO = '''#!/usr/bin/env python3
"""Dependency-free batch loader used by the Web UI smoke check."""

from __future__ import annotations

import csv
import json
from pathlib import Path


base = Path(__file__).resolve().parent
with (base / "toy_tabular.csv").open("r", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

features = [[float(row["feature_a"]), float(row["feature_b"]), float(row["feature_c"])] for row in rows]
labels = [int(row["label"]) for row in rows]
batch_size = 4
batches = [
    {
        "batch_index": index,
        "x_shape": [len(features[index:index + batch_size]), len(features[0])],
        "y_shape": [len(labels[index:index + batch_size])],
        "label_sum": sum(labels[index:index + batch_size]),
    }
    for index in range(0, len(rows), batch_size)
]
summary = {
    "rows": len(rows),
    "feature_count": len(features[0]),
    "batch_size": batch_size,
    "batch_count": len(batches),
    "first_batch": batches[0],
    "dataset_methods": ["__len__", "__getitem__"],
}
(base / "batch_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
'''

STATIC_CHECK = '''#!/usr/bin/env python3
"""Static checks for Round 20 Week 1 generated files."""

from __future__ import annotations

import ast
import csv
import json
import subprocess
import sys
from pathlib import Path


base = Path(__file__).resolve().parent
tensor = (base / "tensor_basics.py").read_text(encoding="utf-8")
dataset = (base / "dataset_dataloader.py").read_text(encoding="utf-8")
ast.parse(tensor)
ast.parse(dataset)

with (base / "toy_tabular.csv").open("r", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

proc = subprocess.run([sys.executable, "stdlib_batch_demo.py"], cwd=base, capture_output=True, text=True, check=False)
summary = {}
if proc.returncode == 0:
    summary = json.loads((base / "batch_summary.json").read_text(encoding="utf-8"))

checks = {
    "tensor_imports": all(text in tensor for text in ("import torch", "import numpy as np", "torch.tensor", "torch.from_numpy")),
    "shape_dtype_device": all(text in tensor for text in ("dtype=torch.float32", ".shape", ".to(device)", "torch.cuda.is_available")),
    "dataset_contract": all(text in dataset for text in ("class ToyTabularDataset", "Dataset", "__len__", "__getitem__")),
    "dataloader_contract": all(text in dataset for text in ("DataLoader", "batch_size=4", "shuffle=True")),
    "toy_data": len(rows) == 12 and set(rows[0]) == {"id", "feature_a", "feature_b", "feature_c", "label"},
    "stdlib_demo_runs": proc.returncode == 0 and summary.get("batch_count") == 3 and summary.get("feature_count") == 3,
    "contract": len(json.loads((base / "tensor_dataloader_contract.json").read_text(encoding="utf-8")).get("workflow", [])) == 4,
}
report = {"ok": all(checks.values()), "checks": checks, "summary": summary, "stderr": proc.stderr.strip()}
(base / "static_check_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
raise SystemExit(0 if report["ok"] else 1)
'''

CONTRACT = {
    "round": 20,
    "week": 1,
    "topic": "tensor_dataset_dataloader",
    "workflow": ["create tensors", "inspect shape dtype device", "build Dataset", "iterate DataLoader batches"],
    "generated_files": [
        "tensor_basics.py",
        "dataset_dataloader.py",
        "toy_tabular.csv",
        "stdlib_batch_demo.py",
        "static_check_report.json",
    ],
}

TOY_ROWS = [
    {"id": 1, "feature_a": "0.1", "feature_b": "1.0", "feature_c": "2.0", "label": "0"},
    {"id": 2, "feature_a": "0.2", "feature_b": "1.1", "feature_c": "2.2", "label": "0"},
    {"id": 3, "feature_a": "0.3", "feature_b": "1.2", "feature_c": "2.4", "label": "0"},
    {"id": 4, "feature_a": "0.4", "feature_b": "1.3", "feature_c": "2.6", "label": "0"},
    {"id": 5, "feature_a": "1.1", "feature_b": "2.0", "feature_c": "0.5", "label": "1"},
    {"id": 6, "feature_a": "1.2", "feature_b": "2.2", "feature_c": "0.4", "label": "1"},
    {"id": 7, "feature_a": "1.3", "feature_b": "2.4", "feature_c": "0.3", "label": "1"},
    {"id": 8, "feature_a": "1.4", "feature_b": "2.6", "feature_c": "0.2", "label": "1"},
    {"id": 9, "feature_a": "2.1", "feature_b": "0.4", "feature_c": "1.1", "label": "2"},
    {"id": 10, "feature_a": "2.2", "feature_b": "0.3", "feature_c": "1.2", "label": "2"},
    {"id": 11, "feature_a": "2.3", "feature_b": "0.2", "feature_c": "1.3", "label": "2"},
    {"id": 12, "feature_a": "2.4", "feature_b": "0.1", "feature_c": "1.4", "label": "2"},
]


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    LAB.mkdir(parents=True)


def write_csv(path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "feature_a", "feature_b", "feature_c", "label"])
        writer.writeheader()
        writer.writerows(TOY_ROWS)


def main() -> None:
    reset_lab()
    (LAB / "tensor_basics.py").write_text(TENSOR_BASICS, encoding="utf-8")
    (LAB / "dataset_dataloader.py").write_text(DATASET_DATALOADER, encoding="utf-8")
    write_csv(LAB / "toy_tabular.csv")
    (LAB / "tensor_dataloader_contract.json").write_text(json.dumps(CONTRACT, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (LAB / "stdlib_batch_demo.py").write_text(STDLIB_BATCH_DEMO, encoding="utf-8")
    check = LAB / "static_check.py"
    check.write_text(STATIC_CHECK, encoding="utf-8")
    check.chmod(0o755)
    proc = subprocess.run(["python3", str(check)], cwd=LAB, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    print("Round 20 Week 1 tensor / Dataset / DataLoader 示例")
    print("sandbox:", LAB)
    print("demo:", LAB / "tensor_basics.py")
    print("report:", LAB / "static_check_report.json")
    mark("r20-w1-ex1")


if __name__ == "__main__":
    main()
