# Development and acceptance status

Baseline: **1.0.0 Pilot**, schema 18, extension ABI V3. Edition of this page: 20 November 2026.
The pilot label does not certify production acceptance. See
[pilot rollout and module upgrade](release-1.0-pilot.md).

## Implemented

Typed list operations and record lifecycle, V3 extensions, document placeholder
registry, seven UI language packs, signed licensing/provisioning and installation
activation, finance/contributions/purchases, banking import and matching,
calendar/events, athlete licenses, permission self-protection, organization
currencies and person module dossiers.

Added since September 2026:

- Training and attendance with wearable/file imports, evaluation, profiles,
  recovery, guardians and retention; [inventory](inventory.md);
  [operational workspaces](de/operational-workspaces.md);
  [extension services and signed UI packages](extension-services-and-ui-packages.md);
  per-user [sidebar order](sidebar-order.md).
- Preview modules and features: [movement/combat analysis](movement-combat-preview.md),
  training AI and Strava – see [pilot scope](#pilot-scope).

## Pilot scope

Decision of 20 November 2026 ("mixed form"):

| Pilot | Preview (not part of the pilot acceptance) |
|---|---|
| Core records, memberships, rights/audit, documents, licensing | Training AI analysis/planning, Strava |
| Finance, contributions, purchases, banking import | Movement and combat analysis |
| Calendar, events, athlete licenses | Analysis app, worker host, Health Connect app |
| Training basics, attendance, inventory | |

Preview features are off by default and are enabled by the host operator with
`CLUBPLATFORM_EXPERIMENTAL`; see [preview features](preview-features.md).

## Changes in 1.0.x (November 2026)

- **Security:** login throttling can no longer be used to lock out all accounts;
  repeated lockouts double up to one hour; background worker failures are logged.
  The reverse-proxy example shipped with the server now sets a 33 MiB body limit,
  HSTS and a login rate limit (`limit_req`).
- **Performance:** password hashing outside the database lock, parallel read-only
  snapshot connections (SQLite WAL / PostgreSQL), batched list labels. Measured on
  the same host: reads 938–966 → 1,491–1,512 requests/s; reads during a login storm
  53–120 → 1,029–1,113 requests/s (p95 168–182 ms → 13–14 ms).
- **Internationalisation:** pilot-scope UI texts and desktop error/status messages use
  language-pack keys (927 keys per pack) with a CI check against new hard-coded text;
  documents support `{{key|locale}}` ([details](document-placeholders.md)); portal PDFs
  embed Noto Sans KR for Hangul.
- **API:** [complete route catalogue](api/club-platform.openapi.json) for all 52
  operations, contract-tested against the server.
- **CI:** pull requests run Linux (SQLite + PostgreSQL), desktop and portal checks before
  merge; the full platform matrix still runs after the merge.

## Remaining gates

- **Phase 5 (I18n):** locale-aware search and sorting (Turkish I/İ, Hangul) on both
  databases; native review of the new translations; desktop PDF output with Hangul on all
  platforms; preview-module texts.
- **Phase 6:** acceptance together with phase 5.
- **Phase 14:** representative bank exports and user acceptance of matching rules; no
  SEPA export in the current scope.
- **Phase 15:** human pilot acceptance on the offered OS/CPU combinations, including
  backup/restore.
- **Operations:** deploy the HTTPS activation service and configure the publisher public
  key. No publisher private keys are committed here.
- Optional portal mTLS/BFF authentication is not implemented; browser origins alone are
  not application identity.

Historical acceptance runs (e.g. baseline `d7a3ebd`, follow-up `1e6657d`) remain evidence
only for their named commits; see the [pilot evidence](pilot.md).
