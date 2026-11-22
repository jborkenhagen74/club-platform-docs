# Sportartneutrale Analyse und Sportmodule

Stand: 21.11.2026.

Erkennung, Analyse, Verfolgung, Replay und Review sind **sportartneutral**. Alles
Sportartspezifische liefern **Sportmodule**. Das Kampfsport-Modul (`martial`) ist
das erste davon. Basketball, Handball, Laufen und andere Sportarten lassen sich als
eigene Module ergänzen, ohne die Analyse zu ändern.

## Aufbau

| Ebene | Modul | Aufgabe |
|---|---|---|
| Einzelperson | Bewegungsanalyse (`movement`) | Aufnahme, Kalibrierung, 2D/3D-Pose einer Person, Technikkatalog, Referenzen |
| Mehrere Personen | Szenen- & Spielanalyse (interne Kennung `combat`) | Szenen mit 2–16 Kameras und 1–30 Personen, 3D-Rekonstruktion, Live-Erfassung, verifizierbares Replay, Review, Wertung, Ablaufvorlagen, Referenzvergleich |
| Sportart | Sportmodule, z. B. Kampfsport (`martial`) | Sportartprofile: Markierungen, Ausrüstung des 3D-Modells, Ereignisarten, Formfamilien, Wertungsvorlagen, Teilnehmergrenze |

Die interne Kennung `combat` bleibt unverändert. Sie steckt in Lizenzen,
Berechtigungen (`combat.*`) und gespeicherten Daten. In der Oberfläche heißt das
Modul „Szenen- & Spielanalyse“.

## Sportartprofile

Ein Sportmodul deklariert in `capabilities.json` die Fähigkeit:

```json
{"key": "sport.profile-provider", "version": 1}
```

Es beantwortet die Service-Operation `sport.profiles.v1` mit einer Liste von
Profilen. Die Analyse findet alle aktiven Anbieter über die Host-Abfrage
`extension.providers`; sie muss die Module nicht kennen. Die Analyse führt die
Profile mit ihrem eigenen Profil „Allgemein“ zusammen.

```json
{"id": "handball", "family": "team", "max_participants": 16,
 "markings": [{"id": "home", "color": [0.9, 0.9, 0.1]}, {"id": "away", "color": [0.1, 0.5, 0.2]}],
 "kinds": ["pass", "shot", "block", "foul"],
 "elements": {},
 "outfit": {"top": "marking", "sleeves": "short", "bottom": "marking", "legs": "shorts",
            "belt": null, "protector": null, "headgear": null,
            "hands": {"kind": "bare", "color": "skin"}, "feet": {"kind": "shoes", "color": [0.1, 0.1, 0.1]}}}
```

Die Felder im Einzelnen:

- `markings`: die zwei Kennfarben der Seiten. „Neutral“ für Trainingsszenen
  ergänzt die Analyse selbst.
- `kinds`: die Ereignisarten im Review, zusätzlich zu den neutralen Arten der
  Analyse (Kontaktkandidat, Treffer, Technik, Beinarbeit, Deckung).
- `elements.forms.families`: die Formfamilien der Sportart, z. B. Taekwondo mit
  Poomsae, Tul und Hyong oder Karate mit Kata. Nur Sportarten mit Formfamilien
  bieten Formvorlagen an. Judo, Boxen oder Handball haben keine; dort ist der
  Reiter ausgeblendet und der Dienst lehnt das Speichern ab. „Allgemein“ bietet
  sportneutrale Ablaufvorlagen (`other`).
- `scoring`: optionale Wertungsvorlage, nur für Regelwerke mit fester
  Punkte-je-Aktion-Tabelle. Sie ist ausdrücklich als Ausgangspunkt gekennzeichnet.
- `max_participants`: die Grenze je Szene, höchstens 30.
- **Erweiterung bestehender Profile:** Ein Profil mit `"extends": "taekwondo"`
  ergänzt ein vorhandenes Profil um Ereignisarten, Formfamilien oder Elemente. So
  kann ein eigenes Taekwondo-Modul z. B. die Kukkiwon-Poomsae als Formfamilie
  hinzufügen, ohne das Kampfsport-Modul zu ändern.
- Doppelte oder ungültige Profile werden nicht übernommen. Sie erscheinen in
  `conflicts` der Antwort auf `sport_profiles`, damit Fehler sichtbar bleiben.
- **Texte** stehen in den Sprachpaketen des liefernden Moduls:
  - Sportname: `module.<modul>.sport_profile.<id>`
  - Markierungen: `….marking.<id>`
  - Ereignisarten: `….kind.<id>`
  - Formfamilien: `….form.<id>`

### Neues Sportmodul anlegen (Kurzanleitung)

1. Modul wie in [Erweiterung V3](extension-v3.md) anlegen und die Fähigkeit
   `sport.profile-provider` deklarieren.
2. Im nativen Dienst `sport.profiles.v1` beantworten (Schema
   `martial.sport-profiles.v1` oder `sport.profiles.v1`). Vorbild:
   `extensions/martial-arts/services/sport_profiles.hpp`; die Profile liegen in
   `sports/profiles.json` und werden beim Bauen eingebettet.
3. Texte in allen Sprachpaketen des Moduls ergänzen.
4. Testen: `extensions/combat/tests/test_analysis_service.py` zeigt, wie Anbieter
   und Erweiterungen geprüft werden. Dort fügt ein simuliertes Handball-Modul
   Profile hinzu, und ein Taekwondo-Zusatzmodul erweitert ein Profil.

Noch nicht vorhanden für Mannschaftssportarten: eine Mannschaftswertung (die
Wertung arbeitet mit genau zwei Sportlern) und ein Bilddetektor für den Ball. Die
Ballverfolgung selbst ist vorhanden (siehe unten).

## 2 bis n Kameras, viele Personen

- Szenen unterstützen **2–16 Kameras** und **1–30 Personen**; eine Sportart kann
  die Personenzahl über ihr Profil begrenzen. Das gilt für Dienst, nativen und
  Python-Worker, Bewegungsanalyse und Live-Erfassung.
- **Personenzuordnung zwischen Kameras und über die Zeit:** optimale Zuordnung
  nach der Ungarischen Methode, mit der bisherigen Unsicherheitsregel. Eine Person
  behält ihre Zuordnung nur, wenn jede fast gleich gute Lösung (innerhalb der
  Marge) übereinstimmt; sonst bleibt sie offen. Das Ergebnis ist identisch mit dem
  früheren vollständigen Durchzählen, geprüft an 3000 bzw. 1500 Zufallsfällen. Die
  Laufzeit ist polynomiell statt exponentiell.
- **Kamerakonsens je Gelenk:**
  - Bis 6 Kameras werden alle Teilmengen exakt geprüft, wie bisher.
  - Darüber werden zuerst alle brauchbaren Kameras gemeinsam trianguliert.
    Gelingt das nicht, wird ein Konsens aus jedem Kamerapaar gebildet: Die
    Kameras, die mit dem Paar innerhalb der Reprojektionsgrenze übereinstimmen,
    werden gemeinsam nachtrianguliert.
  - Die Mehrdeutigkeitsprüfung bleibt unverändert.
- **Messung:** 10 Personen mit 8 Kameras im Kreis werden exakt rekonstruiert, mit
  stabilen Identitäten; nativ etwa 0,3 s je Bild ohne Optimierung für Echtzeit.
- **Schrittweiser Start bei Verdeckung:** Sieht kein Kamerapaar alle Personen,
  werden Personen einzeln aufgenommen. Das geschieht, sobald ein Kamerapaar eine
  Person eindeutig trianguliert und mindestens drei Kameras sie bestätigen.
  - Getestet mit 10 Personen und 8 Kameras, bei denen jede Kamera je Bild 2–3
    Personen verpasst.
  - Ein Track, der schon eine Person hatte, bekommt nie eine andere. So gibt es
    keine Identitätswechsel, was für die Wertung wichtig ist.
  - Bei starker Verdeckung bleibt eine Person lieber kurz offen, als falsch
    zugeordnet zu werden.

## Ball- und Objektverfolgung

- Objekt-Detektionen je Kamera und Bild (`objects`: Klasse, x, y, Konfidenz)
  werden über Kamerapaare trianguliert; bestätigende weitere Kameras werden
  hinzugenommen.
- Über die Zeit verfolgt mit Geschwindigkeitsvorhersage und eindeutiger
  Zuordnung.
- Eine neue Spur braucht mindestens 3 Kameras; Spuren enden nach 1 s ohne
  Messung. Die Höchstzahl je Klasse steht in der Szenenkonfiguration, z. B.
  `"objects": {"ball": {"max": 1}}`.
- Ausgabe je Bild: Position, Kamerazahl, Reprojektionsfehler und Geschwindigkeit
  in m/s. Fehlende Messungen bleiben fehlend, es wird nichts interpoliert. Der
  Dienst prüft diese Angaben.
- Anzeige im Replay: orange Kugel in 3D, Markierung im Kamerabild und in den
  Kacheln.
- Geprüft mit einer Wurfparabel über 8 Kameras: Positionen exakt, eine stabile
  Kennung, Fehldetektionen ignoriert, ein verdecktes Bild bleibt leer.
- **Noch offen:** der Bilddetektor für den Ball (Plan:
  Planung Turnierbetrieb, Abschnitt 4). Die
  Python-Variante verfolgt noch keine Objekte.

## Vergleich mit Referenzvideos aus einer Perspektive

Veröffentlichte Referenzen haben meist nur eine Kamera, z. B. die Formen auf dem
Kanal des Kukkiwon. Der Vergleich nutzt die 3D-Aufnahme des Sportlers und schätzt
die Perspektive der Referenz:

1. **Referenz aufbereiten:** `clubplatform-reference-pose --sports2d-model
   manifest.json --video referenz.mp4 --out referenz.pose2d.json`. Das Werkzeug
   gehört zum nativen Worker-Paket und extrahiert je Bild die Gelenke der größten
   Person. Gespeichert werden nur Posendaten, nie das Video. Nur Videos verwenden,
   deren Nutzung erlaubt ist.
2. **Vergleichen:**
   - In der Oberfläche unter Replay → „Vergleich mit Referenzvideo“: Person und
     optional ein Zeitfenster aus der Replayposition wählen.
   - Oder auf der Kommandozeile: `clubplatform-reference-compare --reference
     referenz.pose2d.json --athlete-scene ergebnis.json --track <id>`.
   - Dienstoperation: `reference_compare`. Ergebnisse werden nicht gespeichert.
3. **Methode:**
   - Die 3D-Bewegung wird aus vielen virtuellen Blickwinkeln (Drehung, Neigung)
     projiziert.
   - Eine Zeitverzerrung (Dynamic Time Warping) gleicht das Tempo aus.
   - Der Blickwinkel mit der besten Übereinstimmung wird verfeinert.
   - Körpergröße und Bildposition werden über die Rumpflänge herausgerechnet.
4. **Ergebnis** (`comparison.monocular.v1`):
   - geschätzter Blickwinkel mit Eindeutigkeitsmaß;
   - Tempo der Referenz relativ zum Sportler;
   - mittlere und 95-%-Abweichung, auf die Körpergröße bezogen und näherungsweise
     in cm;
   - Abweichung je Gelenk und Gelenkwinkel;
   - die Abschnitte mit der größten Abweichung, mit Sprung ins Replay;
   - Abdeckung, Warnungen und Grenzen.
5. **Grenzen:**
   - Bewegungen auf die Referenzkamera zu oder von ihr weg sind nicht sichtbar.
   - Die 2D-Posenerkennung des Referenzvideos hat eigene Fehler.
   - Die Perspektive wird als Parallelprojektion angenähert.
   - Ein **gespiegeltes Video** sieht genauso aus wie eine Aufnahme von der
     Gegenseite. Die Abweichungswerte sind davon unabhängig; für den richtigen
     Blickwinkel muss die Spiegelung angegeben werden.
   - Sind beide Aufnahmen 2D, ist der Vergleich nur bei ähnlichem Blickwinkel
     aussagekräftig (Modus `2d_to_2d`).
6. **Geprüft** mit synthetischen Bewegungen (`tests/monocular_compare_tests.cpp`):
   - Blickwinkel auf ±4° genau erkannt;
   - Tempounterschiede gemessen (z. B. 25 % langsamer);
   - eine absichtlich abweichende Handhaltung zeitlich und dem richtigen Gelenk
     zugeordnet;
   - Spiegelung, Zeitfenster und Fehlerfälle.

   Das Extraktionswerkzeug ist nur syntaxgeprüft, weil die ONNX-Laufzeit und die
   Modelle in der Entwicklungsumgebung fehlen. Ein Test mit einem echten
   Referenzvideo steht noch aus.
