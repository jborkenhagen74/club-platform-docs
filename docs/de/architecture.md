# Architektur und Sicherheitsmodell

Der Desktop-Controller verwendet ausschließlich das gemeinsame `Client`-Interface. `LocalClient` bindet die authentifizierten Core-Dienste im Prozess ein; `RestClient` verwendet dieselben Operationen über `/api/v1`. Die Auswahl erfolgt beim Anwendungsstart. Der UI-Controller hat keine Build-Abhängigkeit auf Host, Anwendung oder Persistenz.

> Zielversion 0.6.0, Vorarbeit G0: HTTP-API `/api/v1` und gemeinsamer `Client` mit `LocalClient`/`RestClient`. Datenbankschema 8 und Extension ABI 2 bleiben bestehen. Alte `/api/...`-Pfade liefern 404. Server, Desktop, Portal und Proxy gemeinsam aktualisieren. Die folgenden Funktionsbeschreibungen stammen aus der 0.5.0-Basis und gelten weiterhin, soweit dieser Hinweis sie aktualisiert. Core Foundation II mit ABI V3 und sieben UI-Sprachen ist noch nicht abgeschlossen.


[Sprachstart](README.md) · [Benutzerhandbuch](user-manual.md)

## Geltungsbereich

Diese Dokumentation beschreibt **Club Platform 0.5.0**, Implementierungsstand
`320a4c2709c13dd56455768a2f8819a815ad3997`, Schema 8 und Erweiterungs-ABI 2.
Die Produktversion, Datenbankmigrationen und ABI-Version sind unterschiedliche
Verträge. Die Dokumentation in fünf Sprachen bedeutet keine vollständige
Lokalisierung der derzeit überwiegend deutschen Anwendung.

Club Platform verwaltet Personen, Organisationen, Mitgliedschaften, Funktionen,
Kontakte, Dateien und sportartspezifische Daten. Eine Person kann mehreren
Organisationen zugeordnet sein. Ein Benutzerkonto ist eine Anmeldeidentität und
entsteht nicht automatisch beim Anlegen einer Person. Organisationen sind
allgemeine Datensätze: Dachverbände, Landesverbände, Vereine, Sportschulen,
Unternehmen oder sonstige Organisationen.

## Betriebsarten und Verantwortlichkeiten

| Betriebsart | Oberfläche | Verarbeitung und Speicherung |
|---|---|---|
| Einzelplatz | Qt Quick/QML | Lokaler Host mit SQLite und denselben Core-Diensten |
| Desktop am Server | Qt Quick/QML | HTTPS-REST; Server besitzt Datenbankverbindung |
| Webportal | React/TypeScript, Tailwind 4 | Statische Webdateien; HTTPS-Proxy zum C++-Server |

Die Anwendungsschicht löst jede Sitzung auf und prüft die Rechte. Der Client darf
keine handelnde Benutzer-ID bestimmen. REST-Objekte mit `actor` oder `actor_id`
werden abgewiesen. Der Server bindet an `127.0.0.1`; TLS und öffentliche
Erreichbarkeit übernimmt ein vorgeschalteter Webserver. Direkte Datenbankzugriffe
gehören nicht zur Clientintegration. SQLite und PostgreSQL sind
Persistenzalternativen, keine gleichzeitig synchronisierten Datenbestände.

Der Remote-Desktop besitzt keinen Offline-Schreibcache. Das Webportal speichert
Sitzungstoken nur im Arbeitsspeicher; ein Neuladen verlangt eine neue Anmeldung.
Im Browser wird lediglich die Darstellungseinstellung lokal gespeichert.

## Datenmodell

UUIDs identifizieren Datensätze unabhängig von Namen oder Mitgliedsnummern.
Veränderliche Datensätze tragen eine Revision; Aktualisierungen müssen die zuvor
gelesene Revision mitsenden. Ein Konflikt schützt vor verloren gegangenen
Änderungen. Eine Revisionsnummer ist im REST-Vertrag eine Zeichenkette, damit
JavaScript keine großen Ganzzahlen unbemerkt rundet.

Personenakten bündeln Identität, persönliche Stammdaten, Kontaktwege, Anschriften,
Beziehungen, Mitgliedschaften, Funktionen, eigene Felder und Dateien. Eine
Mitgliedschaft verbindet Person und Organisation; Abteilung und Beitragsgruppe
sind zusätzliche Zuordnungen. Die Beitragsgruppe ist eine Stammdatendefinition,
kein automatischer Zahlungs- oder SEPA-Prozess.

Die direkte übergeordnete Organisation bildet eine Hierarchie. Beispiel:
Deutsche Taekwon-Do Union → Landesverband → Sportschule. Weitere Verbands- oder
Kooperationsbeziehungen werden separat erfasst. Eine Hierarchie gewährt keine
zusätzlichen Benutzerrechte; sie ist kein Sicherheits- oder Mandantenfilter.
Zyklische Elternzuordnungen sind nicht zulässig.

Eigene Felder haben Definition, Datentyp, Gruppenrechte und Werte. Lesen und
Schreiben sind getrennte Berechtigungen. Ein reines Schreibrecht macht den
vorhandenen Wert nicht sichtbar. Feldtypänderungen müssen alle vorhandenen Werte
konvertieren können; andernfalls wird die Änderung als Ganzes verworfen.

## Anmeldung und Rechte

Passwörter werden mit Argon2id gehasht; Sitzungstoken werden serverseitig ebenfalls
nicht im Klartext gespeichert. Standardmäßig endet eine Sitzung spätestens nach
acht Stunden oder nach 30 Minuten ohne berechtigte Aktivität. Fünf fehlgeschlagene
Anmeldungen führen zum konfigurierten Sperrintervall von 30 Sekunden. Clients
sollten Fehler verständlich anzeigen und keine schnellen Wiederholschleifen starten.

Benutzer → Gruppen → Rollen → Berechtigungen: Ohne passende Freigabe wird ein
Zugriff verweigert. `records.read/write` betreffen allgemeine Datensätze,
`memberships.read/write` Mitgliedschaften und Funktionen. `security.manage`
verwaltet Zugänge und Branding; `schema.manage` Felddefinitionen, Vorlagen und
Erweiterungsinstallation. `audit.read` betrifft Audit-Zugriff der Core-API;
0.5.0 veröffentlicht dafür keine eigene HTTP-Route. `*` ist eine umfassende
Administratorberechtigung. Mindestens ein aktiver Administrator muss erhalten bleiben.

Feldrechte sind zusätzlich zu allgemeinen Rechten zu beachten. Native
Sportdatensätze verlangen außerdem `martial.read` bzw. `martial.write`.
Es gibt in diesem Stand keine automatische Einschränkung eines Kontos auf „seine“
Person oder Organisation. Das Portal ist ein berechtigungsgeprüftes
Verwaltungsfrontend, kein fertiges Mitgliederselbstbedienungsportal.

## Dateien, Transaktionen und Grenzen

Dateien liegen einschließlich Inhalt in der Datenbank. Ein separates Medienverzeichnis
muss für diese Inhalte nicht mitgesichert werden. Normale Dateien dürfen maximal
5 MiB groß sein; Profilbilder und Branding maximal 2 MiB auf der Serverseite.
Die Oberflächen skalieren PNG/JPEG und begrenzen die Bildfläche auf 16 Megapixel.
Ein Foto ersetzt das bisherige Foto desselben Datensatzes. Allgemeine Dateiuploads
sind kein Mechanismus zur Installation nativer Erweiterungen.

Änderungen und zugehörige Audit-Einträge gehören zusammen in eine Transaktion.
Der lokale SQLite-Adapter serialisiert Schreibtransaktionen; PostgreSQL nutzt die
entsprechenden Transaktions-/Sperrmechanismen. Das garantiert nicht, dass ein
mehrseitiger CSV-Export ein zeitpunktgenauer Datenbanksnapshot ist.

Nicht als fertig voraussetzen: signierte Installer, automatische Installation von
Updates, Rechnungs-/Zahlungsläufe, Terminverwaltung, Offline-Synchronisation,
Mandantentrennung, automatische Dokumentversendung oder frei ladbare
Plugin-Menüs/REST-Routen. [Versionierung](versioning.md) trennt diese Punkte von
bereits implementierten Funktionen.
