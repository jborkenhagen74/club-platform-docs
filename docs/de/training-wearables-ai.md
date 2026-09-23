# Wearable-Import, Trainingsauswertung und lokale KI

Stand: 23.09.2026 · Feature-Branch `feature/training-wearable-import`.
Training-Extension 1.3.0, Extension-Schema 3, Host-Schema 21, ABI V3.
Dieser Stand ergänzt die [Trainings- und Anwesenheitsbasis](../training-attendance.md).
Er ist ein Entwicklungsstand, noch kein veröffentlichtes Pilot-Update.

## Abgleich mit dem Konzept vom 21.09.2026

| Konzept | Implementierter Stand | Noch offen |
|---|---|---|
| Sportneutraler Trainingskern | Geräte, Einheiten, Samples/Segmente; persistente Trainingsprofile mit unveränderlichen Zonenversionen; tägliche Recovery-Einträge | Weitere Athletenstammdaten und validierte Recovery-Modelle |
| Nachvollziehbare Imports | Originaldatei mit SHA-256; transaktionaler Import; Metadatenkorrektur mit Historie; Batch-Export und endgültige Löschung; persistente Hintergrundaufträge | Korrektur von Messwerten und Zeitstempeln |
| Anbieter | CSV mit Mapping, normalisiertes JSON, TCX, GPX, Apple-Health-XML; Mi-Fitness-CSV und ZIP anhand eines Originalexports geprüft | Android-Health-Connect-App, Strava-OAuth-Synchronisation |
| Berechnungen | Version `training-v1`, zeitgewichteter Puls, Zonenzeiten, Abdeckung, Messlücken, Session-RPE-Last | Erweiterte Recovery-/Belastungsmodelle, Taekwondo-spezifische Metriken |
| Grafiken | Pulskurve, Zonen, Wochen/Monate; Überlagerung von 2–4 normalisierten Kurven; Aktivitäts-/Gerätefilter und JSON-Auswertungsbericht | Druckfertige Vergleichsberichte und zusätzliche Filter |
| Berechtigungen | Personenreichweite und getrennte Freigaben; Audit/Widerruf; Export, Batch-Löschung und vollständige Trainingsdatenlöschung; befristet geprüfte Sorgeberechtigte; bestätigte automatische Aufbewahrungsfristen | Externe Nachweisprüfung bleibt organisatorisch erforderlich |
| KI | Lokaler Dienst als Standard; optionaler HTTPS-Endpunkt mit separater Remote-Freigabe; gespeicherte Modell-/Prompt-Metadaten und Eingabe-Hash | Verifikation konkreter entfernter Provider und signierter Modellpakete |
| Automatisierung | Signierter, personenbezogener Ereignisabruf mit Cursor und separater Automationsfreigabe; Verifikationsbeispiel für n8n | Ausgehende Webhook-Zustellung mit Wiederholungen und geprüfter importierbarer n8n-Workflow |

Diese Tabelle ist zugleich die offene Umsetzungsliste. Der generische CSV-Import
ist keine direkte Mi-Fitness-, Health-Connect- oder Strava-Kontoverbindung.
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
Originalmessung. Ein Profil enthält derzeit Zonengrenzen und eine optionale
Bezeichnung; es ist noch kein vollständiger sportmedizinischer Athletenpass.

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

**Auswertung als JSON exportieren** speichert die aktuell angezeigten berechneten
Kennzahlen samt Algorithmen-/Profilversion. Dieser Bericht ist kein druckfertiges PDF.

Eine Einheit öffnen, **Einheit korrigieren** aufklappen/aktivieren und Titel,
Aktivität oder subjektive RPE ändern. Die API erlaubt zusätzlich Segmentkorrekturen.
Zeitstempel, Quelle, Identität und Messwerte bleiben unverändert. Jeder erfolgreiche
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
   an; anschließend unter **Erweiterungen** `training` auf Version 1.3.0 aktualisieren.
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
und dem Pfad `/v1/chat/completions` verwenden; URL-Zugangsdaten, Query-Parameter,
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
| `correct` | `id`, `expected_revision`, `changes` mit `title`, `activity`, `rpe` und/oder `segments` |
| `purge` | `confirm_person_id`, identisch mit `person_id` |
| `curves` | `ids` mit 2–4 unterschiedlichen Einheits-UUIDs derselben Person |
| `events` | `after`: letzter erfolgreich verarbeiteter Cursor, initial 0 |

Für Profil und Recovery gilt `expected_revision: 0` beim Neuanlegen. Eine unbekannte
Profilrevision liefert ein leeres Profil; eine Auswertung damit wird abgewiesen.
Summary/KI unterstützen zusätzlich `activity` und `device` als exakte Filter.
Kurven, Originalexport und Recovery-Details benötigen die `raw`-Freigabe;
Profil/Batchliste/Auswertung benötigen für Trainer `summary`.
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
ist ein Pull-Verfahren; ausgehende Webhooks und eine Zustellwarteschlange sind
noch nicht implementiert. Einrichtung und ein ausführbarer Python-Verifikator
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
