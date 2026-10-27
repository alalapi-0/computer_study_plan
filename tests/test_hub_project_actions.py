"""Finite WAV actions; synthetic bytes and owned temporary roots only."""
import copy
import hashlib
import io
import math
import os
import re
from pathlib import Path
import struct
import tempfile
import time
import unittest
import wave
from unittest.mock import patch
from scripts import hub_project_actions as actions


def tone():
    stream = io.BytesIO()
    with wave.open(stream, 'wb') as wav:
        wav.setparams((1, 2, 16000, 4000, 'NONE', 'not compressed'))
        wav.writeframes(struct.pack('<4000h', *(round(12000*math.sin(2*math.pi*440*i/16000)) for i in range(4000))))
    return stream.getvalue()


class WavActionsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.work = self.root / 'workspace'; (self.work / 'output').mkdir(parents=True)
        self.path = self.work / 'output/tone.wav'; self.path.write_bytes(tone())
        artifact = actions.inspect_tone(tone())
        self.attempt = dict(id='a'*32, scenario_id=actions.SCENARIO, scenario_version=1,
                            scenario_hash='b'*64, status='active', checks=[dict(status='passed', passed=True,
                            operation_id='check-1', artifact_binding=artifact, artifact_action_code=actions.CODE_VERSION,
                            artifact_runtime_code='c'*64)], inputs=[], view_events=[])

    def test_exact_wav_binding_and_immutable_export_recovery(self):
        binding = actions.prepare(self.attempt, self.work, 'c'*64)
        self.assertEqual(binding['artifact']['frames'], 4000)
        identity = actions.receipt_id('export-1', binding)
        actions.store_export(self.root, identity, tone())
        before = (self.root / 'exports' / (identity+'.wav')).stat()
        actions.store_export(self.root, identity, tone())
        after = (self.root / 'exports' / (identity+'.wav')).stat()
        self.assertEqual((before.st_ino, before.st_mtime_ns), (after.st_ino, after.st_mtime_ns))
        self.assertEqual(actions.read_export(self.root, dict(receipt_id=identity, binding=binding)), tone())
        self.assertNotEqual(actions.receipt_id('export-2', binding), identity)

    def test_stale_check_code_content_and_ended_attempt(self):
        self.attempt['checks'][-1]['artifact_binding']['sha256'] = '0'*64
        with self.assertRaisesRegex(actions.ActionError, 'changed_since_check'): actions.prepare(self.attempt, self.work, 'c'*64)
        self.attempt['checks'][-1]['artifact_action_code'] = '0'*64
        with self.assertRaisesRegex(actions.ActionError, 'code_version'): actions.prepare(self.attempt, self.work, 'c'*64)
        self.attempt['status'] = 'stopped'
        with self.assertRaises(actions.ActionError) as caught: actions.prepare(self.attempt, self.work, 'c'*64)
        self.assertEqual(caught.exception.status, 410)

    def test_links_hardlinks_parent_escape_and_oversize(self):
        self.path.unlink(); self.path.symlink_to(self.root / 'outside')
        with self.assertRaises(actions.ActionError): actions.read_tone(self.work)
        self.path.unlink(); self.path.write_bytes(tone()); os.link(self.path, self.root / 'linked')
        with self.assertRaises(actions.ActionError): actions.read_tone(self.work)
        (self.root / 'linked').unlink(); self.path.write_bytes(b'x'*64001)
        with self.assertRaises(actions.ActionError): actions.read_tone(self.work)
        with self.assertRaises(actions.ActionError): actions.read_tone(self.work / '..')
        (self.root / 'alias').symlink_to(self.work, target_is_directory=True)
        with self.assertRaises(actions.ActionError): actions.read_tone(self.root / 'alias')

    def test_export_destination_links_unknown_reference_and_wrong_signal(self):
        (self.root/'exports').symlink_to(self.work, target_is_directory=True)
        with self.assertRaises(actions.ActionError): actions.store_export(self.root, 'd'*64, tone())
        with self.assertRaises(actions.ActionError): actions.read_export(self.root, {'receipt_id': '../outside'})
        with self.assertRaises(actions.ActionError): actions.inspect_tone(b'not a WAV'*8)
        self.assertNotIn(str(self.root), str(actions.prepare(self.attempt, self.work, 'c'*64)))

    def test_read_race_and_trailing_private_bytes_are_rejected(self):
        with self.assertRaises(actions.ActionError): actions.inspect_tone(tone()+b'private trailer')
        original = os.read; changed = False
        def racing(fd, size):
            nonlocal changed
            result = original(fd, size)
            if not changed:
                changed = True
                self.path.write_bytes(tone()+b'x')
            return result
        with patch.object(actions.os, 'read', side_effect=racing):
            with self.assertRaisesRegex(actions.ActionError, 'changed'): actions.read_tone(self.work)

    def test_export_canonical_numbers_remain_type_safe_and_bounded(self):
        binding = actions.prepare(self.attempt, self.work, 'c'*64)
        js = copy.deepcopy(binding); js['artifact']['frequency_hz'] = 440
        self.assertEqual(actions.canonical_export_binding(binding), actions.canonical_export_binding(js))
        self.assertIn('"duration_seconds":0.25', actions.canonical_export_binding(binding))
        fractional = copy.deepcopy(binding); fractional['artifact']['frequency_hz'] = 440.125
        self.assertIn('"frequency_hz":440.125', actions.canonical_export_binding(fractional))
        boolean = copy.deepcopy(binding); boolean['artifact']['channels'] = True
        self.assertIn('"channels":true', actions.canonical_export_binding(boolean))
        self.assertNotEqual(actions.canonical_export_binding(boolean), actions.canonical_export_binding(binding))
        for value in (float('nan'), float('inf'), float('-inf')):
            invalid = copy.deepcopy(binding); invalid['artifact']['frequency_hz'] = value
            with self.assertRaises(actions.ActionError): actions.canonical_export_binding(invalid)
        for invalid in ([], {**binding, 'extra': 1}, {**binding, 'artifact': []}, {**binding, 'check_id': 'x'*8193}):
            with self.assertRaises(actions.ActionError): actions.canonical_export_binding(invalid)
        missing = copy.deepcopy(binding); del missing['artifact']['frames']
        with self.assertRaises(actions.ActionError): actions.canonical_export_binding(missing)

    def test_location_is_finite_and_nonexecuting(self):
        self.assertIn('locate=1', actions.location(actions.SCENARIO, 'a'*32))
        for name in ('../private', '/absolute', 'x;pwd'):
            with self.assertRaises(actions.ActionError): actions.location(name)


class NativeWavActionsTest(unittest.TestCase):
    def input_until(self, manager, attempt, command, operation, marker):
        cursor = manager.snapshot(attempt)["cursor"]
        manager.input(attempt, command + "\n", operation)
        deadline = time.monotonic() + 8
        output = ""
        while time.monotonic() < deadline:
            snapshot = manager.snapshot(attempt, cursor=cursor)
            self.assertEqual(snapshot["attempt"]["status"], "active")
            output += snapshot["output"]; cursor = snapshot["cursor"]
            # Bash brackets PTY output with CSI controls (including ?2004l).
            # Normalize accumulated text so controls split across reads are handled.
            # Match only a whole newline-terminated line, never a command echo
            # containing the marker or an incomplete final output fragment.
            normalized = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", output).replace("\r", "")
            if marker in normalized.split("\n")[:-1]: return
            time.sleep(.05)
        self.fail("learner PTY did not produce the bounded completion marker")

    def test_real_check_export_replay_reset_and_restart(self):
        from scripts.lab_runtime import LabManager
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temporary:
            state = Path(temporary) / 'state'
            manager = LabManager(root / 'content/scenarios', state)
            try:
                self.assertTrue(manager.capabilities()['available'])
                first = manager.start(actions.SCENARIO, 'wav-start')['attempt']['id']
                self.assertFalse(manager.check(first, 'wav-initial')['attempt']['checks'][-1]['passed'])
                self.input_until(manager, first, "sed -i 's/RATE = 8000/RATE = 16000/; s/AMPLITUDE = 32767/AMPLITUDE = 12000/' app/generate_tone.py && python3 app/generate_tone.py", 'wav-repair', 'wrote 4000 frames at 16000 Hz')
                checked = manager.check(first, 'wav-check')['attempt']['checks'][-1]
                self.assertTrue(checked['passed']); self.assertIn('artifact_binding', checked)
                binding = manager.prepare_wav(first)
                self.assertIs(type(binding['artifact']['frequency_hz']), float)
                js_binding = copy.deepcopy(binding)
                js_binding['artifact']['frequency_hz'] = int(js_binding['artifact']['frequency_hz'])
                # Browser JSON.stringify turns 440.0 into 440. Persist that first,
                # then replay the original Python-shaped binding and receipt.
                receipt = manager.export_wav(first, 'wav-export', js_binding)
                self.assertEqual(manager.export_wav(first, 'wav-export', js_binding), receipt)
                self.assertEqual(manager.export_wav(first, 'wav-export', binding), receipt)
                self.assertEqual(hashlib.sha256(manager.download_wav(receipt['receipt_id'])).hexdigest(), binding['artifact']['sha256'])
                changed = copy.deepcopy(binding); changed['scenario_version'] += 1
                with self.assertRaisesRegex(actions.ActionError, 'conflict'):
                    manager.export_wav(first, 'wav-export', changed)
                for key, value in (('frequency_hz', 441), ('channels', True), ('size', float('nan')),
                                   ('frequency_hz', float('inf')), ('frequency_hz', float('-inf'))):
                    bad = copy.deepcopy(binding); bad['artifact'][key] = value
                    for operation in ('wav-export', 'wav-invalid-' + key):
                        with self.subTest(key=key, value=value, operation=operation):
                            with self.assertRaises(actions.ActionError): manager.export_wav(first, operation, bad)
                for key, value in (('scenario_version', True), ('code_version', '0'*64),
                                   ('permission_version', 'different'), ('action_version', 'different')):
                    bad = copy.deepcopy(binding); bad[key] = value
                    with self.assertRaises(actions.ActionError): manager.export_wav(first, 'wav-export', bad)
                    with self.assertRaises(actions.ActionError): manager.export_wav(first, 'wav-invalid-version', bad)
                for bad in ({**binding, 'extra': 1}, {**binding, 'artifact': None}):
                    with self.assertRaises(actions.ActionError): manager.export_wav(first, 'wav-export', bad)
                self.assertEqual(len(list((state/'exports').glob('*.wav'))), 1)
                self.input_until(manager, first, "printf changed > output/tone.wav && printf 'WAV_TAMPER_%s\\n' COMPLETE", 'wav-change', 'WAV_TAMPER_COMPLETE')
                with self.assertRaises(actions.ActionError): manager.export_wav(first, 'wav-stale', binding)
                manager.reset(first, 'wav-reset')
                with self.assertRaises(actions.ActionError): manager.download_wav(receipt['receipt_id'])
                self.assertTrue((state/'exports'/(receipt['receipt_id']+'.wav')).is_file())
            finally: manager.close()
            restarted = LabManager(root/'content/scenarios', state)
            try:
                self.assertEqual(restarted.export_wav(first, 'wav-export', binding), receipt)
                self.assertEqual(restarted.export_wav(first, 'wav-export', js_binding), receipt)
                self.assertEqual(len(list((state/'exports').glob('*.wav'))), 1)
            finally: restarted.close()


if __name__ == '__main__': unittest.main()
