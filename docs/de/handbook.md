# Benutzerhandbuch

Diese Seite ist der Schnelleinstieg. Die [ausführliche Bedienungsanleitung mit
Screenshots](bedienung.md) erklärt sämtliche Funktionsbereiche Schritt für Schritt.
Der [Formularatlas](formulare.md) führt jede Finanz-/Terminaktion mit ihren Feldern auf.

## Einstieg und Stammdaten

Melde Dich mit Deinem Benutzerkonto an. Unter Einstellungen kannst Du Sprache und Format-Locale getrennt wählen. Die Modulnavigation berücksichtigt gültige Lizenz, Aktivierung und Betriebsbereitschaft. Für den Zugriff werden zusätzlich Deine Rechte geprüft; ein sichtbarer Menüpunkt erteilt keine Berechtigung. Die Modulverwaltung zeigt auch gefundene, aber noch nicht nutzbare Module.

Lege Personen und Organisationen an. In der Personenakte verwaltest Du Stammdaten, Kontakte, Adressen, Mitgliedschaften, Funktionen sowie Dateien. Organisationen können hierarchisch zugeordnet werden. Lade Nachweise im passenden Dateien-/Dokumentenbereich hoch. Ein Benutzerkonto kann genau einer Person zugeordnet werden; diese Verknüpfung steuert personenbezogene Ansichten.

Listen lassen sich über beschriftete Such-, Sortier- und Filterfelder eingrenzen. „Gleich“, „Ungleich“, „Kleiner als“ usw. entsprechen typisierten Vergleichen; der Filterwert muss zum Feldtyp passen. Öffnen führt zum Datensatz bzw. Zuordnungsdialog. Verwandte Zuordnungen werden im Dialog hinzugefügt oder entfernt.

## Rechte und Lebenszyklus

Administratoren vergeben Gruppen, Rollen und Rechte über die entsprechenden Dialoge. Die Rechteauswahl enthält Bezeichnungen und Hilfetexte. Ein Administrator darf sich nicht selbst die effektiven administrativen Rechte entziehen. Prüfe Änderungen zusätzlich mit einem getrennten Testbenutzer.

Archivieren blendet Stammdaten aus dem aktiven Bestand aus und kann rückgängig gemacht werden. Endgültiges Löschen ist nur ohne schützende Referenzen möglich. Finanzhistorie wird durch Gegenbuchungen korrigiert, nicht gelöscht. Eine fehlende Moduldatei kann eine sichere Referenzprüfung verhindern und dadurch die Löschung blockieren.

## Finanzen, Beiträge und Käufe

Lege in der Organisation die Währung fest, bevor Finanzdaten entstehen. Danach ist ein Währungswechsel gesperrt; bestehende Beträge werden nicht umgerechnet. Gib Beträge in der Oberfläche als Dezimalwerte ein, beispielsweise `12,50` EUR. Intern verwendet die API weiterhin ganzzahlige kleinste Währungseinheiten.

Erstelle ein Konto für eine Person oder Organisation. Forderungen erhöhen, Zahlungen vermindern den offenen Saldo; der Zahlungsbetrag selbst wird positiv dargestellt, die Saldenwirkung separat. Ordne Zahlungen offenen Forderungen zu. Teilzahlungen sind möglich; Überzahlungen bleiben als nicht zugeordneter Rest. Korrekturen erfolgen über Storno und neue Buchung.

Beiträge verwenden Pläne und Mitgliedschaftszuordnungen; Käufe verwenden Produkte und Positionen. In der Personenakte erscheinen freigeschaltete Personenkonten. Organisationsbezogene Leserechte begrenzen Funktionäre auf ihre zugehörigen Organisationen.

## Banking

Wähle bei Bedarf eine offene Forderung. Die Vorschläge zeigen übereinstimmende Referenz oder Betrag und werden erst nach Bestätigung gebucht. Teilzahlungen lassen den Rest offen; Überzahlungen bleiben als Guthaben verfügbar. Weitere Forderungen kannst Du anschließend im Finanzkonto zuordnen. Größere Importe werden seitenweise angezeigt: „Weitere Buchungen laden“.

Aktiviere Finance und Banking. Öffne im Finanzbereich Banking, lade die Konten und lege ein Bankkonto mit Organisation, IBAN und Name an. Die Währung stammt aus der Organisation.

Wähle Konto, CSV oder CAMT.053 und die UTF-8-Datei. Für CSV kannst Du das JSON-Mapping bearbeiten oder laden; im Portal auch speichern. Prüfe Datum, Vorzeichen, Währung und Verwendungszweck in der Vorschau. Bestätige anschließend den Import. Erst die gesonderte, bestätigte Zuordnung zum Personenkonto erzeugt einen Zahlungseingang.

Prüfe mögliche Duplikate ohne eindeutige Bankreferenz besonders sorgfältig. Abbuchungen bleiben zur manuellen Prüfung erhalten und werden nicht als Zahlungseingänge gebucht. [Vollständiger Mapping-Vertrag und Grenzen](../banking.md).

## Kalender und Veranstaltungen

Klicke im Monatskalender einen Tag an und erfasse Titel, Datum, Uhrzeit und Zuordnung. Beachte die Zeitzone und gegebenenfalls Wiederholung. Personen sehen eigene Termine; Funktionäre benötigen die passenden Organisationsrechte und eine aktuelle Funktion. Die Personenakte bietet eine Terminübersicht.

Veranstaltungen verwalten Anmeldung, Fristen, Kapazität und Warteliste. Gebühren benötigen das Finanzmodul. Kostenlose Veranstaltungen können unabhängig vom Kalendermodul genutzt werden. Erinnerungen sind derzeit innerhalb der Anwendung verfügbar; E-Mail und Push sind nicht implementiert.

## Sportlerlizenzen und Dokumente

Im Kampfsportbereich der Person erfasst Du Lizenzname, Erteilungsdatum, Ablaufdatum, erteilende Organisation oder Freitext sowie den Warnzeitraum in Tagen. Mehrere Fotos/Nachweise sind möglich. Bei aktiviertem Kalender werden Ablaufdaten aus den Lizenzdaten angezeigt; ändere die Fachlizenz, nicht die abgeleitete Kalenderanzeige.

Dokumentvorlagen verwenden registrierte Platzhalter. Wähle bei mehreren passenden Adressen, Funktionen oder Prüfungen den Kontext ausdrücklich aus. Vorschau und Ausgabe prüfen die Rechte erneut. [Vollständige Platzhalterliste](placeholders.md).
