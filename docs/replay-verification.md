# Verifizierbares Live-Replay, Tracking-Genauigkeit und freie 3D-Kamera

Stand: 21.11.2026. Betrifft `src/replay` (Bibliothek und Prüfwerkzeuge), den
Combat-Worker (`apps/analysis/live_capture.cpp`) und den Combat-Dienst.

## Worum es geht – und was dieses Dokument nicht behauptet

Ziel ist eine Grundlage, auf der ein Live-Videoreplay und das Motion-Tracking
**von Dritten überprüft** werden können, z. B. im Rahmen einer Anerkennung durch
World Taekwondo (WT). Dafür trennen wir zwei grundverschiedene Fragen:

| Frage | Was technisch möglich ist | Umsetzung |
|---|---|---|
| Ist das Replay vollständig und unverändert? | **Beweisbar exakt**: jedes aufgezeichnete Bild ist bytegenau gespeichert, gehasht und verkettet. Fehlende Bilder sind ausdrücklich vermerkt. | Aufzeichnungsformat v1, `clubplatform-replay-verify` |
| Wie genau ist das markerlose Tracking? | **Nur messbar, nie „100 %“**: Jedes kamerabasierte Verfahren hat einen Messfehler. Man kann ihn gegen Referenzdaten bestimmen und Grenzwerte prüfen. | `clubplatform-tracking-validate` |

**Nicht** Inhalt dieses Dokuments sind konkrete WT-Anforderungen,
Prüfverfahren oder Grenzwerte. Diese legt WT bzw. ein von WT beauftragtes
Prüflabor fest. Sie müssen dort angefragt und dann als Akzeptanzkriterien
eingetragen werden. Hier werden keine Werte erfunden.

## 1. Aufzeichnungsformat v1

Eine Aufzeichnung ist ein Verzeichnis:

```
manifest.jsonl          eine JSON-Zeile je Ereignis, hashverkettet
camera-0.frames         Bildbytes der ersten Kamera, lückenlos hintereinander
camera-1.frames         …
```

Zeilentypen in `manifest.jsonl` (Schlüssel sortiert, kompakt serialisiert):

- `header`: `format` (1), `session_id`, `producer`, `started_utc_us` und `cameras`
  mit `id`, `width`, `height`, `nominal_interval_us` und `encoding`.
- `frame`: `camera`, `index` (je Kamera fortlaufend ab 0), `pts_us`
  (Präsentationszeit der Quelle), `received_us` (Empfangszeit des Rechners),
  `offset`, `size` und `sha256` der Bildbytes.
- `gap`: `camera`, `from_pts_us`, `to_pts_us` und `reason`. Gründe sind
  `source_interval` (die Quelle hat mehr als 1,5 Sollintervalle übersprungen),
  `encoder_overload`, `source_unavailable` und `timestamp_regression`.
- `seal`: Abschluss mit Bild- und Lückenanzahl, optional `public_key` und
  `signature` (Ed25519 über den Kopf-Hash).

Jede Zeile trägt `hash = SHA-256(vorheriger_hash + "\n" + Zeile_ohne_hash)`.
Der letzte Hash ist der **Kopf-Hash**, der die gesamte Aufzeichnung festlegt.

Garantien (alle durch Tests belegt, `tests/replay_tests.cpp`):

- Bilder werden weder neu berechnet noch interpoliert. `frame_at(t)` liefert das
  letzte echte Bild mit `pts ≤ t`.
- Fehlende Bilder werden nie verdeckt, sondern als `gap` vermerkt.
- Manipulationen werden erkannt: geänderte Bildbytes oder Manifestzeilen,
  ein entferntes Siegel, abgeschnittene Dateien oder angehängte Daten lassen die
  Prüfung scheitern.
- **Live-Replay**: Bildbytes werden vor ihrer Manifestzeile geschrieben, und
  Leser übernehmen nur vollständige Zeilen. Eine Aufzeichnung kann also schon
  während der Aufnahme frame-genau abgespielt werden.
- Mehrere Kameras schreiben parallel (getestet mit 4 × 500 Bildern). Die
  Reihenfolge je Kamera bleibt erhalten.

Eine unabhängige Zweitimplementierung in Python (`tools/replay/replay_format.py`)
schreibt und prüft dasselbe Format. Die Tests prüfen wechselseitig: C++ prüft
Python-Aufzeichnungen und umgekehrt. Damit ist die Spezifikation nicht nur
durch den eigenen Code definiert.

## 2. Live-Aufnahme im Combat-Worker

- Jedes von der Kamera gelieferte Bild wird aufgezeichnet, in voller Auflösung
  und je Kamera mit einem eigenen Encoder-Thread. Die Pose-Erkennung nutzt
  weiterhin nur das jeweils neueste Bild. Das betrifft die Messung, nicht das
  Replay.
- Zeitstempel: Liefert das Gerät Präsentationszeiten, werden diese verwendet.
  Sonst wird eine monotone Rechneruhr verwendet; die Entscheidung fällt beim
  ersten Bild. Fallen Gerätezeitstempel später aus, bricht die Kamera ab, statt
  Zeitbasen zu mischen.
- Ein voller Encoder-Puffer (2 s) verwirft keine Bilder stillschweigend. Das
  übersprungene Intervall wird als `encoder_overload` vermerkt.
- Voraussetzung ist ein absoluter Medienordner `CLUBPLATFORM_COMBAT_STORE`. Die
  Aufzeichnung liegt dort unter `live-replays/<job_id>/`. Eine Sitzung dauert
  höchstens zehn Minuten.
- Beim Beenden wird die Aufzeichnung versiegelt und sofort geprüft. Der Kopf-Hash
  wird mit `live_finish` an den Dienst übergeben und dort in der Datenbank
  **verankert**. Wird die Aufzeichnung später vor Ort ersetzt, erkennt der Dienst
  die Abweichung.
- Dienstoperationen:
  - `replay_frame` (`job_id`, `camera_id`, `time_us` oder `index`) liefert ein
    einzelnes Originalbild mit Metadaten, Lückenhinweis und verankertem
    Kopf-Hash. Benötigt werden `combat.read` und `combat.live`.
  - `replay_verify` ist nur dann `ok`, wenn die Kette intakt, die Aufzeichnung
    versiegelt **und** der Kopf-Hash gleich dem verankerten ist.

**Wichtige Einschränkung:** Gespeichert werden die vom Betriebssystem
dekodierten Kamerabilder, neu als JPEG (Qualität 92) kodiert. Die Integrität
ist ab der Kodierung im Worker bewiesen, nicht ab dem Kamerasensor. Für eine
Beweiskette ab der Kamera wäre eine Durchleitung des Originalstroms der Kamera
(z. B. MJPEG/H.264 ohne Neukodierung) nötig. Siehe offene Punkte.

## 3. Mehrkamera-Synchronisation

`synchronized(reader, t, clocks)` bildet für jede Kamera über ein `ClockModel`
(`common = offset + rate · pts`) den gemeinsamen Zeitpunkt ab. Es liefert das
passende echte Bild, den **Zeitfehler je Kamera** und ein Flag, ob dieser
höchstens ein halbes Sollintervall beträgt. Es wird nichts interpoliert. Liegt
der Zeitpunkt in einer Lücke, wird das gemeldet.

Ohne Hardware-Synchronisation (Genlock/Trigger, PTP-Zeitstempel) bleiben
Latenzunterschiede zwischen Kameras unkorrigiert. Sie werden dann sichtbar
ausgewiesen, aber nicht beseitigt. Für eine Prüfung unter Wettkampfbedingungen
ist hardware-synchronisierte Aufnahme dringend zu empfehlen.

## 4. Prüfwerkzeuge für Dritte

```sh
# Integrität (Exit 0 nur bei intakter Aufzeichnung)
clubplatform-replay-verify /pfad/live-replays/<job_id>
# zusätzlich: Siegel muss mit genau diesem öffentlichen Schlüssel signiert sein
clubplatform-replay-verify /pfad/live-replays/<job_id> --trusted-key <hex>
# unabhängige Zweitprüfung ohne Projektcode
python3 tools/replay/replay_format.py verify /pfad/live-replays/<job_id>
```

Der Bericht ist JSON und enthält `ok`, `sealed`, `head`, Bild- und
Lückenanzahl sowie die Lücken je Kamera.

## 5. Tracking-Genauigkeit messen

```sh
clubplatform-tracking-validate --tracked ergebnis.json --reference referenz.csv \
  [--time-tolerance-ms N] [--time-offset-ms N] [--max-p95-mm N] [--min-coverage F]
```

- `ergebnis.json` ist ein Ergebnis `motion.scene.v1` in Metern mit Skelett
  `body12-mediapipe-v1`.
- `referenz.csv` hat die Kopfzeile `time_ms,track,joint,x,y,z` mit Metern im
  **selben Weltkoordinatensystem**. Typische Quelle ist ein markerbasiertes
  Motion-Capture-System, das gleichzeitig mit denselben, kalibrierten Kameras
  aufgezeichnet wird.
- Methode, siehe `src/replay/include/clubplatform/replay/accuracy.hpp`:
  - absoluter 3D-Fehler ohne verdeckte Nachausrichtung;
  - Zuordnung zum zeitlich nächsten Trackingbild innerhalb der Toleranz,
    standardmäßig ein halbes Bildintervall;
  - fehlende Zuordnung, Tracking-Lücke oder fehlender Punkt zählen als
    **fehlend** und niemals als 0 mm;
  - ein Zeitversatz zwischen den Systemen wird nur explizit angegeben und im
    Bericht ausgewiesen.
- Bericht `tracking.accuracy.v1`:
  - Abdeckung, Mittelwert, Median, P95 und Maximum in mm;
  - PCK bei 25/50/100 mm, bezogen auf alle Referenzpunkte;
  - alles gesamt und je Gelenk;
  - die angewandten Kriterien und die SHA-256-Hashes beider Eingabedateien.
- Exit-Code 0 nur, wenn alle angegebenen Kriterien erfüllt sind. Die Grenzwerte
  (`--max-p95-mm`, `--min-coverage`) kommen von der prüfenden Stelle.

## 6. Freie Kamerafahrt im 3D-Replay

Im Modus **Frei** (Web und Desktop) ist die Rekonstruktion aus jeder Perspektive
abspielbar, synchron zur Zeitachse und Bild für Bild:

- Ziehen dreht um den Zielpunkt. Shift-Ziehen oder rechte bzw. mittlere
  Maustaste verschiebt den Zielpunkt. Mausrad oder zwei Finger zoomen. Zwei
  Finger verschieben gleichzeitig.
- Tastatur, wenn die Ansicht fokussiert ist:
  - Pfeiltasten drehen, Shift+Pfeile verschieben;
  - `+`/`-` zoomen, Pos1 setzt die Ansicht zurück;
  - Komma und Punkt springen ein Bild, die Leertaste startet oder pausiert die
    Wiedergabe.
- Schieberegler und die Schnellansichten Vorne, Seite und Oben bleiben
  erhalten. **Ansicht zurücksetzen** stellt die Ausgangsperspektive her.
- Ein Bodenraster (1-m-Raster) dient der Orientierung.
- Die Kamerafahrt verändert nur die Darstellung, nie die rekonstruierten
  Koordinaten. Das Originalvideo ist weiterhin nur in seiner festen
  Kameraperspektive deckungsgleich (Modus Überlagerung).

## 6a. Darstellung: Skelett, generisches 3D-Modell, Kamera-Screens

Im Replay (Web und Desktop) lassen sich Darstellung und Kamera-Screens frei wählen:

- **Darstellung**: *Skelett*, *3D-Modell* oder *Modell und Skelett*.
- **Kamera-Screens**: *Aus*, *Kacheln*, *Im 3D-Raum* oder *Kacheln und 3D-Raum*.

### Erkennung und Rekonstruktion (unverändert)

Die 2D-Posen kommen je nach Worker von RTMPose mit YOLOX (ONNX Runtime, C++)
oder vom MediaPipe Pose Landmarker (Python). Beide werden auf das Skelett
`body12-mediapipe-v1` mit 12 Gelenken abgebildet. Die 3D-Punkte entstehen durch
geometrische Triangulation (DLT) über die kalibrierten Kameras.

### Generisches Taekwondoin-Modell

- Das Modell besteht aus einfachen Grundkörpern: Zylinder und Ellipsoide.
- Weißer Dobok und schwarzer Gürtel.
- Rumpfschutz (Hogu) und Kopfschutz tragen die **Markierungsfarbe**:
  - Chung (blau), standardmäßig für den ersten Track;
  - Hong (rot), standardmäßig für den zweiten Track;
  - Neutral, für Trainingsszenen.
- Die Markierung ist je Sportler umstellbar. Die Skelettlinien und die
  Projektion in den Kamerabildern verwenden dieselbe Farbe.
- **Gliedmaßen enden exakt an den gemessenen Gelenken.** Generisch sind nur die
  Körpervolumen: Dicke der Gliedmaßen, Rumpf, Kopf und Füße. Sie werden mit der
  Körpergröße skaliert.
- **Körpergröße**:
  - Sie wird je Track automatisch geschätzt: Oberschenkel + Unterschenkel +
    Rumpf, geteilt durch den anthropometrischen Anteil 0,779 (Drillis &
    Contini).
  - Das Verfahren ist haltungsunabhängig und verwendet den Median über alle
    Bilder.
  - Angezeigt werden die Streuung (Interquartilsabstand) und die Anzahl der
    verwendeten Bilder.
  - Werte außerhalb von 1,00–2,30 m werden begrenzt und als unplausibel
    gekennzeichnet.
  - Die Größe kann je Sportler manuell in cm überschrieben werden.
- Fehlen Gelenke in einem Bild, entfallen die betroffenen Körperteile. Eine
  Tracking-Lücke bleibt also sichtbar und wird nicht ergänzt.
- Das Modell ist eine **Darstellungshilfe, keine Messung**. Die Größenschätzung
  ist nur so genau wie das Tracking.

### Kamera-Screens

- **Kacheln**:
  - Je Kamera eine Kachel mit dem Originalbild: das Video der analysierten
    Szene oder das Live-Vorschaubild, jeweils zur eigenen Quellzeit der Kamera.
  - Darüber liegt das Skelett, projiziert über die Kalibrierung, einschließlich
    Verzeichnung.
  - Ein Klick wechselt in die exakte Perspektive dieser Kamera (Modus
    Überlagerung).
  - **Alle Kameravideos laden** lädt die Videos aller Kameras nacheinander.
- **Im 3D-Raum**:
  - Jede Kamera erscheint an ihrer kalibrierten Position als Pyramide.
  - Auf der Bildebene wird ihr Bild angezeigt; der Abstand ist einstellbar.
  - Bild und Skelett decken sich nur aus Sicht der jeweiligen Kamera. Das Bild
    ist eine einfache Lochkamera-Projektion ohne Entzerrung.
- Die Projektion der Web-3D-Ansicht ist per Test mit der bisherigen
  Orbit-Projektion abgeglichen: 1048 Punkte, Abweichung < 10⁻⁴. Modellteile,
  Größenschätzung und Bildecken der Screens sind ebenfalls getestet
  (`tests/combat_athlete_tests.mjs`, `tests/combat_replay_camera_tests.mjs`).
- **Desktop**: Dieselbe Rechenlogik kommt aus `extensions/combat/desktop/athlete.mjs`.
  Die QML-Ansicht ist nur syntaxgeprüft, weil Qt Quick 3D und Qt Multimedia in
  der Entwicklungsumgebung fehlen. Ausrichtung der Screen-Textur und Darstellung
  sind auf dem Zielsystem zu prüfen.

## 7. Stand der Verifizierungsreife

Technisch belegt (automatisierte Tests, lokal ausgeführt):

- Vollständigkeit, Bytegenauigkeit und Manipulationserkennung der Aufzeichnung,
  einschließlich unabhängiger Zweitimplementierung;
- frame-genauer Zugriff, auch während der Aufnahme;
- Verankerung des Kopf-Hashs im Server und Abgleich bei jedem Abruf;
- Genauigkeitsauswertung mit nachvollziehbarer Methode. Die Rechenregeln sind
  mit synthetischen Daten bekannter Fehler geprüft, zum Beispiel ein exakter
  30-mm-Versatz, fehlende Gelenke und Zeitversatz.

Noch offen, vor einer Einreichung:

1. **WT-Anforderungen einholen**: Prüfverfahren, Grenzwerte, Hardwarevorgaben
   und Formate direkt bei World Taekwondo bzw. dem benannten Prüflabor anfragen
   und als Akzeptanzkriterien festhalten.
2. **Test auf Zielhardware**: Der Worker-Code ist nur kompiliert und
   syntaxgeprüft, weil Qt Multimedia ≥ 6.5 in der Entwicklungsumgebung fehlt.
   Nötig ist eine Aufnahme mit den realen Kameras: Bildrate, Lücken, Last.
3. **Originalstrom statt Neukodierung**, damit die Beweiskette ab der Kamera
   beginnt.
4. **Hardware-Synchronisation** der Kameras (Trigger/Genlock oder PTP) und
   Messung der Restabweichung.
5. **Referenzmessung**: Vergleichsaufnahmen mit einem markerbasierten System
   unter wettkampfnahen Bedingungen und Auswertung mit
   `clubplatform-tracking-validate`.
6. **Signaturschlüssel**: Der Worker versiegelt derzeit ohne eigene Signatur;
   der Schutz entsteht durch die Verankerung im Server. Für Prüfungen außerhalb
   des Servers sollte das Siegel mit einem geschützten Geräteschlüssel signiert
   werden, z. B. Installationsschlüssel oder HSM.
