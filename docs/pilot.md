# Pilot und Abnahme

Der technische Pilot verwendet ausschließlich synthetische Personen und
Organisationen, einen temporären Host, eine getrennte SQLite-Datenbank und
kurzlebige Testlizenzen. Produktionsdaten und Herausgeberschlüssel werden nicht
verwendet. Die öffentliche Dokumentation enthält keine Datenbank und keine Tokens.

## Prüfverfahren

Der echte native Server wird gestartet; Playwright führt die Browserabläufe
auf großem Bildschirm und im mobilen Chromium-Profil aus. Es handelt sich nicht
um eine Simulation der Fach-API. Die Prüfung der ausgeblendeten Modulnavigation
verwendet bewusst eine manipulierte Antwort nur im zugehörigen UI-Test;
die übrigen Fachabläufe arbeiten gegen den tatsächlichen Host.

Die plattformübergreifenden nativen Tests prüfen zusätzliche Positiv-/Negativfälle,
gleichzeitige Buchungen, Rechte, Revisionen und Migrationen. Die PostgreSQL-Suite
prüft den zweiten Datenbankadapter und dessen eigenes Wiederherstellungsverfahren.

| Bereich | Technischer Prüfinhalt |
|---|---|
| Personen | Anlegen, Akte öffnen, Filter, Sortierung, Archiv und Wiederherstellung |
| Rechte | Gruppenzuordnung hinzufügen/entfernen, Rechteauswahl und Infotext; native Selbstschutz- und Zugriffstests |
| Sprache | Sieben Sprachen ohne Sitzungsverlust; zusätzlich temporäres achtes Sprachpaket mit Fallback |
| Kampfsport | Graduierung, Sportlerlizenz und zugehörige Nachweisdatei |
| Dokumente | Platzhalterauswahl, Vorschau, PDF-Download und CSV-Auswertung |
| Finanzen | Konto, Zahlung, Betrag/Saldenwirkung und exakte Währungseingabe |
| Beiträge | Mitgliedschaft, Beitragsplan, Zuweisung, Abrechnung und Wiederholungsprüfung |
| Käufe | Produkt, Kauf mit zwei Positionseinheiten und Teilrückgabe zum ursprünglichen Preis |
| Banking | CSV-Mapping, Vorschau ohne Speicherung, Import, Referenzvorschlag, bestätigte Zahlung und Überzahlungsrest |
| Kalender | Tagesklick, Datum/Uhrzeit, Personenzuordnung und gespeicherter Termin |
| Veranstaltungen | Kostenpflichtige Veranstaltung und Teilnahme, Gebühren im selben Finanzkonto |
| Restore | Inhaltsvergleich aller Tabellen, widerrufene Sitzungen, erneuter Hoststart und Anmeldung, sieben Module einsatzbereit |

Die Screenshots einzelner Formulare dienen der Bedienungserklärung. Eine Aufnahme
eines leeren Formulars beweist für sich genommen keinen erfolgreichen Schreibvorgang.
Die Behauptung eines erfolgreichen Pilots setzt den dazugehörigen grünen Workflow
und den [Restorebericht](images/pilot/restore-report.json) voraus.

## Nachweisdateien und Wiederholung

Am 20. September 2026 bestanden am Code-Commit
`1e6657db89cfd3c37cba6aca0e227eabeedbd235` alle **28 Browserprüfungen** im
[Portal-Workflow](https://github.com/jborkenhagen74/club-platform/actions/runs/35519627684).
Der anschließende Restore meldet Schema 18, erfolgreiche Integritätsprüfung,
identische Tabelleninhalte mit Ausnahme widerrufener Sitzungen, erfolgreiche
Neuanmeldung und sieben einsatzbereite Module. Der geprüfte Bestand enthält
unter anderem 14 Finanzbuchungen, zwei Beitragsforderungen, zwei Käufe und zwei
Veranstaltungsteilnahmen. Das ist eine technische Prüfung mit Testdaten.

Auch die [native Plattformmatrix](https://github.com/jborkenhagen74/club-platform/actions/runs/35519627677)
ist für diesen Commit vollständig grün: Windows, Linux, macOS ARM und Intel,
PostgreSQL, Qt sowie die macOS-Installation. Release-Jobs wurden auf dem
Feature-Branch planmäßig übersprungen.

Siehe [Screenshot-Verzeichnis](images/pilot/README.md) für Commit, Workflow und
Abbildungszuordnung. Im privaten Repository liegen die Tests unter
`apps/portal/tests/`, die Wiederherstellungsprüfung unter `restore-pilot.py` und
das SQLite-Werkzeug unter `scripts/pilot-data.py`.

Der Portal-Workflow **Portal and pilot packages** baut Server, Module und Portal,
führt die Testfälle aus und stellt `club-platform-pilot-evidence` bereit.
Die Qt-Prüfung stellt `club-platform-native-screenshots` bereit. Die Datenbank,
Test-Signierschlüssel und Sitzungen werden nicht als Dokumentationsartefakt verteilt.

Zum Wiederholen im vorbereiteten Entwickler-Build:

```bash
python3 apps/portal/tests/run-host.py \
  build/apps/server/clubplatform-server \
  build/extensions/clubplatform_martial.so
```

Die Pfade beziehen sich auf den Linux-CI-Build. Für Dein macOS-Preset passe die
beiden Pfade an den entsprechenden Buildbaum an. Der Test startet eine separate
temporäre Datenbank und benötigt das mitgebaute Signierwerkzeug sowie Playwright.
Er ist nicht für eine vorhandene produktive Datenbank gedacht.

## Noch erforderliche fachliche Abnahme

Der automatisierte Pilot ersetzt keine Abnahme durch Deinen Verein oder Deine
Sportschule. Für die fachliche Freigabe bleibt ein repräsentativer, anonymisierter
Bankexport nötig. Prüfe damit CSV-Mapping beziehungsweise unterstütztes CAMT-Profil,
Soll/Haben, doppelte Referenzen, Teilzahlungen und Überzahlungen am Originalbestand.

Prüfe anschließend mit einem echten Rollenmodell eine eigene Person, eine fremde
Person und aktuelle/beendete Organisationsfunktionen. Lass die zuständigen Nutzer
den Tagesablauf und die Dokumente beurteilen. Erst danach erfolgt die Release-
beziehungsweise Produktivfreigabe. Domain, Zielhost und Schlüsselkonfiguration
des produktiven HTTPS-Aktivierungsdiensts sind gesonderte Betriebsentscheidungen.

Der [Gesamtstatus](status.md) enthält die verbleibenden technischen Gates.
