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

The migration fixture correction passed Linux, PostgreSQL, both macOS builds,
macOS installation, Qt and portal checks. Matching passed native macOS tests;
its remaining platform and browser checks are pending. Windows dependency
compilation previously hit the 30-minute job limit: binary caching and a Windows
60-minute cold-build limit have been added. These are development checks, not
a production deployment or final pilot acceptance.

## Remaining gates

- Phase 5: complete legacy UI/error extraction, Desktop parameter/plural semantics,
  full locale-aware document formatting/search, eighth-pack integration,
  Korean font embedding and PDF rendering. Equal key counts alone do not prove this.
- Phase 6: discovery/load-failure management UI and full I18n acceptance.
- Phase 14: representative bank exports and user acceptance of matching rules; no SEPA
  export is included in the current foundation scope.
- Phase 15: final platform/package matrix, restored-backup pilot and user acceptance.
- Operations: deploy the HTTPS activation service and configure the publisher
  public key. No publisher private keys are committed here.
- Optional portal mTLS/BFF authentication is not implemented; browser origins
  alone are not application identity.

The five language handbooks and placeholder catalogues cover the current user
flows. Detailed implementation references retain their original German/English
language; this is not a claim that every technical appendix has been translated.
API supplements are available; a comprehensive OpenAPI contract for every legacy
endpoint remains an acceptance task.
