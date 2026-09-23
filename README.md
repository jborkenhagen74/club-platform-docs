# Club Platform – API documentation and examples

Public documentation and examples for integrating with Club Platform.

**Club Platform 1.0.0 Pilot · schema 18 · extension ABI V3.**

[Current pilot status and upgrade instructions](docs/release-1.0-pilot.md). Pilot is a prerelease channel; native acceptance remains a separate gate.

New: [ausführliche bebilderte Bedienungsanleitung (Deutsch)](docs/de/bedienung.md),
[Formularatlas mit allen Aktionen](docs/de/formulare.md),
[Pilot und Wiederherstellung](docs/pilot.md),
[Screenshot-Verzeichnis](docs/images/pilot/README.md).

Field-by-field form references: [EN](docs/en/formulare.md) ·
[FR](docs/fr/formulare.md) · [ES](docs/es/formulare.md) · [한국어](docs/ko/formulare.md).
Screenshots retain their German UI labels so they can be compared with the tested build.

| Language | User guide | Operations and integration | Complete placeholders |
|---|---|---|---|
| Deutsch | [Handbuch](docs/de/handbook.md) | [Betrieb](docs/de/operations.md) | [70 Platzhalter](docs/de/placeholders.md) |
| English | [Handbook](docs/en/handbook.md) | [Operations](docs/en/operations.md) | [70 placeholders](docs/en/placeholders.md) |
| Français | [Manuel](docs/fr/handbook.md) | [Exploitation](docs/fr/operations.md) | [70 variables](docs/fr/placeholders.md) |
| Español | [Manual](docs/es/handbook.md) | [Operación](docs/es/operations.md) | [70 marcadores](docs/es/placeholders.md) |
| 한국어 | [사용 설명서](docs/ko/handbook.md) | [운영](docs/ko/operations.md) | [자리표시자 70개](docs/ko/placeholders.md) |

Builds: [Windows, macOS, Linux installers and native license publisher](docs/build-installers-publisher.md).

Detailed German guides (21 September 2026):

- Builds and installers for Desktop, Server and Publisher: [Markdown](docs/de/build-und-installer.md) · [PDF](docs/pdf/Club-Platform-Build-und-Installer-DE.pdf)
- External module development without private Core source: [Markdown](docs/de/module-entwicklung-ohne-core.md) · [PDF](docs/pdf/Club-Platform-Modulentwicklung-DE.pdf)


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

## Earlier multilingual chapters

The original 0.5/0.6 G0 chapters are retained and explicitly marked as historical: [DE](docs/de/README.md), [EN](docs/en/README.md), [FR](docs/fr/README.md), [ES](docs/es/README.md), [KO](docs/ko/README.md). Use the current handbooks, API supplements and ABI-V3 guide for the 1.0 pilot.

[Contribution and documentation checks](CONTRIBUTING.md).

## Trainingsausbau (Feature-Stand)

- [Wearable-Import, Diagramme und lokale KI](docs/de/training-wearables-ai.md)
- [Trainingsanwesenheit und Freigaben](docs/training-attendance.md)
- [Wearable-Handbuch als PDF](docs/pdf/Club-Platform-Training-Wearables-KI-DE.pdf)

Der Feature-Stand benötigt Host-Schema 19 und Training 1.1.0.
Der veröffentlichte 1.0-Pilot-Stand wird dadurch noch nicht ersetzt.
