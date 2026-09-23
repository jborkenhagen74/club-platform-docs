# Wearable-Import, Trainingsauswertung und lokale KI

Stand: 23.09.2026 · Feature-Branch `feature/training-wearable-import`.
Training-Extension 1.4.0, Extension-Schema 4, Host-Schema 21, ABI V3.
Dieser Stand ergänzt die [Trainings- und Anwesenheitsbasis](../training-attendance.md).
Er ist ein Entwicklungsstand, noch kein veröffentlichtes Pilot-Update.

## Abgleich mit dem Konzept vom 21.09.2026

| Konzept | Implementierter Stand | Betriebsabnahme / Grenze |
|---|---|---|
| Trainingskern | Versionierte Zonen, Athletenprofil mit Größe, Gewicht, Ruhe-/Maximalpuls, Erfahrung, Trainingsziel und dominanter Seite; Recovery-Baseline | Keine klinisch validierte Diagnose oder Verletzungsprognose |
| Imports und Korrekturen | Original und Hash unverändert; begründete Messwert-/Zeitkorrekturen, Historie, Revisionen, Export, Löschung, Hintergrundaufträge | Originale bleiben bis zur bestätigten Löschung erhalten |
| Anbieter | CSV, JSON, TCX, GPX, Apple Health, Mi Fitness; Android-Health-Connect-Begleiter; private Strava-OAuth-Liveansicht | Health Connect auf realem Gerät und Strava mit registriertem App-Konto abnehmen |
| Berechnungen | Zeitgewichteter Puls, Zonen, Abdeckung, RPE-Last; 7-/28-Tage-Last, Monotonie, Strain; persönliche 28-Tage-Recovery-Baseline; Runden-/Segmentmetriken und manuelle Taekwondo-Zähler | Fehlende Daten bleiben unbekannt; keine automatische Erkennung von Treffern aus Pulsdaten |
| Berichte | Kurven, Zonen, Wochen/Monate, 2–4 Kurven; Dauer-/Abdeckungs-/RPE-Filter; PDF-Berichte in Portal und Desktop | Portal-PDF kann geladene Vergleichskurven einschließen; Desktop-PDF vergleicht Kennzahlen und Segmente tabellarisch |
| Berechtigungen | Getrennte Freigaben; zusätzliches Rohkorrekturrecht; Sorgeberechtigte, Widerruf, automatische Löschung | Prüfung von Sorgeberechtigungsnachweisen bleibt organisatorisch |
| KI | OpenAI-kompatible Chat-Completions und native Ollama-API; echte TLS-Vertragsprüfung mit Testserver; Ed25519-/SHA-256-Prüfung von GGUF-Paketen | Ein konkretes externes Anbieter-Konto und das tatsächlich geladene Runtime-Modell sind damit nicht attestiert |
| Automatisierung | Signierter Abruf, dauerhafter Webhook-Dispatcher, Wiederholungen, n8n-Prüfvorlage | Die tatsächliche n8n-Installation nimmt der Betreiber manuell ab |

Die Entwicklungsfunktionen sind umgesetzt. Die genannten Betriebsabnahmen sind
keine bereits durchgeführten Live-Tests. Strava-API-Daten werden wegen der seit
01.06.2026 geltenden Anbietervorgaben weder importiert noch mit anderen Daten oder
KI ausgewertet. Quellen: [Strava API Policy](https://www.strava.com/legal/api_policy),
[Health Connect](https://developer.android.com/health-and-fitness/health-connect/get-started).
Anwesenheiten bleiben separat: Eine importierte Einheit erzeugt keine Teilnahme.

## Neue Arbeitsbereiche in Desktop und Portal

Die Trainingsansicht trennt **Auswertung**, **Import**, **Trainingsprofil**,
**Recovery** und **Datenverwaltung**. Erstellung und Datenverwaltung stehen
so außerhalb der eigentlichen Auswertung. Alle Texte liegen in den sieben
Sprachpaketen; Diagramme verwenden die Oberflächenfarbe und unterschiedliche
Linienarten, damit der Vergleich auch bei hohem Kontrast verständlich bleibt.

### Trainingsprofil und Zonenversionen

1. **Trainingsprofil → Neu laden** öffnet den aktuellen Stand. Version 0 bedeutet:
   noch kein Profil gespeichert.
2. Vier aufsteigende Pulsgrenzen zwischen 20 und 260 eingeben und speichern.
   Es erfolgt keine automatische altersabhängige Zonenvorgabe.
3. Jede Speicherung erzeugt eine neue unveränderliche Profilversion. Gleichzeitige
   Änderungen werden mit einem Konflikt abgewiesen; danach neu laden.
4. Unter **Auswertung** die Option **Gespeicherte Pulszonen verwenden** aktivieren.
   Ohne diese Option gelten die vier explizit eingegebenen Grenzen.
5. Die API kann mit `zone_boundaries: null` und `profile_revision: 1` eine frühere
   Konfiguration verwenden. Ohne Revisionsangabe gilt das neueste Profil.
   Antworten nennen die verwendete `profile_revision`; 0 steht für manuelle Grenzen.

Die Version ist eine Berechnungskonfiguration, keine rückwirkende Änderung einer
Originalmessung. Zusätzlich sind Größe (cm), Gewicht (kg), Ruhepuls, gemessener
Maximalpuls, Erfahrung (Jahre), geplante Trainingstage/Woche, dominante Seite und
Trainingsziel optional. Leere Zahlen bedeuten unbekannt. Diese Werte ändern die
expliziten Zonengrenzen nicht automatisch. Das Profil ist kein medizinischer Pass.

### Recovery erfassen

Unter **Recovery** zunächst die Einträge laden. Den Zeitraum dafür unter
**Auswertung** einstellen. Ein vorhandener Tag kann ausgewählt und bearbeitet
werden; für einen neuen Tag das Datum eingeben. Die API verwendet Mitternacht UTC.

Optionale Werte: Schlafstunden (0–24), Müdigkeit und Muskelkater (je 0–10),
Ruhepuls (0–260 bpm) sowie HRV (0–1000 ms). Leer bedeutet unbekannt, nicht null
Stunden oder optimale Erholung. Die Grenzen sind technische Eingabegrenzen.
Die Anwendung erstellt daraus keinen medizinischen Erholungs- oder Risikoscore.
Speichern prüft die Revision, damit ein anderer Bearbeiter nicht überschrieben wird.
Trainer benötigen für die Detailansicht die `raw`-Freigabe, zum Schreiben `write`.

### Vergleichen und korrigieren

Aktivitäts- und Gerätefilter vergleichen den vollständigen gespeicherten Wert;
leer bedeutet alle. In der Einheitenliste zwei bis vier Einheiten markieren und
**Kurven vergleichen** wählen. Die Zeitachse ist auf 0–100 % der jeweiligen Dauer
normiert. Lücken über 30 Sekunden werden weiterhin nicht verbunden; es werden
keine künstlichen Messwerte interpoliert. Die Linienarten entsprechen der Legende.
Ein gleicher Prozentwert ist keine Zusage gleicher sportlicher Belastung.

**PDF-Auswertungsbericht** exportiert den aktuell angezeigten Stand einschließlich
UTC-Zeitraum, Filtern, Profilversion, Zonengrenzen, Abdeckung und Segmenten. Das
Portal nimmt bereits geladene Vergleichskurven auf; der Desktop erstellt einen
tabellarischen PDF-Vergleich. Zusätzliche Filter sind Mindest-/Höchstdauer in
Minuten, Mindestabdeckung (0–1) und RPE-Unter-/Obergrenze. Ein RPE-Filter schließt
Einheiten ohne RPE aus. Nach Filteränderungen zuerst neu laden.

Eine Einheit öffnen, **Einheit korrigieren** aufklappen/aktivieren und Titel,
Aktivität oder subjektive RPE ändern. Die API erlaubt zusätzlich Segmentkorrekturen.
Unter **Messwerte und Zeiten korrigieren** können zusätzlich `start`, `end`,
`samples` und `segments` als JSON korrigiert werden. Rohänderungen verlangen
`training.correct_raw`, eine Begründung und die Bestätigung der Einheits-ID.
Quelle und Importidentität bleiben unverändert. Jeder erfolgreiche
Schreibvorgang erhöht die Revision; der vorherige normalisierte Stand bleibt
in einer Korrekturhistorie. Die Originaldatei und ihr Hash bleiben unverändert.
Eine spätere Auswertung verwendet die korrigierten Angaben.

### Export und endgültige Löschung

Unter **Datenverwaltung → Neu laden** erscheinen die Imports dieser Person.
**Import exportieren** erzeugt JSON mit Originaldatei, Hash, Quelle und den aktuell
normalisierten Einheiten. Hierfür gilt die `raw`-Freigabe; der Export kann Daten
enthalten, die in der Oberfläche nicht sichtbar sind, beispielsweise GPS-Inhalte.

**Löschen** entfernt einen bestätigten Batch samt Einheiten und Korrekturhistorie.
Ein erneuter Import derselben Datei ist anschließend möglich. Das mit der
Person verknüpfte Konto oder eine gültig geprüfte sorgeberechtigte Person mit `training.write`, `training.delete`, `records.read`
und `records.write` darf löschen. Ein Trainer oder Administrator ohne diese
Personenverknüpfung oder geprüfte Sorgeberechtigung darf es auch mit Wildcard-Recht nicht. Löschung bleibt nach
Widerruf der Speicherfreigabe möglich.

**Trainingsdaten endgültig löschen** entfernt sämtliche importierten und manuellen
Trainingseinheiten, Geräte, Profilversionen, Recovery-Einträge, Korrekturhistorien
und KI-Laufmetadaten dieser Person. Die Trainingsfreigaben werden widerrufen.
Anwesenheit, Personendaten und der minimale Audit-Nachweis bleiben erhalten.
Bereits exportierte Dateien und ältere Backups werden dadurch nicht verändert.
Aufbewahrungsfristen und Sorgeberechtigungen werden ebenfalls in der Datenverwaltung bearbeitet; Details stehen am Ende dieser Anleitung.

## Einrichtung und Rechte

1. Host und Desktop/Portal aus demselben Feature-Stand bauen und installieren.
   ICU, libxml2, zlib und libcurl gehören bereits zu den Host-Abhängigkeiten.
2. Vor dem Update eine Datenbanksicherung erstellen. Der Host legt Migration 21
   an; anschließend unter **Erweiterungen** `training` auf Version 1.4.0 aktualisieren.
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
Ein erneuter Import ist kein Korrekturwerkzeug. Für Metadaten die separate Korrektur verwenden; Originaldateien unverändert aufbewahren.

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
Altersformel. Individuelle Zonenversionen werden separat im Trainingsprofil gespeichert.
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
6. In der Auswertung Zeitraum und Zonen festlegen, **KI-Erklärung** wählen.

Standard ist `http://127.0.0.1:<port>/v1/chat/completions`.
Weiterleitungen und Proxys sind deaktiviert. Verbindungstimeout 3 Sekunden,
Gesamtzeit 12 Sekunden; der RemoteClient wartet bis zu 20 Sekunden.
Maximal 32 KB berechnete Eingabedaten, 64 KB Antwort und 12.000 Zeichen Erklärung.

Ein entfernter Self-hosted- oder Cloud-Dienst ist ausdrücklich optional:

```sh
export CLUBPLATFORM_TRAINING_AI_REMOTE=true
export CLUBPLATFORM_TRAINING_AI_URL=https://ai.example.org/v1/chat/completions
export CLUBPLATFORM_TRAINING_AI_MODEL=your-versioned-model
# Optional: API-Schlüssel ausschließlich in der Host-Umgebung setzen.
# CLUBPLATFORM_TRAINING_AI_API_KEY
```

Der Host-Administrator wählt den Endpunkt. Anfragen aus Desktop/Portal können
keine Zieladresse vorgeben. Entfernte Ziele müssen HTTPS mit gültigem Zertifikat
und dem Pfad `/v1/chat/completions` oder `/api/chat` verwenden; URL-Zugangsdaten, Query-Parameter,
Weiterleitungen und Proxy-Nutzung sind nicht zugelassen.
Zusätzlich zur `ai`-Freigabe ist für jeden HTTPS-Aufruf eine benannte
`ai_remote`-Freigabe nötig, auch beim eigenen Konto. Beide werden vor und nach
Inference geprüft. Ohne explizites Host-Opt-in erfolgt kein entfernter Aufruf.
Die technische Anbindung wurde lokal getestet, nicht gegen einen echten
Cloud-Account oder einen konkreten entfernten Modellserver.

Nach erfolgreicher erneuter Autorisierung speichert der Host den konfigurierten
Modellnamen, Provider-Typ, Promptversion `training-explanation-v1`,
Algorithmusversion und SHA-256 der de-identifizierten Eingabekennzahlen.
Die generierte Erklärung selbst wird nicht als Trainingsdatensatz persistiert.
Der Modellname ist kein kryptografischer Beleg des tatsächlich geladenen Modells.

Übertragen werden Zeitabdeckung, Pulskennzahlen, Zonen und RPE-Last. Entfernt
werden Personen-/Datensatzkennungen, Titel, Aktivitäten, Zeitstempel, Rohdatei
und Samples. Der Dienst erhält keine Datenbankverbindung, Werkzeuge,
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
/api/v1/training/commands/profile
/api/v1/training/commands/profile-save
/api/v1/training/commands/recovery
/api/v1/training/commands/recovery-save
/api/v1/training/commands/batches
/api/v1/training/commands/export-batch
/api/v1/training/commands/delete-batch
/api/v1/training/commands/correct
/api/v1/training/commands/purge
/api/v1/training/commands/curves
/api/v1/training/commands/events
```

Alle Anfragen enthalten `person_id`. Import/Vorschau zusätzlich `format`,
`provider`, `content` und optional `mapping`. Detail benötigt `id`.
Summary/KI benötigen `from`, `until` und `zone_boundaries` (vier Zahlen oder `null` für das Profil).
Die Grenzen sind exklusiv/inklusiv wie oben beschrieben.

Fehler: 400 ungültige Eingaben, 403 fehlende Rechte/Freigaben, 404 unbekannte
Einheit, 409 Dublette mit verändertem Inhalt oder nicht verfügbarer KI-Dienst.
Import-Batches, Samples und Einheiten liegen in der Host-Datenbank und sind
Bestandteil ihrer Sicherung. Rohdateien können zusätzliche sensible Daten
enthalten, auch wenn die normalisierte Ansicht diese nicht zeigt.

### Neue REST-Nutzdaten

Alle Beispiele benötigen zusätzlich `person_id`. Die Operation steht hinter
`/api/v1/training/commands/`.

| Operation | Weitere Felder |
|---|---|
| `profile` | Optional `revision`; ohne Angabe neueste Version |
| `profile-save` | `expected_revision`, `zone_boundaries`, optional `label` |
| `recovery` | `from`, `until` (exklusiv) |
| `recovery-save` | `day` (UTC-Mitternacht), `expected_revision`; optionale numerische Werte `sleep_hours`, `fatigue`, `soreness`, `resting_hr`, `hrv_ms` |
| `batches` | Keine |
| `export-batch` | `batch_id` |
| `delete-batch` | `batch_id`, identischer `confirm_batch_id`, aktueller `fingerprint` |
| `correct` | `id`, `expected_revision`, `changes`; bei Messwert-/Zeitänderungen zusätzlich `reason`, `confirm_session_id` |
| `history` | `id`; letzte 50 vorherige Stände |
| `recovery-analysis` | `day` als UTC-Mitternacht |
| `purge` | `confirm_person_id`, identisch mit `person_id` |
| `curves` | `ids` mit 2–4 unterschiedlichen Einheits-UUIDs derselben Person |
| `events` | `after`: letzter erfolgreich verarbeiteter Cursor, initial 0 |

Für Profil und Recovery gilt `expected_revision: 0` beim Neuanlegen. Eine unbekannte
Profilrevision liefert ein leeres Profil; eine Auswertung damit wird abgewiesen.
Summary/KI unterstützen zusätzlich `activity` und `device` als exakte Filter.
Kurven, Originalexport und Recovery-Details benötigen die `raw`-Freigabe;
Profil und Änderungshistorie benötigen ebenfalls `raw`; Batchliste/Auswertung benötigen für Trainer `summary`.
Korrekturen und Dateneingaben benötigen Schreibrechte und für Trainer `write`.

## Signierte Ereignisse für n8n

Der optionale Abruf liefert maximal 100 Ereignisse pro Seite. Der Host benötigt
`CLUBPLATFORM_TRAINING_EVENT_KEY`: einen zufälligen 32-Byte-Schlüssel als
64-stellige Hex-Zeichenfolge. Der Konsument benötigt `records.read`,
`training.read`, `training.automation`, die Personenreichweite und eine explizite
benannte `automation`-Freigabe. Auch das eigene Konto braucht diese Freigabe.

Die Antwort enthält `payload` als exakte JSON-Zeichenfolge, `signature` als
HMAC-SHA256-Hexwert und `algorithm`. Der Konsument verifiziert die unveränderten
UTF-8-Bytes, Schema `training-events-v1`, die erwartete Person und ein höchstens
fünf Minuten altes `issued_at`. Ereignisse anhand `id` deduplizieren und
`next_cursor` erst nach erfolgreicher Verarbeitung der Seite speichern.

Die Ereignisse enthalten Typ, ID, Sequenz und Zeitpunkt; keine Messwerte,
Freitexte oder Originaldateien. Datenquelle ist der minimale Audit-Nachweis.
Ein Widerruf sperrt auch den historischen Abruf. Die signierte Schnittstelle
ist ein Pull-Verfahren; der optionale Dispatcher ergänzt ausgehende Zustellung
mit dauerhaftem Cursor und Wiederholungen. Einrichtung und Python-Verifikator
stehen im Produkt-Repository unter `examples/integrations/n8n/`.

## Prüfung vor Freigabe

```sh
ctest --test-dir BUILD --output-on-failure -R 'clubplatform-(training-|language-packs|foundation-sqlite)'
npm run build --prefix apps/portal
```

Automatische Tests prüfen Zeitzonen, Schaltjahre, CSV-Mapping, XML-Formate,
DTD-/Entity-Ablehnung, Messlücken, Zonen, Dubletten, Transaktionen, Freigaben
und tatsächliche HTTP-Kommunikation mit einem lokalen KI-Testdienst.
Die HTTP-Tests kontrollieren entfernte Identitäten, blockierte KI-Aufrufe nach Widerruf, Profilrevisionen, Recovery-Validierung, Kurven-/Exportrechte, unveränderte Originaldateien, Löschbestätigungen und signierte Ereignisse.
Desktop/QML sowie Windows/macOS müssen zusätzlich in der nativen CI geprüft werden.


## Mi-Fitness-Originalexport und ZIP-Import

Unter **Import** kann die vollständige Mi-Fitness-ZIP gewählt werden. Desktop und
Portal wählen für ZIP-Dateien automatisch `mi-fitness-zip` und kodieren die Datei
für den Transport als Base64. Eine einzelne `hlth_center_sport_record.csv` kann
mit `mi-fitness-csv` importiert werden. Für Textdateien gelten 2 MiB, für ZIP-Dateien
16 MiB komprimiert, 64 MiB insgesamt entpackt und höchstens 256 Archiveinträge.
Es werden keine Dateien auf dem Server-Dateisystem entpackt. Pfadtraversierung,
Symlinks, verschlüsselte Archive, fehlerhafte Prüfsummen und uneindeutige relevante
CSV-Dateien werden abgelehnt.

Der Adapter liest `hlth_center_sport_record.csv` und optional
`hlth_center_fitness_data.csv`. Herstellerwerte wie Dauer, Distanz, Kalorien und
mittlerer Puls bleiben als `source_metrics` erhalten. Sie erzeugen keine
synthetische Pulskurve. `start_time` und `end_time` bestimmen die Zeitspanne;
eine abweichende Herstellerdauer wird als Qualitätswarnung ausgewiesen.
GPX-Downloadlinks werden nicht abgerufen; aggregierte Tageswerte ersetzen keine
Rohmessungen. ZIP-Exporte müssen genau ein Quellkonto enthalten.

Puls und Einheit werden standardmäßig nur bei identischer Quellenkennung `Sid`
verbunden. Eine Zuordnung verschiedener Quellen muss ausdrücklich unter Mapping
angegeben werden, beispielsweise mit erfundenen Kennungen:

```json
{"source_map":{"app-source":"wearable-source"}}
```

Die verwendete Quellenkennung und Qualitätswarnungen erscheinen in der Vorschau.
Reguläre `heart_rate`-Werte haben Vorrang vor `single_heart_rate`; widersprüchliche
Werte gleicher Priorität werden als fehlend behandelt. Eine geänderte Zuordnung
überschreibt keinen bestehenden Import: zuerst den alten Batch prüfen/exportieren
und ausdrücklich löschen, danach erneut importieren.

Der privat bereitgestellte Originalexport vom 23.09.2026 enthält zwei Einheiten.
Bei strikter Quellenzuordnung besitzen beide keine passenden Rohpulswerte. Bei
expliziter Zuordnung von App zu Armband stehen für die Geheinheit sechs Werte zur
Verfügung; für die Laufeinheit fehlen passende Werte weiterhin. Persönliche
Kennungen und Originaldateien sind nicht Bestandteil des Repositorys oder der CI.

Der Batch-Export enthält `raw_encoding` (`utf-8` oder `base64`) und `format`.
Bei ZIP erhält Base64-Dekodierung von `raw_content` die unveränderten Archivbytes.
Der SHA-256-Fingerprint bezieht sich auf die UTF-8-Bytes von `raw_content`, bei ZIP
also auf die gespeicherte Base64-Zeichenfolge.

## Hintergrundaufträge

**Import im Hintergrund** legt einen dauerhaften Auftrag an. Mit
**Importaufträge aktualisieren** werden Status und Ergebnis neu geladen; wartende
oder laufende Aufträge können abgebrochen werden. Es gibt höchstens einen aktiven
Auftrag je Person und eine Warteschlangengrenze von acht aktiven Aufträgen im
Einzelhostbetrieb. Der Worker verarbeitet seriell, prüft Berechtigungen vor dem
Parsen und erneut vor dem Speichern und schreibt Einheiten transaktional.

Nach einem Prozessabbruch kann ein laufender Auftrag nach Ablauf seiner
zehnminütigen Bearbeitungsfrist erneut übernommen werden. Eine eindeutige
Bearbeitungskennung verhindert das Speichern durch einen veralteten Worker.
Abbruch und vollständige Trainingsdatenlöschung verhindern spätere Übernahme
der Ergebnisse. Nach Abschluss, Fehler oder Abbruch wird die Auftragskopie der
Quelldatei entfernt; erfolgreiche Originalimporte bleiben im zugehörigen Batch.
Die Fehleranzeige enthält keine Originaldateien oder vertraulichen Messwerte.

## Sorgeberechtigte und automatische Löschung

Unter **Datenverwaltung** lädt eine berechtigte Verwaltungsperson die vorhandenen
Sorgeberechtigungen und bestätigt Benutzer-ID, Nachweisreferenz und Ablaufdatum.
Erforderlich ist `training.guardians.manage`; niemand darf die eigene
Sorgeberechtigung bestätigen. Die Laufzeit beträgt höchstens 366 Tage. Die
Software dokumentiert die Prüfung, ersetzt aber nicht die Prüfung des Nachweises.
Geprüfte Sorgeberechtigte benötigen zusätzlich die normalen Trainingsrechte.

Eine aktive Sorgeberechtigung erlaubt die Verwaltung der Trainingsdaten und
Freigaben der betroffenen Person. Neu erteilte Trainingsfreigaben speichern ihren
Urheber. Nach Ablauf oder Widerruf einer Sorgeberechtigung vermitteln dessen
Freigaben keinen Zugriff mehr; ein ausdrücklicher Widerruf setzt sie zusätzlich
auf zurückgezogen. Frühere Freigaben ohne Urheberzuordnung bleiben kompatibel.
Anwesenheitsfreigaben sind von diesem Verfahren unabhängig.

**Automatische Löschung** ist standardmäßig deaktiviert (`0`). Athlet oder
geprüfte sorgeberechtigte Person kann mit Löschrecht und ausdrücklicher Bestätigung
1 bis 3650 Tage einstellen. Der Host prüft fällige Daten ungefähr jede Minute.
Import-Batches werden nach ihrem Importzeitpunkt gelöscht, manuelle Einheiten nach
Trainingsdatum, Recovery nach Tagesdatum, KI-Metadaten und abgeschlossene Aufträge
nach Erstellzeitpunkt. Alte Profilversionen werden entfernt, die aktuelle Version
bleibt erhalten. Geräte, Freigaben, Sorgeberechtigungsnachweise und Audit-Einträge
werden durch diese Frist nicht gelöscht. Fehlt dem Urheber der Löschregel die
aktuelle Berechtigung, wird die Regel nicht ausgeführt. Änderungen verwenden eine
Revisionsprüfung, damit parallele Bearbeitung keine Regel unbemerkt überschreibt.


## Optionaler Webhook-Dispatcher und n8n-Vorlage

Im Produkt-Repository unter `examples/integrations/n8n/` ergänzt
`deliver-training-events.py` den signierten Abruf um ausgehende Zustellung.
Ein externer Zeitplan startet den Einzellauf mit einer privaten SQLite-Statusdatei.
Diese enthält nur Konfigurationshash, Cursor, Fehlerzahl und nächsten Versuch;
Originaldateien, Messwerte und Zugangsdaten werden dort nicht gespeichert.
Die README erklärt die erforderlichen Umgebungsvariablen und Ausführung.

Jeder Zustellversuch ruft die Ereignisse erneut mit aktueller Berechtigung ab.
Ein Widerruf verhindert weitere Zustellungen; bereits versandte oder laufende
Anfragen können nicht zurückgerufen werden. Nur eine HTTP-200-Antwort mit dem
passenden `accepted_cursor` bestätigt die vollständige Seite. Ansonsten bleibt
der Cursor erhalten. Wiederholungen beginnen nach 30 Sekunden und verdoppeln
sich bis höchstens einer Stunde. Ein neuer Scheduler-Aufruf führt den Versuch aus.
Außerhalb von Loopback gilt HTTPS; Weiterleitungen und Umgebungsproxies sind aus.

Zustellung erfolgt mindestens einmal: Empfänger müssen nach Ereignis-ID
idempotent arbeiten. Der zusätzlich übertragene `Idempotency-Key` kennzeichnet
eine unveränderte Seite; durch neue Ereignisse können sich Seitengrenzen ändern.
Ein Absturz nach Verarbeitung und vor Bestätigung kann erneute Zustellung auslösen.

`training-webhook.workflow.json` ist eine inaktive, geheimnisfreie n8n-Importvorlage.
Sie prüft Signatur, Person, Zeitfenster und Reihenfolge und bestätigt anschließend
nur den Empfang. Sie erzeugt keine Anwesenheit und verändert keine Trainingsdaten.
Eigene idempotente Verarbeitung gehört zwischen Prüfung und Bestätigung.
Python-Tests prüfen Wiederholungen, Widerruf, Neustartzustand und HTTP-Weiterleitungen;
Node.js-Tests führen den unveränderten Prüfcode mit gültigen und manipulierten
Umschlägen aus. Import und Ausführung in der tatsächlich eingesetzten n8n-Version
mit deren Task-Runner- und Geheimnisrichtlinien bleiben als Abnahmeschritt offen.
Es wurde kein externer Webhook aktiviert oder mit persönlichen Daten angesprochen.


## Ergänzungen in Training 1.4

### Belastung, Recovery und Taekwondo

Die Auswertung liefert `load_statistics` mit zwei Fenstern (7 und 28 Tage), die
am exklusiven `until` enden. Erfasste Last ist RPE × Dauer in Minuten. Enthält
der gewählte Zeitraum das Fenster nicht vollständig oder fehlt bei einer
erfassten Einheit die RPE, bleiben Monotonie und Strain unbekannt. Ansonsten ist
Monotonie der mittlere tägliche erfasste Load geteilt durch dessen
Populationsstandardabweichung; Strain ist Gesamtload × Monotonie. Bei
Standardabweichung null werden beide nicht berechnet. Tage ohne Aufzeichnung
sind **keine bestätigten Ruhetage**. Filter gelten auch für diese Statistik;
sie beschreibt dann ausschließlich die gefilterte Auswahl.

`recovery-analysis` benötigt `day` als UTC-Mitternacht und vergleicht diesen Tag
mit den vorherigen 28 Tagen. Pro Messgröße sind mindestens sieben vorherige
Beobachtungen nötig. Mittelwert, Standardabweichung und Differenz sind nachvollziehbar;
bei konstanter Basis gibt es keinen standardisierten Abstand. Die Anzeige ist
kein klinisch validierter Erholungsindex und empfiehlt keine Belastungssteigerung.
Algorithmen: `recorded-load-v1`, `personal-recovery-baseline-v1`.

Segmente können `kind` (`work`, `rest`, `round`, `technique`) und
`manual_counts` (`kicks`, `punches`, `points`, `penalties`; ganze Zahlen 0–100000)
enthalten. Diese Zähler werden manuell erfasst, nicht aus Pulsdaten geschätzt.
Je Segment erscheinen Dauer, abgedeckte Zeit, Abdeckung, zeitgewichteter Puls,
Spitzenpuls und Zonenzeiten. Halteintervalle sind wie im Hauptdiagramm auf
30 Sekunden begrenzt und werden an beiden Segmentgrenzen abgeschnitten.

### Rohkorrekturen und API

`correct` akzeptiert zusätzlich zu den Metadaten `start`, `end` und `samples`.
Bei diesen Feldern sind `reason`, `confirm_session_id` und das zusätzliche Recht
`training.correct_raw` erforderlich; auch eine Trainerfreigabe für `raw` bleibt
notwendig. `expected_revision` schützt vor konkurrierenden Änderungen.
Die Startzeit wird im Suchindex mitgeändert. `history` mit `id` liefert die letzten
50 vorherigen Stände. Originaldatei und Fingerprint ändern sich nie dadurch.
Die Qualitätsanzeige kennzeichnet eine Messwertkorrektur; alle Auswertungen
verwenden anschließend die korrigierte Version.

### Health Connect auf Android

Das Produkt enthält unter `apps/health-connect/` einen nativen Kotlin-Begleiter.
Der Club-Platform-Kern bleibt C++. Voraussetzungen: Android 9 oder neuer,
verfügbares Health Connect, Leserechte für Training und Herzfrequenz sowie ein
HTTPS-Host mit gültigem Zertifikat. Der Begleiter schreibt keine Daten in
Health Connect und besitzt keine Hintergrund- oder Werbeberechtigungen.

1. Projekt mit JDK 17, Android SDK 36 und Gradle 8.13 bauen:
   `gradle -p apps/health-connect :app:assembleDebug :app:testDebugUnitTest :app:lintDebug`.
   Der separate GitHub-Workflow erzeugt eine Debug-APK; eine signierte
   Produktionsverteilung gehört zur Betreiberfreigabe.
2. APK installieren, Datenschutzhinweis lesen und beide Leserechte freigeben.
3. HTTPS-Server, Benutzername, Passwort und Ziel-Personen-ID eingeben; anmelden.
4. UTC-Tag innerhalb der letzten 30 Tage wählen und Trainings laden.
5. Training wählen, Vorschau laden und Zielperson, Zeitraum und Samplezahl prüfen.
6. Import ausdrücklich bestätigen. Der Host prüft zusätzlich seine Freigaben.

Workout und Puls müssen dieselbe Health-Connect-Quell-App haben. Die App liest
alle Seiten; fehlender Puls bleibt leer. Uploads sind auf 2 MiB begrenzt.
Unveränderte Wiederholungen erkennt der Host als Dublette; geänderte Quellen
überschreiben keine korrigierte Einheit. Passwörter, Tokens und Vorschauen werden
nicht dauerhaft gespeichert. Beim Verlassen wird die Vorschau gelöscht.
Widerruf in Health Connect verhindert neue Lesevorgänge; bereits importierte
Daten löscht man separat unter Training → Datenverwaltung.

### Strava: private OAuth-Liveansicht

Der Hostbetreiber registriert eine Strava-App und konfiguriert:

```text
CLUBPLATFORM_STRAVA_CLIENT_ID=<registrierte numerische ID>
CLUBPLATFORM_STRAVA_CLIENT_SECRET=<geheim>
CLUBPLATFORM_STRAVA_REDIRECT_URI=https://club.example/api/v1/training/strava/callback
```

Callback-Domain in Strava freigeben. Unter **Datenverwaltung → Strava** den Hinweis
bestätigen, verbinden, bei Strava `activity:read` gewähren und die vollständige
Rückleitungs-URL in die Anwendung kopieren. Die Callback-Seite selbst tauscht
keine Tokens aus. Erst der angemeldete ursprüngliche Athlet kann mit dem einmaligen,
zehn Minuten gültigen Zustand den Austausch abschließen.

**Neu laden** liest höchstens die letzten 30 Aktivitäten als Namen, Zeit,
Sportart und Link. Es gibt keine Datenbankimporte, Exportberichte, Trainer-/Elternsicht,
Hintergrundsynchronisation, KI-Nutzung oder Kombination mit anderen Trainingsdaten.
Die Anzeige wird nach spätestens einer Minute geleert. Tokens liegen nur im
Hostspeicher, sind an diese Anmeldung gebunden und höchstens eine Stunde nutzbar;
ein Neustart verlangt erneute Verbindung. Beim Tokenrefresh wird der Refresh-Token
ersetzt. Abmelden allein widerruft nicht die App-Freigabe bei Strava: Dafür
**Verbindung widerrufen** verwenden oder die Strava-Einstellungen für Apps öffnen.
Bei Netzfehlern werden lokale Verbindungsdaten verworfen; einen ausstehenden
anbieterweiten Widerruf in Strava selbst durchführen.

Die API-Operationen heißen `strava-begin` (`consent: true`), `strava-finish`
(`code`, `state`, `scope`), `strava-sync` und `strava-disconnect`. Sie stehen
nur dem aktiv mit der Person verknüpften Benutzer offen. HTTP-Antworten sind
`no-store`. `CLUBPLATFORM_STRAVA_TEST_ORIGIN` erlaubt ausschließlich einen lokalen
HTTP-Testserver unter `127.0.0.1`; diese Variable gehört nicht in den Produktivbetrieb.

### Ollama und signierte GGUF-Pakete

Neben `/v1/chat/completions` unterstützt der Host die native Ollama-Route
`http://127.0.0.1:11434/api/chat`, mit `stream: false` und begrenzter Tokenzahl.
HTTPS benötigt weiterhin Betreiber-Opt-in und die separate `ai_remote`-Freigabe.
`CLUBPLATFORM_TRAINING_AI_CA_FILE` kann eine betreiberseitige private CA-Datei
angeben; Zertifikats- und Hostnamenprüfung bleiben eingeschaltet.

Für ein signiertes Modellpaket einen privaten Ordner mit GGUF-Datei und
signiertem `manifest.json` bereitstellen. Unsigniertes Payload-Beispiel:

```json
{"schema":"training-model-v1","model_id":"training-local","format":"gguf","file":"training.gguf","size":12345,"sha256":"<SHA-256 der GGUF-Datei>","license":"<Lizenzbezeichnung>"}
```

`size`, Hash und Lizenz durch die tatsächlichen Werte ersetzen. Signieren:

```sh
clubplatform-sign sign model publisher-secret.hex model-payload.json model-package/manifest.json
```

Hostkonfiguration:

```text
CLUBPLATFORM_TRAINING_AI_MODEL=training-local
CLUBPLATFORM_TRAINING_MODEL_PACKAGE=/operator/model-package
CLUBPLATFORM_TRAINING_MODEL_PUBLIC_KEY=<vertrauenswürdiger Ed25519-Public-Key als Hex>
```

Vor jedem Modellaufruf prüft der Host Signatur, Modell-ID, Dateiname, Größe,
GGUF-Kennung und SHA-256. Manipulationen verhindern die Übermittlung von Daten.
Das Paketverzeichnis muss betreiberseitig schreibgeschützt sein. Es findet kein
Download oder Ausführen fremden Codes statt. Ohne Paketkonfiguration bleibt der
bestehende Dienstbetrieb möglich, mit `model_package.verified: false`.
Die signierte Datei attestiert nicht, welche Bytes eine getrennte Runtime
wirklich geladen hat; entsprechend bleibt `runtime_attested: false`.

Automatisierte Vertragsprüfungen verwenden synthetische Daten gegen einen
OpenAI-kompatiblen Testdienst, einen Ollama-Testdienst und einen tatsächlichen
HTTPS-Testdienst mit expliziter Test-CA. Sie prüfen außerdem Signatur-/Hashfehler,
Remote-Einwilligung und Widerruf während laufender Anfragen. Diese Tests ersetzen
keine Abnahme eines konkreten Cloud-Kontos mit dessen eigenen Bedingungen.
