# Native services and independently installable UI packages

> Build and packaging commands on this page refer to the implementation source tree
> (private repository). Module authors without core source follow the
> [external module guide](de/module-entwicklung-ohne-core.md).

## What is separate

Finance/banking, scheduling and training/AI implementations are compiled into the
native extension libraries. The host does not link those implementations.
Attendance dossier/consent policies and martial license record policies also run
inside their extensions. `clubplatform_foundation` contains shared generic
permissions, audit and record helpers; it is statically linked on each side, not
passed through the plugin boundary.

Existing module/license IDs and installed data are retained. The financial family
continues to use the finance service; the scheduling family uses the calendar
service. This change does not split training, wearables and AI into new license IDs.

## Service ABI 1

`sdk/include/clubplatform/service_v1.h` defines the optional exported companion
`clubplatform_service_v1`, alongside the unchanged V2/V3 entry point. The boundary
uses C function pointers, UTF-8 JSON and caller-owned output sinks. No C++ objects,
exceptions, allocators, authentication tokens or database handles cross it.

Replies are `{"value":...}` or
`{"error":{"code":0..6,"message":"..."}}`. Calls are synchronous. Input/output
pointers are valid only for the duration of their callback. Providers must catch
all exceptions before returning. Responses are bounded to 64 MiB. Native services
have the same trust level as native extensions; this interface is not a sandbox.

The host operations are:

| Operation | Contract |
|---|---|
| `session.actor` | Authenticated actor ID, resolved by the host |
| `session.scope` | Opaque per-session/per-module digest; no bearer token |
| `clock` | Host clock in seconds |
| `module.ready` | Checks installed version, activation and license |
| `storage.begin/commit/rollback` | Host-owned transaction and connection lock |
| `storage.query` | SQL plus positional nullable string parameters; nullable string rows |
| `storage.json_text/binary_collation` | Persistence-dialect helpers |
| `extension.invoke` | Existing declared V3 capability |
| `extension.service` | Internal cross-service call, inheriting the current transaction |
| `worker.stopped` | Cooperative cancellation signal |

A provider must finish or roll back every transaction it opens. The host rolls
back a transaction left open when a call returns or fails. Nested services borrow
an existing transaction and cannot commit it. Calendar fee posting and finance
ledger changes therefore commit or roll back together. Authorization, scoped data
access and audit stay in that transaction. Background services must recheck the
stored job actor and current permissions before committing a result.

Flags declare record policies, entity-deletion callbacks, fast/slow background
workers, foreign-key reference enforcement and schema migrations. Unknown flags
are rejected. Workers execute through `worker.tick` (with a maintenance hint) or
`worker.slow`; providers must observe cancellation during expensive work.

`POST /api/v1/extensions/{module}/commands/{operation}` reaches only the public
`command` service entry with `{module,operation,input}`. Internal worker, ledger,
record-policy and migration entries are not remotely selectable. The provider
validates its public operation and permissions. Existing REST/client methods remain
compatibility adapters. New providers do not require new host REST routes.
Desktop packages use `session.extensionCommand(requestId,module,operation,input)`
and receive `extensionReady(requestId,module,operation,result)`. Both local and
remote client adapters implement the same generic entry. Public command results
used by this desktop API are JSON objects; errors use the existing session error
signal. Respect `session.busy` and correlate replies by request ID.

Record hooks cover creation/field definitions, save, post-save, list/read, individual
list rows and archive/restore/delete. Historical training/attendance/athlete-license
binaries which relied on host privacy rules are rejected if their service policy is
missing; generic legacy record plugins continue to work.

A provider opting into `CLUB_SERVICE_MIGRATIONS` receives `schema.migrate` for each
new manifest schema version inside the installation transaction, before record
conversion and history insertion. Use the extension's append-only manifest migration
history. Do not start or commit a transaction from this callback. The sample V3
extension demonstrates extension-owned SQL migration and rollback.

Historical host SQL migrations through schema 22 remain frozen for upgrade/hash
compatibility. They are not edited, replayed under new definitions or removed from
existing installations. Future module-specific schema changes belong to the service
migration callback, not new host migration branches.

## UI package format and trust

A package is a signed JSON envelope using the existing Ed25519 catalog public key
and the distinct signature purpose `clubplatform/ui/v1`. The signed payload is:

```json
{
  "format": 1,
  "host_ui_api": 1,
  "module_id": "finance",
  "module_version": "1.1.3",
  "files": {
    "desktop/Finance.qml": "...",
    "web/entry.js": "..."
  }
}
```

Every file path and byte is signed. Maximum payload: 4 MiB and 256 text files.
Only flat `desktop/*.qml`, `desktop/*.js` and `web/entry.js` paths are accepted.
Traversal, symlinks in package paths, unknown API versions, modified content and
mismatching module versions are rejected. The store is operator-controlled;
clients cannot supply a trust key or select filesystem paths over HTTP.

Package revisions are content-addressed. Installation writes an immutable envelope
and atomically switches its `active` pointer. Activation verifies both its hash and
signature again. Rollback explicitly selects a previously installed digest. This
allows UI fixes without changing the native module's exact version or rebuilding
the host/portal. Restart the desktop or reload the portal/catalog to pick up updates.

When no package exists, the matching bundled view remains available. An installed
but invalid or incomplete package fails visibly; it is not treated as absent.

### Build and sign

Run from the repository root after `npm ci` in `apps/portal`:

```sh
node tools/ui/build-package.mjs extensions/finance finance-ui.json
build/tools/distribution/clubplatform-sign sign ui issuer/secret.hex finance-ui.json finance-ui.signed.json
```

The signing executable is built with `CLUBPLATFORM_BUILD_PUBLISHER_TOOLS=ON` (or in
test builds). Keep `issuer/secret.hex` offline and out of the customer installation.
Use the trusted publisher's public key, never a public key supplied alongside an
untrusted package. On Windows, append `.exe` to executable names and account for
the chosen CMake configuration output directory.

The web builder bundles the extension's code and data while binding React and
versioned host helpers to `globalThis.clubPlatformUiV1`. It uses the host React
instance, translations, money helpers, design components, report renderer and
nested `ExtensionView`. The resulting module has no runtime package imports.
Existing QML views import the host `ClubPlatform` UI API and generic resources.

### Install and activate

The installer is built with every host build:

```sh
build/src/application/clubplatform-ui-package /srv/clubplatform/ui PUBLIC_KEY_HEX install finance-ui.signed.json
```

The command prints the installed digest. To roll back:

```sh
build/src/application/clubplatform-ui-package /srv/clubplatform/ui PUBLIC_KEY_HEX activate finance 1.1.3 PREVIOUS_DIGEST
```

Configure the processes which load the package:

```sh
export CLUBPLATFORM_UI_PACKAGES=/srv/clubplatform/ui
export CLUBPLATFORM_CATALOG_PUBLIC_KEY=PUBLIC_KEY_HEX
```

For remote desktop, install the signed package and configure trust on the desktop
machine as well as the server. It independently verifies and extracts QML into a
private temporary directory before loading it. The server never sends arbitrary
QML paths to the client.

The portal requests `/api/v1/extensions/{module}/ui` with its existing session.
The server checks module readiness/read permission and verifies the installed
bundle on each request. The portal checks module identity, exact version and UI API
then imports a temporary Blob containing the verified JavaScript. It never imports
a JavaScript URL from a native manifest. The reverse proxy must allow `blob:` in
`script-src`; `config/hosting/nginx.conf.example` includes this policy. Only install
code from the trusted publisher: signed UI code has normal application privileges.

## Verification

The test suite checks C service error/rollback transport, real finance/calendar and
training workflows, SQL migration rollback, signature/content/path/version rejection,
package replacement and rollback, and QML execution from an unbundled module.
The desktop/mobile portal suite builds, signs and installs the actual six web UI
packages before launching the server. A runtime sentinel in the test packages proves
that the externally loaded code was executed. No sentinel is emitted by normal builds.

Cross-platform source is included; Linux CI evidence and Windows/macOS release
validation must be reported separately. Real Ollama model quality remains a trainer
acceptance check, distinct from transport and consent tests.

## Central module gate (since 1.0.x)

Before the host dispatches any module route – `/finance/...`, `/calendar`, `/events`,
`/training/commands/...`, `/module-dossiers/...` and `/extensions/{module}/commands/...` –
it resolves the session and checks that the addressed module is licensed, installed,
enabled and that its required dependencies are ready (`401` without session, `403`
`module_not_licensed`, `409` when not installed/disabled). Events stay usable without a
calendar licence. Modules keep their own permission and sub-module checks (for example
banking or contributions operations inside finance); the host gate is an additional,
uniform layer, not a replacement. Covered by the implementation's HTTP regression tests.
