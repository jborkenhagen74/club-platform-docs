# Phasen 12 und 13: Kalender und Veranstaltungen

Die nativen Module `calendar` und `events` verwenden Schema 14, dieselben
Anwendungsdienste im Einzelplatzbetrieb und Server sowie gemeinsame Formulare
in Qt und Portal. Alle neuen Beschriftungen und Statuswerte liegen in den sieben
Sprachpaketen. Die Module müssen geladen, lizenziert, installiert und aktiviert sein.

## Lokal auf Deinem Mac testen

Einmalig die neue Zeitzonenabhängigkeit installieren und den bestehenden Build
neu konfigurieren (Qt weiterhin aus Deiner vorhandenen Installation):

```sh
brew install icu4c
export ICU_ROOT="$(brew --prefix icu4c)"
export QT_ROOT="$HOME/Qt/6.11.2/macos"
cmake --preset user-macos-vscode-debug -DQt6_DIR="$QT_ROOT/lib/cmake/Qt6"
cmake --build --preset user-macos-vscode-debug --parallel
ctest --test-dir build/user-macos-vscode-debug --output-on-failure
./scripts/run-dev-macos.sh
```

Der bisherige Build-Preset bleibt erhalten. Das Startskript findet Homebrew-ICU
automatisch und verwendet `runtime-extensions`, wo alle Entwicklungs-Module
zusammengeführt werden. Eine `.app` ist ein Verzeichnis; direkt ausgeführt wird
deren Datei `Contents/MacOS/clubplatform-desktop`.

Die nach [Lizenzanleitung](licensing-provisioning.md) signierte Testlizenz muss
`calendar` und `events` enthalten, für Gebühren außerdem `finance`. Eine Lizenz
mit ausschließlich den bisherigen Modulen schaltet die neuen Module nicht frei.
In **Erweiterungen → Installieren / aktualisieren** die Module installieren.
Vorhandene Datenbanken werden automatisch migriert; zuvor eine Sicherung erstellen.

## Bedienung

1. Mindestens eine Person und Organisation anlegen.
2. **Kalender** öffnen und **Neu laden** wählen. Beim Anlegen Titel,
   Beschreibung, Ort, Eigentümer, Beginn, Ende und Zeitzone eintragen.
   Desktop-Zeitangaben verwenden `2026-10-15T18:00`; im Portal gibt es Datumsfelder.
3. Wiederholung auswählen: keine, täglich, wöchentlich oder monatlich.
   Intervall und Anzahl bestimmen die endliche Serie. Speichern, danach neu laden.
4. Für einen eigenen Kalendertermin eine Erinnerung mit Minuten Vorlauf anlegen.
   Fällige Erinnerungen erscheinen in der geöffneten Kalenderansicht; dort lassen
   sie sich bestätigen. Die Ansicht aktualisiert sich alle 60 Sekunden.
5. **Veranstaltungen** öffnen: Organisation, verantwortliche Person, Kategorie,
   Termin, Anmeldebeginn, Anmeldeschluss, Platzanzahl und Gebühr angeben.
   Gebühren werden als Dezimalbetrag in der Organisationswährung eingetragen
   (`12,50` bedeutet bei EUR 12,50 Euro). Die Organisation legt diese Währung im Finanzmodul fest.
6. Einen Termin und eine Person zur Anmeldung auswählen. Bei kostenpflichtigen
   Terminen vorher ein Finanzkonto derselben Person und Organisation anlegen
   und dieses Konto bei Anmeldung oder Einladung auswählen.
7. Bei belegten Plätzen landen weitere Anmeldungen auf der Warteliste. Nach
   einer Absage den ersten Wartenden ausdrücklich auf „Bestätigt“ setzen.
   Einladungen reservieren keinen Platz. Anwesenheit kann ab Terminbeginn
   als „Teilgenommen“ oder „Nicht erschienen“ erfasst werden.
8. Einzelne Teilnahmen oder den ganzen Termin stornieren. Bestehende Gebühren
   werden durch Gegenbuchungen aufgehoben; Buchungen werden nicht gelöscht.

Nach Änderungen bewusst **Neu laden** wählen. Eine erfolgreiche Speicherung
bleibt auch dann erfolgreich, wenn die spätere Aktualisierung scheitert.
Veraltete Teilnehmerrevisionen oder Platzanzahlen führen zu einem Konflikt:
neu laden, aktuelle Daten prüfen und die Änderung erneut ausführen.

## Fachliche Regeln

- `events` funktioniert für kostenlose Veranstaltungen ohne `calendar` und ohne
  `finance`. Für Gebührenbuchung und Storno wird zusätzlich `finance.write`
  mit aktivem Finanzmodul verlangt. Ohne dieses Recht bleibt die gesamte Aktion
  einschließlich Teilnehmerzustand unverändert.
- `calendar.read`/`calendar.write` und `events.read`/`events.write` trennen Lesen
  und Verwaltung. Erinnerungen gehören dem angemeldeten Benutzer; andere Leser
  können sie weder sehen noch bestätigen. Kalendertermine selbst sind für alle
  Benutzer mit `calendar.read` sichtbar, keine privaten Kalender.
- Veranstaltungsprojektion im Kalender erfordert zusätzlich `events.read` und
  das aktive Ereignismodul. Eine Projektion erzeugt keine zweite Terminzeile.
  `events` veröffentlicht hierfür die Capability `calendar.source`.
- Anmeldungen sind innerhalb des einschließlich geltenden Anmeldefensters erlaubt.
  Bei einer Serie gilt das angegebene Fenster gemeinsam für alle Vorkommen.
  Platzprüfung, Warteliste, Gebühren, Idempotenz und Audit laufen in einer Transaktion.
- `registered`, `confirmed`, `attended`, `no_show` belegen einen Platz;
  `invited`, `waiting`, `cancelled` nicht. Wartende rücken in Anmeldereihenfolge
  ausdrücklich nach. Eine stornierte Teilnahme ist endgültig; erneute Anmeldung
  derselben Person zu demselben Vorkommen ist in dieser Version nicht vorgesehen.
- Absagen erzeugen höchstens eine Gegenbuchung pro Gebühr und lösen zugehörige
  Zahlungszuordnungen. Es erfolgt keine automatische Bankauszahlung.
- Unterstützte RRULE-Teilmenge: `FREQ=DAILY|WEEKLY|MONTHLY`, `COUNT=1..366`,
  optional `INTERVAL=1..365`. Unbekannte Parameter werden abgewiesen.
  Monatsserien überspringen nicht existierende Monatstage (31. Januar → 31. März).
- IANA-Zeitzonen werden mit ICU ausgewertet. Lokale Uhrzeiten bleiben über
  Sommerzeitwechsel erhalten. Nicht existierende Uhrzeiten weisen die gesamte
  Serie zurück; doppelte Uhrzeiten verwenden ausdrücklich „früher“ oder „später“.
  Ganztagstermine haben ein exklusives Enddatum und können 23 oder 25 Stunden dauern.
- Jahre 1970–2100, maximal 366 Tage pro Vorkommen. Abfragen umfassen höchstens
  366 Tage und 1000 Vorkommen je Quelle; für größere Bestände Zeitfenster verkleinern.

## REST-Vertrag

Basis `/api/v1`, Bearer-Sitzung erforderlich. Listen:
`GET /calendar?from=<Unixsekunden>&until=<Unixsekunden>` und entsprechend `/events`.
Zeitfenster sind halboffen; auch überlappende Termine werden geliefert.
Antwort: `occurrences`, `participants`, `reminders`, `persons`, `organizations`,
`accounts`, `now`. Teilnehmer werden nur in der Veranstaltungsansicht geliefert;
Finanzkonten nur bei zusätzlicher Finanz-Leseberechtigung.

Schreiben: `POST /{calendar|events}/commands/{operation}` mit maximal 16 KiB JSON.
Jeder Befehl trägt eine eindeutige `source_id` (maximal 128 Zeichen).
Identische Wiederholung desselben Benutzers liefert dasselbe Ergebnis;
geänderte Nutzlast bei gleicher ID führt zu HTTP 409.
Zahlenwerte wie Kapazität, Geldbetrag, Minuten und Revision sind kanonische
nichtnegative Dezimalstrings. `all_day` ist boolesch.

| Modul | Operation | Wesentliche Felder neben `source_id` |
|---|---|---|
| Beide | `create` | `title`, `description`, `location`, `start`, `end`, `timezone`, `all_day`, optional `rrule`, `fold` |
| Kalender | `create` zusätzlich | `owner_id` |
| Events | `create` zusätzlich | `organization_id`, `responsible_person`, `category`, `registration_start`, `registration_deadline`, `capacity`, `fee`, `currency` (Organisationswährung; REST-`fee` bleibt ganzzahlig in kleinsten Einheiten) |
| Beide | `cancel` | `occurrence_id` |
| Kalender | `remind` | `occurrence_id`, `minutes_before` |
| Kalender | `acknowledge` | `reminder_id` |
| Events | `register` | `occurrence_id`, `person_id`, optional `account_id`, `status` (`registered` oder `invited`) |
| Events | `participant` | `participant_id`, `revision`, `status` |
| Events | `capacity` | `occurrence_id`, `previous_capacity`, `capacity` |

HTTP 400: ungültige Eingabe/Zeiten; 401: keine gültige Sitzung; 403: fehlende
Lizenz/Berechtigung; 404: unbekanntes Objekt; 409: Zustand/Revision/Idempotenzkonflikt.
Transportfehler dürfen mit unveränderter Nutzlast und gleicher `source_id`
wiederholt werden.

## Abnahme und Grenzen

Foundation-Tests laufen gegen SQLite und in CI auch PostgreSQL, einschließlich
Zeitumstellung, kostenloser Modulunabhängigkeit, konkurrierender Platzvergabe,
Warteliste, Rechte, Lizenzentzug, Gebührenstorno und Audit-Rollback.
Ein echter HTTP-Host prüft die REST-Grenze. Playwright deckt das Kalenderformular
auf Desktop und Mobilgeräten ab. Qt-Build und macOS-Installation bleiben eigene
CI-Gates. Ein lokaler Portal-Build ersetzt diese Laufzeittests nicht.

Bewusster Umfang: keine E-Mail-/Push-Zustellung, kein Hintergrund-Reminderdienst
bei geschlossener Anwendung, kein iCalendar-Import/Export, keine freien RRULE-
Zusatzregeln und keine Drag-and-drop-Serienbearbeitung. Termine werden angelegt
oder einzelne Vorkommen abgesagt; Terminänderungen erfolgen durch Ersatztermine.

Die vorherige Pipeline-Ursache `stack-use-after-scope` in
`finance_sessions.cpp` wurde durch stabile Listenlebensdauer korrigiert.
Auswahllisten in den Finanz- und Terminformularen haben explizite zugängliche
Beschriftungen, damit Optionen die Feldnamen nicht verändern.

Die überarbeitete Monatsansicht, kompakte Zuordnungsdialoge und die Sichtbarkeit
lizenzierter Module sind unter [Bedienung und lokale Prüfung](usability.md) beschrieben.
