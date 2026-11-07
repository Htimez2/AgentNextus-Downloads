import hashlib
import json
import os
import pathlib
import re
import shutil
import urllib.parse
import urllib.request
import zipfile

tag = os.environ['RELEASE_TAG']
if not re.fullmatch(r'v\d+\.\d+\.\d+-preview\.\d+', tag):
    raise SystemExit('Only preview tags are accepted')
urls = json.loads(os.environ['SOURCE_ARTIFACTS'])
if len(urls) != 4:
    raise SystemExit('Exactly four verified platform artifacts are required')
out = pathlib.Path('transfer')
out.mkdir(exist_ok=True)
hashes = {}
for index, url in enumerate(urls):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != 'https' or not parsed.hostname.endswith('.blob.core.windows.net'):
        raise SystemExit('Only GitHub artifact storage URLs are accepted')
    print('::add-mask::' + url, flush=True)
    archive = out / f'artifact-{index}.zip'
    try:
        with urllib.request.urlopen(url, timeout=120) as source, archive.open('wb') as target:
            shutil.copyfileobj(source, target)
    except Exception:
        raise SystemExit('Artifact download failed; refresh the temporary artifact links')
    with zipfile.ZipFile(archive) as source:
        receipt = source.read('SHA256SUMS.txt').decode('utf-8')
        expected = {}
        for line in receipt.splitlines():
            match = re.fullmatch(r'([a-f0-9]{64})  (Agent-Nextus-[\w.-]+\.(?:exe|dmg|zip|AppImage|deb))', line)
            if not match:
                raise SystemExit('Invalid native checksum receipt')
            expected[match[2]] = match[1]
        for name, digest in expected.items():
            if not name.startswith('Agent-Nextus-' + tag[1:] + '-') or pathlib.PurePosixPath(name).name != name:
                raise SystemExit('Artifact does not match this preview version')
            entry = source.getinfo(name)
            if not 1000000 < entry.file_size < 2000000000:
                raise SystemExit('Unexpected package size')
            target = out / name
            with source.open(entry) as src, target.open('wb') as dst:
                shutil.copyfileobj(src, dst)
            actual = hashlib.sha256()
            with target.open('rb') as data:
                for chunk in iter(lambda: data.read(1024 * 1024), b''):
                    actual.update(chunk)
            if actual.hexdigest() != digest:
                raise SystemExit('Package checksum mismatch')
            if name in hashes and hashes[name] != digest:
                raise SystemExit('Conflicting package receipts')
            hashes[name] = digest
            print(f'Verified {name} ({entry.file_size} bytes)', flush=True)
    archive.unlink()

version = tag[1:]
prefix = f'https://github.com/Htimez2/AgentNextus-Downloads/releases/download/{tag}/'
buttons = [
    ('windows-x64', 'Windows · x64', f'Agent-Nextus-{version}-win-x64.exe'),
    ('mac-arm64', 'macOS · Apple Silicon', f'Agent-Nextus-{version}-mac-arm64.dmg'),
    ('mac-x64', 'macOS · Intel', f'Agent-Nextus-{version}-mac-x64.dmg'),
    ('linux-appimage', 'Linux · AppImage', f'Agent-Nextus-{version}-linux-x86_64.AppImage'),
    ('linux-deb', 'Linux · DEB', f'Agent-Nextus-{version}-linux-amd64.deb'),
]
for _, _, name in buttons:
    if name not in hashes:
        raise SystemExit('A required verified platform package is missing')
manifest = {
    'version': version,
    'releaseUrl': f'https://github.com/Htimez2/AgentNextus-Downloads/releases/tag/{tag}',
    'checksumsUrl': prefix + 'SHA256SUMS.txt',
    'files': [{'id': ident, 'label': label, 'url': prefix + name, 'sha256': hashes[name], 'bytes': (out / name).stat().st_size} for ident, label, name in buttons],
}
(out / 'download-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
(out / 'SHA256SUMS.txt').write_text(''.join(f'{digest}  {name}\n' for name, digest in sorted(hashes.items())))
(out / 'release-files.txt').write_text(''.join(str(out / name) + '\n' for name in sorted(hashes)))
print(f'All {len(hashes)} packages verified; upload list contains binaries only.', flush=True)
