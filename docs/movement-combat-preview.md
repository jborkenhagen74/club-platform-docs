# Bewegungs- und Kampfanalyse (Vorschau)

Stand: November 2026 · Movement 2.5 · Combat 0.5 · **nicht Teil der Pilotabnahme**.

Beide Module analysieren Trainingsvideos lokal (Pose-Erkennung, Mehrkamera-Kalibrierung,
Wiederholungs- und Technikvergleich, Kampfszenen mit Wertung und Korrekturen). Sie werden
nur mit dem Build-Schalter `CLUBPLATFORM_BUILD_MOVEMENT_PILOT=ON` gebaut und benötigen
die separate Analyse-Laufzeit (native Worker, Modelle, Videospeicher), die im Desktop
unter **Einstellungen → Analyse-Laufzeit und Kameraquellen** konfiguriert wird.

Der Erweiterungskatalog kennzeichnet beide Module mit `preview: true`; Desktop und Portal
zeigen „Vorschau“ in der Modulübersicht.

## Grenzen der Vorschau

- Videos und daraus abgeleitete Bewegungsdaten sind personenbezogen, häufig von
  Minderjährigen. Einwilligung, Zweckbindung und Löschfristen sind vor Produktivbetrieb
  fachlich und rechtlich festzulegen.
- Kalibrierung und Synchronisierung gelten je Aufnahmesituation; eine geänderte
  Kameraaufstellung erfordert eine neue Kalibrierung.
- Die Oberflächentexte der Analyse-Dialoge sind noch nicht vollständig übersetzt.
- Plattformabdeckung (CoreML/CUDA, Kameras) ist nicht abgenommen.

Weitere Vorschaufunktionen und der Laufzeitschalter: [Vorschaufunktionen](preview-features.md).
