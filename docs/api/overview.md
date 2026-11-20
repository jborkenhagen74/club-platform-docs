# REST API overview

All application routes use `/api/v1`; health is separately at `/health`.
Authentication uses Bearer sessions, not cookies. User authorization and module
licensing are independent checks. Errors use appropriate HTTP status and an
`error` code; do not depend on unlocalized exception text.

- **[Complete route catalogue (all 52 operations)](club-platform.openapi.json)** – also as [YAML with /api/v1 paths](../../openapi/club-platform.yaml); contract-tested against the server routes
- [Typed lists and record lifecycle](list-lifecycle.openapi.json)
- [Documents and V3 modules](documents-v3.openapi.json)
- [Licensing, provisioning and installation activation](licensing-provisioning.openapi.json)
- [Finance, contributions and purchases](finance.openapi.json)
- [Banking import](banking.openapi.json)
- [Calendar and event command contract](../calendar-events.md)
- [Module dossiers and currency settings](../currencies-and-dossiers.md)

The route catalogue covers every registered route with parameters, error codes and
preview-feature behaviour (`409 feature.experimental_disabled`). The module files above
remain the detailed payload references for their operations. [Acceptance status](../status.md).

The earlier comprehensive [schema-8 G0 contract](../../openapi/archive/club-platform-0.6-g0.yaml) is preserved as historical reference. Its pagination, lifecycle and licensing descriptions are superseded by the current supplements above.
