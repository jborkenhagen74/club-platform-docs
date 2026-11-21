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

## Verifizierbares Live-Replay und Tracking-Genauigkeit

Die Live-Erfassung der Kampfanalyse zeichnet jedes Kamerabild in voller Auflösung mit
Quellzeitstempel, SHA-256-Hashkette und ausdrücklich vermerkten Lücken auf. Der Kopf-Hash
wird im Server verankert. Unverändertheit und Vollständigkeit lassen sich mit
`clubplatform-replay-verify` (oder einer unabhängigen Python-Implementierung) prüfen. Die
Genauigkeit des markerlosen Trackings ist nicht „exakt“, sondern wird mit
`clubplatform-tracking-validate` gegen Referenzdaten gemessen. Das 3D-Replay ist mit
freier Kamerafahrt (Maus, Touch, Tastatur) abspielbar und zeigt wahlweise Skelett, generische
Sportlermodelle in der Ausrüstung der gewählten Sportart (Sportartprofile aus dem Kampfsport-Modul:
Taekwondo, Karate, Judo, Boxen, Kickboxen, Muay Thai, Ringen, MMA, Allgemein; nach geschätzter oder
eingegebener Körpergröße skaliert) sowie die Kamerabilder als Kacheln oder als Screens an den Kamerapositionen im 3D-Raum. Format, Werkzeuge und der Stand der
Verifizierungsreife, einschließlich der vor einer WT-Einreichung offenen Punkte:
[Verifizierbares Live-Replay](replay-verification.md).

Weitere Vorschaufunktionen und der Laufzeitschalter: [Vorschaufunktionen](preview-features.md).
