# Bedienung: Module, Zuordnungen und Kalender

## Sichtbarkeit der Module

Ein Modul erscheint in der Navigation erst, wenn es lizenziert, geladen, installiert
und aktiviert ist und seine Abhängigkeiten bereit sind. Dies gilt auch für Aktionen
der Untermodule Beiträge und Käufe innerhalb der Finanzen.

Unter **Erweiterungen** bleiben auch nicht nutzbare Module sichtbar, damit eine
Lizenz importiert und die Installation vorgenommen werden kann. „Geladen“ bedeutet,
dass die native Datei erkannt wurde; es ist keine Lizenzfreigabe. Die Prüfungen auf
dem Server bleiben unabhängig von der Darstellung wirksam.

## Kompakte Zuordnungen

Die Übersichten für Benutzer einer Gruppe, Rollen einer Gruppe und Berechtigungen
einer Rolle zeigen den übergeordneten Eintrag jeweils einmal. **Öffnen** zeigt den
Dialog mit den vorhandenen Zuordnungen. Bei Gruppen lässt sich zwischen Benutzern
und Rollen wechseln. **Hinzufügen** weist einen Eintrag zu; **Entfernen** hebt genau
diese Zuordnung auf. Die Person, das Benutzerkonto oder die Rolle selbst wird dabei
nicht gelöscht. Der Schutz vor Entfernung des letzten Administrators bleibt aktiv.

Neue Gruppen und Rollen entstehen weiterhin über **Neu anlegen**. Bestehende
Gruppen- und Rollennamen sind in dieser Version nicht umbenennbar; der Dialog dient
der Verwaltung ihrer Zuordnungen.

## Kalender und Termine

Der Kalender zeigt einen Monat mit Einträgen pro Tag. Pfeile wechseln den Monat,
**Heute** springt zum aktuellen Monat. Ein Klick auf einen Tag öffnet im Desktop
dessen Einträge und die Terminanlage; im Portal öffnet er direkt die Terminanlage.
Das gewählte Datum ist vorbelegt. Im Desktop bietet der Tagesdialog zusätzlich die
Anlage einer Veranstaltung an, wenn das Veranstaltungsmodul bereit ist.

Datum und Uhrzeit werden im Desktop mit Kalenderauswahl und getrennten Stunden-
und Minutenfeldern gewählt; das Portal verwendet HTML-Datums-/Zeitfelder.
Bei ganztägigen Terminen ist das Ende weiterhin der erste nicht enthaltene Tag.

Unter **Zugeordnete Person oder Organisation** wird der Bezug ausgewählt. Für den
Ablauf einer Personenlizenz beispielsweise einen Termin mit Titel „Lizenzablauf“,
der betreffenden Person und dem Ablaufdatum anlegen. Anschließend kann über die
Kalenderaktion eine Erinnerung eingerichtet werden. Termine aus Ablaufdaten werden
hierbei nicht automatisch erzeugt.

## Lokal prüfen

```bash
cmake --build --preset user-macos-vscode-debug --parallel
./scripts/run-dev-macos.sh
```

Beim Start den öffentlichen Lizenzschlüssel wie in der Lizenzanleitung setzen.

1. Ohne gültige Modullizenz: keine Modulnavigation, Status in Erweiterungen sichtbar.
2. Mit Lizenz und installierten/aktivierten Modulen: passende Navigation sichtbar.
3. Gruppen/Rollen öffnen, eine Zuordnung hinzufügen und wieder entfernen.
4. Kalendertag wählen, Datum/Uhrzeit und Person prüfen, Termin speichern.
5. Kalender neu laden und prüfen, dass der Termin am gewählten Tag erscheint.
