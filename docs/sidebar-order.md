# Individuelle Reihenfolge im Desktop-Seitenmenü

Am Griff rechts neben einem Menüeintrag ziehen und an der markierten Position
loslassen. Am oberen und unteren Rand scrollt das Menü automatisch. Escape oder
Loslassen außerhalb des Menüs bricht das Verschieben ab. Alternativ den Griff
fokussieren und Alt+Pfeil hoch/runter drücken.

Alle Einträge einschließlich Erweiterungen, Administration und Einstellungen sind
verschiebbar. Die bisherige Trennung zwischen Core und Modulen entfällt, damit
beispielsweise Training direkt unter Personen stehen kann.

Die Reihenfolge wird lokal in QSettings gespeichert, getrennt nach angemeldetem
Benutzernamen und Datenbankpfad beziehungsweise Serveradresse. Sie bleibt bei einem
Neustart erhalten; sie wird nicht zwischen Rechnern oder mit dem Webportal
synchronisiert. Ein geänderter Benutzername oder Verbindungsort beginnt mit der
Standardreihenfolge. Abmelden entfernt die aktive Zuordnung aus dem Speicher.

Unter Einstellungen / Darstellung stellt **Menüreihenfolge zurücksetzen** die
Standardreihenfolge wieder her. Neue Module werden angehängt. Vorübergehend
ausgeblendete Module behalten ihre gespeicherte Position. Die Reihenfolge verändert
keine Berechtigungen oder Lizenzprüfungen.

## Prüfung

Automatisierte Sortierprüfung: `node tests/navigation_order_tests.cjs`.

Manuell mit dem Qt-Desktop prüfen:

- Core- und Modul-Einträge nach oben und unten ziehen; Einfügemarkierung prüfen.
- Bei vielen Modulen am Rand scrollen; außerhalb ablegen und Escape testen.
- Nach Verschieben weiterhin dieselbe Ansicht anzeigen; Klick navigiert wie zuvor.
- Neustart mit Benutzer A; Reihenfolge bleibt erhalten.
- Abmelden, Benutzer B anmelden; eigene Reihenfolge verwenden, danach A prüfen.
- Gleicher Login an anderer Datenbank/Serveradresse; unabhängige Reihenfolge.
- Modul deaktivieren und wieder aktivieren; gespeicherte Position bleibt erhalten.
- Kompakte Seitenleiste und Tastaturbedienung testen; Reihenfolge zurücksetzen.

## Gruppen

Über **Gruppen verwalten** unten im Seitenmenü eigene Gruppen anlegen, umbenennen
oder auflösen. Ein Klick auf den Gruppenkopf klappt die Gruppe auf oder zu.
Zustand und Zuordnung werden mit der Reihenfolge je Benutzer und Verbindung
lokal gespeichert. Die bisherige Reihenfolge wird beim ersten Laden übernommen.

Einträge auf die **Mitte** eines Gruppenkopfs ziehen, um sie zuzuordnen; das
funktioniert auch bei geschlossenen Gruppen. Auf einen Eintrag innerhalb einer
Gruppe ziehen, um davor/dahinter einzusortieren. Am oberen oder unteren Rand eines
Gruppenkopfs ablegen, um einen Eintrag wieder außerhalb der Gruppe zu platzieren.
Gruppenköpfe selbst am Griff verschieben. Es gibt eine Gruppenebene ohne
verschachtelte Untergruppen. Beim Auflösen bleiben auch derzeit ausgeblendete
Modul-Einträge erhalten. Zurücksetzen entfernt Gruppen und individuelle Reihenfolge.

Zusätzliche manuelle Prüfung: zwei Gruppen anlegen, umbenennen, schließen und
neu starten; Einträge zwischen Gruppen und nach außerhalb verschieben; leere und
gefüllte Gruppen auflösen; anschließend Benutzer wechseln und Zuordnung prüfen.

## Banking

Banking ist als `finance.sections`-Beitrag registriert. Die Desktop-Finanzansicht
bettet `banking/workspace` ein. Es ist daher unter **Finanzen** erreichbar, sofern
das Banking-Modul bereit ist und der Benutzer Leseberechtigung besitzt; ein eigener
Navigationsbeitrag wird derzeit nicht registriert.
