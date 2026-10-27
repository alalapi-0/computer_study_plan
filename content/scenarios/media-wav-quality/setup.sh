#!/bin/bash
set -euo pipefail
mkdir -p /workspace/app /workspace/input /workspace/output
printf '{"duration_seconds":0.25,"frequency_hz":440,"channels":1,"sample_width_bytes":2,"sample_rate_hz":16000}\n' > /workspace/input/spec.json
cat > /workspace/app/generate_tone.py <<'PY'
import math
import struct
import wave
from pathlib import Path

RATE = 8000
DURATION = 0.25
FREQUENCY = 440
AMPLITUDE = 32767
frames = []
for index in range(round(RATE * DURATION)):
    sample = int(AMPLITUDE * math.sin(2 * math.pi * FREQUENCY * index / RATE))
    frames.append(struct.pack("<h", sample))
with wave.open("/workspace/output/tone.wav", "wb") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(RATE)
    wav.writeframes(b"".join(frames))
print(f"wrote {len(frames)} frames at {RATE} Hz")
PY
python3 /workspace/app/generate_tone.py >/dev/null
