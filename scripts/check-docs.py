"""Validate public JSON contracts, catalogue parity and relative Markdown links."""
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
for path in root.rglob('*.json'):
    if '.git' not in path.parts:
        json.loads(path.read_text(encoding='utf-8'))
catalogue = json.loads((root/'docs/reference/placeholders.json').read_text(encoding='utf-8'))['placeholders']
keys = [p['key'] for p in catalogue]
assert len(keys) == len(set(keys)) == 70
for locale in ('de', 'en', 'fr', 'es', 'ko'):
    folder = root/'docs'/locale
    for name in ('handbook.md', 'operations.md', 'placeholders.md', 'formulare.md'):
        assert (folder/name).is_file(), (locale, name)
    text = (folder/'placeholders.md').read_text(encoding='utf-8')
    actual = re.findall(r'^\| `\{\{([^}]+)\}\}` \|', text, re.M)
    assert set(actual) == set(keys) and len(actual) == len(keys), locale
for path in root.rglob('*.md'):
    if '.git' in path.parts:
        continue
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
        if ':' in target or target.startswith('#'):
            continue
        assert (path.parent/target.split('#')[0]).exists(), (path, target)
print('Public docs: JSON, five handbook sets, 70 placeholders and relative links valid')
