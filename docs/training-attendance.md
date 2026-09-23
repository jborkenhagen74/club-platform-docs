# Training & Wearables und Trainingsanwesenheit – erster Ausbau

Stand: 22.09.2026. Branch `feature/training-attendance`, auf dem deklarativen
Extension-Refactoring aufgebaut. Beide Module verwenden ABI V3 und eingebettete
JSON-Definitionen. Ein nachträgliches Bearbeiten externer JSON-Dateien ändert keine
installierte Binärdatei.

## Umfang und Abgrenzung

| Modul-ID | Funktion dieses Ausbaus |
|---|---|
| `training` | Personenbezogene Geräte und manuell erfasste Trainingseinheiten; eigene Freigaben |
| `attendance` | Teilnahme und Leistungsbewertung je Sportler/Einheit; personenbezogene Zeitraumauswertung; eigene Freigaben |

`attendance` funktioniert ohne `training`. Eine Anwesenheit ist keine automatisch
importierte Wearable-Trainingseinheit. Beide dürfen dieselbe fachliche
`session_key` verwenden, werden aber nicht automatisch synchronisiert.

Die weiterführenden Wearable-Importe, Messreihen, grafischen Auswertungen und die
lokale KI-Anbindung sind im [Wearable-Handbuch](de/training-wearables-ai.md)
beschrieben. Dort steht auch der genaue Abgleich mit den noch offenen Punkten
des ursprünglichen Konzepts. Die Anwesenheitsleistung bleibt eine manuelle
Bewertung und ist keine medizinische Aussage.

## Build, Installation und Lizenz

Die bestehenden Build-Profile und Installer nehmen die beiden Module über
CMake `install(TARGETS ...)` automatisch in `extensions/` auf. Für lokale Builds
werden die Module zusätzlich nach `runtime-extensions/` kopiert. Die Publisher-
Oberfläche bietet **Training & Wearables** und **Trainingsanwesenheit** als
separat lizenzierbare Optionen an. Eine bisherige Lizenz schaltet neue Module
nicht automatisch frei.

1. Den Feature-Branch bauen, wie in der bestehenden
   [Build-Anleitung](build-installers-publisher.md) beschrieben.
2. Im Publishing-Tool die benötigten Module wählen, eine Lizenz für die
   Installation ausstellen und importieren; gegebenenfalls aktivieren.
3. Unter **Erweiterungen** die gewünschten Module installieren/aktualisieren.
4. Die Rollen um die benötigten Modulrechte und `records.*`-Rechte ergänzen.
5. Benutzerkonten mit den zugehörigen Personen verknüpfen.

Quellen: `extensions/training/`, `extensions/attendance/`;
native Validierung/Auswertung: `extensions/training-support/module.cpp`.
Die Host-Freigabeprüfung liegt zentral in
`src/application/src/training_scope.hpp` und gilt für LocalClient und REST.

## Freigaben und Rechte

Ein Administrator erhält durch `*` **keinen automatischen Trainingszugriff auf
andere Personen**. Jede Person verwaltet ihre eigenen Freigaben im jeweiligen
Personendossier. Dafür benötigt ihr verknüpftes Konto die Modulrechte
`<modul>.read`, `<modul>.write`, `records.read` und `records.write`.
Die Freigaben sind für `training` und `attendance` getrennt.

Im jeweiligen Tab **Freigaben** einen Datensatz anlegen:

| Feld | Werte und Bedeutung |
|---|---|
| `purpose` | `storage`: Erfassung/Nutzung eigener Daten; `summary`: Übersichten; `records`: einzelne Datensätze; `write`: Änderungen durch einen anderen Benutzer |
| `grantee_user_id` | Bei `storage` leer, ansonsten die UUID des begünstigten Benutzerkontos (keine Personen-ID, kein Loginname) |
| `status` | `granted` oder `withdrawn` |

Zuerst eine Freigabe mit `purpose=storage`, leerer Benutzer-ID und
`status=granted` anlegen. Erst danach können Daten erfasst werden.
Für Trainer je gewünschtem Zugriff einen zusätzlichen Freigabedatensatz
anlegen. Freigaben ersetzen keine Rollenrechte:

- Lesen einzelner Datensätze: `<modul>.read`, `records.read`, passende
  Personenreichweite und Freigabe `records`.
- Änderungen: `<modul>.write`, `records.write`, passende Personenreichweite und
  Freigabe `write`; Archivieren/Wiederherstellen benötigt zusätzlich die
  entsprechenden bestehenden Modul-/Datensatzrechte.
- Anwesenheitsübersicht: `attendance.read`, `attendance.summary`, `records.read`,
  passende Personenreichweite und Freigabe `summary`.
- Personenreichweite: bestehende Organisationszuordnung mit
  `<modul>.read.organization` / `<modul>.write.organization` oder explizite
  `<modul>.read.all` / `<modul>.write.all`. Auch `.all` ersetzt keine Freigabe.

Zum Widerrufen den vorhandenen Freigabedatensatz auf `withdrawn` ändern.
Freigaben werden nicht archiviert/gelöscht; ihre Änderungen bleiben auditierbar.
Pro Person, Zweck und begünstigtem Benutzer existiert höchstens eine aktive
Freigabe. Eine Änderung wird mit Akteur, Person, Zweck, Empfänger, Status,
Policy-Version und Zeitstempel protokolliert. Änderungen an Trainingsdaten und
Lesezugriffe auf Datensätze/Übersichten werden ebenfalls protokolliert.

Ein Widerruf sperrt nachfolgende Serverzugriffe sofort. Bereits angezeigte Daten
werden dadurch nicht aus dem Gedächtnis oder Bildschirm eines Empfängers entfernt.
Ein Widerruf von `storage` sperrt die Nutzung der Trainingsdaten für alle; die
Person kann ihre Freigaben weiterhin bearbeiten. Bestehende Datensätze werden
nicht automatisch gelöscht. Ein automatischer Aufbewahrungs-/Löschprozess sowie
Freigaben durch Sorgeberechtigte sind noch nicht Bestandteil dieses Ausbaus.

## Anwesenheit und Leistung erfassen

1. **Personen** öffnen, Sportler auswählen und das Personendossier öffnen.
2. Unter dem Modul **Trainingsanwesenheit** die **Freigaben** wie oben einrichten.
3. Zum Tab **Teilnahmen** wechseln und einen Datensatz anlegen.
4. `session_key`: stabile, eindeutige Kennung der Einheit, z. B.
   `tkd-2026-09-22-1800`. Dieselbe Einheit darf bei vielen Sportlern vorkommen,
   aber nur einmal je Sportler. Für eine zweite Einheit am selben Tag eine
   andere Kennung verwenden. Bereits erfasste Teilnahmen über **Bearbeiten**
   ändern, nicht erneut anlegen.
5. `training_date`: lokales fachliches Trainingsdatum `YYYY-MM-DD`;
   `title`: verständliche Trainingsbezeichnung.
6. `status`: `present` (anwesend), `late` (verspätet), `absent` (abwesend) oder
   `excused` (entschuldigt). In diesem Ausbau werden die Codes als Text eingegeben.
7. `performance`: optional eine ganze Zahl von **0 bis 10**. Die Trainer sollten
   die Bedeutung der Skala vorab gemeinsam festlegen. Für `absent`/`excused`
   bleibt das Feld leer. Notizen sind optional.
8. Speichern. Ungültige Daten und doppelte Kennungen werden abgewiesen.

Archivierte Teilnahmen fließen nicht in Auswertungen ein. Beim Wiederherstellen
wird erneut auf doppelte Einheitskennungen geprüft. Gleichzeitige Änderungen
verwenden die bestehende Revisionsprüfung.

## Auswertungen in Desktop und Webportal

Im Personendossier **Trainingsübersicht** öffnen:

1. Von- und Bis-Datum auswählen, **Neu laden** ausführen. Beide Grenzen zählen
   einschließlich; voreingestellt ist das laufende Jahr bis heute.
2. Die Gesamtzeile zeigt Teilnahmen, bewertete Teilnahmen und Durchschnitt für
   genau diesen frei gewählten Zeitraum.
3. Die Gruppierung auf **Pro Woche**, **Pro Monat** oder **Pro Jahr** stellen.
   Wochen beginnen montags; als Wochenkennung erscheint das Montagsdatum.
   Damit bleibt eine Woche über den Jahreswechsel zusammen.
4. Für einen einzelnen Monat/ein einzelnes Jahr dessen Anfang und Ende als
   Zeitraum setzen. Für eine beliebige Periode beliebige Von-bis-Daten verwenden.

`present` und `late` zählen als Teilnahme. Mehrere Einheiten an einem Tag zählen
mehrfach. Abwesende/entschuldigte Einträge zählen nicht als Teilnahme.
Der Durchschnitt ist die Summe der Bewertungen geteilt durch die Anzahl der
**bewerteten Teilnahmen**, nicht der Mittelwert der Wochenmittelwerte.
Eine echte 0 zählt mit; ein leeres Bewertungsfeld nicht. Bei fehlenden Bewertungen
erscheint `—` (API: `null`). Gruppen ohne jegliche Einträge werden nicht als
zusätzliche Nullzeilen aufgeführt. Teilwochen am Rand enthalten nur die Einträge
innerhalb des gewählten Zeitraums.

Die API liefert zusätzlich Abwesenheits-/Entschuldigungszahlen und die
Algorithmusversion `attendance-v1`. Auswertungen berücksichtigen sämtliche
passenden aktiven Einträge, unabhängig von der 100-Einträge-Seitengröße der
normalen Listen.

## Training & Wearables: erste manuelle Datenbasis

Nach separater `training`-Speicherfreigabe:

- **Geräte**: Hersteller, Modell, Gerätekennung und Datenquelle eintragen.
  Datenquelle + Gerätekennung sind pro Person eindeutig.
- **Trainingseinheiten**: Kennung, Datum, Bezeichnung, Sport/Aktivität,
  Dauer in Minuten (1–1440), optionale Notizen erfassen.

Die Person ist immer explizit vorgegeben. Es findet weder eine automatische
Namenszuordnung noch eine Verbindung mit einem Wearable-Anbieterkonto statt.

## REST-Vertrag für Integrationen

Authentifizierte bestehende Management-API, z. B.:

```http
POST /api/v1/management/ext:attendance.entry
Authorization: Bearer <session-token>
Content-Type: application/json
```

```json
{
  "id": "",
  "revision": "0",
  "values": {
    "person_id": "UUID-DER-PERSON",
    "session_key": "tkd-2026-09-22-1800",
    "training_date": "2026-09-22",
    "title": "Abendtraining",
    "status": "present",
    "performance": "8",
    "notes": ""
  }
}
```

Alle definierten Werte werden als Strings übertragen, auch optionale leere
Felder. Zum Ändern die zurückgegebenen `id` und `revision` verwenden.
Die Typen heißen `training.device`, `training.session`, `training.consent`,
`attendance.entry`, `attendance.consent`.

Listen: `GET /api/v1/management/ext:attendance.entry?owner=<person-uuid>`.
Ein fehlender Personenfilter wird für beide Module abgewiesen, auch für Admins.

Übersicht:
`GET /api/v1/module-dossiers/attendance/person/<person-uuid>?from=<unix-seconds>&until=<unix-seconds>`.
Zeitgrenzen sind UTC-Mitternacht des jeweiligen fachlichen Datums, **inklusiv**.
Gültige Daten beginnen am 01.01.1900; die maximale Anfrage umfasst 36.600 Tage.
Ungültige/umgekehrte Bereiche werden abgewiesen. Die Antwort enthält
`person_id`, `from`, `until`, `algorithm_version`, `total`, `weekly`, `monthly`,
`yearly`; jede Statistik enthält `attended`, `rated`, `average`, `absent`, `excused`.
Es gibt keine Möglichkeit, die personenbezogene Prüfung über eine andere
Listenseite oder einen archivierten Datensatz zu umgehen.

## Prüfungen

- `clubplatform-training-modules`: tatsächliche native Module, Validierung,
  Schaltjahr, Jahreswechsel, inklusive Grenzen, unbewertete/Null-Leistung,
  gewichtete Durchschnitte, >100 Einträge und Referenzschutz.
- `clubplatform-training-http`: echter Server mit temporärer SQLite-Datenbank
  und Testlizenz, Freigaben, Admin-Abweisung, getrennte Zugriffsarten,
  Widerruf, Dubletten und Wiederherstellung sowie vollständige Auswertungen.
- Bestehender `clubplatform-extension-definitions`-Test sichert weiterhin die
  unveränderten Verträge der bisherigen sieben Extensions.

```sh
ctest --test-dir <build-directory> --output-on-failure -R 'clubplatform-(training-|extension-definitions)'
```

Die Tests erzeugen eigene kurzlebige Lizenzschlüssel; Produktionsschlüssel
werden dafür nicht benötigt.
