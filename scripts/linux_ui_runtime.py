#!/usr/bin/python3.12
"""Fixed, fail-closed Linux runtime for the existing isolated UI fixture."""
from __future__ import annotations

import hashlib
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
ENTRY = ROOT / 'scripts/external-ui-python'
HELPER = ROOT / 'scripts/linux_ui_runtime.py'
PYTHON = Path('/usr/bin/python3.12')
UUID = '9d258b70-f313-4a5d-9cf6-c715c5edca3d'
RUNTIME = Path('/home/alalapi/Runtimes/computer-study-plan')
VENV = RUNTIME / 'ui-venv'
BROWSERS = RUNTIME / 'browsers'
CACHE = Path('/home/alalapi/Caches/computer-study-plan')
TEMP = Path('/home/alalapi/Temp/computer-study-plan')
MANIFEST = RUNTIME / 'linux-ui-manifest.json'
REQ = ROOT / 'requirements-ui.txt'
LOCK = ROOT / 'toolchains/linux-ui/requirements.lock'
REQ_SHA = '4f10b0c2863c9ad8acc6ff6b64b75a5b9c4200b4c12a8dbfcbc21c3031c5b32d'
ACTIONS = {'--bootstrap', '--check', '--ui-test', '--self-test'}


class Refusal(RuntimeError):
    pass


def require(condition, reason):
    if not condition:
        raise Refusal(reason)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_guard(path, expected, *, filesystem='ext4', uuid=UUID, owner=None):
    path, expected = Path(path), Path(expected)
    require(str(path) == str(expected) and '..' not in path.parts, '规范路径或映射漂移')
    for component in [path, *path.parents]:
        require(not component.is_symlink(), '路径包含符号链接')
    require(path.exists() and path.resolve(strict=True) == expected, '路径缺失或物理身份漂移')
    require(path.stat().st_uid == (os.getuid() if owner is None else owner), '目标所有者不符')
    value = subprocess.check_output(['/usr/bin/findmnt', '-n', '-o', 'FSTYPE,UUID', '-T', str(path)], text=True).split()
    require(value == [filesystem, uuid], '文件系统或 UUID 不符')


def guard(entry):
    require(platform.system() == 'Linux', '仅支持 Linux')
    require('..' not in str(entry).split('/') and '//' not in str(entry), '入口词法路径越界')
    invoked = Path(os.path.abspath(entry))
    require(invoked == ENTRY and Path(__file__).absolute() == HELPER, '入口来源校验失败')
    for path in [ROOT, ENTRY, HELPER, REQ, LOCK, RUNTIME, CACHE, TEMP]:
        path_guard(path, path)
    require(ROOT.is_dir() and all(p.is_dir() for p in [RUNTIME, CACHE, TEMP]), '目标不是目录')
    require(digest(REQ) == REQ_SHA, 'requirements-ui.txt 漂移')
    require(sys.version_info[:2] == (3, 12) and Path(sys.executable).resolve() == PYTHON, '固定 Python 身份不符')
    require(not (ROOT / '.venv-ui').exists() and not (ROOT / '.venv-ui').is_symlink(), '拒绝仓内 UI 环境')
    for name in ['PLAYWRIGHT_DOWNLOAD_HOST', 'PLAYWRIGHT_CHROMIUM_DOWNLOAD_HOST', 'NODE_OPTIONS']:
        require(not os.environ.get(name), '拒绝下载来源或 Node 执行覆盖')
    require(os.environ.get('PLAYWRIGHT_BROWSERS_PATH', str(BROWSERS)) == str(BROWSERS), '浏览器映射漂移')


def environment(temp=TEMP):
    env = dict(os.environ)
    for key in ['PYTHONPATH', 'PYTHONHOME', 'PYTHONSTARTUP', 'NODE_OPTIONS']:
        env.pop(key, None)
    env.update(PYTHONDONTWRITEBYTECODE='1', PYTHONNOUSERSITE='1',
               PLAYWRIGHT_BROWSERS_PATH=str(BROWSERS), TMPDIR=str(temp),
               XDG_CONFIG_HOME=str(CACHE / 'config'), XDG_CACHE_HOME=str(CACHE / 'xdg'),
               PIP_CACHE_DIR=str(CACHE / 'pip'), PIP_DISABLE_PIP_VERSION_CHECK='1',
               GIT_OPTIONAL_LOCKS='0')
    return env


def tree(root):
    result = {}
    for p in sorted(root.rglob('*')):
        s = p.lstat()
        item = dict(mode=stat.S_IMODE(s.st_mode), uid=s.st_uid, bytes=s.st_size, nlink=s.st_nlink)
        if stat.S_ISLNK(s.st_mode):
            item.update(type='link', target=os.readlink(p))
        elif stat.S_ISREG(s.st_mode):
            item.update(type='file', bytes=s.st_size, sha256=digest(p), nlink=s.st_nlink)
        elif stat.S_ISDIR(s.st_mode):
            item.update(type='directory')
        else:
            raise Refusal('运行时包含特殊文件')
        result[str(p.relative_to(root))] = item
    return result


def identity():
    code = "import importlib.metadata as m,json,site,sys;print(json.dumps(dict(executable=sys.executable,prefix=sys.prefix,version=sys.version,sites=site.getsitepackages(),packages=sorted((d.metadata['Name'],d.version) for d in m.distributions()))))"
    result = subprocess.check_output([str(VENV / 'bin/python'), '-I', '-B', '-c', code], env=environment(), text=True)
    data = json.loads(result)
    require(data['prefix'] == str(VENV) and data['executable'] == str(VENV / 'bin/python'), '运行时 prefix/executable 不符')
    require(dict(data['packages']).get('playwright') == '1.60.0', 'Playwright 版本不符')
    require(all(str(VENV) in site for site in data['sites']), 'site-packages 越界')
    return data


def ready(entry):
    guard(entry)
    for p in [VENV, BROWSERS, MANIFEST]:
        path_guard(p, p)
    require(VENV.is_dir() and BROWSERS.is_dir() and MANIFEST.is_file(), '缺少运行时证据')
    require((VENV / 'bin/python').resolve(strict=True) == PYTHON, '运行时基础 Python 漂移')
    data = json.loads(MANIFEST.read_text())
    require(set(data) == {'version', 'python_sha256', 'requirements_sha256', 'lock_sha256', 'identity', 'runtime_tree', 'browser_tree', 'browser_descriptor', 'provenance_sha256'}, 'manifest 字段漂移')
    require(data['version'] == 1 and data['python_sha256'] == digest(PYTHON), '基础 Python 漂移')
    require(data['requirements_sha256'] == REQ_SHA and data['lock_sha256'] == digest(LOCK), '依赖锁漂移')
    for name, expected in data['provenance_sha256'].items():
        require(name in {'pip-install-report.json', 'browser-download-descriptors.txt'}, '来源文件越界')
        path_guard(RUNTIME / name, RUNTIME / name)
        require(digest(RUNTIME / name) == expected, '安装来源元数据漂移')
    require(set(data['provenance_sha256']) == {'pip-install-report.json', 'browser-download-descriptors.txt'}, '缺少安装来源')
    # Verify package bytes before importing anything from the isolated runtime.
    require(data['runtime_tree'] == tree(VENV), '完整运行时树漂移')
    require(data['browser_tree'] == tree(BROWSERS), '完整浏览器树漂移')
    descriptor = VENV / 'lib/python3.12/site-packages/playwright/driver/package/browsers.json'
    require(data['browser_descriptor'] == json.loads(descriptor.read_text()), '官方浏览器描述漂移')
    require(data['identity'] == identity(), '运行时身份漂移')
    executable = BROWSERS / 'chromium_headless_shell-1223/chrome-headless-shell-linux64/chrome-headless-shell'
    path_guard(executable, executable)
    require(os.access(executable, os.X_OK), '固定浏览器不可执行')
    return data


def bootstrap(entry):
    guard(entry)
    require(all(not p.exists() and not p.is_symlink() for p in [VENV, BROWSERS, MANIFEST]), '运行时目标冲突，拒绝覆盖')
    subprocess.run([str(PYTHON), '-m', 'venv', str(VENV)], env=environment(), check=True)
    guard(entry)
    subprocess.run([str(VENV / 'bin/python'), '-I', '-m', 'pip', '--isolated', '--disable-pip-version-check', '--no-input',
                    'install', '--index-url', 'https://pypi.org/simple', '--cache-dir', str(CACHE / 'pip'),
                    '--require-hashes', '--report', str(RUNTIME / 'pip-install-report.json'), '-r', str(LOCK)], env=environment(), check=True)
    guard(entry)
    descriptor = subprocess.check_output([str(VENV / 'bin/python'), '-I', '-m', 'playwright', 'install', '--dry-run', '--only-shell', 'chromium'], env=environment(), text=True)
    require('chromium-headless-shell v1223' in descriptor and 'https://cdn.playwright.dev/' in descriptor, '官方浏览器描述不符')
    guard(entry)
    (RUNTIME / 'browser-download-descriptors.txt').write_text(descriptor)
    subprocess.run([str(VENV / 'bin/python'), '-I', '-m', 'playwright', 'install', '--only-shell', 'chromium'], env=environment(), check=True)
    guard(entry)
    descriptor = VENV / 'lib/python3.12/site-packages/playwright/driver/package/browsers.json'
    data = dict(version=1, python_sha256=digest(PYTHON), requirements_sha256=REQ_SHA,
                lock_sha256=digest(LOCK), identity=identity(), runtime_tree=tree(VENV),
                browser_tree=tree(BROWSERS), browser_descriptor=json.loads(descriptor.read_text()),
                provenance_sha256={name: digest(RUNTIME / name) for name in ['pip-install-report.json', 'browser-download-descriptors.txt']})
    guard(entry)
    with MANIFEST.open('x') as output:
        json.dump(data, output, ensure_ascii=False, indent=2)
        output.write('\n')
    ready(entry)


def run_tests(entry):
    ready(entry)
    guard(entry)
    temp = Path(tempfile.mkdtemp(prefix='ui-test.', dir=TEMP))
    try:
        ready(entry)
        require(Path('/usr/bin/bwrap').is_file() and not Path('/usr/bin/bwrap').is_symlink(), '缺少固定 Linux 隔离工具')
        command = ['/usr/bin/bwrap', '--ro-bind', '/', '/', '--tmpfs', '/home/alalapi',
                   '--dir', '/home/alalapi/Projects', '--ro-bind', str(ROOT), str(ROOT),
                   '--dir', str(RUNTIME.parent), '--ro-bind', str(RUNTIME), str(RUNTIME),
                   '--dir', str(CACHE.parent), '--bind', str(CACHE), str(CACHE),
                   '--dir', str(TEMP.parent), '--bind', str(TEMP), str(TEMP),
                   '--tmpfs', '/run', '--tmpfs', '/tmp', '--remount-ro', '/tmp',
                   '--proc', '/proc', '--dev', '/dev', '--unshare-net', '--unshare-pid',
                   '--die-with-parent', '--chdir', str(ROOT),
                   str(VENV / 'bin/python'), '-B', '-m', 'unittest', 'discover',
                   '-s', 'tests/ui', '-p', 'test_*.py', '-t', '.', '-v']
        result = subprocess.run(command, cwd=ROOT, env=environment(temp))
        ready(entry)
        return result.returncode
    finally:
        guard(entry)
        require(temp.parent == TEMP and temp.name.startswith('ui-test.'), '清理目标越界')
        path_guard(temp, temp)
        shutil.rmtree(temp)


def self_test(entry):
    ready(entry)
    checks = []
    def refuses(name, function):
        try:
            function()
        except (Refusal, FileNotFoundError):
            checks.append(name)
            return
        raise Refusal('负向检查未拒绝: ' + name)
    refuses('wrong-uuid', lambda: path_guard(ROOT, ROOT, uuid='00000000-0000-0000-0000-000000000000'))
    refuses('wrong-filesystem', lambda: path_guard(ROOT, ROOT, filesystem='apfs'))
    refuses('wrong-owner', lambda: path_guard(ROOT, ROOT, owner=os.getuid() + 1))
    refuses('mapping-escape', lambda: path_guard(CACHE, TEMP))
    refuses('lexical-escape', lambda: guard(str(ROOT / 'scripts/../scripts/external-ui-python')))
    refuses('bootstrap-collision', lambda: bootstrap(entry))
    guard(entry)
    temp = Path(tempfile.mkdtemp(prefix='guard-test.', dir=TEMP))
    try:
        shutil.copyfile(ENTRY, temp / 'copied-wrapper')
        (temp / 'copied-wrapper').chmod(0o700)
        (temp / 'linked-wrapper').symlink_to(ENTRY)
        (temp / 'project-link').symlink_to(ROOT)
        for name, script, action, expected in [
            ('copied-entry', temp / 'copied-wrapper', '--check', 78),
            ('symlink-entry', temp / 'linked-wrapper', '--check', 78),
            ('parent-symlink', temp / 'project-link/scripts/external-ui-python', '--check', 78),
            ('unknown-action', ENTRY, '--unknown', 64),
        ]:
            result = subprocess.run([str(script), action], env=environment(), capture_output=True)
            require(result.returncode == expected, '负向命令返回不符: ' + name)
            checks.append(name)
        for args in [[], ['--check', 'extra']]:
            result = subprocess.run([str(ENTRY), *args], env=environment(), capture_output=True)
            require(result.returncode == 64, '固定动作参数未拒绝')
            checks.append('usage-' + str(len(args)))
        refuses('target-symlink', lambda: path_guard(temp / 'project-link', temp / 'project-link'))
        refuses('wrong-repository', lambda: guard(str(TEMP / 'external-ui-python')))
        for name, overrides in [
            ('browser-path-override', {'PLAYWRIGHT_BROWSERS_PATH': str(TEMP)}),
            ('download-host-override', {'PLAYWRIGHT_DOWNLOAD_HOST': 'https://invalid.example'}),
            ('node-options-override', {'NODE_OPTIONS': '--require=invalid'}),
        ]:
            env = environment()
            env.update(overrides)
            result = subprocess.run([str(ENTRY), '--check'], env=env, capture_output=True)
            require(result.returncode == 78, '执行或来源覆盖未拒绝: ' + name)
            checks.append(name)
        binary = temp / 'bin'
        guard(entry)
        binary.mkdir()
        fake = binary / 'uname'
        for platform_name, label in [('unsupported', 'unsupported-platform'), ('Darwin', 'darwin-dispatch')]:
            guard(entry)
            fake.write_text('#!/bin/sh\nprintf "%s\\n" "' + platform_name + '"\n')
            fake.chmod(0o700)
            env = environment()
            env['PATH'] = str(binary) + ':' + env.get('PATH', '/usr/bin:/bin')
            result = subprocess.run([str(ENTRY), '--check'], env=env, capture_output=True)
            require(result.returncode == 78, '平台分支未拒绝: ' + label)
            if platform_name == 'Darwin':
                require('入口来源校验失败'.encode() in result.stderr, '未抵达原 Mac guard')
                # A missing adjacent Mac body must not become an empty successful zsh command.
                copied = temp / 'copied-wrapper'
                result = subprocess.run([str(copied), '--check'], env=env, capture_output=True)
                require(result.returncode == 78 and 'Mac 入口正文缺失或不可读'.encode() in result.stderr,
                        'Darwin 复制入口缺少正文未拒绝')
                checks.append('darwin-copied-missing-body')
                guard(entry)
                shutil.copyfile(ROOT / 'scripts/external-ui-python-macos', temp / 'external-ui-python-macos')
                result = subprocess.run([str(copied), '--check'], env=env, capture_output=True)
                require(result.returncode == 78 and '入口来源校验失败'.encode() in result.stderr,
                        'Darwin 复制入口未抵达原来源守卫')
                checks.append('darwin-copied-with-body')
            checks.append(label)
        # Task-owned sealed runtime only; restore exact bytes even if refusal fails.
        original = MANIFEST.read_bytes()
        try:
            guard(entry)
            MANIFEST.write_text('{}')
            refuses('manifest-tamper', lambda: ready(entry))
        finally:
            guard(entry)
            MANIFEST.write_bytes(original)
        guard(entry)
        missing = temp / 'manifest.saved'
        try:
            MANIFEST.rename(missing)
            refuses('missing-manifest', lambda: ready(entry))
        finally:
            guard(entry)
            missing.rename(MANIFEST)
        executable = BROWSERS / 'chromium_headless_shell-1223/chrome-headless-shell-linux64/chrome-headless-shell'
        guard(entry)
        with executable.open('rb') as stream:
            first = stream.read(16)
        try:
            guard(entry)
            with executable.open('r+b') as stream:
                stream.write(b'X' + first[1:])
            refuses('browser-executable-tamper', lambda: ready(entry))
        finally:
            guard(entry)
            with executable.open('r+b') as stream:
                stream.write(first)
        extra = VENV / 'unexpected-runtime-file'
        try:
            guard(entry)
            with extra.open('x') as stream:
                stream.write('task-owned guard fixture')
            refuses('runtime-tree-tamper', lambda: ready(entry))
        finally:
            guard(entry)
            extra.unlink()
        ready(entry)
        print(json.dumps({'self_test': 'PASS', 'checks': checks}, ensure_ascii=False))
    finally:
        guard(entry)
        path_guard(temp, temp)
        shutil.rmtree(temp)


def main():
    if len(sys.argv) != 3 or sys.argv[2] not in ACTIONS:
        print('用法: scripts/external-ui-python {--bootstrap|--check|--ui-test|--self-test}', file=sys.stderr)
        return 64
    entry, action = sys.argv[1:]
    try:
        if action == '--bootstrap':
            bootstrap(entry)
        elif action == '--ui-test':
            return run_tests(entry)
        elif action == '--self-test':
            self_test(entry)
        else:
            ready(entry)
            print('external-ui-python: Linux Python3.12/Playwright1.60/Chromium1223 OK')
        return 0
    except (Refusal, OSError, ValueError, subprocess.SubprocessError) as error:
        print('外置 UI Python 保护: ' + str(error), file=sys.stderr)
        return 78


if __name__ == '__main__':
    raise SystemExit(main())
