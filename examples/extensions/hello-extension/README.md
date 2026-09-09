# ABI 2 attendance example

[Deutsch](../../../docs/de/extensions/getting-started.md) · [English](../../../docs/en/extensions/getting-started.md) · [Français](../../../docs/fr/extensions/getting-started.md) · [Español](../../../docs/es/extensions/getting-started.md) · [한국어](../../../docs/ko/extensions/getting-started.md)

The original example directory is retained; its implementation now demonstrates the
supported ABI 2 with `attendance.session`, fields `attended_on` and `course`.
It requires CMake 3.25+, a C++23 compiler and the public header, with no private Core dependency.
Run from the repository root:

```sh
cmake -S examples/extensions/hello-extension -B build/hello-extension -DCMAKE_BUILD_TYPE=Release
cmake --build build/hello-extension --config Release --parallel
ctest --test-dir build/hello-extension -C Release --output-on-failure
```

Place the `.dll`, `.so` or `.dylib` in a dedicated trusted extension directory, restart
the host with `--extensions /absolute/path`, then activate extensions as administrator.
Assign `records.read/write` and `attendance.read/write` as appropriate. Create a record
through `/api/management/ext:attendance.session` with values `person_id`, `attended_on`
and `course`. Do not upload executable modules through an entity's Files tab.

The validator deliberately adds no business constraint beyond the host's manifest
validation. See the translated chapters for activation, permissions, deployment and
schema-change limitations. The test loads the actual built library, resolves its C
entry point, checks ABI/manifest lifetime and calls its validator.
