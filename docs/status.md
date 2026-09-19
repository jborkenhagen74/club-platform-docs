# Development and acceptance status

Baseline: `feature/calendar-events`, schema 18, extension ABI V3.
Documentation synchronization does not merge or publish a software release.

Implemented: typed list operations and lifecycle, V3 extensions, document
registry, seven UI language packs, signed licensing/provisioning, installation
activation, finance/contributions/purchases, calendar/events, athlete licenses,
permission self-protection, organization currencies and person module dossiers.

Banking now has mapped UTF-8 CSV and bounded CAMT.053 import, preview, confirmed
transaction persistence, duplicate detection and confirmed incoming-payment
posting into the shared ledger. Native parser and GUI compilation passed the
macOS CI runs; banking HTTP tests also passed. The portal check passed. A legacy
migration test fixture has been corrected; the complete native matrix is being
rerun. Outgoing payments, automatic matching and direct bank connectivity are
not implemented. Phase 14 is therefore an import increment, not full acceptance.

## Remaining gates

- Phase 5: complete legacy UI/error extraction, Desktop parameter/plural semantics,
  full locale-aware document formatting/search, eighth-pack integration,
  Korean font embedding and PDF rendering. Equal key counts alone do not prove this.
- Phase 6: discovery/load-failure management UI and full I18n acceptance.
- Phase 14: reviewed matching rules and representative bank exports; no SEPA
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
