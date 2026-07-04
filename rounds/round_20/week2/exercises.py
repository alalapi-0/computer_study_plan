#!/usr/bin/env python3
"""Round 20 · Week 2: generate nn.Module and training loop examples."""

from __future__ import annotations

import ast
import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round20" / "week2_auto" / "training_loop"

MODEL = '''"""Minimal nn.Module example for Round 20 Week 2."""

import torch
from torch import nn


class TinyClassifier(nn.Module):
    def __init__(self, input_size: int = 3, hidden_size: int = 8, num_classes: int = 2) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)


def count_parameters(model: nn.Module) -> int:
    return sum(parameter.numel() for parameter in model.parameters())


if __name__ == "__main__":
    model = TinyClassifier()
    sample = torch.rand((4, 3))
    output = model(sample)
    print(model)
    print("input shape:", tuple(sample.shape))
    print("output shape:", tuple(output.shape))
    print("parameters:", count_parameters(model))
'''

TRAIN_LOOP = '''"""Training loop skeleton for Round 20 Week 2."""

from __future__ import annotations

import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from model import TinyClassifier


def build_loaders(batch_size: int = 8) -> tuple[DataLoader, DataLoader]:
    X = torch.tensor(
        [[0.1, 1.0, 2.0], [0.2, 1.2, 2.2], [1.1, 2.0, 0.5], [1.3, 2.2, 0.4]] * 8,
        dtype=torch.float32,
    )
    y = torch.tensor([0, 0, 1, 1] * 8, dtype=torch.long)
    train_dataset = TensorDataset(X[:24], y[:24])
    test_dataset = TensorDataset(X[24:], y[24:])
    return DataLoader(train_dataset, batch_size=batch_size, shuffle=True), DataLoader(test_dataset, batch_size=batch_size)


def train_one_epoch(model: nn.Module, loader: DataLoader, loss_fn: nn.Module, optimizer: torch.optim.Optimizer) -> float:
    model.train()
    total_loss = 0.0
    for X_batch, y_batch in loader:
        pred = model(X_batch)
        loss = loss_fn(pred, y_batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += float(loss.item())
    return total_loss / len(loader)


def evaluate(model: nn.Module, loader: DataLoader, loss_fn: nn.Module) -> dict:
    model.eval()
    total_loss = 0.0
    correct = 0
    with torch.no_grad():
        for X_batch, y_batch in loader:
            pred = model(X_batch)
            total_loss += float(loss_fn(pred, y_batch).item())
            correct += int((pred.argmax(dim=1) == y_batch).sum().item())
    return {"loss": round(total_loss / len(loader), 4), "accuracy": round(correct / len(loader.dataset), 4)}


def main() -> None:
    train_loader, test_loader = build_loaders()
    model = TinyClassifier()
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
    for epoch in range(3):
        loss = train_one_epoch(model, train_loader, loss_fn, optimizer)
        metrics = evaluate(model, test_loader, loss_fn)
        print("epoch:", epoch, "train_loss:", round(loss, 4), "metrics:", metrics)


if __name__ == "__main__":
    main()
'''

STDLIB_GRADIENT_DEMO = '''#!/usr/bin/env python3
"""Dependency-free gradient descent smoke check for the Web UI."""

from __future__ import annotations

import json
from pathlib import Path


xs = [1.0, 2.0, 3.0, 4.0]
ys = [2.0, 4.0, 6.0, 8.0]
weight = 0.0
lr = 0.05
history = []
for epoch in range(8):
    preds = [weight * x for x in xs]
    errors = [pred - y for pred, y in zip(preds, ys)]
    loss = sum(error * error for error in errors) * len(errors) ** -1
    grad = sum(2 * error * x for error, x in zip(errors, xs)) * len(xs) ** -1
    weight = weight - lr * grad
    history.append({"epoch": epoch, "loss": round(loss, 4), "weight": round(weight, 4)})

summary = {
    "initial_loss": history[0]["loss"],
    "final_loss": history[-1]["loss"],
    "loss_decreased": history[-1]["loss"] < history[0]["loss"],
    "steps": ["forward", "loss", "zero_grad", "backward", "optimizer_step"],
    "history": history,
}
Path("training_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
'''

STATIC_CHECK = '''#!/usr/bin/env python3
"""Static checks for Round 20 Week 2 generated files."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path


base = Path(__file__).resolve().parent
model_source = (base / "model.py").read_text(encoding="utf-8")
train_source = (base / "train_loop.py").read_text(encoding="utf-8")
ast.parse(model_source)
ast.parse(train_source)

proc = subprocess.run([sys.executable, "stdlib_gradient_demo.py"], cwd=base, capture_output=True, text=True, check=False)
summary = {}
if proc.returncode == 0:
    summary = json.loads((base / "training_summary.json").read_text(encoding="utf-8"))

checks = {
    "module_shape": all(text in model_source for text in ("class TinyClassifier", "nn.Module", "super().__init__", "def forward", "nn.Linear", "nn.ReLU")),
    "parameter_count": "model.parameters()" in model_source and "numel()" in model_source,
    "training_steps": all(text in train_source for text in ("model.train()", "pred = model", "loss_fn", "optimizer.zero_grad()", "loss.backward()", "optimizer.step()")),
    "eval_steps": all(text in train_source for text in ("model.eval()", "torch.no_grad()", "argmax")),
    "loader_contract": all(text in train_source for text in ("TensorDataset", "DataLoader", "batch_size")),
    "stdlib_demo_runs": proc.returncode == 0 and summary.get("loss_decreased") is True,
    "contract": len(json.loads((base / "training_loop_contract.json").read_text(encoding="utf-8")).get("training_steps", [])) == 5,
}
report = {"ok": all(checks.values()), "checks": checks, "summary": summary, "stderr": proc.stderr.strip()}
(base / "static_check_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
raise SystemExit(0 if report["ok"] else 1)
'''

CONTRACT = {
    "round": 20,
    "week": 2,
    "topic": "nn_module_training_loop",
    "model_parts": ["__init__", "forward", "parameters"],
    "training_steps": ["forward", "loss", "zero_grad", "backward", "optimizer_step"],
    "eval_steps": ["model.eval", "torch.no_grad", "argmax", "accuracy"],
}


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    LAB.mkdir(parents=True)


def main() -> None:
    reset_lab()
    (LAB / "model.py").write_text(MODEL, encoding="utf-8")
    (LAB / "train_loop.py").write_text(TRAIN_LOOP, encoding="utf-8")
    (LAB / "stdlib_gradient_demo.py").write_text(STDLIB_GRADIENT_DEMO, encoding="utf-8")
    (LAB / "training_loop_contract.json").write_text(json.dumps(CONTRACT, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    check = LAB / "static_check.py"
    check.write_text(STATIC_CHECK, encoding="utf-8")
    check.chmod(0o755)
    proc = subprocess.run(["python3", str(check)], cwd=LAB, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    print("Round 20 Week 2 nn.Module 与训练循环示例")
    print("sandbox:", LAB)
    print("demo:", LAB / "train_loop.py")
    print("report:", LAB / "static_check_report.json")
    mark("r20-w2-ex2")


if __name__ == "__main__":
    main()
