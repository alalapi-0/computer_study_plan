#!/usr/bin/python3.12
"""Test source selector. The fixed canonical runtime guard remains authoritative.

Only --ui-test is supported. No installation, runtime edits, environment source
selector, arbitrary CLI root, or guard monkeypatch. Git commands here are read
only identity checks performed by the future test invocation, not by authors.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import shutil
import stat
import subprocess
import sys
import tempfile

ROOT = Path('/home/alalapi/Projects/computer-study-plan')
SOURCE = Path(__file__).absolute().parents[1]


def clean_environment():
    return {k: v for k, v in os.environ.items() if not k.startswith('GIT_') and k not in {'PYTHONPATH', 'PYTHONHOME', 'PYTHONSTARTUP', 'NODE_OPTIONS'}}


def load_guard():
    path = ROOT / 'scripts/linux_ui_runtime.py'
    if any(p.is_symlink() for p in [path, *path.parents]): raise RuntimeError('linked_guard')
    spec = importlib.util.spec_from_file_location('_canonical_csp_ui_guard', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if Path(module.__file__) != path: raise RuntimeError('guard_identity')
    return module


def validate_git_identity(guard, git):
    """Bind both directions of the registered worktree pointer, not just common-dir."""
    def absolute(raw):
        path = Path(raw)
        guard.require(path.is_absolute() and str(path) == raw and ".." not in path.parts, 'gitdir lexical escape')
        guard.path_guard(path, path)
        return path
    common = absolute(git(ROOT, 'rev-parse', '--path-format=absolute', '--git-common-dir'))
    guard.require(common == ROOT / '.git', 'canonical common directory drift')
    guard.require(absolute(git(ROOT, 'rev-parse', '--absolute-git-dir')) == common, 'canonical gitdir drift')
    guard.require(absolute(git(SOURCE, 'rev-parse', '--path-format=absolute', '--git-common-dir')) == common, 'foreign worktree')
    guard.require(absolute(git(SOURCE, 'rev-parse', '--show-toplevel')) == SOURCE, 'worktree root drift')
    gitdir = absolute(git(SOURCE, 'rev-parse', '--absolute-git-dir'))
    guard.require(gitdir.is_dir(), 'gitdir is not a real directory')
    entries = git(ROOT, 'worktree', 'list', '--porcelain', '-z').split('\0')
    guard.require('worktree ' + str(SOURCE) in entries, 'unregistered worktree')
    if SOURCE == ROOT:
        guard.require(gitdir == common, 'canonical gitdir drift')
    else:
        guard.require(gitdir.parent == common / 'worktrees' and gitdir.name not in ('', '.', '..'), 'outside registered gitdir')
        def pointer(path):
            guard.path_guard(path, path)
            fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
            try:
                info = os.fstat(fd)
                guard.require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and info.st_size <= 4096, 'invalid worktree pointer')
                raw = os.read(fd, 4097)
                after = os.fstat(fd)
                named = path.stat(follow_symlinks=False)
                identity = lambda value: (value.st_dev, value.st_ino, value.st_mode, value.st_size, value.st_mtime_ns, value.st_ctime_ns, value.st_nlink)
                guard.require(len(raw) == info.st_size and identity(info) == identity(after) == identity(named), 'worktree pointer changed')
                guard.path_guard(path, path)
                return raw.decode('utf-8', errors='strict').removesuffix('\n')
            finally: os.close(fd)
        guard.require(pointer(gitdir / 'gitdir') == str(SOURCE / '.git'), 'forged worktree backlink')
        guard.require(pointer(SOURCE / '.git') == 'gitdir: ' + str(gitdir), 'forged worktree pointer')
    return common, gitdir


def validate_source(guard):
    guard.path_guard(SOURCE, SOURCE)
    guard.require(Path(__file__).absolute() == SOURCE / 'scripts/worktree_ui_fixture.py', 'selector identity')
    guard.path_guard(Path(__file__).absolute(), Path(__file__).absolute())
    guard.require(not (SOURCE / '.venv-ui').exists() and not (SOURCE / '.venv-ui').is_symlink(), 'candidate local runtime refused')
    env = clean_environment()
    def git(root, *args):
        return subprocess.check_output(['/usr/bin/git', '-C', str(root), *args], env=env, text=True).strip()
    common, gitdir = validate_git_identity(guard, git)
    for relative in ('requirements-ui.txt', 'toolchains/linux-ui/requirements.lock'):
        path = SOURCE / relative
        guard.path_guard(path, path)
        guard.require(path.read_bytes() == (ROOT / relative).read_bytes(), 'candidate runtime lock drift')
    records = {}
    public = [SOURCE / name for name in ('index.html', 'practice_ui.js', 'practice_ui.css', 'progress.html', 'progress_ui.js', 'progress_ui.css', 'progress_data.js', 'rounds_data.js', 'vendor/xterm/xterm.js', 'vendor/xterm/xterm.css', 'requirements-ui.txt', 'toolchains/linux-ui/requirements.lock', 'tests/__init__.py', 'tests/ui/__init__.py')]
    public += sorted((SOURCE / 'tests/ui').glob('*.py'))
    public += [SOURCE / 'scripts/worktree_ui_fixture.py']
    for path in public:
        guard.path_guard(path, path)
        records[str(path.relative_to(SOURCE))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return {'source_root': str(SOURCE), 'common_dir': str(common), 'git_dir': str(gitdir), 'files': records,
            'source_fingerprint': hashlib.sha256(json.dumps(records, sort_keys=True).encode()).hexdigest()}


def command(guard):
    # Same isolation and mounts as canonical run_tests; only source bytes differ.
    return ['/usr/bin/bwrap', '--ro-bind', '/', '/', '--tmpfs', '/home/alalapi',
            '--dir', '/home/alalapi/Projects', '--ro-bind', str(SOURCE), str(ROOT),
            '--dir', str(guard.RUNTIME.parent), '--ro-bind', str(guard.RUNTIME), str(guard.RUNTIME),
            '--dir', str(guard.CACHE.parent), '--bind', str(guard.CACHE), str(guard.CACHE),
            '--dir', str(guard.TEMP.parent), '--bind', str(guard.TEMP), str(guard.TEMP),
            '--tmpfs', '/run', '--tmpfs', '/tmp', '--remount-ro', '/tmp',
            '--proc', '/proc', '--dev', '/dev', '--unshare-net', '--unshare-pid',
            '--die-with-parent', '--chdir', str(ROOT), str(guard.VENV / 'bin/python'),
            '-B', '-m', 'unittest', 'discover', '-s', 'tests/ui', '-p', 'test_*.py', '-t', '.', '-v']


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if args not in ([], ['--ui-test']): return 64
    if platform.system() == 'Darwin':
        return subprocess.run([str(SOURCE / 'scripts/external-ui-python'), '--ui-test']).returncode
    if platform.system() != 'Linux': return 78
    guard = load_guard()
    guard.ready(ROOT / 'scripts/external-ui-python')
    binding = validate_source(guard)
    temp = Path(tempfile.mkdtemp(prefix='ui-test.', dir=guard.TEMP))
    try:
        guard.ready(ROOT / 'scripts/external-ui-python')
        guard.require(Path('/usr/bin/bwrap').is_file() and not Path('/usr/bin/bwrap').is_symlink(), 'missing bwrap')
        env = guard.environment(temp)
        env = {k: v for k, v in env.items() if not k.startswith('GIT_')}
        print(json.dumps({'candidate_binding': binding}), flush=True)
        result = subprocess.run(command(guard), cwd=SOURCE, env=env)
        guard.ready(ROOT / 'scripts/external-ui-python')
        guard.require(validate_source(guard) == binding, 'candidate changed during tests')
        return result.returncode
    finally:
        guard.guard(ROOT / 'scripts/external-ui-python')
        guard.require(temp.parent == guard.TEMP and temp.name.startswith('ui-test.'), 'cleanup scope')
        guard.path_guard(temp, temp)
        shutil.rmtree(temp)


if __name__ == '__main__':
    if platform.system() == 'Linux' and (sys.version_info[:2] != (3, 12) or Path(sys.executable).resolve() != Path('/usr/bin/python3.12')):
        os.execve('/usr/bin/python3.12', ['/usr/bin/python3.12', '-B', str(Path(__file__).absolute()), *sys.argv[1:]], clean_environment())
    try: raise SystemExit(main())
    except (RuntimeError, OSError, subprocess.SubprocessError) as exc:
        print('candidate UI fixture refused: ' + str(exc), file=sys.stderr)
        raise SystemExit(78)
