#!/usr/bin/env python3
"""Validate OpenAPI and important wire-format compatibility invariants."""
from pathlib import Path
import re
import yaml
from openapi_spec_validator import validate
root = Path(__file__).resolve().parents[1]
spec = yaml.safe_load((root / 'openapi/club-platform.yaml').read_text(encoding='utf-8'))
validate(spec)
paths = spec['paths']; schemas = spec['components']['schemas']
assert spec['info']['version'] == '0.6.0'
assert sum(len(p) for p in paths.values()) == 31
assert schemas['Revision']['type'] == 'string'
assert schemas['StringValues']['additionalProperties']['type'] == 'string'
assert paths['/api/v1/roles/permission']['post']['requestBody']['content']['application/json']['schema']['properties']['enabled']['type'] == 'boolean'
assert 'next_cursor' not in schemas['AssetPage']['properties']
assert paths['/api/v1/branding']['get']['security'] == []
assert paths['/api/v1/auth/login']['post']['security'] == []
assert all(path == '/health' or path.startswith('/api/v1/') for path in paths)
# Example manifest must agree with the documented native ABI and resource namespace.
source = (root / 'examples/extensions/hello-extension/hello_extension.cpp').read_text()
import json
manifest = json.loads(re.search(r'R"\((.*?)\)"', source, re.S).group(1))
assert manifest['id'] == 'attendance'
assert manifest['types'][0]['key'] == 'attendance.session'
assert [field['type'] for field in manifest['types'][0]['fields']] == ['date', 'text']
print('OK: OpenAPI 3.1, 31 operations, wire types and example manifest.')
