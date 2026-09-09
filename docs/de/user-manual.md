# Benutzerhandbuch

[Sprachstart](README.md) · [Installation](installation.md) · [Betrieb](operations.md)

**Ausgabe:** 0.5.0 / 2026-09-09. Für Mitarbeitende, Trainer, Verwaltung und
Administratoren. Beispiele verwenden erfundene Personen. Die Menünamen entsprechen
der derzeit überwiegend deutschen Oberfläche; Bildschirmgröße und Berechtigungen
können beeinflussen, welche Bedienelemente sichtbar sind.

## Inhalt

1. [Grundbegriffe](#grundbegriffe)
2. [Anmelden und Arbeitsplatz prüfen](#anmelden-und-arbeitsplatz-prüfen)
3. [Organisationen und Struktur](#organisationen-und-struktur)
4. [Personenakte](#personenakte)
5. [Mitgliedschaften und Funktionen](#mitgliedschaften-und-funktionen)
6. [Fotos und Unterlagen](#fotos-und-unterlagen)
7. [Kampfsport](#kampfsport)
8. [Eigene Felder](#eigene-felder)
9. [Dokumente und Auswertungen](#dokumente-und-auswertungen)
10. [Ansicht und Hilfe](#ansicht-und-hilfe)
11. [Administration](#administration)
12. [Fehler und tägliche Kontrolle](#fehler-und-tägliche-kontrolle)

## Grundbegriffe

Eine **Person** ist beispielsweise Mitglied, Trainer, Kontaktperson oder Förderer.
Ein **Benutzer** ist ein Konto für die Anmeldung. Das sind unterschiedliche
Datensätze: Eine angelegte Person kann ohne Konto verwaltet werden, und ein Konto
wird nicht automatisch mit einer Person verbunden.

Eine **Organisation** kann eine Sportschule, ein Verein, ein Verband oder ein
Unternehmen sein. Eine **Mitgliedschaft** verbindet eine Person mit einer
Organisation und enthält unter anderem Mitgliedsnummer, Status und Zeitraum.
Eine **Funktion** beschreibt eine Tätigkeit oder Position in einer Organisation.
Eine **Beziehung** erfasst beispielsweise eine Kontakt- oder Unterstützerrolle.
Diese Einträge nicht durch mehrfaches Anlegen derselben Person ersetzen.

Die Akte bündelt zusammengehörige Daten. Ein Reiterwechsel ändert nicht automatisch
die Person oder Organisation. Rechte ergeben sich aus Deinem Benutzerkonto;
eine übergeordnete Organisation gewährt keine zusätzlichen Zugriffsrechte.

## Anmelden und Arbeitsplatz prüfen

1. Desktop öffnen oder die vom Administrator bereitgestellte HTTPS-Adresse besuchen.
2. Im Desktop prüfen, ob Einzelplatz oder Serververbindung verwendet wird. Dieselben
   Namen in verschiedenen Datenbanken sind nicht automatisch derselbe Datenbestand.
3. Benutzername und Passwort eingeben, dann `Anmelden` wählen.
4. Nach der Anmeldung prüfen, ob die erwarteten Akten erreichbar sind.

Ein leerer Einzelplatz-Desktop bietet `Administrator einrichten`. Diese Funktion
ist für die Erstinbetriebnahme, nicht zum Anlegen weiterer normaler Konten.
Serverkonten richtet die Administration ein. Passwörter benötigen mindestens zwölf
Zeichen. Nach wiederholten Fehlversuchen kurz warten und die Eingabe prüfen.

Das Webportal verlangt nach Neuladen der Seite eine neue Anmeldung. Sitzungen
laufen standardmäßig spätestens nach acht Stunden oder nach 30 Minuten Inaktivität
ab. Vor längeren Unterbrechungen speichern und abmelden. Ein Browserfenster offen
zu lassen ist keine sichere Sperre des Arbeitsplatzes. Passwortänderung ist im
Desktop unter `Administration → Passwort ändern` erreichbar; im Portal gibt es
in diesem Stand dafür keine eigene Maske.

## Organisationen und Struktur

### Organisation anlegen

1. `Organisationen` öffnen und vorab suchen, ob der Eintrag bereits existiert.
2. `Neu anlegen` wählen und den vollständigen Namen eingeben.
3. Organisationsart auswählen: `Dachverband`, `Landesverband`, `Verein`,
   `Sportschule`, `Unternehmen` oder `Sonstige`.
4. Vorhandene Angaben ergänzen: Kurzname, Registerdaten, Gründungsdatum,
   Website, E-Mail, Telefon, Anschrift und Verbandskennungen.
5. `Speichern`, anschließend die Akte erneut öffnen und die Angaben kontrollieren.

Felder ohne vorhandene Information leer lassen, soweit sie optional sind.
Keine erfundenen Register- oder Verbandsnummern als Platzhalter verwenden.
Die Organisationseinstellungen bestimmen nicht automatisch Rollen oder Kontozugriffe.

### Hierarchie aufbauen

Zuerst den Dachverband anlegen, dann den Landesverband mit dem Dachverband als
übergeordneter Organisation, zuletzt Verein oder Sportschule mit dem Landesverband
als übergeordneter Organisation. Das Feld über eine Referenzauswahl mit einem
vorhandenen Datensatz verbinden; ein bloßer Namenstext erzeugt keine Verknüpfung.

Im Desktop zeigt `Struktur` die Unterorganisationen. Weitere Beziehungen zu
Verbänden gehören zu `Verbandszugehörigkeit` und erhalten Rolle und Zeitraum.
Eine Organisation darf nicht ihr eigener Vorfahr werden. Bei einer Fehlermeldung
den Elternpfad kontrollieren, nicht einfach einen zweiten gleichnamigen Verband anlegen.

### Weitere Bereiche

`Abteilungen` enthalten Name und Sportart. `Beiträge` enthält Beitragsgruppen mit
Betrag in **Cent**, Währung und Intervall: 25,00 EUR werden als `2500` Cent erfasst.
Diese Stammdaten führen keine Zahlung aus. Mitglieder, Funktionen, Beziehungen,
Kontakte, Anschriften und Dateien können aus der Organisationsakte heraus geöffnet
werden. Manche Ansichten unterscheiden sich zwischen Desktop und Portal.

## Personenakte

### Person neu erfassen

1. `Personen` öffnen und nach Vor-/Nachname suchen, um Dubletten zu vermeiden.
2. Eine neue Person mit Vorname und Nachname anlegen und speichern.
3. Den Datensatz bzw. `Akte öffnen` wählen.
4. Stammdaten schrittweise ergänzen; nach jedem abgeschlossenen Bereich speichern.

Die Suche ist wörtlich und berücksichtigt Groß-/Kleinschreibung. Wird eine Person
nicht gefunden, Suchtext verkürzen und weitere Seiten berücksichtigen. Eine Liste
zeigt maximal 100 Einträge pro Seite; die erste Seite ist nicht zwingend der gesamte Bestand.

### Reiter sinnvoll verwenden

| Bereich | Zweck |
|---|---|
| Übersicht | Vorname/Nachname und Identität |
| Persönlich | Geburtsdatum, Anrede, Geschlecht, Sorgeberechtigte und Notfallkontakt |
| Kontakt | Telefon-/E-Mail- oder weitere Kontaktwege mit Bezeichnung |
| Anschriften | Adressen mit nachvollziehbarer Bezeichnung |
| Mitgliedschaften | Zuordnung zu Organisation, Status, Nummer, Zeitraum |
| Funktionen | Rolle/Position in einer Organisation |
| Beziehungen | Weitere Kontakt- und Organisationsbeziehungen |
| Dateien | Sonstige Unterlagen; Foto steht im Aktenkopf |
| Eigene Felder | Zusätzlich definierte und für Dich freigegebene Core-Felder im Desktop |
| Graduierungen/Prüfungshistorie | Nach Aktivierung des Kampfsportmoduls |
| Dokumente/Dokumentvorlagen | Ausgabe gespeicherter Vorlagen für diese Person |

Datumsfelder folgen dem System- bzw. Browserformat. In technischen Exporten und
Schnittstellen können ISO-Daten wie `2026-09-08` erscheinen. Keine fremden
Datumsformate in ein Feld erzwingen, das bereits eine Systemvorgabe zeigt.

Auf schmalen Portalbildschirmen wählst Du den Reiter unter `Aktenbereich` aus.
Im Desktop können Aktenentwürfe mit `Entwurf behalten und schließen` gehalten
werden; ein Punkt markiert sie. Das ist **kein Speichern in der Datenbank**.
Im Portal die offene Bearbeitungsmaske speichern oder bewusst verwerfen, bevor
Du navigierst. Ungespeicherte Daten nicht als gesichert betrachten.

## Mitgliedschaften und Funktionen

In der Personenakte `Mitgliedschaften → Neu anlegen` öffnen. Die Person ist aus
der Akte vorgegeben; die Organisation ausdrücklich auswählen. Mitgliedsnummer,
Status und Beginn eintragen. Je nach Datenlage Mitgliedsart, Abteilung,
Beitragsgruppe und Austrittsangaben ergänzen. Bei Erfassung aus der Organisationsakte
ist umgekehrt die Organisation vorgegeben und die Person auszuwählen.

Ein Ende darf nicht vor dem Beginn liegen. `Aktiv`, `Ruhend` und `Beendet` sind
fachliche Zustände; nicht mit dem Aktivstatus eines Benutzerkontos verwechseln.
Bei einem Austritt vorhandenen Eintrag ändern und Enddatum/Grund dokumentieren,
statt die Person erneut anzulegen. Automatische Beitragsberechnung, Mahnung,
Lastschrift oder rechtliche Fristberechnung sind nicht Bestandteil dieses Stands.

Unter `Funktionen` eine Bezeichnung und den Gültigkeitszeitraum erfassen, zum
Beispiel Trainer oder Geschäftsführung. Solche fachlichen Funktionen erteilen
keine Benutzerrechte. Eine Trainerfunktion ersetzt keine Rollenfreigabe für
`martial.write`. Dieselbe Person kann mehrere Mitgliedschaften und Funktionen haben.

## Fotos und Unterlagen

Das Foto der Person bzw. Organisationslogo gehört an die feste Stelle im Aktenkopf.
`Foto auswählen`, `Logo auswählen` oder `Foto / Logo hochladen` verwenden. PNG und
JPEG sind vorgesehen. Die Oberfläche skaliert Bilder; sehr große oder beschädigte
Dateien können abgewiesen werden. Die Auswahl eines neuen Profilbilds ersetzt das
bisherige Bild dieses Datensatzes.

Für Verträge, Bescheinigungen oder andere Unterlagen den Reiter `Dateien` bzw.
`Unterlagen und Dateien` öffnen. `Datei hochladen` wählen, Datei auswählen und
Erfolgsmeldung abwarten. Anschließend Dateiname und Zuordnung kontrollieren.
Maximal 5 MiB pro Datei; das entspricht 5 × 1.024 × 1.024 Bytes. Dateinamen sollten
den Inhalt verständlich benennen. Keine Zugangsdaten oder ausführbare Plugins als
Arbeitsunterlagen verwenden.

Zum Abrufen den Eintrag wählen bzw. `Herunterladen` benutzen und einen Zielort
festlegen. Das Öffnen erfolgt anschließend bewusst mit einem geeigneten Programm.
Die Originaldatei außerhalb der Anwendung nicht löschen, bevor der Upload und ein
Kontrolldownload geprüft wurden. Eine allgemeine Löschoberfläche ist in 0.5.0
nicht vorhanden; bei falsch zugeordneten Dateien die Administration ansprechen.
Nicht jede Dateiliste ist automatisch nach Dateinamen durchsuchbar.

## Kampfsport

Der Administrator muss die Bibliothek auf dem Host bereitstellen und aktivieren.
Anschließend erscheinen `Graduierungen` und `Prüfungshistorie` in Personenakten.
Fehlen die Reiter, zuerst Aktivierung/Verbindung prüfen; bei einer Zugriffsverweigerung
sind zusätzlich die persönlichen Modulrechte zu prüfen.

Eine Graduierung enthält Disziplin/Stil, Stufe von 1 bis 30, freie Bezeichnung,
Verleihungsdatum und optional Prüfer. Beispiel: Disziplin `Taekwon-Do`, Stufe `8`,
Bezeichnung `8. Kup`. Die neutrale Stufenzahl bedeutet keine universelle Rangfolge
zwischen verschiedenen Verbänden. Die eigene Graduierungsordnung fachlich beachten.

Eine Prüfung enthält Disziplin, angestrebte Stufe, Datum, Ergebnis, Prüfer und
optionale Bemerkungen. Für das Ergebnis exakt `passed` (bestanden) oder `failed`
(nicht bestanden) verwenden. Eine gespeicherte Prüfung erzeugt nicht automatisch
eine neue Graduierung oder Urkunde; diese Schritte separat durchführen und prüfen.
Es gibt keine automatische Prüfungszulassung oder Gebührenabrechnung.

## Eigene Felder

Im Desktop definiert die Administration unter den Felddefinitionen zusätzliche
Felder für einen Datensatztyp. Typen: Text, ganze Zahl, Dezimalzahl, Ja/Nein, Datum.
Anschließend Feldrechte je Gruppe festlegen und den Wert in der Personen- oder
Organisationsakte unter `Eigene Felder` bearbeiten.

Ist nur Schreiben erlaubt, wird ein vorhandener Wert nicht angezeigt. Ein leer
angezeigtes Feld beweist dann nicht, dass nichts gespeichert ist. Vor einer
Feldtypänderung Daten prüfen und sichern: Wenn auch nur ein Wert nicht konvertierbar
ist, wird die Änderung ohne Teilmigration abgewiesen. Im Portal werden Definitionen
und Feldrechte dieser Core-Felder derzeit nicht verwaltet.

## Dokumente und Auswertungen

Administratoren legen unter `Dokumentvorlagen` Titel und reinen Text an. Erlaubte
Platzhalter sind unverändert:

```text
Teilnahmebestätigung

Hiermit bestätigen wir die Teilnahme von {{given_name}} {{family_name}}.
Ausstellungsdatum: {{date}}
```

Keine weiteren Namen wie `{{member_number}}` erfinden: unbekannte Platzhalter
werden abgewiesen. Die Vorlage enthält keinen ausführbaren Code. Die Person
zum Befüllen wählst Du durch Öffnen ihrer Akte.

Desktop: gespeicherte Vorlage im Reiter `Dokumente` öffnen und
`Gespeicherte Vorlage als PDF öffnen` wählen. Zielpfad angeben; der System-PDF-
Betrachter zeigt die Ausgabe. Im Portal `PDF-Vorschau` wählen. Falls der mobile
Browser keine eingebettete Vorschau zeigt, `PDF öffnen` oder `Herunterladen` nutzen.
Namen, Datum, Umbrüche und Inhalt vor Weitergabe prüfen. Es findet kein automatischer
E-Mail-Versand statt. Das Vorlagendatum wird derzeit als ISO-Datum eingesetzt.

Für Listen erst Bereich und Suchfilter wählen, dann `CSV exportieren` bzw.
`Gefilterte Liste exportieren`. Der Export kann bis zu 5.000 Einträge über alle
Seiten enthalten. Währenddessen sollte niemand den betreffenden Bestand bearbeiten.
In der Tabellenkalkulation UTF-8 und Komma als Trennzeichen verwenden. Ein führendes
Apostroph bei formelähnlichen Werten ist eine Schutzmaßnahme; nicht ungeprüft entfernen.
Leere Listen bedeuten keine automatische Fehlfunktion: Filter und Rechte prüfen.

## Ansicht und Hilfe

Desktop: `Einstellungen → Ansicht → Darstellung und Farben`. Systemmodus folgt
Hell/Dunkel; alternativ eines der fünf Layouts wählen, darunter hoher Kontrast.
Im Desktop sind außerdem eigene Farbanpassungen möglich. Portal:
`Einstellungen → Ansicht`; Systemmodus oder Hell, Dunkel, Wald, Pflaume,
hoher Kontrast. Eigene Farbwerte sind dort noch keine separate Funktion.

Administratoren legen unter `Einstellungen → Startbildschirm` bzw. den
entsprechenden Portal-Einstellungen Logo und Hintergrund fest. Diese Bilder
werden bereits vor Anmeldung angezeigt: ausschließlich dafür geeignete Inhalte
verwenden. Sie sind nicht das individuelle Foto einer Person.

Desktop: `Hilfe → Nach Updates suchen` prüft stabile Releases. Bei einem privaten
Repository kann die Abfrage ohne passenden Zugriff scheitern; das beweist nicht,
dass die installierte Version aktuell ist. Die Prüfung installiert nichts.
Versionswechsel mit der Administration anhand des Betriebsplans durchführen.

## Administration

Einen neuen Benutzer anlegen, einer Gruppe zuordnen, der Gruppe eine Rolle zuweisen
und der Rolle erforderliche Rechte geben. Diese Kette vollständig prüfen. Für
allgemeine Lesezugriffe `records.read`, für Mitgliedschaften zusätzlich
`memberships.read`, für Kampfsport zusätzlich `martial.read` verwenden. Schreibrechte
nur bei Bedarf ergänzen. `*` nicht als schnelle Reparatur aller Fehlermeldungen vergeben.

Das letzte aktive Administratorkonto darf nicht deaktiviert oder seiner letzten
Adminzuordnung beraubt werden. Bei Passwortverlust das dokumentierte lokale
Wiederherstellungsverfahren nutzen; kein öffentliches „Admin zurücksetzen“-API
wird angeboten. Eine fachliche Funktion in einer Akte ist keine Sicherheitsrolle.
Feldrechte erfordern zusätzlich eine passende Gruppenfreigabe.

## Fehler und tägliche Kontrolle

| Beobachtung | Nächster Schritt |
|---|---|
| Nach Namenseingabe kein Fortgang | Speichern/Neu-anlegen-Aktion und sichtbare Fehlermeldung prüfen; Fenstergröße und aktuellen Build kontrollieren |
| Änderungen nicht sichtbar | Richtige Akte und Betriebsart prüfen, aktualisieren, Filter zurücksetzen |
| Zugriff verweigert | Administration um Prüfung der konkreten Rolle und gegebenenfalls Feld-/Modulrechte bitten |
| Datensatz wurde geändert | Eigene Eingaben sichern, aktuellen Stand laden, Unterschiede bewusst übernehmen |
| Netzwerkfehler nach Speichern | Nicht erneut klicken; zunächst prüfen, ob die Änderung bereits gespeichert wurde |
| Modul fehlt | Hostverzeichnis, Aktivierung und passende Modulversion prüfen lassen |
| PDF öffnet sich nicht | Speicherort prüfen, Systembetrachter bzw. „PDF öffnen“ im Portal verwenden |
| Datei zu groß | Geeignete kleinere Datei erstellen; Original aufbewahren |

Am Tagesende offene Entwürfe bearbeiten, wichtige Änderungen durch erneutes Lesen
kontrollieren und abmelden. Backupstatus und Wiederherstellungsproben sind Aufgaben
der Administration. Bei Supportanfragen Produktversion, Betriebsart, Zeitpunkt,
Aktion und Fehlermeldung nennen; Passwörter, Token und unnötige Personendaten weglassen.
