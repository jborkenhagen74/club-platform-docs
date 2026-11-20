# Vorschaufunktionen und Pilotumfang

Seit der Scope-Entscheidung vom 20.11.2026 sind folgende Funktionen **Vorschau** und
standardmäßig ausgeschaltet. Der Server-/Desktop-Betreiber schaltet sie über eine
Umgebungsvariable des Host-Prozesses frei (kommagetrennt, `all` für alle):

```bash
export CLUBPLATFORM_EXPERIMENTAL=training-ai,strava
```

| Schlüssel | Umfang | Ohne Freigabe |
|---|---|---|
| `training-ai` | Training: KI-Auswertung (`ai`), KI-Planung (`plan-preview`, `plan-adapt`), KI-Jobs, Modellliste/Verbindungstest, Speichern der KI-Einstellungen; KI-Hintergrundworker | HTTP 409 `feature.experimental_disabled`; `ai-settings` bleibt lesbar und meldet `experimental_enabled: false`; Worker verarbeitet keine KI-Jobs |
| `strava` | Training: `strava-begin`, `strava-finish`, `strava-sync` | HTTP 409 `feature.experimental_disabled`; `strava-disconnect` bleibt möglich |

Die Module Movement und Combat bleiben zusätzlich an den Build-Schalter
`CLUBPLATFORM_BUILD_MOVEMENT_PILOT` gebunden. Der Erweiterungskatalog
(`GET /api/v1/extensions`) liefert `preview: true` für diese Module und beim
Training `preview_features` mit dem jeweiligen Freigabestatus; Desktop und Portal
zeigen das als „Vorschau“ an. Vorschaufunktionen sind nicht Teil der Pilotabnahme.

## Einordnung

| Pilotumfang | Vorschau |
|---|---|
| Kernakten, Mitgliedschaften, Rechte/Audit, Dokumente, Lizenzierung | Training: KI-Auswertung und KI-Planung, Strava |
| Finanzen, Beiträge, Käufe, Banking-Import | Bewegungs- und Kampfanalyse ([Überblick](movement-combat-preview.md)) |
| Kalender, Veranstaltungen, Athletenlizenzen | Analyse-App, Worker-Host, Health-Connect-App |
| Training-Grundfunktionen, Anwesenheit, [Inventar](inventory.md) | |

Vorschaufunktionen verarbeiten teils Gesundheits- und Videodaten. Vor einer Freigabe im
Produktbetrieb sind eine Datenschutzbewertung (Einwilligung, Minderjährige,
Aufbewahrung/Löschung) und eine eigene Abnahme erforderlich.

## Fehlercode

Gesperrte Vorschauoperationen antworten mit HTTP 409:

```json
{"error":"feature.experimental_disabled"}
```

Desktop und Portal übersetzen den Code in allen sieben Sprachen.
