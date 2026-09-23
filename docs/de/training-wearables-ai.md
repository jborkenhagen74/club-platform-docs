# Wearable-Import, Trainingsauswertung und lokale KI

Stand: 23.09.2026 · Feature-Branch `feature/training-wearable-import`.
Training-Extension 1.1.0, Extension-Schema 2, Host-Schema 19, ABI V3.
Dieser Stand ergänzt die [Trainings- und Anwesenheitsbasis](../training-attendance.md).
Er ist ein Entwicklungsstand, noch kein veröffentlichtes Pilot-Update.

## Abgleich mit dem Konzept vom 21.09.2026

| Konzept | Implementierter Stand | Noch offen |
|---|---|---|
| Sportneutraler Trainingskern | Separate Analysebibliothek, Geräte/manuelle Einheiten, importierte Einheiten mit Samples, Segmenten und Qualitätsangaben | Persistente Athletenprofile, individuelle Zonenversionen, Recovery-Daten |
| Nachvollziehbare Imports | Unveränderte UTF-8-Datei im Import-Batch, SHA-256, eindeutige Person/Quelle/Einheit, transaktionaler Import | Hintergrundimport großer Archive, Korrektur-/Löschverfahren |
| Anbieter | CSV mit Mapping, normalisiertes JSON, TCX, GPX, Apple-Health-XML | Verifizierte Mi-Fitness-Beispieldatei, Android-Health-Connect-App, Strava-OAuth-Synchronisation |
| Berechnungen | Version `training-v1`, zeitgewichteter Puls, Zonenzeiten, Abdeckung, Messlücken, Session-RPE-Last | Erweiterte Recovery-/Belastungsmodelle, Taekwondo-spezifische Metriken |
| Grafiken | Pulskurve, Zonenanteile, Wochen-/Monatsdauer, Einheitenvergleich in Desktop und Portal | Überlagerung normalisierter Pulskurven, weitergehende Filter und Vergleichsberichte |
| Berechtigungen | Explizite Person, Speicherfreigabe, benannte Trainerfreigaben, getrennte Rohdaten-/KI-Zwecke, Audit, Widerruf | Sorgeberechtigtenverfahren, Aufbewahrungs-/Löschprozess, gesonderter Exportdienst |
| KI | Optionaler lokaler Chat-Completions-Dienst; ausschließlich berechnete Kennzahlen; keine Datenbank-/Aktionswerkzeuge | Frei wählbarer entfernter Self-hosted-/Cloud-Endpunkt, persistierte Modell-/Promptversionen |
| Automatisierung | Kern benötigt kein n8n | Signierte Ereignisse und n8n-Workflows |

Diese Tabelle ist zugleich die offene Umsetzungsliste. Der generische CSV-Import
ist keine direkte Mi-Fitness-, Health-Connect- oder Strava-Kontoverbindung.
Anwesenheiten bleiben separat: Eine importierte Einheit erzeugt keine Teilnahme.

## Einrichtung und Rechte

1. Host und Desktop/Portal aus demselben Feature-Stand bauen und installieren.
   ICU, libxml2 und libcurl gehören bereits zu den Host-Abhängigkeiten.
2. Vor dem Update eine Datenbanksicherung erstellen. Der Host legt Migration 19
   an; anschließend unter **Erweiterungen** `training` auf Version 1.1.0 aktualisieren.
3. Eine gültige Lizenz mit Modul `training` verwenden. `attendance` ist optional
   und separat zu lizenzieren. Die KI benötigt keine zusätzliche Modul-ID.
4. Das Benutzerkonto mit der Sportlerperson verknüpfen. Im Personendossier unter
   **Training & Wearables → Freigaben** zunächst `purpose=storage`,
   `grantee_user_id` leer, `status=granted` speichern.
5. Rollenrechte und gegebenenfalls Trainerfreigaben gemäß Tabelle einrichten.

| Aktion | Rollenrechte zusätzlich zu `records.read` | Benötigte Freigabe |
|---|---|---|
| Vorschau/Import | `training.write`, `records.write` | Eigene Speicherfreigabe; Trainer zusätzlich `write` |
| Zeitraumauswertung | `training.read` | Eigene Speicherfreigabe; Trainer zusätzlich `summary` |
| Messreihe öffnen | `training.read` | Eigene Speicherfreigabe; Trainer zusätzlich `raw` |
| KI-Erklärung | `training.read`, `training.ai` | Speicher- und **immer ausdrücklich `ai`**, auch für sich selbst; Trainer zusätzlich `summary` |

Bei `ai`, `raw`, `summary` und `write` ist `grantee_user_id` die UUID des
begünstigten **Benutzerkontos**. Für eigene KI die eigene Benutzer-UUID eintragen.
Trainer benötigen weiterhin die passende Personenreichweite durch
`training.read.all`/`training.write.all` oder Organisationsrechte.
Ein Administrator-Wildcard ersetzt die Freigabe nicht.

Eine vorhandene Freigabe durch Änderung auf `withdrawn` widerrufen. Folgeanfragen
werden gesperrt; die KI-Antwort wird vor ihrer Rückgabe erneut autorisiert.
Der Widerruf löscht gespeicherte Dateien nicht. Eine bereits an den lokalen
KI-Prozess übergebene Anfrage kann dadurch nicht zurückgerufen werden.

## Datei importieren

1. Die gewünschte Person ausdrücklich auswählen und ihre Wearable-Auswertung öffnen.
2. Format wählen, eine stabile Quellenkennung eingeben, beispielsweise `watch-export`.
   Dieselbe Quelle bei späteren Imports beibehalten. Die Kennung ist ein Label,
   kein Nachweis einer Verbindung mit dem Hersteller.
3. UTF-8-Datei auswählen. Grenze: **2 MiB pro Datei**, höchstens 1.000 Einheiten
   und 100.000 Samples je normalisierter Einheit. ZIP-Dateien vorher entpacken.
4. Für CSV bei abweichenden Spaltennamen das Mapping eintragen.
5. **Vorschau** prüfen: Person, Bezeichnungen, Zeitpunkte und Messwertanzahlen.
6. **Training importieren** ausführen. Alle Einheiten werden zusammen gespeichert.
   Bei einem Fehler wird der ganze Batch zurückgerollt.
7. Den passenden Von-bis-Zeitraum einstellen und **Neu laden** klicken.

Identische Dateiinhalte für dieselbe Person und Quelle werden als bereits
importiert erkannt. Eine bekannte Einheitskennung in einer veränderten Datei
führt zu einem Konflikt; vorhandene Daten werden nicht überschrieben.
Gibt es keine externe Kennung, verwendet der Import Start, Ende und Aktivität.
Die Dateierkennung berücksichtigt keine nachträglich geänderte CSV-Zuordnung:
Ein Import ist kein Korrekturwerkzeug. Originaldateien unverändert aufbewahren.

### Unterstützte Dateiformate

- **JSON:** einzelne Einheit, Array von Einheiten oder Objekt mit `sessions`-Array.
- **CSV:** eine Zeile pro Messwert, gemeinsame Einheitskennung; Trennzeichen
  Komma, Semikolon oder Tab; Anführungszeichen und CRLF werden unterstützt.
- **TCX:** `TrainingCenterDatabase/Activities/Activity` mit Trackpoints und
  optional `HeartRateBpm/Value`. Der Zeitraum reicht vom ersten bis letzten
  Zeitstempel der Messreihe; separate Lap-Dauern werden noch nicht übernommen.
- **GPX:** Tracks mit Zeitstempeln und optionalem `hr`-Element in Extensions.
  Ohne Pulswerte kann eine Einheit zeitlich erfasst werden, hat aber keine
  berechenbare Pulskennzahl. GPS-Koordinaten werden nicht normalisiert, können
  jedoch in der unveränderten Originaldatei enthalten sein.
- **Apple Health:** `export.xml`, Workouts und
  `HKQuantityTypeIdentifierHeartRate`-Records mit Einheit `count/min`.
  Pulswerte werden anhand des Workout-Zeitfensters zugeordnet. Überlappende
  Workouts können deshalb dieselben Samples enthalten. Keine automatische
  Zusammenführung verschiedener Geräte. Große Gesamtexporte benötigen zuvor
  einen passend begrenzten Export; die Anwendung kürzt sie nicht stillschweigend.

Apple-Health-Elementdeklarationen sind erlaubt; externe DTDs und Entities werden
abgewiesen. Alle Adapter nutzen dieselbe Zeit-, Sample- und Dublettenvalidierung.
Die Tests verwenden synthetische Formatbeispiele, keine Kompatibilitätszusage
für jedes konkrete Geräte-/App-Exportformat.

### JSON-Beispiel

```json
{
  "external_id": "training-2026-09-23-1",
  "title": "Abendtraining",
  "activity": "taekwondo",
  "device": "watch-1",
  "start": "2026-09-23T18:00:00+02:00",
  "end": "2026-09-23T18:02:00+02:00",
  "rpe": 5,
  "samples": [
    {"timestamp": "2026-09-23T18:00:00+02:00", "heart_rate": 110},
    {"timestamp": "2026-09-23T18:00:10+02:00", "heart_rate": 120},
    {"timestamp": "2026-09-23T18:01:40+02:00", "heart_rate": 130}
  ],
  "segments": [
    {"label": "Technik", "start": "2026-09-23T18:00:00+02:00",
     "end": "2026-09-23T18:02:00+02:00"}
  ]
}
```

Zeiten benötigen einen expliziten UTC-Offset oder UTC-Epoch-Sekunden.
Sekundenbruchteile werden auf ganze Sekunden abgeschnitten. Gültiger Zeitbereich:
1970–2100; Einheit länger als null und höchstens 24 Stunden.
Identische Werte zum selben Zeitpunkt werden zusammengeführt; widersprüchliche
Werte am selben Zeitpunkt führen zur Ablehnung. Fehlende Pulswerte und Werte
außerhalb 20–260 werden als ungültig gezählt und aus der Messreihe ausgeschlossen.
Das ist ein technischer Prüfbereich, keine medizinische Bewertung.

### CSV-Beispiel

```csv
id,start,end,ts,hr
training-1,2026-09-23T16:00:00Z,2026-09-23T16:02:00Z,2026-09-23T16:00:00Z,110
training-1,2026-09-23T16:00:00Z,2026-09-23T16:02:00Z,2026-09-23T16:00:10Z,120
```

```json
{"delimiter":",","fields":{"external_id":"id","timestamp":"ts","heart_rate":"hr"}}
```

Ohne Mapping heißen Spalten wie die normalisierten Felder. `external_id`,
`start` und `end` sind Pflicht; Beginn und Ende müssen pro Einheit übereinstimmen.
CSV übernimmt derzeit keine Segmente oder RPE; dafür JSON verwenden.

## Diagramme und Kennzahlen lesen

Von- und Bis-Datum in der Oberfläche sind eingeschlossen. Intern wird nach dem
Start der Einheit in UTC gefiltert: `from <= start < until`. Die Oberfläche
setzt `until` auf den Folgetag. Eine Einheit wird nicht an Mitternacht geteilt.
Wochen beginnen montags, Monate am ersten Tag; Randperioden enthalten nur die
gewählten Einheiten. Leere Perioden werden nicht als Nullbalken ergänzt.

Vier aufsteigende Pulsgrenzen definieren fünf Zonen. Die angezeigten Beispielwerte
100/120/140/160 müssen bewusst angepasst werden; es gibt keine automatische
Altersformel oder gespeicherte individuelle Zonenkonfiguration.
Grenzwertgleichheit gehört zur jeweils höheren Zone.

- Die Pulskurve zeigt bpm über Minuten seit Trainingsbeginn. Lücken zwischen
  Messpunkten über 30 Sekunden werden nicht verbunden. Segmentgrenzen erscheinen
  zusätzlich als beschriftete Zeitintervalle.
- Die Analyse hält jeden gültigen Pulswert bis zum nächsten Sample, maximal
  30 Sekunden. Die restliche Zeit gilt als unbekannt. Eine verworfene Probe
  stoppt diesen begrenzten Hold nicht eigenständig.
- Der Durchschnittspuls wird nach abgedeckter Zeit gewichtet. Der Spitzenpuls
  ist der größte gültige Messwert. Fehlende Werte erscheinen als `—`/`null`.
- Zonenzeiten beziehen sich auf diese abgedeckte Zeit. Balken sind durch die
  gesamte Einheitsdauer normiert, damit Messlücken nicht verschwinden.
- Wochen-/Monatsbalken zeigen die Trainingsdauer in Minuten; Anzahl der
  importierten Einheiten steht daneben. Vergleichbare Aktivitäten auswählen.
- Session-RPE-Last = optionale subjektive RPE (0–10) × Dauer in Minuten,
  Einheit AU. Ohne RPE keine Last. Periodensummen enthalten nur bewertete
  Einheiten und geben deren Anzahl an. Das ist kein Verletzungsrisiko-Score.

## Lokale KI einrichten

Die KI ist optional. Ohne Dienst funktionieren Import und numerische Auswertung.
Sie läuft auf **dem Rechner des Hosts**: beim LocalClient im Desktop-Rechner,
beim RemoteClient neben dem Server, nicht im Browser des Sportlers.

1. Einen OpenAI-kompatiblen lokalen Chat-Completions-Dienst bereitstellen,
   beispielsweise `llama-server` aus llama.cpp mit einer passenden GGUF-Datei.
   Modell und Runtime sind nicht im Club-Platform-Installer enthalten.
2. Den Dienst ausschließlich an Loopback binden. Beispiel nach Installation
   von llama.cpp und Bereitstellung eines Modells als `models/training.gguf`:

```sh
llama-server -m models/training.gguf --host 127.0.0.1 --port 8081
```

3. Vor dem Start von Club Platform dessen Host-Umgebung konfigurieren:

```sh
export CLUBPLATFORM_TRAINING_AI_URL=http://127.0.0.1:8081/v1/chat/completions
export CLUBPLATFORM_TRAINING_AI_MODEL=local
```

PowerShell:

```powershell
$env:CLUBPLATFORM_TRAINING_AI_URL = 'http://127.0.0.1:8081/v1/chat/completions'
$env:CLUBPLATFORM_TRAINING_AI_MODEL = 'local'
```

4. Host aus dieser Umgebung starten. Bei Start über Finder oder einen
   Systemdienst müssen die Variablen in dessen Startkonfiguration gesetzt sein;
   ein Export in einem anderen Terminal reicht nicht.
5. Die benannte `ai`-Freigabe und das Rollenrecht `training.ai` einrichten.
6. In der Auswertung Zeitraum und Zonen festlegen, **Lokale KI-Erklärung** wählen.

Erlaubt ist ausschließlich `http://127.0.0.1:<port>/v1/chat/completions`.
Keine Weiterleitungen, Proxys, Cloud-Adressen oder API-Schlüssel in dieser
Ausbaustufe. Verbindungstimeout 3 Sekunden, Gesamtzeit 12 Sekunden; ein langsames
Modell liefert einen sichtbaren Fehler. Der RemoteClient wartet bis zu 20 Sekunden.
Maximal 32 KB berechnete Eingabedaten, 64 KB Antwort und 12.000 Zeichen Erklärung.

Übertragen werden Zeitabdeckung, Pulskennzahlen, Zonen und RPE-Last. Entfernt
werden Personen-/Datensatzkennungen, Titel, Aktivitäten, Zeitstempel, Rohdatei
und Samples. Der lokale Dienst erhält keine Datenbankverbindung, Werkzeuge,
Dateizugriffe oder ausführbaren Aufgaben von Club Platform. Seine eigene
Konfiguration und Protokollierung bleiben Verantwortung des Betreibers.

Die Erklärung wird als generierter Klartext angezeigt. Sie kann falsch sein
und muss mit den Kennzahlen abgeglichen werden. Der Prompt verlangt deutsche
Erläuterungen ohne Diagnosen, erfundene Messwerte oder neue Berechnungen.
Die Anwendung ersetzt bei Fehlern keinen echten Modellaufruf durch Beispieltext.

## REST und Betrieb

Authentifizierte POST-Endpunkte:

```text
/api/v1/training/commands/preview
/api/v1/training/commands/import
/api/v1/training/commands/summary
/api/v1/training/commands/detail
/api/v1/training/commands/ai
```

Alle Anfragen enthalten `person_id`. Import/Vorschau zusätzlich `format`,
`provider`, `content` und optional `mapping`. Detail benötigt `id`.
Summary/KI benötigen `from`, `until` und `zone_boundaries` (Array aus vier Zahlen).
Die Grenzen sind exklusiv/inklusiv wie oben beschrieben.

Fehler: 400 ungültige Eingaben, 403 fehlende Rechte/Freigaben, 404 unbekannte
Einheit, 409 Dublette mit verändertem Inhalt oder nicht verfügbarer KI-Dienst.
Import-Batches, Samples und Einheiten liegen in der Host-Datenbank und sind
Bestandteil ihrer Sicherung. Rohdateien können zusätzliche sensible Daten
enthalten, auch wenn die normalisierte Ansicht diese nicht zeigt.

## Prüfung vor Freigabe

```sh
ctest --test-dir BUILD --output-on-failure -R 'clubplatform-(training-|language-packs|foundation-sqlite)'
npm run build --prefix apps/portal
```

Automatische Tests prüfen Zeitzonen, Schaltjahre, CSV-Mapping, XML-Formate,
DTD-/Entity-Ablehnung, Messlücken, Zonen, Dubletten, Transaktionen, Freigaben
und tatsächliche HTTP-Kommunikation mit einem lokalen KI-Testdienst.
Der KI-Test kontrolliert entfernte Identitäten und blockierten Aufruf nach Widerruf.
Desktop/QML sowie Windows/macOS müssen zusätzlich in der nativen CI geprüft werden.
