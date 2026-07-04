#!/usr/bin/env python3
"""Round 21 · Week 3: generate text feature and subword comparison examples."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round21" / "week3_auto" / "text_features"

TRADITIONAL_TEXT_FEATURES = '''"""Traditional text feature pipeline shape for Round 21 Week 3."""

from __future__ import annotations

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


texts = [
    "great movie love it",
    "terrible waste of time",
    "amazing excellent film",
    "boring bad movie",
]
labels = [1, 0, 1, 0]

count_vectorizer = CountVectorizer()
count_matrix = count_vectorizer.fit_transform(texts)
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(texts)

classifier = LogisticRegression()
classifier.fit(tfidf_matrix, labels)
pred = classifier.predict(tfidf_matrix)

print("count shape:", count_matrix.shape)
print("tfidf shape:", tfidf_matrix.shape)
print(classification_report(labels, pred, target_names=["negative", "positive"]))
'''

SUBWORD_COMPARE = '''"""Whitespace, BPE, and WordPiece tokenization comparison."""

from __future__ import annotations


COMPARISON = [
    {
        "strategy": "whitespace",
        "input": "unbelievable movie",
        "tokens": ["unbelievable", "movie"],
        "note": "simple but likely to create unknown tokens",
    },
    {
        "strategy": "BPE",
        "input": "unbelievable movie",
        "tokens": ["un", "believ", "able", "movie"],
        "note": "frequent pieces are merged into a subword vocabulary",
    },
    {
        "strategy": "WordPiece",
        "input": "playing movie",
        "tokens": ["play", "##ing", "movie"],
        "note": "continuation pieces are often marked with ##",
    },
]


if __name__ == "__main__":
    for row in COMPARISON:
        print(row["strategy"], "=>", row["tokens"])
'''

STDLIB_TEXT_FEATURES_SMOKE = '''#!/usr/bin/env python3
"""Dependency-free text feature smoke check for the Web UI."""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path


texts = [
    "great movie love it",
    "terrible waste of time",
    "amazing excellent film",
    "boring bad movie",
    "really enjoyed movie",
    "hated terrible minute",
]
labels = [1, 0, 1, 0, 1, 0]
tokens_by_doc = [text.split() for text in texts]
vocabulary = sorted({token for tokens in tokens_by_doc for token in tokens})
doc_freq = defaultdict(int)
for token in vocabulary:
    doc_freq[token] = sum(1 for tokens in tokens_by_doc if token in tokens)

tfidf_rows = []
for tokens in tokens_by_doc:
    counts = Counter(tokens)
    total = len(tokens)
    row = {}
    for token in vocabulary:
        tf = counts[token] / total if total else 0.0
        idf = math.log((1 + len(texts)) / (1 + doc_freq[token])) + 1
        row[token] = round(tf * idf, 4)
    tfidf_rows.append(row)

class_scores = {0: Counter(), 1: Counter()}
for tokens, label in zip(tokens_by_doc, labels):
    class_scores[label].update(tokens)


def predict(text: str) -> str:
    tokens = text.split()
    positive = sum(class_scores[1][token] for token in tokens)
    negative = sum(class_scores[0][token] for token in tokens)
    return "positive" if positive >= negative else "negative"


top_features = sorted(tfidf_rows[0].items(), key=lambda item: item[1], reverse=True)[:4]
predictions = {
    "great excellent movie": predict("great excellent movie"),
    "terrible boring waste": predict("terrible boring waste"),
}
summary = {
    "document_count": len(texts),
    "vocabulary_size": len(vocabulary),
    "top_features": top_features,
    "predictions": predictions,
    "subword_examples": {
        "BPE": ["un", "believ", "able"],
        "WordPiece": ["play", "##ing"],
    },
    "workflow": ["tokens", "counts", "tfidf", "linear classifier"],
}
Path("text_features_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
'''

STATIC_CHECK = '''#!/usr/bin/env python3
"""Static checks for Round 21 Week 3 generated files."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path


base = Path(__file__).resolve().parent
traditional_source = (base / "traditional_text_features.py").read_text(encoding="utf-8")
subword_source = (base / "subword_compare.py").read_text(encoding="utf-8")
ast.parse(traditional_source)
ast.parse(subword_source)

proc = subprocess.run([sys.executable, "stdlib_text_features_smoke.py"], cwd=base, capture_output=True, text=True, check=False)
summary = {}
if proc.returncode == 0:
    summary = json.loads((base / "text_features_summary.json").read_text(encoding="utf-8"))

contract = json.loads((base / "text_features_contract.json").read_text(encoding="utf-8"))
checks = {
    "sklearn_shape": all(text in traditional_source for text in ("CountVectorizer", "TfidfVectorizer", "LogisticRegression", "classification_report")),
    "subword_examples": all(text in subword_source for text in ("BPE", "WordPiece", "##ing", "whitespace")),
    "smoke_runs": proc.returncode == 0 and summary.get("vocabulary_size", 0) >= 10,
    "predictions": summary.get("predictions", {}).get("terrible boring waste") == "negative",
    "contract": contract.get("workflow") == ["bag_of_words", "tfidf", "linear_classifier", "subword_compare"],
}
report = {"ok": all(checks.values()), "checks": checks, "summary": summary, "stderr": proc.stderr.strip()}
(base / "static_check_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
raise SystemExit(0 if report["ok"] else 1)
'''

CONTRACT = {
    "round": 21,
    "week": 3,
    "topic": "traditional_text_features_subwords",
    "workflow": ["bag_of_words", "tfidf", "linear_classifier", "subword_compare"],
    "required_files": [
        "traditional_text_features.py",
        "subword_compare.py",
        "stdlib_text_features_smoke.py",
        "text_features_summary.json",
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
    (LAB / "traditional_text_features.py").write_text(TRADITIONAL_TEXT_FEATURES, encoding="utf-8")
    (LAB / "subword_compare.py").write_text(SUBWORD_COMPARE, encoding="utf-8")
    (LAB / "text_features_contract.json").write_text(json.dumps(CONTRACT, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    smoke = LAB / "stdlib_text_features_smoke.py"
    smoke.write_text(STDLIB_TEXT_FEATURES_SMOKE, encoding="utf-8")
    smoke.chmod(0o755)
    check = LAB / "static_check.py"
    check.write_text(STATIC_CHECK, encoding="utf-8")
    check.chmod(0o755)
    proc = subprocess.run(["python3", str(check)], cwd=LAB, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    print("Round 21 Week 3 traditional text feature / subword 示例")
    print("sandbox:", LAB)
    print("demo:", LAB / "traditional_text_features.py")
    print("report:", LAB / "static_check_report.json")
    mark("r21-w3-ex3")


if __name__ == "__main__":
    main()
