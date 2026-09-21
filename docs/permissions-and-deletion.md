# Berechtigungen und Löschen

## Rechte zuweisen

Unter **Administration → Rollen → Öffnen** eine Rolle auswählen. Das Auswahlmenü
zeigt die verfügbaren Rechte mit übersetzten Bezeichnungen. Der Infotext erläutert
die ausgewählte Aktion und ihren Geltungsbereich. Weitere Rechte geladener Module
werden aus deren Deklaration ergänzt. Die technischen Schlüssel bleiben unverändert.

- Grundrechte wie `calendar.read` erlauben zunächst den Zugriff auf die eigene
  verknüpfte Person.
- `.organization` benötigt zusätzlich das entsprechende Grundrecht und eine
  aktuell gültige Funktion in der Organisation.
- `.all` benötigt ebenfalls das Grundrecht und erweitert den Zugriff auf alle Personen.
- `*` erlaubt alle allgemeinen Aktionen. Gesonderte Feldrechte gelten weiterhin.

Die Beschreibung eines Rechts ersetzt weder die Modulfreischaltung noch die Prüfung
von Feld- und Datensatzrechten.

## Schutz vor eigenem Rechteentzug

Änderungen an Gruppenmitgliedschaften, Gruppenrollen, Rollenberechtigungen und
Kontostatus dürfen die effektiven allgemeinen Rechte des ausführenden Administrators
nicht verringern. Das gilt auch bei mehreren Administratoren und bei gemeinsam
verwendeten Rollen. Eine gleichwertige Berechtigung über eine andere Rolle verhindert
keinen überflüssigen Zuordnungsabbau: Entscheidend ist der tatsächliche Rechteverlust.

Die Änderung wird bei einem Verstoß vollständig zurückgerollt. Ein anderer
Administrator muss den beabsichtigten Rechteentzug durchführen. Der bisherige Schutz,
dass mindestens ein nutzbarer Administrator verbleiben muss, gilt zusätzlich.

## Personen und Organisationen löschen

In der Desktop-Personenliste stehen **Archivieren/Wiederherstellen** und
**Endgültig löschen** im Menü **⋯**. Auch in Personenakten und Organisationslisten
sind diese Aktionen vorhanden. Die Rückfrage nennt bei der Personenliste den Namen.
Für das endgültige Löschen einer Person oder Organisation sind `records.delete`
und `security.manage` erforderlich.

Löschen ist möglich, wenn keine Verknüpfungen mehr bestehen. Kontakte, Adressen,
Dateien, Mitgliedschaften, Funktionen, Konten, Unterorganisationen oder Moduldatensätze
können es weiterhin verhindern – auch nach ihrer Archivierung. Es werden keine
verknüpften Daten automatisch mitgelöscht. **Archivieren** erhält diese Daten.

Die eingebauten Finanz- und Kalenderdienste verwenden die Verknüpfungsprüfung der
Datenbank. Bei anderen Erweiterungen läuft die Prüfung unabhängig von Aktivierung
und Softwarelizenz. Fehlt die nötige Moduldatei oder Prüffunktion, wird das Löschen
mit einer erklärenden Meldung abgelehnt; Moduldatei laden/aktualisieren oder archivieren.
