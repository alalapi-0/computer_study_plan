import json
import math
import stat
import struct
import subprocess
import sys
import wave
from pathlib import Path

EXPECTED_SPEC = b'{"duration_seconds":0.25,"frequency_hz":440,"channels":1,"sample_width_bytes":2,"sample_rate_hz":16000}\n'


def emit(**payload):
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def regular(path, limit):
    try:
        st = path.lstat()
    except OSError:
        return False
    return stat.S_ISREG(st.st_mode) and not path.is_symlink() and st.st_size <= limit


mode = sys.argv[1] if len(sys.argv) > 1 else "check"
spec = Path("/workspace/input/spec.json")
generator = Path("/workspace/app/generate_tone.py")
if mode == "ready":
    ready = Path("/usr/bin/python3").exists() and spec.is_file() and generator.is_file()
    emit(ready=ready, passed=False, evidence=["Python stdlib media fixture available"] if ready else ["platform or setup output missing"])
    raise SystemExit(0)
if not regular(spec, 4096) or spec.read_bytes() != EXPECTED_SPEC:
    emit(ready=True, passed=False, evidence=["protected WAV specification is missing, linked, oversized, or changed"])
    raise SystemExit(0)
if not regular(generator, 24_000):
    emit(ready=True, passed=False, evidence=["generator must be a bounded regular file"])
    raise SystemExit(0)
artifact = Path("/workspace/output/tone.wav")
if not regular(artifact, 64_000):
    emit(ready=True, passed=False, evidence=["the learner-produced WAV is missing, linked, or oversized"])
    raise SystemExit(0)


def inspect_wav(path):
    with wave.open(str(path), "rb") as wav:
        params = (wav.getnchannels(), wav.getsampwidth(), wav.getframerate(), wav.getnframes())
        frames = wav.readframes(wav.getnframes())
    samples = struct.unpack("<" + "h" * (len(frames) // 2), frames)
    peak = max(abs(value) for value in samples)
    rms = round(math.sqrt(sum(value * value for value in samples) / len(samples)))
    positive_crossings = sum(1 for left, right in zip(samples, samples[1:]) if left <= 0 < right)
    frequency = positive_crossings / (len(samples) / params[2])
    return params, peak, rms, frequency


try:
    initial = inspect_wav(artifact)
    run = subprocess.run(["/usr/bin/python3", str(generator)], text=True, capture_output=True, timeout=4)
    regenerated = inspect_wav(artifact)
except (OSError, ValueError, ZeroDivisionError, struct.error, wave.Error, subprocess.TimeoutExpired) as exc:
    emit(ready=True, passed=False, evidence=[f"WAV qualification failed safely: {type(exc).__name__}: {exc}"])
    raise SystemExit(0)
def qualified(measurement):
    params, peak, rms, frequency = measurement
    return params == (1, 2, 16000, 4000) and 7000 <= rms <= 9000 and peak <= 12_100 and 435 <= frequency <= 445


passed = run.returncode == 0 and qualified(initial) and qualified(regenerated)
params, peak, rms, frequency = regenerated
emit(ready=True, passed=passed, evidence=[f"learner artifact qualified before rerun={qualified(initial)}", f"generator exit={run.returncode}", f"channels,width,rate,frames={params!r}", f"rms={rms}, peak={peak}, estimated_hz={frequency:.1f}"])
