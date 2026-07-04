#!/usr/bin/env python3
"""Round 20 · Week 3: generate eval/no_grad and checkpoint examples."""

from __future__ import annotations

import ast
import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round20" / "week3_auto" / "checkpoint_eval"

EVAL_CHECKPOINT = '''"""eval, no_grad, and checkpoint example for Round 20 Week 3."""

from __future__ import annotations

import json
from pathlib import Path

import torch
from torch import nn


class TinyRegressor(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.linear = nn.Linear(2, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.linear(x)


def save_checkpoint(model: nn.Module, path: Path, metadata: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), path)
    path.with_suffix(".manifest.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")


def load_for_inference(path: Path) -> nn.Module:
    model = TinyRegressor()
    state_dict = torch.load(path, map_location="cpu")
    model.load_state_dict(state_dict)
    model.eval()
    return model


def predict_once(model: nn.Module, sample: torch.Tensor) -> torch.Tensor:
    model.eval()
    with torch.no_grad():
        return model(sample)


def main() -> None:
    checkpoint_path = Path("checkpoints/tiny_regressor.pt")
    model = TinyRegressor()
    save_checkpoint(model, checkpoint_path, {"model": "TinyRegressor", "input_shape": [None, 2]})
    loaded = load_for_inference(checkpoint_path)
    output = predict_once(loaded, torch.tensor([[0.2, 0.8]], dtype=torch.float32))
    print("checkpoint:", checkpoint_path)
    print("output shape:", tuple(output.shape))


if __name__ == "__main__":
    main()
'''

STDLIB_CHECKPOINT_DEMO = '''#!/usr/bin/env python3
"""Dependency-free checkpoint smoke check for the Web UI."""

from __future__ import annotations

import json
from pathlib import Path


base = Path(__file__).resolve().parent
checkpoint_dir = base / "checkpoints"
checkpoint_dir.mkdir(exist_ok=True)
state = {"linear.weight": [[0.25, 0.75]], "linear.bias": [0.1]}
manifest = {
    "model": "TinyRegressor",
    "input_shape": ["batch", 2],
    "output_shape": ["batch", 1],
    "rules": ["recreate model code", "load state", "model.eval", "no_grad for inference"],
}
(checkpoint_dir / "tiny_regressor_state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
(checkpoint_dir / "tiny_regressor_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")

loaded = json.loads((checkpoint_dir / "tiny_regressor_state.json").read_text(encoding="utf-8"))
weights = loaded["linear.weight"][0]
bias = loaded["linear.bias"][0]
sample = [0.2, 0.8]
prediction = sum(value * weight for value, weight in zip(sample, weights)) + bias
summary = {
    "checkpoint_files": sorted(path.name for path in checkpoint_dir.glob("*.json")),
    "prediction": round(prediction, 3),
    "rules": manifest["rules"],
    "has_manifest": True,
}
(base / "checkpoint_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
'''

STATIC_CHECK = '''#!/usr/bin/env python3
"""Static checks for Round 20 Week 3 generated files."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path


base = Path(__file__).resolve().parent
source = (base / "eval_and_checkpoint.py").read_text(encoding="utf-8")
ast.parse(source)

proc = subprocess.run([sys.executable, "stdlib_checkpoint_demo.py"], cwd=base, capture_output=True, text=True, check=False)
summary = {}
if proc.returncode == 0:
    summary = json.loads((base / "checkpoint_summary.json").read_text(encoding="utf-8"))

checks = {
    "eval_no_grad": all(text in source for text in ("model.eval()", "torch.no_grad()", "predict_once")),
    "state_dict_save": all(text in source for text in ("torch.save(model.state_dict()", "torch.load", "load_state_dict")),
    "manifest": "manifest.json" in source and "input_shape" in source,
    "model_structure": all(text in source for text in ("class TinyRegressor", "nn.Module", "nn.Linear")),
    "stdlib_demo_runs": proc.returncode == 0 and summary.get("has_manifest") is True and len(summary.get("checkpoint_files", [])) == 2,
    "contract": len(json.loads((base / "checkpoint_contract.json").read_text(encoding="utf-8")).get("rules", [])) == 4,
}
report = {"ok": all(checks.values()), "checks": checks, "summary": summary, "stderr": proc.stderr.strip()}
(base / "static_check_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
raise SystemExit(0 if report["ok"] else 1)
'''

CONTRACT = {
    "round": 20,
    "week": 3,
    "topic": "eval_no_grad_checkpoint",
    "rules": ["call model.eval before evaluation", "use torch.no_grad for inference", "save state_dict", "keep model code and manifest"],
    "outputs": ["eval_and_checkpoint.py", "checkpoint_summary.json", "static_check_report.json"],
}


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    LAB.mkdir(parents=True)


def main() -> None:
    reset_lab()
    (LAB / "eval_and_checkpoint.py").write_text(EVAL_CHECKPOINT, encoding="utf-8")
    (LAB / "stdlib_checkpoint_demo.py").write_text(STDLIB_CHECKPOINT_DEMO, encoding="utf-8")
    (LAB / "checkpoint_contract.json").write_text(json.dumps(CONTRACT, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    check = LAB / "static_check.py"
    check.write_text(STATIC_CHECK, encoding="utf-8")
    check.chmod(0o755)
    proc = subprocess.run(["python3", str(check)], cwd=LAB, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    print("Round 20 Week 3 eval/no_grad/checkpoint 示例")
    print("sandbox:", LAB)
    print("demo:", LAB / "eval_and_checkpoint.py")
    print("report:", LAB / "static_check_report.json")
    mark("r20-w3-ex3")


if __name__ == "__main__":
    main()
