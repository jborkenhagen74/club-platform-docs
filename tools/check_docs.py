#!/usr/bin/env python3
"""Check language parity, local Markdown links/anchors and documented baseline."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'docs-manifest.json').read_text(encoding='utf-8'))
errors = []
def slug(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    return re.sub(r'[^\w\- ]', '', text.lower()).replace(' ', '-')
def anchors(text):
    found = set(re.findall(r'<a\s+(?:id|name)=[\"\']([^\"\']+)', text))
    counts = {}
    for title in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', text, re.M):
        key = slug(title); n = counts.get(key, 0); counts[key] = n + 1
        found.add(key if n == 0 else f'{key}-{n}')
    return found
for language in manifest['languages']:
    for chapter in manifest['chapters']:
        path = ROOT / 'docs' / language / chapter
        if not path.is_file() or len(path.read_text(encoding='utf-8')) < 300:
            errors.append(f'Missing/incomplete chapter: {path.relative_to(ROOT)}')
count = 0
for path in ROOT.rglob('*.md'):
    if any(part in {'.git', 'build', 'node_modules'} for part in path.relative_to(ROOT).parts):
        continue
    count += 1
    text = path.read_text(encoding='utf-8')
    if len(re.findall(r'^```', text, re.M)) % 2:
        errors.append(f'Unclosed code fence: {path.relative_to(ROOT)}')
    plain = re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text, flags=re.M | re.S)
    for target in re.findall(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)', plain):
        url = urlsplit(target)
        if url.scheme or url.netloc:
            continue
        dest = (path.parent / unquote(url.path)).resolve() if url.path else path
        if not dest.is_relative_to(ROOT) or not dest.exists():
            errors.append(f'Broken link: {path.relative_to(ROOT)} -> {target}')
        elif url.fragment and dest.suffix == '.md' and unquote(url.fragment) not in anchors(dest.read_text(encoding='utf-8')):
            errors.append(f'Broken anchor: {path.relative_to(ROOT)} -> {target}')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f'OK: {count} Markdown files; {len(manifest["languages"])} languages × {len(manifest["chapters"])} chapters; local links and anchors.')
