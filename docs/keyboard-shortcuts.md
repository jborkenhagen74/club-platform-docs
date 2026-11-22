# Tastenkürzel

Für Hauptmenü, Suche, Einstellungen und Modulfunktionen, z. B. das Video-Replay (IVR) und das 3D-Replay, lassen sich eigene Tasten und Tastenkombinationen hinterlegen. Das gilt im Webportal und im Desktop-Client mit denselben Aktionen und derselben Schreibweise.

## Bedienung

- **Portal:** Einstellungen (Avatar → Einstellungen) → Abschnitt **Tastenkürzel**.
- **Desktop:** Menü Einstellungen → **Tastenkürzel**.

Die Aktionen sind nach Bereichen gruppiert, z. B. „Hauptmenü und allgemein“, „Szenenanalyse: 3D-Replay“ und „Szenenanalyse: Video-Replay (IVR)“. Je Aktion gibt es drei Schaltflächen:

| Schaltfläche | Wirkung |
|---|---|
| **Ändern** | Die nächste gedrückte Taste oder Kombination wird übernommen. Esc bricht ab. |
| **Entfernen** | Die Aktion ist danach nicht mehr mit einer Taste belegt. |
| **Standard** | Stellt die mitgelieferte Belegung wieder her. |

**Alle zurücksetzen** stellt alle Standardbelegungen wieder her.

Eine Kombination darf mehrfach vergeben werden. Die Überschneidung wird dann aber angezeigt („Mehrfach belegt“, „auch belegt durch …“) und nicht stillschweigend verworfen. Zwei Aktionen überschneiden sich, wenn sie dieselbe Taste haben und
- im selben Bereich liegen, oder
- eine davon im Bereich „Hauptmenü und allgemein“ liegt, denn dieser Bereich wirkt überall.

Die Pfeiltasten können deshalb im 3D-Replay und im IVR unterschiedliche Aufgaben haben.

Jeder Hauptmenüeintrag ist belegbar, auch die Einträge von Modulen und die Schnellaktionen („Person anlegen“, „Organisation anlegen“). Neue Module erscheinen automatisch in der Liste. Nur die Core-Einträge haben eine Standardbelegung, Moduleinträge sind anfangs „nicht belegt“.

### Speicherung

Die Belegung wird je Benutzer und Server bzw. Datenbank gespeichert:
- **Portal:** im Browser.
- **Desktop:** in den lokalen Einstellungen (QSettings), mit demselben Schlüssel wie die Menüreihenfolge.

Die Belegung wird nicht zwischen Rechnern oder zwischen Portal und Desktop synchronisiert. Berechtigungen und Lizenzprüfungen ändert sie nicht: Ein Kürzel öffnet nur, was auch über das Menü erreichbar ist.

### Eingabefelder

Während in einem Textfeld geschrieben wird, lösen einfache Tasten wie Leertaste, Buchstaben, Pfeile, „,“ und „.“ keine Aktion aus. Kombinationen mit Strg/Alt/Cmd, Funktionstasten und Esc wirken weiterhin.

## Standardbelegung

### Hauptmenü und allgemein

| Aktion | Taste |
|---|---|
| Suche / Befehle öffnen | Strg+K (macOS: Cmd+K) |
| Einstellungen | Strg+, |
| Start | Alt+1 |
| Personen | Alt+2 |
| Organisationen | Alt+3 |
| Auswertungen | Alt+9 |
| Administration | Alt+0 |

Auf dem Desktop öffnet „Einstellungen“ den Dialog „Darstellung“, wie der Eintrag Einstellungen im Seitenmenü.

### Szenenanalyse: 3D-Replay

Die Tasten wirken, solange die räumliche Ansicht den Fokus hat.

| Aktion | Taste |
|---|---|
| Kamera drehen links/rechts | Pfeil links/rechts |
| Kamera neigen oben/unten | Pfeil hoch/runter |
| Ansicht verschieben | Umschalt+Pfeil |
| Vergrößern / Verkleinern | + / - |
| Ansicht zurücksetzen | Pos1 |
| Vorheriges / nächstes Bild | , / . |
| Wiedergabe / Pause | Leertaste |

### Szenenanalyse: Video-Replay (IVR)

| Aktion | Taste |
|---|---|
| Vorheriges / nächstes Bild | , / . |
| 1 Sekunde zurück / vor | Pfeil links / rechts |
| 2 Sekunden zurück | Umschalt+Pfeil links |
| 10 Sekunden zurück | Strg+Pfeil links |
| Wiedergabe / Pause | Leertaste |
| Langsamer / Schneller | [ / ] |
| Live folgen | L |
| Vergrößern / Verkleinern / Zoom zurücksetzen | + / - / 0 |
| Videobeweis angefordert / bestätigt / abgelehnt | R / Y / N |
| Markierung | M |
| Einspruch | P |
| Erste / zweite Seite auswählen | A / B |
| Wertungsaktion 1–6 für die gewählte Seite | 1–6 |
| Unterbrechung / Fortsetzung | I |
| Rundenbeginn / Rundenende | O |
| Nächster Kampf | nicht belegt |

## Schreibweise

Die Tasten werden in Qt-„Portable Text“ notiert, z. B.:
- Kombinationen: `Ctrl+K`, `Ctrl+Shift+K`, `Alt+1`;
- Sondertasten: `Space`, `Left`, `PgUp`, `F1`;
- Zeichen: `+`, `-`, `,`, `[`.

`Ctrl` steht unter macOS für Cmd.

Bei Zeichen wie `,` `+` `[` wird Umschalt nicht berücksichtigt. Ob man für ein Zeichen Umschalt braucht, hängt vom Tastaturlayout ab: „+“ ist auf der deutschen Tastatur eine eigene Taste, auf der US-Tastatur liegt es auf Umschalt+=.

Wird eine Kombination mit Strg, Alt oder Cmd gedrückt, gilt die physische Buchstaben- bzw. Zifferntaste. Alt+1 ergibt unter macOS sonst „¡“.

## Für Entwickler: neue Funktionen und Module

Jede Benutzerfunktion, die auf Tasten reagiert, wird als **Aktion** deklariert und nie fest im Code abgefragt.

1. **Deklaration:**
   - Core-Aktionen stehen in `resources/shortcuts/core.json`.
   - Modul-Aktionen stehen in `extensions/<modul>/shortcuts.json`.
   - Schema `clubplatform.shortcuts.v1`.
   - Jede Aktion hat `id` (Präfix = Modul-ID aus `manifest.json`), `label_key` (in allen Sprachdateien des Moduls bzw. des Core), `default` (leer erlaubt) und `context`.
   - Bereiche (`contexts`) gruppieren Aktionen, die gleichzeitig aktiv sind.
2. **Portal:**
   - Das Modul ruft `registerShortcuts(json)` auf.
   - Die Ansicht nutzt `onKeyDown={useShortcutKeys('<kontext>', {'<id>': () => …})}` aus `apps/portal/src/shortcuts.ts`.
   - `<ShortcutHint context="…"/>` zeigt die aktuelle Belegung.
3. **Desktop:**
   - Das Modul liefert dieselbe `shortcuts.json` (sie wird über `cmake/ExtensionUi.cmake` eingebettet).
   - QML prüft in `Keys.onPressed` mit `preferences.shortcutMatches("<id>", event.key, event.modifiers)`.
   - Globale Aktionen laufen über `Shortcut {sequence: window.shortcutKeys("<id>")}`.
4. **Hauptmenü:** Einträge brauchen nichts weiter. Portal (`registerNavigation`) und Desktop (`registerNavigationShortcuts`) erzeugen `nav.<route>` automatisch.
5. **Tests:**
   - `tests/shortcuts_tests.py` (CTest `clubplatform-shortcuts`) prüft:
     - Schema, eindeutige IDs, Modulpräfix;
     - Übersetzungen;
     - gültige und überschneidungsfreie Standardbelegungen;
     - dass jede im Code verwendete Aktions-ID deklariert ist;
     - dass jede Modul-Aktion in Web **und** Desktop behandelt wird.
   - Die Notation prüfen `tests/shortcut_keys_tests.mjs` (Portal) und `tests/desktop_shortcuts_tests.cpp` (Desktop) mit denselben Erwartungen.
   - Die Bedienung prüft Playwright (`combat.spec.ts`, `usability.spec.ts`).

## Prüfung

```sh
python3 tests/shortcuts_tests.py
node tests/shortcut_keys_tests.mjs
ctest -R 'shortcut'          # inkl. clubplatform-desktop-shortcuts im Desktop-Build
```

Manuell auf dem Desktop prüfen:
- Kürzel ändern, entfernen und auf Standard setzen.
- Hauptmenü per Alt+Ziffer aufrufen.
- Im IVR und im 3D-Replay mit geänderter Belegung arbeiten.
- macOS: Cmd statt Strg.
