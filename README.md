# Club Platform – API documentation and examples

Public documentation and examples for integrating with Club Platform.

Development baseline: schema 18 / extension ABI V3. This is not a release claim.

| Language | User guide | Operations and integration | Complete placeholders |
|---|---|---|---|
| Deutsch | [Handbuch](docs/de/handbook.md) | [Betrieb](docs/de/operations.md) | [70 Platzhalter](docs/de/placeholders.md) |
| English | [Handbook](docs/en/handbook.md) | [Operations](docs/en/operations.md) | [70 placeholders](docs/en/placeholders.md) |
| Français | [Manuel](docs/fr/handbook.md) | [Exploitation](docs/fr/operations.md) | [70 variables](docs/fr/placeholders.md) |
| Español | [Manual](docs/es/handbook.md) | [Operación](docs/es/operations.md) | [70 marcadores](docs/es/placeholders.md) |
| 한국어 | [사용 설명서](docs/ko/handbook.md) | [운영](docs/ko/operations.md) | [자리표시자 70개](docs/ko/placeholders.md) |

Current technical references:

- [Banking: mapped CSV and CAMT.053](docs/banking.md), [mapping example](resources/banking/csv-mapping.json)
- [Finance/contributions/purchases](docs/finance-contributions-purchases.md), [currencies and dossiers](docs/currencies-and-dossiers.md)
- [Calendar/events](docs/calendar-events.md), [athlete licenses](docs/athlete-licenses.md)
- [Permissions and deletion](docs/permissions-and-deletion.md), [usability](docs/usability.md)
- [Licensing/provisioning](docs/licensing-provisioning.md), [activation authority](tools/activation/README.md)
- [ABI V3](docs/extension-v3.md), [documents](docs/document-placeholders.md)
- [Acceptance status and remaining gates](docs/status.md)

The original `sdk/extension_api.h` and hello example are historical ABI material.
Use `sdk/include/clubplatform/extension_v3.h` and `sdk/examples/v3-extension` for current extensions.

## Contents

- `docs/extensions` – extension ABI, lifecycle and UI contributions
- `docs/frontends` – REST-based frontend integration
- `openapi` – public REST API contract draft
- `sdk` – public extension ABI header
- `examples/extensions` – compilable native extension examples
- `examples/frontends` – minimal browser/client examples

The proprietary Club Platform implementation is intentionally not contained in this repository.
