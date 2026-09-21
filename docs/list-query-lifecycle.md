# Phase 1 und 2: Listen und Datensatzlebenszyklus

Stand: 2026-09-15. Phase 0 wurde durch den Auftraggeber abgeschlossen.
Diese Erweiterung verwendet weiterhin HTTP `/api/v1` und native ABI 2 und ergänzt
**Migration 9**. Die unveränderten Migrationen 1–8 bleiben prüfbar.

## Bedienung

Personenlisten bieten Sortierfeld, Richtung und Archivansicht. In den Akten und
Verwaltungslisten gibt es zusätzlich einen Feldfilter. Die Liste wird vollständig
im Application-Dienst gefiltert und sortiert; Desktop und Portal erhalten jeweils
nur eine Seite. Der ausgewählte Sortierzustand bleibt während der Sitzung beim
Filtern, Bearbeiten, Aktenwechsel und Seitenwechsel erhalten. Eine Änderung der
Abfrage beginnt wieder auf Seite 1. Die Dateienliste behält ihre bisherige
Upload-/Download-Bedienung und ID-Pagination.

Im Desktop liegen die Aktionen im Menü **⋯** des jeweiligen Datensatzes. Im Portal
stehen die Schaltflächen direkt an der Karte. Archivieren blendet den Datensatz in
aktiven Listen aus und erhält seine Beziehungen, Felder und Unterlagen. Zum
Wiederherstellen die Archivansicht wählen. Archivierte Personen und Organisationen
lassen sich weiterhin als Akte öffnen. Der archivierte Stammdatensatz muss vor dem
Bearbeiten wiederhergestellt werden; seine verbundenen Datensätze behalten ihren
eigenen Lebenszyklus.

Endgültiges Löschen verlangt eine Bestätigung. Bestehende Referenzen blockieren den
Vorgang vollständig. Dann zuerst fachlich prüfen, ob eine Referenz entfernt werden
darf, oder den Datensatz archivieren. Ein Konflikt ist kein Anlass, dieselbe Anfrage
ungeprüft zu wiederholen: aktuellen Stand laden und Revision kontrollieren.

## Gemeinsamer Vertrag

`domain::ListQuery`, `ListFilter`, `ListPage` sind Qt-freie DTOs. `query_list` und
`transition` stehen in Foundation, authentifizierter SessionApplication und dem
Client-Interface bereit. LocalClient benutzt die lokalen Dienste; RestClient ruft
HTTP auf. Der Actor stammt ausschließlich aus der Sitzung.

| Eigenschaft | Vertrag |
|---|---|
| `search` | Wörtliche, UTF-8-/groß-/kleinschreibungssensitive Suche, höchstens 256 Bytes |
| `sort` | Ein freigegebenes Feld, Standard `id`; ID als eindeutiger zweiter Schlüssel |
| `direction` | `asc` oder `desc`, gilt auch für den ID-Schlüssel |
| `page_size` | 1 bis 100, Standard 100 |
| `filters` | Höchstens 16 UND-verknüpfte typisierte Filter |
| `cursor` | Opaquer Fortsetzungswert; unverändert an dieselbe Abfrage zurückgeben |
| `state` | `active` (Standard), `archived`, `all`; nur Ressourcen mit Archivzustand |

Filter: `field`, `op`, `type`, `value`. Operatoren: `eq`, `ne`, `lt`, `le`, `gt`,
`ge`, `contains`; `contains` ist ausschließlich für Text zulässig. Typen: `text`,
`integer`, `decimal`, `boolean`, `date`. Der Wert wird auf dem Draht als Zeichenfolge
übertragen, beispielsweise `"12"`, `"true"` oder `"2026-09-15"`. Typfalsche Filter
und unbekannte Felder/Operatoren werden mit 400 abgewiesen. Die Oberflächen bieten
einen Feldfilter gleichzeitig; der API-Vertrag unterstützt bis zu 16.

Ganzzahlen und Centbeträge werden numerisch, ISO-Daten chronologisch sortiert.
Für Texte gilt bewusst **UTF-8 binary v1**: SQLite `BINARY`, PostgreSQL `C`.
Dies ist eine definierte, systemunabhängige Collation, keine deutsche
Wörterbuchsortierung und kein türkisches Case-Folding. `I`, `İ`, `ı`, `i`, Umlaute,
Akzente und Hangul bleiben unterscheidbar. Localeabhängige Suche/Collation wird
zusammen mit Phase 5 erweitert und benötigt eine eigene Cursor-Version.
Leere optionale Text-/Datumswerte stehen lexikalisch am Anfang aufsteigender Listen;
fehlende optionale Zahlen werden als NULL vor Zahlen angeordnet, in beiden Richtungen.

Der Cursor enthält Query-Fingerprint und letzten Sortierwert/ID. Er ist an Ressource,
Owner, Actor, Suche, Filter, Richtung, Seitengröße, Status und Collation gebunden.
Er ist **kein Berechtigungsnachweis**; jede Seite prüft aktuelle Rechte. Er ist nicht
verschlüsselt und kann den letzten bereits sichtbaren Sortierwert enthalten.
`page_size + 1` bestimmt zuverlässig, ob eine weitere Seite existiert. Es gibt keine
leere Zusatzseite, wenn die Trefferzahl genau der Seitengröße entspricht.

Keyset-Pagination garantiert für unveränderte Daten auch bei gleichen Sortierwerten
keine Duplikate oder Auslassungen. Sie ist kein eingefrorener Datenbank-Snapshot:
Änderungen an Sortierwerten zwischen zwei Anfragen können einen Datensatz über die
Seitengrenze verschieben. Nach eigenen Änderungen setzt die UI den Cursor zurück.

## Ressourcen und Rechte

| Ressourcen | Listenrecht | Lebenszyklusrechte |
|---|---|---|
| Personen, Organisationen, Kontakte, Adressen, Beziehungen, Profile, Abteilungen, Organisationszugehörigkeiten | `records.read` | `records.archive`, `records.restore`, `records.delete` |
| Mitgliedschaften, Funktionen, Beitragsgruppen | `memberships.read` | `memberships.archive`, `memberships.restore`, `memberships.delete` |
| Dokumentvorlagen | `records.read` | `schema.archive`, `schema.restore`, `schema.delete` |
| `ext:<type>` (Graduierungen, Prüfungen) | `records.read` und `<module>.read` | `records.<action>` und `<module>.<action>` |
| Benutzer, Gruppen, Rollen und Sicherheitszuordnungen | `security.manage` | Bestehende Aktivierungs-/Zuweisungsoperationen, kein generisches Löschen |
| Felddefinitionen | `schema.manage` | Bestehende Definition-/Typmigrationsoperationen |
| Feldwerte | `records.read` plus einzelne Feldrechte | Bestehendes berechtigungsgeprüftes Leeren |
| Installierte Erweiterungen (`extensions`) | `records.read` | Keine Lösch-/Archivoperation auf nativen Bibliotheken |

Endgültiges Löschen von Personen/Organisationen benötigt **zusätzlich
`security.manage`**. Ein normales Schreibrecht erteilt kein Löschrecht. Bestehende
Administratoren mit `*` können die neuen Aktionen bereits ausführen; weitere Rollen
müssen ausdrücklich berechtigt werden. Nicht revisionierte Sicherheitszuordnungen
werden weiterhin über ihre vorhandenen fachlichen Operationen geändert, damit die
Sicherung des letzten Administrators nicht umgangen wird.

Felder der Ressourcen sind fest freigegeben. Erweiterungsfelder stammen aus dem
installierten und geladenen Manifest. Bei eigenen Feldwerten lassen sich nur
`id`, `key`, `value_type` abfragen: Filter/Sortierung nach geschützten Werten würden
Informationen verraten. Feldrechte werden schon **vor LIMIT** berücksichtigt.
Schreibgeschützte Sichtbarkeit und reine Schreibrechte bleiben getrennt.

## Transaktion und Referenzen

Alle drei Aktionen prüfen Revision und Berechtigung und schreiben Daten/Audit in
derselben serialisierten Transaktion. Archivieren/Wiederherstellen erhöhen die
Revision um eins. Veraltete Revision, bereits erreichter Zustand und referenzierte
Löschung liefern 409. Audit-Einträge verwenden `<resource>.archive`, `.restore`,
`.delete`; keine persönlichen Feldwerte werden kopiert. Audit-Zeilen bleiben erhalten.

Keine pauschalen Cascades: Fremdschlüssel schützen Kontakte, Unterlagen, Mitglieder,
Benutzerzuordnungen und weitere Bezüge. Historische Textreferenzen für
Organisationshierarchie, Abteilungen und Beitragsgruppen werden zusätzlich geprüft.
Beim Löschen einer Person/Organisation werden deren konkrete Zeile und Entity-Zeile
atomar entfernt; ein Fehler im zweiten Schritt rollt auch den ersten zurück.

**ABI-2-Grenze:** Installierte native Module können unbekannte Referenzen besitzen.
Solange irgendein Modul installiert ist, blockiert deshalb das endgültige Löschen
von Personen/Organisationen konservativ. Archivieren/Wiederherstellen funktioniert.
Eine vollständige modulübergreifende Referenzfreigabe gehört zum kommenden ABI-3-
Vertrag. Es werden keine gesetzlichen Aufbewahrungsfristen erfunden. Noch nicht
implementierte Finanz-, Kauf-, Kalender- und Eventressourcen erhalten ihre Regeln
mit ihren jeweiligen Phasen; gebuchte Daten dürfen später nur storniert werden.

Maschinenlesbarer Teilvertrag: [OpenAPI-Ergänzung](api/list-lifecycle.openapi.json).

CSV-Exporte übernehmen die aktuelle Sortierung, Feldfilter und Archivansicht und
bleiben auf 5.000 Datensätze begrenzt.

## HTTP-Beispiele

```http
GET /api/v1/management/persons?sort=family_name&direction=asc&page_size=25&state=active
Authorization: Bearer <session>
```

Antwort: `{"items":[{"id":"…","revision":"1","values":{},"labels":{}}],"next_cursor":"…"}`.
`/api/v1/persons` unterstützt dieselben Parameter und behält sein flaches Personen-
Antwortformat. Bestehende Aufrufe ohne neue Query-Parameter verwenden weiter `after`
und `q`; beide Paginationmodelle dürfen nicht vermischt werden.

```http
POST /api/v1/management/persons/<id>/archive
Content-Type: application/json
Authorization: Bearer <session>

{"expected_revision":"1"}
```

Wiederherstellen: `POST .../<id>/restore`. Löschen: `DELETE .../<id>`, jeweils mit
demselben Revision-Body. Erfolg: 204. Fehler: 400/401/403/404/409. CORS erlaubt auch
DELETE ausschließlich für den konfigurierten Portal-Ursprung.

## Migration, Prüfung und Rollout

Vor dem ersten Start mit Schema 9 einen geprüften Backup erstellen. Neue Software
migriert automatisch; bestehende Datensätze starten unarchiviert und behalten ihre
Revision. Ein Downgrade auf Schema-8-Binärdateien benötigt den vorherigen Backup und
die dazugehörigen Binärdateien; eine nachträgliche Entfernung von Archivspalten im
Produktivbestand ist kein Rollbackverfahren. Server, Desktop und Portal gemeinsam
aktualisieren.

Prüfungen: Foundation-Suite mit demselben Bestand für SQLite/PostgreSQL, lokale und
HTTP-Client-Verträge, HTTP-Pagination/Lebenszyklus, Desktop lokal/remote und vier
Playwright-Abläufe auf Desktop/Mobil. Migration, Backup/Restore und Audit-Rollback
bleiben Teil der regulären CI. Neue UI-Schlüssel liegen gemeinsam in
`resources/i18n/core.de.json`; dynamische Packs und sieben vollständige Sprachen
bleiben Phase 5.
