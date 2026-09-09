# REST-Vertrag und Integrationsregeln

[Sprachstart](../README.md) · [OpenAPI](../../../openapi/club-platform.yaml)

## Tatsächliche URLs

Version 0.5.0 verwendet `/api`, **nicht `/api/v1`**. `/health` liegt außerhalb
dieses Präfixes. Die OpenAPI-Datei beschreibt den implementierten HTTP-Vertrag;
interne Core-Methoden sind nicht automatisch REST-Endpunkte. Routen für Termine,
`/members`, Audit-Ausgaben oder beliebige Plugin-Callbacks dürfen nicht aus dem
früheren Entwurf abgeleitet werden.

| Bereich | Routen |
|---|---|
| Sitzung | `POST /api/auth/login`, `GET /api/auth/me`, `POST /api/auth/logout`, `POST /api/auth/password` |
| Personen | `GET/POST /api/persons`, `GET/PUT /api/persons/{id}` |
| Verwaltung | `GET/POST /api/management/{resource}` |
| Dateien | `GET/POST /api/assets`, `GET /api/assets/{id}`, öffentliches `GET /api/branding` |
| Erweiterungen | `GET /api/extensions`, `POST /api/extensions/install` |
| Dokumente | `POST /api/documents/render`, `GET /api/reports` |
| Rechte/Felder | Benutzer-, Gruppen-, Rollen- und Feldrouten gemäß OpenAPI |

## Sitzung und Datentypen

Anmeldung sendet `{"login":"…","password":"…"}`. Erfolgreiche Antwort enthält
`user_id`, `login`, `expires_at` (Unix-Sekunden) und ein Token. Folgeaufrufe senden
`Authorization: Bearer TOKEN`. Das Token ist kein Benutzer-ID-Ersatz, den der
Client selbst erzeugen darf. `401` beendet den lokalen Sitzungszustand; Passwort
oder Token nicht automatisch in persistenten Browser-Speicher schreiben.

JSON-Anfragen benötigen `Content-Type: application/json`. Verwaltungswerte sind
Zeichenketten: beispielsweise `"8"`, `"true"`, `"2026-09-08"`. In dedizierten
Rechte-Endpunkten sind `enabled`, `active`, `read`, `write` dagegen echte
JSON-Booleans. Revisionsnummern bleiben Zeichenketten. IDs sind UUIDs, außer
zusammengesetzten Verwaltungs-IDs wie Gruppen-/Rollenzuordnungen.

Neue Person:

```json
{"given_name":"Erika","family_name":"Mustermann"}
```

Personenänderung über `PUT /api/persons/{id}`:

```json
{"revision":"1","given_name":"Erika","family_name":"Muster"}
```

Für generische neue Datensätze `{"id":"","revision":"0","values":{…}}`
senden. Beim Bearbeiten die gelesene ID und Revision verwenden. Nicht alle
Ressourcen sind bearbeitbar; `persons` und `organization_children` dienen im
generischen Zugriff als Lesesichten. Personen separat oder über `person_identity`
bearbeiten. Zuordnungstabellen besitzen eigene Aktivierungssemantik.

## Ressourcen und Beziehungen

`organizations`, `person_profiles`, `contacts`, `addresses`, `relationships`,
`memberships`, `positions`, `departments`, `fee_groups` und
`organization_affiliations` bilden die Akten. Kontakte/Anschriften verwenden
`entity_id`, persönliche Daten `person_id`, Organisationsbereiche `organization_id`.
Mitgliedschaft und Funktion enthalten Person und Organisation. `owner` filtert
je nach Ressource nach der geöffneten Akte; es erteilt keine Rechte.

Administration: `users`, `groups`, `roles`, `group_members`, `group_roles`,
`role_permissions`, `field_definitions`, `field_permissions`, `field_values`.
Vorlagen: `document_templates`. Native Datensätze:
`ext:martial.graduation` und `ext:martial.exam`. Die Feldlisten stehen in der
[sprachneutralen Ressourcenreferenz](../../../reference/resources.md).
Nicht bekannte Felder nicht blind mitsenden: einige Ressourcen verlangen eine
exakte Feldmenge. Antwort-`labels` sind Anzeigehilfen; geschrieben werden die IDs.

Listen enthalten maximal 100 Einträge. `after` ist der letzte gelesene Cursor,
`q` eine wörtliche Suche mit Beachtung der Groß-/Kleinschreibung. Listen mit
`next_cursor` werden bis `null` gelesen. Dateilisten besitzen keinen
`next_cursor`: bei 100 Treffern die letzte ID als `after` verwenden. Auf einer
leeren Folgeseite aufhören. Vorlagen ignorieren derzeit Such-/Ownerfilter;
nicht jede generische Ressource unterstützt jeden Filter.

## Dateien und Dokumente

Uploads senden `owner`, `purpose`, `filename`, `media_type`, `content` als Base64
**ohne** Data-URI-Präfix. Zweck `file` oder `photo` gehört zu Person/Organisation;
`logo`/`background` verwenden leeren Owner und verlangen `security.manage`.
Listen enthalten Metadaten; der Einzelabruf enthält den Inhalt. Branding ist
öffentlich, weil es vor der Anmeldung angezeigt wird. Dort keine vertraulichen
Informationen als Bild hinterlegen.

`/api/documents/render` erhält `template_id`, `person_id`, `date` und liefert
`title` und `body`, kein PDF. PDF wird vom Client erzeugt. Datum ist ISO, auch
wenn die Benutzeroberfläche ein lokales Format zeigt. `/api/reports` liefert
UTF-8-CSV mit BOM; freigegeben sind Personen, Organisationen, Mitgliedschaften,
Funktionen und native Datensätze. Maximum 5.000 Zeilen; größere Auswertungen
gezielt eingrenzen. Ein mehrseitiger Export ist kein transaktionaler Snapshot.

## Fehler und Transport

| Status | Behandlung |
|---|---|
| 400 | Felder, Typen, Pflichtwerte oder JSON prüfen |
| 401 | Sitzung verwerfen, neu anmelden |
| 403 | Berechtigung sowie Host-/Origin-Konfiguration prüfen |
| 404 | ID und tatsächlich vorhandene Ressource prüfen |
| 409 | Neu lesen, Unterschiede vergleichen, bewusst erneut bearbeiten |
| 500 | Vorgang überprüfen lassen; keine blinde Schreibwiederholung |

Bei einem Timeout kann ein Schreibvorgang bereits bestätigt worden sein. Erst
lesen, dann entscheiden, ob erneut geschrieben werden muss. Es gibt keine
allgemeinen Idempotency-Keys oder Batchtransaktionen im HTTP-Vertrag.
Standard-JSON ist auf 16 KiB begrenzt, Asset-Anfragen zusätzlich durch die
8-MiB-HTTP-Grenze und die Grenzen des dekodierten Inhalts. Genau ein konfigurierter
Browser-Ursprung wird zugelassen; Preflight verwendet `OPTIONS /api/…`.
Der Host akzeptiert als Upstream-Host `localhost` oder `127.0.0.1` mit optionalem
Port. Clients außerhalb des Servers verwenden den HTTPS-Proxy.
