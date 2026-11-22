# Kampfdaten und Kampfprotokoll: lückenlose Nachverfolgbarkeit

Jede Videoaufzeichnung eines Kampfes (ein Segment der Live-Sitzung) trägt:
- **Kampfdaten:** wer, wer hat gerichtet, wann, wo, welche Veranstaltung, welcher Kampf;
- ein **offizielles Protokoll:** Wertungen, Strafen, Unterbrechungen, Runden, Entscheidung, Korrekturen und weitere Einträge.

Alles ist zeitlich an die Originalaufnahme gebunden, wird nur angefügt und ist gegen nachträgliche Änderungen gesichert. Das **Kampfprotokoll** fasst Kampfdaten, Aufnahme und Protokoll prüfbar zusammen.

## Zwei getrennte Ansichten: Formen und Kampf

Jede Szene gehört zu einer **Disziplin**. Sie wird beim Anlegen gewählt und kann in den Einstellungen geändert werden. Ohne eigene Wahl gilt: eine Person = Formen, ab zwei Personen = Kampf. Portal und Desktop zeigen je Disziplin nur die passenden Elemente; der Server weist Einträge der anderen Disziplin ab.

| | Formen | Kampf |
|---|---|---|
| Reiter | Vorbereitung, Replay, Trainerprüfung, **Formenwertung & Abschnitte**, Formvorlagen, Live & Formenwertung, Aufzeichnungen | Vorbereitung, Replay, Trainerprüfung, **Wettkampfregeln & Wertung**, Live & Instant Replay, Aufzeichnungen |
| Einstellungen | Bewegungsabschnitte (Formsegmentierung), Formenwertung (Startwert, Abzugsarten, Präsentationsbestandteile, Zusammenfassung der Richter) | Wettkampfregeln (Runden, Grenzen, Wertungsaktionen) |
| Ergebnisse | erkannte Bewegungsabschnitte | Wertungstafel, Wertungsentscheidungen |
| Trainerprüfung | Technik, Beinarbeit, Deckung … – **keine** Treffer oder Kontaktkandidaten | alle Arten der Sportart |
| Video-Replay (IVR) | **Wertungsprotokoll Formen**: Beginn/Ende der Form, Abzüge und Präsentation je Kampfrichter, Richterwertungen, Endnote | **Kampfprotokoll**: Wertungen, Strafen, Runden, Kampfbeginn/-ende, Entscheidung |
| Kampfdaten | Ausführende (1–3, Team/Paar), Kampfrichter | Kämpfer je Seite, Kampfrichter |

Gemeinsam sind: Unterbrechung/Fortsetzung, Verletzung, Notiz, Korrektur, Videobeweis, Einspruch und Markierung.

### Formenwertung

- **Eintrag je Kampfrichter:** Jeder Eintrag gehört zu einem Kampfrichter (Auswahl aus den Kampfdaten oder freie Eingabe).
- **Abzüge** gibt es während der Form, z. B. klein −0,1 und groß −0,3. Die Arten und Werte stammen aus den Regeln der Szene.
- **Präsentation** wird nach dem Ende der Form vergeben, einmal je Kampfrichter. Jeder Bestandteil hat seinen Höchstwert. Eine Änderung erfordert zuerst eine Korrektur.
- **Berechnung** durch den Server:
  - Genauigkeit = Startwert − Abzüge (nicht unter 0);
  - Richterwertung = Genauigkeit + Präsentation;
  - Endnote = Mittelwert der Richter; beim gekappten Mittelwert ab fünf Richtern ohne höchste und niedrigste Wertung.
  - Gerundet wird auf drei Nachkommastellen, damit jeder Prüfer dasselbe Ergebnis erhält.
- **Vorlagen:** Taekwondo bringt eine Poomsae-Vorlage mit (Startwert 4,0; Abzüge 0,1/0,3; Präsentation 3 × 2,0). Sie ist mit „aktuelle WT-Regeln prüfen“ gekennzeichnet. Andere Sportarten verwenden die anpassbare Standardvorlage.
- **Tastenkürzel (belegbar):**
  - Q / W: erste / zweite Abzugsart für den gewählten Kampfrichter;
  - S: Beginn / Ende der Form.
- **Prüfwerkzeug:** `tools/replay/contest_record.py` rechnet bei Formen Richterwertungen und Endnote unabhängig nach.

## Kampfdaten

Portal und Desktop: im Video-Replay (IVR) unter **Kampfprotokoll → Kampfdaten**. Die Kampfdaten können vor dem Kampf (für den nächsten Kampf), währenddessen oder danach erfasst werden.

| Bereich | Felder |
|---|---|
| Veranstaltung | Name, Kennung, Kampfnummer, Kategorie/Gewichtsklasse, Runde im Turnier |
| Zeit | geplant, Beginn, Ende – ISO 8601 mit Zeitzonenabstand (z. B. `2026-11-22T14:03:12+01:00`), Zeitzone (z. B. `Europe/Berlin`) |
| Ort | Austragungsort, Stadt, Land, Kampffläche |
| Kämpfer | je Seite des Sportartprofils (z. B. Chung/Hong): Name, Verein, Nation, Startnummer; optional Verknüpfung mit einer Person |
| Offizielle | Funktion (Hauptkampfrichter, Punktrichter, IVR-Operator, Protokollführer, Technischer Delegierter, Supervisor, Coach, Sonstige), Name, Lizenz |
| Bemerkungen | Freitext |

Jede Speicherung erzeugt eine **neue Revision** mit Bearbeiter, Zeitpunkt und Prüfwert. Ältere Revisionen bleiben erhalten. Wer mit einem veralteten Stand speichert, wird abgewiesen. Die Revisionen sind untereinander verkettet (`prev_hash` → `hash`).

Neben den eingetragenen Zeiten enthält das Protokoll die **Zeitpunkte aus der Aufnahme selbst**: Startzeit der Aufnahme (UTC) sowie den ersten und letzten Bildzeitstempel je Kamera.

## Offizielles Protokoll

Jeder Eintrag bezieht sich auf die Position in der Aufnahme (`time_us`, Empfangszeit am Rechner). Er enthält Bearbeiter, Serverzeit, laufende Nummer, auf Wunsch einen Offiziellen und eine Notiz sowie die gezeigten Kameras.

| Art | Bedeutung | Prüfung durch den Server |
|---|---|---|
| Wertung (`score`) | Aktion des Sportartprofils für eine Seite (z. B. „kick head (+3)“) | Seite und Aktion müssen existieren; die Aktion darf keine Strafe sein; nicht nach der Entscheidung |
| Strafe (`penalty`) | Strafaktion für die Seite, die bestraft wird; Punkte gehen laut Profil z. B. an den Gegner | Aktion muss eine Strafe sein |
| Unterbrechung / Fortsetzung | mit Grund (Kal-yeo/Stopp, medizinisch, technisch, Videobeweis, sonstiges) | keine doppelte Unterbrechung, keine Fortsetzung ohne offene Unterbrechung |
| Rundenbeginn / Rundenende | Runden werden fortlaufend gezählt | nur abwechselnd |
| Kampfbeginn / Kampfende | | nur einmal, in dieser Reihenfolge |
| Entscheidung | Sieger (Seite, Unentschieden, kein Sieger) und Entscheidungsart; der Stand wird festgehalten | nur eine gültige Entscheidung |
| Verletzung | Seite, Notiz | |
| Videobeweis angefordert / bestätigt / abgelehnt, Einspruch, Markierung, Notiz | wie bisher | |
| Korrektur | **storniert** einen früheren Eintrag mit Pflichtbegründung | nur einmal je Eintrag; Korrekturen selbst sind nicht korrigierbar |

- **Nur anfügen:** Einträge werden nie geändert oder gelöscht. Ein Fehler wird durch eine Korrektur storniert, die Stornierung bleibt im Protokoll sichtbar. Danach wird bei Bedarf der richtige Eintrag neu gesetzt.
- **Spielstand:** Punkte, Strafen, offene Unterbrechung, Runde und Entscheidung berechnet der Server aus den gültigen Einträgen. Die Punkte stammen aus den Wertungsaktionen der Szene (Sportmodul) und werden nie vom Client übernommen.
- **Hashkette:** Jeder Eintrag enthält den Prüfwert des vorherigen Eintrags desselben Kampfes (`prev_hash`) und seinen eigenen (`hash`, SHA-256 über den Inhalt).
  - Wird ein gespeicherter Eintrag geändert, eingefügt oder entfernt, bricht die Kette.
  - Die Oberfläche zeigt „Protokollkette intakt (n)“ bzw. einen Alarm.
- **Rechte:**
  - Wertungen, Strafen, Ablauf, Entscheidung, Verletzung und Korrekturen erfordern `combat.review` (Offizielle).
  - Videobeweis anfordern, Einspruch, Markierung und Notiz erfordern `combat.read`.
  - Kampfdaten speichern erfordert `combat.review`.

## Kampfprotokoll exportieren und prüfen

**Kampfprotokoll exportieren** im IVR (Desktop: Datei speichern) bzw. Dienstoperation `contest_record` liefert `combat.contest-record.v1` mit folgendem Inhalt:
- **Szene:** Szene, Sportart, Seiten und Wertungsaktionen;
- **Kampfdaten** mit allen Revisionen;
- **Aufnahme:** Kopf-Hash, Verankerung im Server, zentrale Ablage, Prüfergebnis, Kameras und Zeitstempel;
- **Protokoll:** alle Einträge einschließlich Stornierungen, der berechnete Spielstand und das Ergebnis der Kettenprüfung;
- **Prüfsumme** des gesamten Protokolls (`record_sha256`).

Unabhängige Prüfung ohne die Plattform:

```sh
python3 tools/replay/contest_record.py kampfprotokoll-A-117.json \
    --recording live-replays/<job>/segment-0001     # optional: Aufnahme gegen den Kopf-Hash
```

Geprüft werden:
- die Prüfsumme des Protokolls;
- die Hashkette des Protokolls und der Kampfdaten-Revisionen;
- der Spielstand, unabhängig nachgerechnet;
- optional die Aufnahme selbst.

Exit-Code 0 nur, wenn alles stimmt.

## Tastenkürzel (frei belegbar)

| Aktion | Standard |
|---|---|
| Erste / zweite Seite auswählen | A / B |
| Wertungsaktion 1–6 für die gewählte Seite | 1–6 (Reihenfolge der Aktionen des Sportartprofils; Strafaktionen werden als Strafe eingetragen) |
| Unterbrechung / Fortsetzung | I |
| Rundenbeginn / Rundenende | O |

## Dienstoperationen

| Operation | Zweck |
|---|---|
| `contest_meta_save` (`job_id`, `segment`, `expected_revision`, `meta`) | neue Revision der Kampfdaten |
| `contest_meta_get` (`job_id`, `segment`) | aktuelle Revision und Verlauf |
| `replay_mark` | Protokolleintrag mit den Arten oben (`side`, `action_id`, `reason`, `winner`, `method`, `replaces`, `official`, `note`) |
| `replay_timeline` | zusätzlich `state` (Spielstand), `chain`, `meta`, `sides`, `scoring_actions` |
| `contest_record` | vollständiges, prüfbares Kampfprotokoll |

Datenbank: Migration 5 (`combat_contest_meta`), Modul 0.7.0. Protokolleinträge liegen wie bisher in `combat_events`. Einträge aus der Zeit vor der Hashkette werden als „nicht verkettet“ ausgewiesen.

## Grenzen

- **Personen, nicht Technik:** Die Kette beweist, dass das Protokoll nach dem Eintrag nicht verändert wurde. Wer einen Eintrag setzen durfte, regeln Rechte und Anmeldung.
- **Unterschrift:** Eine Unterschrift der Offiziellen (z. B. mit Geräteschlüssel) ist noch nicht enthalten.
- **TK-Strike:** Eine automatische Übernahme von Wertungen aus TK-Strike ist geplant, aber noch nicht umgesetzt. Bis dahin werden Wertungen im IVR eingetragen.
- **Regeln:** Die Wertungsaktionen stammen aus dem Sportartprofil bzw. den Analyse-Einstellungen der Szene. Ob sie dem aktuellen Regelwerk entsprechen, prüft der Veranstalter.
