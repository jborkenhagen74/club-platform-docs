# Operative Module und Auswertungen

Stand: 24.09.2026.

## Rechte und Reichweite

| Daten / Aktion | Erforderliche Rechte | Einwilligung |
|---|---|---|
| Teilnahmen lesen | `records.read`, `attendance.read`, Personenreichweite | Nein |
| Teilnahmen anlegen / bearbeiten | `records.write`, `attendance.write`, Personenreichweite | Nein |
| Teilnahmeübersicht | `records.read`, `attendance.read`, `attendance.summary`, Lesereichweite | Nein |
| Geräte lesen / verwalten | `records.read` / `records.write`, `training.read` / `training.write`, jeweilige Reichweite | Nein |
| Trainingseinheiten, Wearables, Rohdaten, KI, externe Weitergabe | Bestehende aktionsbezogene Rechte und Freigaben | Weiterhin erforderlich; kein Wildcard-Bypass |
| Kostenlose Veranstaltung erstellen | `events.write` und Organisationsreichweite | Keine Trainingsfreigabe |
| Kostenpflichtige Veranstaltung erstellen | Zusätzlich `finance.write` und freigeschaltetes Finanzmodul | Keine Trainingsfreigabe |

Reichweite: eigene verknüpfte Person, `<modul>.<aktion>.organization` mit aktiver
Funktion in der Organisation und aktiver Mitgliedschaft/Funktion der Zielperson,
oder `<modul>.<aktion>.all`. Die Bereichsrechte ersetzen das Grundrecht nicht.
`*` erfüllt Grund- und Bereichsrechte. Lizenz, Modulinstallation, Validierungen,
Archivierungs-/Löschrechte und sensible Freigaben gelten weiterhin.

## Webportal und Qt-Desktop

- **Training & Wearables**: Person wählen; Geräte, manuelle Trainingseinheiten und
  Freigaben über eigene Tabs. Import, Profil, Recovery und Datenverwaltung sind
  über den Wearable-Bereich erreichbar.
- **Trainingsanwesenheit**: Person wählen; Teilnahmen mit Einheitskennung, Datum,
  Status, optionaler Leistungsbewertung und Notizen anlegen. Statuswerte sind
  `present`, `late`, `absent`, `excused`. Bestehende Freigaben sind kompatibel
  weiterhin sichtbar, aber keine Voraussetzung für diese Vorgänge.
- **Kampfsport**: eigener Modulbereich mit Tabs für Graduierungen, Prüfungen und
  Lizenzen statt Navigation auf den ersten zufälligen Datensatztyp.
- **Veranstaltungen**: eigener Veranstaltungsbereich; keine zusätzliche generische
  Kopie in der Modulnavigation.
- **Administration** bleibt ein eigener Bereich. Modulmenüs berücksichtigen die
  vom Server gelieferten Leserechte. Schreibaktionen benötigen weiterhin die
  serverseitige Autorisierung für die ausgewählte Person.

Beim Personenwechsel werden Entwürfe nur nach bestätigtem Verwerfen aufgegeben.
Modulnavigation verwendet `training` beziehungsweise `module:<id>`; der
Extension-Katalog liefert zusätzlich Arbeitsbereich und effektive Lese-/Schreibrechte.

## Schreibgeschützte Auswertungen

**Auswertungen** enthält keine Erstellen-, Bearbeiten- oder Löschaktionen und führt
nicht in die Verwaltung. Auswahlmöglichkeiten sind Personen, Organisationen,
Finanzen, Training, Anwesenheiten und die Datensatztypen weiterer Module.
Personenbezogene Berichte verlangen eine ausdrückliche Personenauswahl.

- Anwesenheiten: monatliche Zusammenfassung, Datumsgrenzen einschließlich.
- Training: bestehende Zusammenfassung der importierten Einheiten; letzter Tag
  bis zum folgenden UTC-Tagesanfang. Einwilligungsprüfung bleibt aktiv.
- Finanzen: Buchungen der zugänglichen Personenkonten im Buchungszeitraum;
  Beträge werden mit Währung dargestellt.
- Sonstige Datensätze: Suche und optionaler Datumsfeldfilter. Ohne gewähltes
  Datumsfeld wird ausdrücklich angezeigt, dass der Zeitraum nicht filtert.
  Alle Listenseiten werden gelesen, oberhalb von 5000 Zeilen muss der Filter
  eingegrenzt werden; keine still abgeschnittenen Berichte.

Filteränderungen verwerfen das alte Ergebnis. Im Portal exportiert **CSV
exportieren** die sichtbaren Ergebniszeilen (mit Schutz vor Tabellenformeln).
Der Desktop exportiert JSON mit Filtermetadaten und Ergebniszeilen. Beide Wege
nutzen dieselben autorisierten Lesedienste; sie schreiben keine Fachdaten.

## Prüfung

Regressionstests decken die operative Consent-Ausnahme, fehlende Reichweite,
Organisationszuordnung einschließlich beendeter Mitgliedschaft, bestehende sensible
Consent-Sperren und kostenlose/kostenpflichtige Veranstaltungen ab. Der Portaltest
`workspaces.spec.ts` erstellt eine Teilnahme ohne Consent und prüft die getrennte
Navigation sowie eine schreibgeschützte Auswertung einschließlich Export auf
Desktop- und Mobilauflösung. Feature-/PR-Änderungen aktivieren keine automatischen
Actions-Läufe.
