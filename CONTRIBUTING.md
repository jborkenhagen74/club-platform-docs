# Maintaining this documentation

This repository documents the public contracts and user-visible behaviour of Club
Platform. The implementation stays in its separate private repository. Never copy
private Core implementation, credentials, production records or CI secrets here.
Public ABI headers and independently written integration examples belong here.

## Structure and translation parity

`docs-manifest.json` identifies the edition, implementation commit, schema, ABI,
five languages and mandatory chapters. Every language must contain the same chapter
set. Write complete explanations and workflows, not links to an untranslated manual.
Keep API keys, flags, commands, version numbers and actual UI captions unchanged.
Describe unavailable or planned features explicitly. Do not imply that translating
this repository localises the running application.

For a behaviour change, update the affected chapter in all five languages, the
shared field reference and OpenAPI where applicable. Human linguistic review can
improve wording; automated validation checks structure and links, not translation
quality. Record future review findings through normal repository review.

Preserve original entry paths as navigation links. Use relative Markdown links so
feature branches, tags and local checkouts resolve consistently. Preserve UTF-8 and
LF endings. The existing license remains in effect for this repository only.

## Validation

From this repository root, with Python 3.11+ and an isolated Python environment:

```sh
python -m venv .venv
```

Activate `.venv/bin/activate` on macOS/Linux or `.venv/Scripts/Activate.ps1` on Windows,
then run:

```sh
python -m pip install -r requirements-docs.txt
python tools/check_docs.py
python tools/check_contract.py
node --check examples/frontends/web-basic/app.js
cmake -S examples/extensions/hello-extension -B build/hello-extension -DCMAKE_BUILD_TYPE=Release
cmake --build build/hello-extension --config Release --parallel
ctest --test-dir build/hello-extension -C Release --output-on-failure
```

The documentation CI validates local links/anchors, all required language chapters,
OpenAPI syntax and selected wire-format invariants. The three-OS example build and
runtime loader test verify that the exported ABI can be consumed independently.
Remote links and live application behaviour are not covered by those checks.

Before release, compare every HTTP method/path and field shape with the intended
implementation commit. Test production deployment/restore procedures against a
separate staging database. Do not label a release or pipeline successful merely
because the documentation checks passed.
