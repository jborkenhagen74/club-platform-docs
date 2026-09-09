# Developing native extensions

> Target version 0.6.0, preparatory G0 work: HTTP API `/api/v1` and shared `Client` with `LocalClient`/`RestClient`. Database schema 8 and extension ABI 2 remain unchanged. Old `/api/...` paths return 404. Upgrade server, desktop, portal and proxy together. The functional descriptions below originate from the 0.5.0 baseline and remain applicable except where this notice updates them. Core Foundation II with ABI V3 and seven UI languages is not complete.


[Language home](../README.md) · [UI contract](ui.md) · [Example](../../../examples/extensions/hello-extension/README.md)

## Compatibility and trust

Host 0.5.0 expects **ABI 2**. `sdk/extension_api.h` remains a historical ABI-1
draft; its lifecycle, menu and REST callbacks are not the running host's contract.
Use `sdk/extension_v2.h` for new modules. The C boundary avoids STL objects and
cross-module deallocation, but a library must still match the OS and CPU architecture.

Native modules execute trusted code with host-process privileges. There is no
plugin sandbox. Protect the module directory administratively, review libraries
before deployment and never search normal upload directories for executable
modules. Loading happens at startup; hot replacement is unsupported.

## Entry point and manifest

Export `clubplatform_extension_v2`. It returns a permanently valid structure with
ABI number, UTF-8 manifest and validator. Strings remain module-owned. The validator
receives a record-type string and a JSON string and returns exactly `1` on success;
exceptions must never cross the C boundary. No database handle is exposed.

The manifest contains `id`, `name`, `version`, `types`. Versions have three numeric
components. Module IDs contain no dots; type keys start with `module.`. A type has
`key`, `label`, `fields`; fields have `key`, `label`, `type`, optionally
`required:false`. Types are `text`, `integer`, `decimal`, `boolean`, `date`.
Keys start with a lower-case letter and use lower-case letters, digits, underscores
and, for namespaced types, dots. Duplicate keys and foreign namespaces are rejected.

Submit every declared field, using an empty string for an absent optional value.
Unknown fields cause rejection. The host checks types and required values before
calling the module validator; current text validation allows 512 UTF-8 bytes per
value. The example adds training attendance and builds against the public header only:

```sh
cmake -S examples/extensions/hello-extension -B build/hello-extension -DCMAKE_BUILD_TYPE=Release
cmake --build build/hello-extension --config Release
```

Copy the resulting library into a dedicated extension directory. Visual Studio
outputs may be inside `Release`/`Debug`. Start the host with `--extensions /absolute/path`
or set `CLUBPLATFORM_EXTENSIONS`. A connected desktop does not load the server's
modules again on the client.

## Activation and records

After loading, an authenticated administrator selects `Erweiterungen aktivieren`
or sends `{}` to `POST /api/v1/extensions/install`. `schema.manage` is required.
Record-type registration and manifest persistence are transactional and audited.
`GET /api/v1/extensions` shows loaded manifests and `installed`; reinstalling the
identical manifest is allowed.

Native records currently belong to people. An example resource is
`/api/v1/management/ext:attendance.session`. Management values additionally carry
`person_id`; the host removes that association before invoking the domain validator.
`attendance.read/write` supplement `records.read/write` and must be assigned to
roles. Visible UI controls never replace server authorisation.

A changed installed manifest is rejected at load time. Merely increasing its
version does not migrate data. Schema changes need an explicit migration and a
verified backup. ABI 2 does not support arbitrary REST routes, background jobs,
packaged QML/JavaScript execution or hot reload; those remain proposals.
