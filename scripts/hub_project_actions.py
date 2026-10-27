"""Finite local actions. No capture, shell, scheduler or normal Hub route.

LabManager alone supplies owned roots and persists operations. Public bindings
contain native UUID, check identity, exact bytes and code/permission versions;
no host path or terminal data. Location is a pure URL, never an execution.
"""
from __future__ import annotations
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import stat
import struct
import wave
from contextlib import contextmanager
from urllib.parse import urlencode

ACTION_VERSION = 'study-wav-actions/1'
PERMISSION_VERSION = 'local-browser-token/wav-only/1'
LIMIT = 64000
SCENARIO = 'media-wav-quality'
CODE_VERSION = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

class ActionError(RuntimeError):
    def __init__(self, reason, status=409):
        super().__init__(reason)
        self.status = status


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def canonical_export_binding(binding):
    """Closed export-only JSON identity; 440 and 440.0 denote the same number.

    Keep bool distinct from numeric 0/1, and keep nonintegral finite floats
    unchanged. Callers compare this encoding with the server's expected binding,
    never Python's bool/int-coercing dictionary equality. No other operation's
    fingerprint or persisted history is migrated by this helper.
    """
    fields = {'action_version', 'permission_version', 'code_version', 'runtime_code_version',
              'scenario_id', 'scenario_version', 'scenario_hash', 'attempt_id',
              'attempt_revision', 'check_id', 'check_revision', 'artifact'}
    artifact_fields = {'sha256', 'size', 'channels', 'sample_width_bytes', 'sample_rate_hz',
                       'frames', 'duration_seconds', 'peak', 'rms', 'frequency_hz'}
    if type(binding) is not dict or set(binding) != fields:
        raise ActionError('invalid_binding_shape', 400)
    artifact = binding['artifact']
    if type(artifact) is not dict or set(artifact) != artifact_fields:
        raise ActionError('invalid_artifact_binding_shape', 400)
    def scalar(value, numeric):
        if numeric:
            if type(value) not in (int, float, bool): raise ActionError('invalid_binding_number', 400)
            if type(value) is float:
                if not math.isfinite(value): raise ActionError('nonfinite_binding_number', 400)
                if value.is_integer(): return int(value)
            return value
        if type(value) is not str or len(value) > 8192:
            raise ActionError('invalid_binding_text', 400)
        return value
    normalized = {key: scalar(value, key == 'scenario_version') for key, value in binding.items() if key != 'artifact'}
    normalized['artifact'] = {key: scalar(value, key != 'sha256') for key, value in artifact.items()}
    try:
        # Preserve the existing bound on the submitted input, measured as UTF-8.
        raw = json.dumps(binding, ensure_ascii=False, allow_nan=False).encode('utf-8')
        result = json.dumps(normalized, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)
        if len(raw) > 8192 or len(result.encode('utf-8')) > 8192:
            raise ActionError('binding_too_large', 400)
        return result
    except (ValueError, OverflowError, UnicodeError) as exc:
        raise ActionError('invalid_binding_encoding', 400) from exc


def location(scenario, attempt=None):
    if not isinstance(scenario, str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,79}', scenario):
        raise ActionError('invalid_scenario', 400)
    params = {'scenario': scenario, 'locate': '1'}
    if attempt is not None:
        if not isinstance(attempt, str) or not re.fullmatch(r'[a-f0-9]{32}', attempt):
            raise ActionError('invalid_attempt', 400)
        params['attempt'] = attempt
    return '/?' + urlencode(params)


@contextmanager
def directory(path):
    """Walk every component by fd, reject links, recheck the entire path on exit."""
    path = Path(path)
    if not path.is_absolute() or '..' in path.parts:
        raise ActionError('invalid_managed_root')
    fds = [os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)]
    try:
        for part in path.parts[1:]:
            fds.append(os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fds[-1]))
        yield fds[-1]
        for index, part in enumerate(path.parts[1:]):
            st = os.stat(part, dir_fd=fds[index], follow_symlinks=False)
            actual = os.fstat(fds[index + 1])
            if (st.st_dev, st.st_ino, st.st_mode) != (actual.st_dev, actual.st_ino, actual.st_mode):
                raise ActionError('managed_path_changed')
    except OSError as exc:
        raise ActionError('managed_file_unavailable', 410) from exc
    finally:
        for fd in reversed(fds): os.close(fd)


def _read_at(parent, name):
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
    try:
        first = os.fstat(fd)
        if not stat.S_ISREG(first.st_mode) or first.st_nlink != 1 or not 44 <= first.st_size <= LIMIT:
            raise ActionError('invalid_artifact')
        chunks = []; size = 0
        while size <= LIMIT:
            chunk = os.read(fd, min(8192, LIMIT + 1 - size))
            if not chunk: break
            chunks.append(chunk); size += len(chunk)
        last = os.fstat(fd); named = os.stat(name, dir_fd=parent, follow_symlinks=False)
        signature = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink, s.st_mode)
        if size != first.st_size or signature(first) != signature(last) or signature(last) != signature(named):
            raise ActionError('artifact_changed')
        return b''.join(chunks)
    finally:
        os.close(fd)


def read_tone(workspace):
    with directory(Path(workspace) / 'output') as fd:
        return _read_at(fd, 'tone.wav')


def inspect_tone(data):
    if not isinstance(data, bytes) or not 44 <= len(data) <= LIMIT:
        raise ActionError('invalid_wav_size')
    if (len(data) != 8044 or data[:4] != b'RIFF' or data[8:16] != b'WAVEfmt ' or data[36:40] != b'data'
            or struct.unpack('<I', data[4:8])[0] != len(data)-8 or struct.unpack('<I', data[16:20])[0] != 16
            or struct.unpack('<I', data[40:44])[0] != 8000):
        raise ActionError('wav_header_not_canonical')
    try:
        with wave.open(io.BytesIO(data), 'rb') as wav:
            params = (wav.getnchannels(), wav.getsampwidth(), wav.getframerate(), wav.getnframes())
            if params != (1, 2, 16000, 4000) or wav.getcomptype() != 'NONE':
                raise ActionError('wav_parameters_not_qualified')
            raw = wav.readframes(4001)
        if len(raw) != 8000: raise ActionError('wav_frames_incomplete')
        samples = struct.unpack('<4000h', raw)
        peak = max(abs(x) for x in samples)
        rms = round(math.sqrt(sum(x*x for x in samples) / 4000))
        hz = sum(1 for a, b in zip(samples, samples[1:]) if a <= 0 < b) / .25
        if not (7000 <= rms <= 9000 and peak <= 12100 and 435 <= hz <= 445):
            raise ActionError('wav_signal_not_qualified')
        return {'sha256': hashlib.sha256(data).hexdigest(), 'size': len(data),
                'channels': 1, 'sample_width_bytes': 2, 'sample_rate_hz': 16000,
                'frames': 4000, 'duration_seconds': .25, 'peak': peak, 'rms': rms, 'frequency_hz': hz}
    except (wave.Error, EOFError, struct.error) as exc:
        raise ActionError('invalid_wav') from exc


def attempt_revision(attempt):
    return digest({k: attempt.get(k) for k in ('id', 'scenario_id', 'scenario_version', 'scenario_hash', 'status', 'checks', 'inputs', 'view_events')})


def prepare(attempt, workspace, runtime_code):
    if attempt['status'] != 'active': raise ActionError('attempt_ended', 410)
    if attempt['scenario_id'] != SCENARIO: raise ActionError('artifact_not_supported', 400)
    checks = attempt.get('checks', [])
    if not checks or checks[-1].get('passed') is not True or checks[-1].get('status') != 'passed':
        raise ActionError('successful_check_required')
    check = checks[-1]
    if check.get('artifact_action_code') != CODE_VERSION or check.get('artifact_runtime_code') != runtime_code:
        raise ActionError('check_code_version_changed')
    artifact = inspect_tone(read_tone(workspace))
    if check.get('artifact_binding') != artifact: raise ActionError('artifact_changed_since_check')
    return {'action_version': ACTION_VERSION, 'permission_version': PERMISSION_VERSION,
            'code_version': CODE_VERSION, 'runtime_code_version': runtime_code,
            'scenario_id': SCENARIO, 'scenario_version': attempt['scenario_version'],
            'scenario_hash': attempt['scenario_hash'], 'attempt_id': attempt['id'],
            'attempt_revision': attempt_revision(attempt), 'check_id': check['operation_id'],
            'check_revision': digest(check), 'artifact': artifact}


def receipt_id(operation_id, binding):
    return digest({'operation_id': operation_id, 'binding': binding})


def store_export(root, identity, data):
    """Exclusive managed leaf; existing exact bytes recover uncertain outcome."""
    if not re.fullmatch('[a-f0-9]{64}', identity): raise ActionError('invalid_receipt', 400)
    with directory(root) as parent:
        try: os.mkdir('exports', 0o700, dir_fd=parent)
        except FileExistsError: pass
    with directory(Path(root) / 'exports') as parent:
        name = identity + '.wav'
        try: fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=parent)
        except FileExistsError:
            if _read_at(parent, name) != data: raise ActionError('export_outcome_uncertain')
            return
        try:
            view = memoryview(data)
            while view:
                count = os.write(fd, view)
                if count <= 0: raise ActionError('export_outcome_uncertain')
                view = view[count:]
            os.fsync(fd)
        finally: os.close(fd)
        if _read_at(parent, name) != data: raise ActionError('export_changed')
        os.fsync(parent)


def read_export(root, receipt):
    identity = receipt.get('receipt_id', '')
    if not re.fullmatch('[a-f0-9]{64}', identity): raise ActionError('invalid_receipt', 400)
    with directory(Path(root) / 'exports') as parent:
        data = _read_at(parent, identity + '.wav')
    if inspect_tone(data) != receipt['binding']['artifact']: raise ActionError('export_changed')
    return data
