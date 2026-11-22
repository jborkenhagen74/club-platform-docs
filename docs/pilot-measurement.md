# Pilotmessung: Messplan und Auswertung

Ziel ist eine belastbare Aussage darüber, wie genau die Club-Platform unter
realen Bedingungen misst. Gemessen werden:
- Zeitabgleich der Kameras;
- Vollständigkeit der Aufnahme;
- 3D-Genauigkeit der Körperpunkte;
- Technikerkennung.

Die Messung ist nur aussagekräftig, wenn die Zielwerte **vor** der ersten Aufnahme
festgelegt und danach nicht mehr verändert werden. Das Werkzeug
`tools/pilot/pilot.py` erzwingt das.

## 1. Was gemessen wird

| Bereich | Messgröße | Werkzeug | Bezug |
|---|---|---|---|
| Zeitabgleich | Versatz je Kamera zur Referenzkamera (Mittel, Maximum, Streuung) aus einer gefilmten Blitzfolge | `pilot.py sync` | Empfangszeit am Rechner (`received_us`), wie im IVR und in der Live-Analyse |
| Aufnahme | Bildverlust, längste Lücke, effektive Bildrate, Schwankung der Ankunftszeit, Lückengründe | `pilot.py recording` | vollständige Aufnahme im Replay-Format |
| 3D-Genauigkeit | mittlerer Fehler, P95, Maximum, Abdeckung, PCK 25/50/100 mm, je Gelenk | `clubplatform-tracking-validate` | gleichzeitig aufgenommenes markerbasiertes Motion-Capture im selben Weltkoordinatensystem |
| Technikerkennung | Makro-Recall, Fehlannahmen bei unbekannten Bewegungen, Ablehnungsrate, Verwechslungsmatrix | `evaluate_recognition.py` bzw. Auswertung des Technikmodells | beschriftete Clips getrennter Personen und Sitzungen |

## 2. Aufbau

- **Ort:** Fläche in Wettkampfgröße. Licht, Hintergrund und Kleidung (Dobok) wie im Einsatz.
- **Kameras:** die geplanten Bedingungen, z. B. 4 und 8 Kameras bei 60 Bildern/s. Fest montiert, Zoom und Fokus fixiert.
- **Kalibrierung:** ChArUco-Brett (siehe [Kamerakalibrierung](camera-calibration.md)). Weltursprung in der Flächenmitte. Kalibrierbericht und markierte Weltbilder zum Versuch ablegen.
- **Zeitabgleich-Prüfung:** Zu Beginn und am Ende jedes Versuchsblocks eine LED oder ein Blitz, für alle Kameras sichtbar. Mindestens 6 Blitze in unregelmäßigen Abständen.
- **Referenzsystem:** markerbasiertes Motion-Capture, gleichzeitig mit denselben Bewegungen.
  - Gemeinsames Koordinatensystem über das Kalibrierbrett oder Marker auf dem Brett.
  - Gemeinsame Zeitbasis über ein Synchronisationssignal. Ein Zeitversatz wird nur ausdrücklich angegeben (`declared_time_offset_ms` im Plan) und im Bericht ausgewiesen.
- **Personen:** mindestens 5, unterschiedliche Körpergrößen und Leistungsstufen. Einwilligung für Aufnahme, Verarbeitung und Auswertung schriftlich einholen.

## 3. Bedingungen und Versuche (Vorschlag)

| Bedingung | Inhalt | Versuche |
|---|---|---|
| langsam-4cam | Grundtechniken, Stellungen, langsam | ≥ 10 je Bedingung, verteilt auf ≥ 5 Personen |
| kick-4cam | schnelle Fußtechniken (z. B. Dollyo, Dwit, Naeryo Chagi) | ≥ 10 |
| kick-8cam | dieselben Techniken mit 8 Kameras | ≥ 10 |
| verdeckung | zwei Personen im Kampf, gegenseitige Verdeckung | ≥ 10 |
| erkennung | beschriftete Technikclips plus bewusst unbekannte Bewegungen; getrennte Personen für Training und Test | nach Klassen, Testpersonen nie im Training |

## 4. Ablauf

1. **Plan anlegen:** `tools/pilot/plan-template.json` kopieren.
   - Bedingungen, Mindestumfang (`minimums`) und Zielwerte (`targets`) eintragen; je Bedingung sind abweichende Ziele möglich.
   - Unter `targets_source` vermerken, wer die Zielwerte festgelegt hat (z. B. Verband oder Prüflabor).
   - Die Beispielwerte der Vorlage sind Platzhalter, keine Empfehlung.
2. **Plan sperren** (vor der ersten Aufnahme):
   ```sh
   python3 tools/pilot/pilot.py lock plan.json      # schreibt plan.json.lock.json (SHA-256, Zeitpunkt)
   ```
   Plan und Sperrdatei sofort an die prüfende Stelle senden. Jede spätere Änderung des Plans lässt die Auswertung scheitern.
3. **Je Versuch:**
   ```sh
   python3 tools/pilot/pilot.py recording live-replays/<job>/segment-0001 -o t001/recording.json
   python3 tools/pilot/pilot.py sync      live-replays/<job>/segment-0001 -o t001/sync.json
   clubplatform-tracking-validate --tracked t001/ergebnis.json --reference t001/mocap.csv > t001/tracking.json
   ```
   Ausgaben werden nie überschrieben. Aufnahmen bleiben versiegelt, ihre Kopf-Hashes stehen in den Berichten.
4. **Erkennung:**
   - Vorhersagen auf den zurückgehaltenen Testclips sammeln.
   - `evaluate_recognition.py` ausführen. Es weist eine Vermischung von Trainings- und Testdaten ab.
   - Pfad unter `recognition` im Plan eintragen.
5. **Auswerten:**
   ```sh
   python3 tools/pilot/pilot.py evaluate plan.json messdaten/ bericht.json   # zusätzlich bericht.md
   ```
   Der Exit-Code ist nur dann 0, wenn das Gesamturteil „erfüllt“ lautet.

## 5. Auswertungsregeln

- Ein Kriterium gilt in einer Bedingung nur dann als erfüllt, wenn **jeder** Versuch es erfüllt. Der Bericht nennt zusätzlich Median und schlechtesten Versuch.
- **Fehlende Ergebnisse** zählen nie als erfüllt, sondern führen zu „zu wenig Daten“. Dasselbe gilt, wenn der Mindestumfang an Versuchen oder Personen nicht erreicht ist.
- **Gesamturteil:**
  - „nicht erfüllt“, sobald ein Kriterium irgendwo verfehlt ist;
  - sonst „zu wenig Daten“, falls etwas fehlt;
  - sonst „erfüllt“.
- **Nachvollziehbarkeit:** Der Bericht enthält Plan-Hash, Sperrzeitpunkt, die Hashes aller Eingabedateien und alle Einzelwerte.
- **Zeitabgleich:**
  - Blitze direkt nach einem fehlenden Bild werden nicht in den Versatz eingerechnet.
  - Bei der Empfangszeit ist der Versatz auf etwa ein Bildintervall genau messbar.
  - Aussagen unterhalb eines Bildintervalls erfordern eine Hardware-Synchronisation der Kameras.

## 6. Einordnung

Ein bestandener Pilot belegt die Genauigkeit für die gemessenen Bedingungen, Personen und den Aufbau, nicht allgemein. Für eine Anerkennung, z. B. als WT-IVR, gibt die prüfende Stelle Verfahren und Grenzwerte vor (siehe [Verifizierbares Live-Replay](replay-verification.md)).

## 7. Geprüft

`tests/pilot_tests.py` (CTest `clubplatform-pilot-measurement`):
- Aufnahme dreier Kameras mit bekannten Ankunftsversätzen (+20 ms, −35 ms) und drei verlorenen Bildern im Replay-Format. Der Versatz wird auf 1 ms genau gefunden, der Bildverlust exakt.
- Gesperrter Plan, Änderung nach dem Sperren, abweichende Ziele je Bedingung.
- Die Urteile „erfüllt“, „nicht erfüllt“ und „zu wenig Daten“.
- Fehlende Erkennungsauswertung.
