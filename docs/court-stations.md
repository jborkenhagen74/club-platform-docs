# Turnierbetrieb mit zentralem Server und Kampfflächen-Stationen

Szenario: Ein Server läuft zentral, alle Clients greifen darauf zu. Jeder Desktop-Client betreibt genau eine Kampffläche: eigene Kameras, eigene Live-Analyse und eigenes Videoreplay (IVR). Jeder abgeschlossene Kampf wird zentral auf dem Server gespeichert, damit er später geprüft werden kann, zum Beispiel bei einem Einspruch.

```
 Kampffläche 1                      Kampffläche 2                     Zentraler Server
 ┌──────────────────────────┐      ┌──────────────────────────┐      ┌─────────────────────────────┐
 │ Desktop (Servermodus)    │      │ Desktop (Servermodus)    │      │ Combat-Dienst + Datenbank   │
 │  Kameras (USB/RTSP)      │      │  Kameras (USB/RTSP)      │      │  Szenen, Rechte, Freigaben  │
 │  Combat-Worker (lokal)   │─────▶│  …                       │─────▶│  verankerte Kopf-Hashes     │
 │  Aufnahme lokal          │ Befehle/Vorschau (REST, Sitzung)    │  Markierungen, Einsprüche   │
 │  IVR aus lokaler Aufnahme│      │                          │      │  Zentrale Ablage:           │
 │  Upload nach dem Kampf   │═════▶│                          │═════▶│  live-replays/<job>/        │
 └──────────────────────────┘      └──────────────────────────┘      │   segment-NNNN (geprüft)    │
                                                                     └─────────────────────────────┘
 Portal/Desktop anderer Clients: Archiv „Aufzeichnungen & Einsprüche“ → IVR aus der zentralen Ablage
```

## Ablauf

1. **Einrichtung je Kampffläche** (Desktop, Menü Einstellungen → Analyse-Laufzeit):
   - **Kampfflächen-Station** ankreuzen.
   - Worker-Programm, Modelle, lokalen Aufnahmeordner und Kameraquellen angeben (2–16 Kameras: Qt-Kamera, Datei oder RTSP/HTTP-URL).
   - Danach neu starten.
   - Diese Pfade gelten nur auf diesem Rechner und werden nie an den Server übertragen.
   - Ohne das Häkchen bleibt ein Client im Servermodus wie bisher reiner Bediener ohne eigene Aufnahme.
2. **Szene je Kampffläche:** Jede Fläche hat eine eigene kalibrierte Szene, z. B. „Fläche 2“. Pro Szene läuft höchstens eine Live-Sitzung, die Flächen arbeiten unabhängig voneinander.
3. **Live-Erfassung starten:**
   - Der Client startet seinen eigenen Combat-Worker.
   - Der Worker meldet sich über die Sitzung des angemeldeten Benutzers beim Server. Rechte, Freigaben und Lease prüft der Server.
   - Die Aufnahme entsteht vollständig im lokalen Aufnahmeordner, pro Kampf ein Segment.
4. **IVR an der Kampffläche:**
   - Solange ein Kampf läuft oder noch nicht zentral gespeichert ist, liest das Videoreplay direkt die lokale Aufnahme. Das hat keine Netzlatenz pro Bild und funktioniert auch bei Netzstörungen.
   - Segmente, Markierungen und Einsprüche kommen vom Server.
5. **Nächster Kampf:**
   - Das laufende Segment wird versiegelt und sein Kopf-Hash im Server verankert. Die Kameras laufen weiter.
   - Danach lädt der Client das Segment im Hintergrund hoch, über eine eigene Verbindung, damit Bedienung und Live-Worker nicht blockiert werden.
6. **Zentrale Ablage:**
   - Der Server nimmt die Dateien in Teilen an (bis 8 MiB je Anfrage, fortsetzbar).
   - Er prüft die vollständige Aufnahme gegen den beim Versiegeln verankerten Kopf-Hash und gegen die Sitzungskennung.
   - Erst dann verschiebt er sie nach `CLUBPLATFORM_COMBAT_STORE/live-replays/<job>/segment-NNNN/`.
   - Eine nach dem Versiegeln veränderte Aufnahme wird abgewiesen und nicht gespeichert.
   - Bei einem Verbindungsabbruch setzt der nächste Versuch an der unterbrochenen Stelle fort, automatisch alle 10 s oder über **Jetzt übertragen**.
7. **Kampfdaten und Protokoll:** Kämpfer, Offizielle, Veranstaltung, Zeit, Ort und Kampfnummer sowie Wertungen, Strafen, Unterbrechungen und Entscheidung werden je Kampf im IVR erfasst ([Kampfprotokoll](contest-log.md)).
8. **Späteres Review, z. B. bei einem Einspruch:**
   - Jeder berechtigte Client öffnet im Portal oder Desktop **Aufzeichnungen** und wählt einen Kampf. Gespeicherte Kämpfe werden aus der zentralen Ablage abgespielt.
   - Je Kampf werden Ablagestatus und Zahl der Einsprüche angezeigt.
   - **Einspruch** (Taste P, belegbar) wird mit Zeit, Seite und Kameras festgehalten. Die Markierungen werden nur angefügt und enthalten den Bearbeiter.
   - Der Zugriff bleibt auch nach einer späteren Änderung der Szene möglich, z. B. nach neuer Kalibrierung am nächsten Turniertag.
9. **Speicherplatz an der Kampffläche:** **Zentral gespeicherte lokale Kopien entfernen** löscht nur Segmente, die der Server bestätigt hat. Nicht gespeicherte oder abgewiesene Segmente bleiben erhalten.

## Statusanzeigen

| Anzeige | Bedeutung |
|---|---|
| Vorläufig | Der Kampf läuft; die Hashkette ist bis zum aktuellen Ende geprüft. |
| Verankert | Versiegelt; der Kopf-Hash ist im Server gespeichert. |
| Zentrale Ablage läuft · n % | Der Upload läuft; der Fortschritt ist auf dem Server sichtbar. |
| Zentral gespeichert | Geprüft und auf dem Server abgelegt; von jedem Client abspielbar. |
| Noch nicht zentral gespeichert | Liegt nur an der Kampffläche (z. B. Station offline). |
| Abgewiesen | Die Aufnahme passt nicht zum versiegelten Stand. Die lokale Kopie bleibt erhalten; der Betreiber muss den Fall klären. |

## Dienstoperationen

Alle Operationen verlangen `combat.live`.

| Operation | Recht | Zweck |
|---|---|---|
| `replay_upload_begin` (`job_id`, `segment`, `files`) | `combat.analyze`, nur Autor der Sitzung | Startet oder setzt die Übertragung fort. Nur versiegelte Segmente; feste Dateimenge: `manifest.jsonl` und eine `camera-N.frames` je Kamera. Prüft den freien Speicher. Liegt die Aufnahme schon im gemeinsamen Speicher, wird sie vor Ort geprüft. |
| `replay_upload_chunk` (`name`, `offset`, `data` Base64) | wie oben | Hängt an; der Offset muss genau passen. |
| `replay_upload_finish` | wie oben | Prüft Vollständigkeit, Hashkette, Siegel, Kopf-Hash und Sitzungskennung, legt dann ab. Bei Abweichung wird der Zwischenstand gelöscht. |
| `replay_archive` (`scene_id` optional) | `combat.read` | Sitzungen mit Segmenten, Bezeichnung, Ablagestatus, Upload-Fortschritt, Zahl der Markierungen und Einsprüche. |
| `replay_mark` mit `kind: "protest"` | `combat.read` | Einspruch zu einem Zeitpunkt. |
| `replay_timeline` | `combat.read` | Zusätzlich `stored` und `upload` je Segment. |

## Speicherbedarf und Netz

Gespeichert werden Originalbilder als JPEG (Qualität 92) in voller Auflösung. Grob gerechnet ergeben 4 Kameras × 30 Bilder/s × 3 Minuten bei 720p etwa 2–4 GB pro Kampf, bei 1080p entsprechend mehr. Die zentrale Ablage braucht also ausreichend Platz: Der Server lehnt einen Upload ab, wenn weniger als die Segmentgröße plus 1 GiB frei ist. Ein kabelgebundenes Netz (mindestens 1 Gbit/s) zwischen Kampfflächen und Server wird empfohlen. Der Upload läuft parallel zum nächsten Kampf.

## Grenzen (Stand 22.11.2026)

- **Nicht im echten Aufbau getestet:**
  - Die Desktop-Teile (Einstellungen, Upload-Thread, lokales IVR im QML) sind hier nur kompiliert bzw. syntaxgeprüft.
  - Getestet sind die Upload- und Lesebausteine (`clubplatform-desktop-court-station`), der Dienst (`test_combat_live_court_station_upload_to_central_storage`) und die Weboberfläche (Playwright).
  - Ein Aufbau mit mehreren echten Kampfflächen steht aus.
- **Kein Löschkonzept:** Es gibt noch keine Aufbewahrungsfristen und kein Löschen auf dem Server. Kämpfe bleiben gespeichert, bis ein Administrator sie entfernt.
- **Einwilligungen:** Der Zugriff folgt dem Einwilligungsmodell der Szene, also den Teilnehmenden der Szene. Für Turniere mit wechselnden Athleten fehlt noch eine passende Rechtsgrundlage bzw. ein Turnier-Einwilligungsmodell im Veranstaltungsmodul.
- **Upload nur durch den Autor:** Hochladen darf nur der Benutzer, der die Live-Sitzung gestartet hat. Wechselt die Anmeldung an einer Station, wartet der Upload, bis dieser Benutzer wieder angemeldet ist.
