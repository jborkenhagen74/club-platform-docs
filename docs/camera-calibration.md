# Kamerakalibrierung (Schachbrett oder ChArUco, 2–16 Kameras)

Desktop: **Einstellungen → Kameras kalibrieren**. Alternativ auf der Kommandozeile
mit `clubplatform-calibrate` (nativ) oder `calibrate.py`; beide verwenden dieselbe
Eingabe und dieselbe Ergebnisstruktur.

1. **Brett wählen:**
   - **ChArUco (empfohlen):** Jede Ecke trägt eine eindeutige Nummer. Der Weltursprung
     ist damit eindeutig, und auch teilweise verdeckte oder angeschnittene Bretter
     werden erkannt; je Kalibrierbild genügen 30 % der Ecken, im Weltbild 50 %.
     Im Dialog **Druckvorlage speichern** (oder
     `clubplatform-calibrate --write-board brett.json --output brett.png`),
     unverkleinert drucken, auf eine ebene, steife Platte kleben und Feld- und
     Markergröße nachmessen. Angegeben werden die **Felder** (z. B. 8 × 6).
   - **Schachbrett:** Angegeben werden die **inneren Ecken**. Das Brett muss vollständig
     sichtbar sein. Ein Schachbrett ist um 180° symmetrisch, deshalb den markierten
     Ursprung prüfen und bei Bedarf die Eckreihenfolge umkehren.
2. **Je Kamera 12–100 Bilder** des Bretts in unterschiedlichen Positionen, Distanzen und
   Neigungen; Auflösung, Zoom und Fokus nicht ändern. Danach die Kameras fixieren.
3. **Weltbild:** Alle Kameras fotografieren dasselbe unbewegte Brett, z. B. auf der
   Mattenmitte. X folgt der ersten Brettreihe, Y zeigt im Brett nach oben, Z aus der
   Brettfläche.
4. **Berechnen:** Eckenerkennung, Intrinsik/Verzerrung je Kamera und Weltpose per PnP.
   Geprüft werden Auflösung, Bildverteilung und Reprojektionsfehler (Standard 1,5 px).
   Ausgabe: `calibration.json`, `report.json` (mit Brettart und Zahl der Weltpunkte) und
   markierte Weltbilder mit dem aus der Pose projizierten Ursprung.
5. **Sichtprüfung** der Weltbilder, dann die Datei importieren und bestätigen. Ein
   niedriger Bildfehler allein beweist keine gemeinsame Weltorientierung.

Beispiel `calibration-input.json` (Pfade relativ zur Datei):

```json
{
  "setup": "Fläche 2, 6 Kameras",
  "board": {"type": "charuco", "columns": 8, "rows": 6, "square_m": 0.04, "marker_m": 0.028, "dictionary": "DICT_5X5_250"},
  "max_rms_px": 1.5,
  "cameras": [
    {"camera_id": "cam-1", "intrinsic_images": ["cam-1/01.png", "…", "cam-1/12.png"], "world_image": "cam-1/world.png"}
  ]
}
```

Für ein Schachbrett entfällt `type` (oder `"chessboard"`); `columns`/`rows` sind dann
die inneren Ecken, `marker_m`/`dictionary` entfallen, `reverse_world_corners` ist je
Kamera möglich. Unterstützte Wörterbücher: `DICT_4X4_*` bis `DICT_7X7_*` (50, 100,
250, 1000) und `DICT_ARUCO_ORIGINAL`. ChArUco benötigt OpenCV ab 4.7 (objdetect) oder
das opencv_contrib-Modul aruco.

**Kameraanzahl:** Der Assistent kalibriert 2–16 Kameras. Szenen der Szenen- und
Spielanalyse und die Live-Aufnahme nutzen 2–16; Einzelpersonen-3D-Sitzungen der
Bewegungsanalyse bleiben auf 2–4 Kameras begrenzt.

**Geprüft:** `tests/calibration_tests.py` rendert Bretter durch bekannte Kameras und
Posen in echte Bilddateien und lässt beide Implementierungen daraus rechnen:
16 Kameras mit Schachbrett, ChArUco mit teilweise verdecktem Bild und eindeutigem
Ursprung, Druckvorlage ↔ Erkennung, Kamerabereich. Intrinsik auf 2 %, Lage auf 1 cm /
etwa 1° genau. Das sind synthetische Bilder; reale Optiken und Drucke sind zu prüfen.

OpenCV-Grundlagen:
https://docs.opencv.org/4.13.0/dc/d43/tutorial_camera_calibration_square_chess.html,
https://docs.opencv.org/4.13.0/df/d4a/tutorial_charuco_detection.html
