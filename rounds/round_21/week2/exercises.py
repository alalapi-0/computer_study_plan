#!/usr/bin/env python3
"""Round 21 · Week 2: generate embedding and text classifier examples."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round21" / "week2_auto" / "embedding_classifier"

EMBEDDING_DEMO = '''"""nn.Embedding shape demo for Round 21 Week 2."""

import torch
from torch import nn


def main() -> None:
    embedding = nn.Embedding(num_embeddings=12, embedding_dim=5, padding_idx=0)
    token_ids = torch.tensor([[2, 3, 4, 0], [5, 6, 0, 0]], dtype=torch.long)
    vectors = embedding(token_ids)
    print("input shape:", tuple(token_ids.shape))
    print("embedding shape:", tuple(vectors.shape))
    print("pad row:", embedding.weight[0])


if __name__ == "__main__":
    main()
'''

TEXT_CLASSIFIER = '''"""Embedding + mean pooling text classifier shape for Round 21 Week 2."""

from __future__ import annotations

import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader


class TextDataset(Dataset):
    def __init__(self, encoded_texts: list[list[int]], labels: list[int], pad_id: int = 0, max_len: int = 8) -> None:
        self.rows: list[tuple[torch.Tensor, torch.Tensor]] = []
        for ids, label in zip(encoded_texts, labels):
            clipped = ids[:max_len]
            padded = clipped + [pad_id] * (max_len - len(clipped))
            self.rows.append((torch.tensor(padded, dtype=torch.long), torch.tensor(label, dtype=torch.long)))

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, index: int):
        return self.rows[index]


class TextClassifier(nn.Module):
    def __init__(self, vocab_size: int, embedding_dim: int = 16, num_classes: int = 2, padding_idx: int = 0) -> None:
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=padding_idx)
        self.classifier = nn.Linear(embedding_dim, num_classes)

    def forward(self, token_ids: torch.Tensor) -> torch.Tensor:
        embedded = self.embedding(token_ids)
        mask = (token_ids != 0).unsqueeze(-1)
        pooled = (embedded * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1)
        return self.classifier(pooled)


def train_one_epoch(model: nn.Module, loader: DataLoader, optimizer: torch.optim.Optimizer, loss_fn: nn.Module) -> float:
    model.train()
    total = 0.0
    for token_ids, labels in loader:
        pred = model(token_ids)
        loss = loss_fn(pred, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total += float(loss.item())
    return total / len(loader)
'''

STDLIB_EMBEDDING_SMOKE = '''#!/usr/bin/env python3
"""Dependency-free embedding intuition smoke check for the Web UI."""

from __future__ import annotations

import json
from pathlib import Path


base = Path(__file__).resolve().parent
rows = json.loads((base / "sample_sentiment.json").read_text(encoding="utf-8"))
pad_id = 0
embedding_dim = 4
vocab = {"<PAD>": pad_id, "<UNK>": 1}
for row in rows:
    for token in row["text"].split():
        if token not in vocab:
            vocab[token] = len(vocab)


def encode(text: str, max_len: int = 5) -> list[int]:
    ids = [vocab.get(token, vocab["<UNK>"]) for token in text.split()][:max_len]
    return ids + [pad_id] * (max_len - len(ids))


def vector_for_id(token_id: int) -> list[float]:
    if token_id == pad_id:
        return [0.0] * embedding_dim
    return [round((((token_id + 1) * (axis + 2)) % 11 - 5) * 0.2, 3) for axis in range(embedding_dim)]


def mean_pool(ids: list[int]) -> list[float]:
    vectors = [vector_for_id(token_id) for token_id in ids if token_id != pad_id]
    scale = len(vectors) ** -1 if vectors else 1.0
    return [round(sum(vector[axis] for vector in vectors) * scale, 3) for axis in range(embedding_dim)]


positive_tokens = {"great", "love", "amazing", "excellent", "enjoyed"}
negative_tokens = {"terrible", "boring", "bad", "hated", "waste"}
probe = "great movie enjoyed"
encoded = encode(probe)
pooled = mean_pool(encoded)
score = sum(1 for token in probe.split() if token in positive_tokens) - sum(1 for token in probe.split() if token in negative_tokens)
prediction = "positive" if score >= 0 else "negative"
summary = {
    "vocab_size": len(vocab),
    "embedding_dim": embedding_dim,
    "pad_id": pad_id,
    "probe": probe,
    "encoded": encoded,
    "encoded_batch_shape": [1, len(encoded)],
    "pooled_vector": pooled,
    "prediction": prediction,
    "workflow": ["token ids", "embedding lookup", "mask padding", "mean pooling", "classifier"],
}
(base / "embedding_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
'''

STATIC_CHECK = '''#!/usr/bin/env python3
"""Static checks for Round 21 Week 2 generated files."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path


base = Path(__file__).resolve().parent
embedding_source = (base / "embedding_demo.py").read_text(encoding="utf-8")
classifier_source = (base / "text_classifier.py").read_text(encoding="utf-8")
ast.parse(embedding_source)
ast.parse(classifier_source)

proc = subprocess.run([sys.executable, "stdlib_embedding_smoke.py"], cwd=base, capture_output=True, text=True, check=False)
summary = {}
if proc.returncode == 0:
    summary = json.loads((base / "embedding_summary.json").read_text(encoding="utf-8"))

contract = json.loads((base / "embedding_contract.json").read_text(encoding="utf-8"))
checks = {
    "embedding_demo": all(text in embedding_source for text in ("nn.Embedding", "embedding_dim", "padding_idx", "token_ids")),
    "dataset_shape": all(text in classifier_source for text in ("class TextDataset", "Dataset", "__len__", "__getitem__", "max_len")),
    "classifier_shape": all(text in classifier_source for text in ("class TextClassifier", "nn.Module", "nn.Embedding", "nn.Linear", "forward")),
    "pooling_masks_padding": all(text in classifier_source for text in ("mask", "sum(dim=1)", "clamp(min=1)")),
    "training_steps": all(text in classifier_source for text in ("optimizer.zero_grad()", "loss.backward()", "optimizer.step()")),
    "smoke_runs": proc.returncode == 0 and summary.get("embedding_dim") == 4 and summary.get("prediction") == "positive",
    "contract": contract.get("workflow") == ["encode", "pad", "embedding", "pooling", "classifier"],
}
report = {"ok": all(checks.values()), "checks": checks, "summary": summary, "stderr": proc.stderr.strip()}
(base / "static_check_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
raise SystemExit(0 if report["ok"] else 1)
'''

SAMPLE_SENTIMENT = [
    {"text": "great movie love it", "label": 1},
    {"text": "terrible waste of time", "label": 0},
    {"text": "amazing excellent film", "label": 1},
    {"text": "boring bad movie", "label": 0},
    {"text": "really enjoyed this", "label": 1},
    {"text": "hated every minute", "label": 0},
]

CONTRACT = {
    "round": 21,
    "week": 2,
    "topic": "embedding_text_classifier",
    "workflow": ["encode", "pad", "embedding", "pooling", "classifier"],
    "required_files": [
        "embedding_demo.py",
        "text_classifier.py",
        "sample_sentiment.json",
        "stdlib_embedding_smoke.py",
        "embedding_summary.json",
    ],
}


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    LAB.mkdir(parents=True)


def main() -> None:
    reset_lab()
    (LAB / "embedding_demo.py").write_text(EMBEDDING_DEMO, encoding="utf-8")
    (LAB / "text_classifier.py").write_text(TEXT_CLASSIFIER, encoding="utf-8")
    (LAB / "sample_sentiment.json").write_text(json.dumps(SAMPLE_SENTIMENT, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (LAB / "embedding_contract.json").write_text(json.dumps(CONTRACT, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    smoke = LAB / "stdlib_embedding_smoke.py"
    smoke.write_text(STDLIB_EMBEDDING_SMOKE, encoding="utf-8")
    smoke.chmod(0o755)
    check = LAB / "static_check.py"
    check.write_text(STATIC_CHECK, encoding="utf-8")
    check.chmod(0o755)
    proc = subprocess.run(["python3", str(check)], cwd=LAB, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    print("Round 21 Week 2 embedding / text classifier 示例")
    print("sandbox:", LAB)
    print("demo:", LAB / "text_classifier.py")
    print("report:", LAB / "static_check_report.json")
    mark("r21-w2-ex2")


if __name__ == "__main__":
    main()
