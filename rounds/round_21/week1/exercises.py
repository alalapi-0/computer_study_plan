#!/usr/bin/env python3
"""Round 21 · Week 1: generate tokenizer and vocabulary examples."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round21" / "week1_auto" / "tokenizer_vocab"

MANUAL_TOKENIZER = '''"""Manual tokenizer and vocabulary mapping for Round 21 Week 1."""

from __future__ import annotations

import re


class SimpleTokenizer:
    def __init__(self) -> None:
        self.pad_token = "<PAD>"
        self.unk_token = "<UNK>"
        self.token_to_id: dict[str, int] = {}
        self.id_to_token: dict[int, str] = {}
        self._add_token(self.pad_token)
        self._add_token(self.unk_token)

    def _add_token(self, token: str) -> int:
        if token not in self.token_to_id:
            index = len(self.token_to_id)
            self.token_to_id[token] = index
            self.id_to_token[index] = token
        return self.token_to_id[token]

    def tokenize(self, text: str) -> list[str]:
        return re.findall(r"[a-z0-9']+", text.lower())

    def build_vocab(self, texts: list[str]) -> None:
        for text in texts:
            for token in self.tokenize(text):
                self._add_token(token)

    def encode(self, text: str) -> list[int]:
        unknown_id = self.token_to_id[self.unk_token]
        return [self.token_to_id.get(token, unknown_id) for token in self.tokenize(text)]

    def decode(self, ids: list[int]) -> str:
        return " ".join(self.id_to_token.get(index, self.unk_token) for index in ids)


def demo() -> None:
    corpus = [
        "The cat sat on the mat",
        "The dog ran in the park",
        "Cats and dogs are great pets",
    ]
    tokenizer = SimpleTokenizer()
    tokenizer.build_vocab(corpus)
    text = "The cat ran fast"
    ids = tokenizer.encode(text)
    print("vocab_size:", len(tokenizer.token_to_id))
    print("encoded:", ids)
    print("decoded:", tokenizer.decode(ids))


if __name__ == "__main__":
    demo()
'''

STDLIB_TOKENIZER_SMOKE = '''#!/usr/bin/env python3
"""Dependency-free tokenizer smoke check for the Web UI."""

from __future__ import annotations

import json
from pathlib import Path

from manual_tokenizer import SimpleTokenizer


base = Path(__file__).resolve().parent
texts = json.loads((base / "sample_texts.json").read_text(encoding="utf-8"))
tokenizer = SimpleTokenizer()
tokenizer.build_vocab(texts)

probe = "The cat ran fast"
encoded = tokenizer.encode(probe)
decoded = tokenizer.decode(encoded)
unknown_id = tokenizer.token_to_id[tokenizer.unk_token]
summary = {
    "corpus_size": len(texts),
    "vocab_size": len(tokenizer.token_to_id),
    "pad_token_id": tokenizer.token_to_id[tokenizer.pad_token],
    "unknown_token_id": unknown_id,
    "probe": probe,
    "tokens": tokenizer.tokenize(probe),
    "encoded": encoded,
    "decoded": decoded,
    "contains_unknown": unknown_id in encoded,
    "first_vocab_items": list(tokenizer.token_to_id.items())[:8],
}
(base / "tokenizer_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
'''

STATIC_CHECK = '''#!/usr/bin/env python3
"""Static checks for Round 21 Week 1 generated files."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path


base = Path(__file__).resolve().parent
manual_source = (base / "manual_tokenizer.py").read_text(encoding="utf-8")
ast.parse(manual_source)

proc = subprocess.run([sys.executable, "stdlib_tokenizer_smoke.py"], cwd=base, capture_output=True, text=True, check=False)
summary = {}
if proc.returncode == 0:
    summary = json.loads((base / "tokenizer_summary.json").read_text(encoding="utf-8"))

strategy = json.loads((base / "tokenizer_strategy_notes.json").read_text(encoding="utf-8"))
contract = json.loads((base / "tokenizer_contract.json").read_text(encoding="utf-8"))
checks = {
    "simple_tokenizer_class": "class SimpleTokenizer" in manual_source,
    "special_tokens": all(text in manual_source for text in ("<PAD>", "<UNK>", "pad_token", "unk_token")),
    "mapping_methods": all(text in manual_source for text in ("build_vocab", "encode", "decode", "token_to_id", "id_to_token")),
    "smoke_runs": proc.returncode == 0 and summary.get("contains_unknown") is True,
    "pad_id_zero": summary.get("pad_token_id") == 0,
    "strategy_notes": {"BPE", "WordPiece"}.issubset({item["name"] for item in strategy["strategies"]}),
    "contract_steps": contract.get("workflow") == ["tokenize", "build_vocab", "encode", "decode"],
}
report = {"ok": all(checks.values()), "checks": checks, "summary": summary, "stderr": proc.stderr.strip()}
(base / "static_check_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
raise SystemExit(0 if report["ok"] else 1)
'''

SAMPLE_TEXTS = [
    "The cat sat on the mat",
    "The dog ran in the park",
    "Cats and dogs are great pets",
    "NLP turns text into model inputs",
]

STRATEGY_NOTES = {
    "topic": "tokenizer_strategies",
    "strategies": [
        {
            "name": "whitespace",
            "example": "deep learning -> ['deep', 'learning']",
            "tradeoff": "simple but weak for punctuation and unknown words",
        },
        {
            "name": "BPE",
            "example": "unbelievable -> ['un', 'believ', 'able'] style pieces",
            "tradeoff": "builds frequent subword merges and reduces unknown tokens",
        },
        {
            "name": "WordPiece",
            "example": "playing -> ['play', '##ing']",
            "tradeoff": "BERT-style subwords with continuation markers",
        },
    ],
}

CONTRACT = {
    "round": 21,
    "week": 1,
    "topic": "tokenization_vocabulary_ids",
    "workflow": ["tokenize", "build_vocab", "encode", "decode"],
    "required_files": [
        "manual_tokenizer.py",
        "sample_texts.json",
        "tokenizer_strategy_notes.json",
        "stdlib_tokenizer_smoke.py",
        "tokenizer_summary.json",
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
    (LAB / "manual_tokenizer.py").write_text(MANUAL_TOKENIZER, encoding="utf-8")
    (LAB / "sample_texts.json").write_text(json.dumps(SAMPLE_TEXTS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (LAB / "tokenizer_strategy_notes.json").write_text(json.dumps(STRATEGY_NOTES, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (LAB / "tokenizer_contract.json").write_text(json.dumps(CONTRACT, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    smoke = LAB / "stdlib_tokenizer_smoke.py"
    smoke.write_text(STDLIB_TOKENIZER_SMOKE, encoding="utf-8")
    smoke.chmod(0o755)
    check = LAB / "static_check.py"
    check.write_text(STATIC_CHECK, encoding="utf-8")
    check.chmod(0o755)
    proc = subprocess.run(["python3", str(check)], cwd=LAB, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    print("Round 21 Week 1 tokenizer / vocab 示例")
    print("sandbox:", LAB)
    print("demo:", LAB / "manual_tokenizer.py")
    print("report:", LAB / "static_check_report.json")
    mark("r21-w1-ex1")


if __name__ == "__main__":
    main()
