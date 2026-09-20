# Development and acceptance status

Baseline: `feature/calendar-events`, schema 18, extension ABI V3.
Documentation synchronization does not merge or publish a software release.

Implemented: typed list operations and lifecycle, V3 extensions, document
registry, seven UI language packs, signed licensing/provisioning, installation
activation, finance/contributions/purchases, calendar/events, athlete licenses,
permission self-protection, organization currencies and person module dossiers.

Banking now has mapped UTF-8 CSV and bounded CAMT.053 import, preview, confirmed
transaction persistence, duplicate detection, cursor pagination and confirmed
incoming-payment posting into the shared ledger. Matching suggests open
receivables in the selected account, distinguishes exact references from amount
matches, and atomically allocates partial or excess payments after confirmation.
Reversals and retries preserve the existing history. Outgoing payments, unattended
matching and direct bank connectivity are not implemented.

The preceding baseline `d7a3ebd` passed the complete native matrix, including
Windows, Linux, PostgreSQL, both macOS architectures, macOS installation and Qt;
all 22 browser checks passed. Windows dependency caching and a 60-minute cold-build
limit resolved the earlier timeout. This corrects the previously stale “Windows
pending” status.

The September 20 follow-up adds Desktop parameter/plural lookup using ICU, more
translated help/menu text, and an administrator-only failed-loader diagnostic.
Failed staged modules stay unavailable; provisioning validation remains strict.
The browser pilot now produces actual UI screenshots and compares all database
tables after backup/restore, revokes sessions and checks a new login and all seven
modules on the restored host. See [pilot evidence and scope](pilot.md).

At follow-up commit `1e6657db89cfd3c37cba6aca0e227eabeedbd235`, the
[complete native matrix](https://github.com/jborkenhagen74/club-platform/actions/runs/35519627677)
passed on Windows, Linux and both macOS architectures, including PostgreSQL,
Qt and macOS installation. The
[portal workflow](https://github.com/jborkenhagen74/club-platform/actions/runs/35519627684)
passed all 28 browser checks and the subsequent restore pilot. Release publishing
was skipped on this feature branch.

## Remaining gates

- Phase 5: complete legacy UI/error extraction,
  full locale-aware document formatting/search,
  Korean font embedding and PDF rendering. Equal key counts alone do not prove this.
- Phase 6: full I18n acceptance. Failed-load diagnosis now keeps the core available
  while retaining the atomic rejection of the entire module load.
- Portal layout: commit `e1bd8f8a568cf9ea0bf439d00b3baa84ab49e685` replaces the
  cramped module table with responsive cards, preserving status fields, diagnostics
  and per-module actions. Forest/Plum theme labels now use all seven language packs.
  Local TypeScript/Vite build and the 553-key language-pack check pass. Browser
  acceptance and replacement screenshots remain pending: both CI runs fail before
  any job step, including one retry, with no job logs available. The precise
  GitHub-side cause has not been established. See the
  [portal run](https://github.com/jborkenhagen74/club-platform/actions/runs/35523793328)
  and [native run](https://github.com/jborkenhagen74/club-platform/actions/runs/35523793447).
  The green matrix and screenshots above apply to the preceding commit only.
- Phase 14: representative bank exports and user acceptance of matching rules; no SEPA
  export is included in the current foundation scope.
- Phase 15: human pilot acceptance. The latest matrix is green; automated restore
  evidence is documented separately and is not a claim of user sign-off.
- Operations: deploy the HTTPS activation service and configure the publisher
  public key. No publisher private keys are committed here.
- Optional portal mTLS/BFF authentication is not implemented; browser origins
  alone are not application identity.

The detailed illustrated operating manual is in German. All five languages have
a handbook, operations guide, complete placeholder catalogue and field-by-field
finance/scheduling form reference. Screenshots retain German labels and distinguish
browser captures from native Qt. The Qt test uses English and exposes remaining
German labels; browser captures use German. Detailed implementation references retain their
original German/English language; this is not a claim that every appendix or the
entire long German operating manual has been translated.
API supplements are available; a comprehensive OpenAPI contract for every legacy
endpoint remains an acceptance task.

## Build and publisher tooling follow-up

Code commit `9761497ffa287c3e8e47702b22da63b222ab9da4` adds a shared Python build
and packaging driver with shell/PowerShell wrappers for desktop, server and
publisher profiles. Native formats are NSIS, productbuild and DEB/RPM; archives
remain available. Customer installers require the public issuer key.
The separate Qt Widgets publisher uses the existing native signer, builds payloads
from form fields and optionally registers signed envelopes via SSH `register-stdin`.
No publisher private key is bundled. See [instructions](build-installers-publisher.md).

Local verification: five build-driver tests, eight activation-service tests,
shell syntax, Python syntax and real TGZ/DEB packaging with synthetic content.
The native publisher/GUI tests and full platform installer acceptance remain
pending. No successful new binary build or production activation deployment is
claimed. The existing illustrated pilot still documents the earlier tested build.
