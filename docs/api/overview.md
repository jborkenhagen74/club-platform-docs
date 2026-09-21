# REST API overview

All application routes use `/api/v1`; health is separately at `/health`.
Authentication uses Bearer sessions, not cookies. User authorization and module
licensing are independent checks. Errors use appropriate HTTP status and an
`error` code; do not depend on unlocalized exception text.

- [Authentication](../../openapi/club-platform.yaml)
- [Typed lists and record lifecycle](list-lifecycle.openapi.json)
- [Documents and V3 modules](documents-v3.openapi.json)
- [Licensing, provisioning and installation activation](licensing-provisioning.openapi.json)
- [Finance, contributions and purchases](finance.openapi.json)
- [Banking import](banking.openapi.json)
- [Calendar and event command contract](../calendar-events.md)
- [Module dossiers and currency settings](../currencies-and-dossiers.md)

These are versioned supplements, not a claim that every legacy route already
has a complete OpenAPI schema. [Acceptance status](../status.md).

The earlier comprehensive [schema-8 G0 contract](../../openapi/archive/club-platform-0.6-g0.yaml) is preserved as historical reference. Its pagination, lifecycle and licensing descriptions are superseded by the current supplements above.
