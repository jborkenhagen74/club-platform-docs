# Sportlerlizenzen und persönlicher Kalender

Diese Sportlerlizenzen sind Nachweise einer Person, keine Freischaltungen der Software.
Erforderlich ist das Kampfsportmodul **martial 1.2.0**, für den Kalender zusätzlich ein
betriebsbereites, lizenziertes **calendar**-Modul. Das Veranstaltungsmodul ist für
Lizenzabläufe nicht erforderlich. Beim ersten Start wird die Datenbank auf Schema 15
aktualisiert; unter **Erweiterungen → Installieren / aktualisieren** anschließend die
neue Kampfsport-Moduldefinition übernehmen.

## Lizenz und Nachweise

1. Personenakte öffnen und **Sportlerlizenzen** auswählen.
2. Name, Erteilungsdatum, Ablaufdatum und Warnzeitraum in Tagen erfassen (0–3650).
3. Die erteilende Stelle als Freitext eintragen oder eine Organisation auswählen.
4. Speichern. Über **Nachweise / Dateien** in der Lizenzzeile ein oder mehrere Bilder,
   PDFs oder andere Nachweise hochladen (höchstens 5 MiB je Datei).
5. Ein vorhandener Dateieintrag lädt die Datei herunter. Die Nachweise bleiben genau
   dieser Lizenz zugeordnet, auch wenn eine Person mehrere Lizenzen besitzt.

Die Übersicht kennzeichnet bald ablaufende und abgelaufene Lizenzen. Der Warnzeitraum
ist eine Anzahl von 24-Stunden-Tagen vor dem Beginn des Ablauftags (Europe/Berlin).
Im Kalender erscheint ein ganztägiger, schreibgeschützter Ablauftermin; während des
Warnzeitraums erscheint zusätzlich eine In-App-Warnung. Es erfolgt keine E-Mail oder
Push-Zustellung. Änderungen an der Lizenz werden beim nächsten Laden berücksichtigt.
Archivierte Lizenzen erscheinen nicht im Kalender. Bei späterer Kalenderfreischaltung
werden vorhandene aktive Lizenzen automatisch berücksichtigt. Es entstehen keine
kopierten Termine, die getrennt aktualisiert oder gelöscht werden müssten.

## Benutzer einer Person zuordnen

In **Administration → Benutzer → Öffnen/Bearbeiten** die zugehörige Person auswählen
und speichern. Auch beim Anlegen eines Kontos ist diese Auswahl möglich. Die Zuordnung
ist optional; eine Person kann höchstens einem Benutzerkonto zugeordnet werden.
Ändern dürfen sie ausschließlich Benutzer mit `security.manage`.

## Berechtigungen und Sichtbarkeit

Alle Regeln gelten im gemeinsamen Backend, für Desktop, Portal und REST gleichermaßen.
Globale Modulrechte allein erlauben nicht länger das Lesen sämtlicher Kalendereinträge.

| Berechtigung | Wirkung |
|---|---|
| `calendar.read` | Eigene Kalendertermine der mit dem Konto verknüpften Person |
| `calendar.read.organization` zusätzlich | Termine von Personen mit aktiver Mitgliedschaft oder Funktion in der Organisation, in der der Leser aktuell eine Funktion innehat |
| `calendar.read.all` zusätzlich | Alle Kalendertermine, z. B. für zentrale Verwaltung |
| `calendar.write` | Eigene Kalendertermine anlegen/ändern |
| `calendar.write.organization` / `.all` zusätzlich | Entsprechender organisationsbezogener/globaler Schreibzugriff |
| `martial.read` und `records.read` | Eigene Sportlerlizenzen und Nachweise lesen |
| `martial.read.organization` zusätzlich | Sportlerlizenzen der eigenen Organisation als aktueller Funktionär lesen |
| `martial.write` und `records.write` | Eigene Sportlerlizenzen und Nachweise erfassen |
| `martial.write.organization` / `.all` zusätzlich | Entsprechender organisationsbezogener/globaler Schreibzugriff |

Auch `martial.read.all` ist verfügbar. Der vorhandene Administrator mit `*` behält
Vollzugriff. Für Lizenzabläufe sind sowohl Kalender-Leserecht als auch das passende
Kampfsport-Leserecht notwendig. Modulfreigabe und personenbezogene Rechte werden
unabhängig geprüft. Gruppenrollen erteilen Rechte; die Datensätze unter **Funktionen**
und **Mitgliedschaften** bestimmen deren Organisationsbereich. Ein Funktionstitel
allein erteilt kein Recht. Start-/Enddatum, Archivierung und aktiver Mitgliedsstatus
werden berücksichtigt; die Organisationshierarchie vererbt keine Freigaben automatisch.

Veranstaltungen sind für berechtigte Funktionäre, die verantwortliche Person und
zugeteilte Teilnehmer sichtbar (`events.read` erforderlich). Änderungen benötigen
organisationsbezogene oder globale Schreibrechte. Teilnehmerlisten werden zusätzlich
personenbezogen eingeschränkt. Private Erinnerungen bleiben an ihr Benutzerkonto
gebunden und verlieren bei Entzug des Zugriffs ihre Sichtbarkeit.

## Prüfung

- Zwei Personen mit getrennten Konten und Kalender-Leserecht: keine fremden Termine.
- Aktuelle Vereinsfunktion plus Organisationsrecht: Termine der aktiven Mitglieder.
- Funktion beenden oder Recht entfernen: Zugriff entfällt beim nächsten Abruf.
- Lizenz mit Ablauf innerhalb des Warnzeitraums: genau ein Ablauftermin plus Warnung.
- Lizenz ändern/archivieren: Projektion passt sich an; keine Duplikate.
- Nachweis-ID eines fremden Sportlers direkt aufrufen: Zugriff verweigert.

## Lokal aktualisieren

App schließen und im Projektverzeichnis den aktuellen Branch abrufen. Anschließend
wie bisher `./scripts/run-dev-macos.sh` verwenden: Das Skript konfiguriert, baut und
startet die Anwendung einschließlich der Module. Beim manuellen Weg zuerst
`cmake --build --preset user-macos-vscode-debug --parallel` ausführen und danach
die App erneut starten. In der Modulverwaltung Kampfsport auf **1.2.0** aktualisieren.
Die Anleitung setzt eine vorhandene Freischaltung für `martial` und optional
`calendar` voraus; die Sportlerlizenzen selbst sind keine Software-Lizenzkeys.
