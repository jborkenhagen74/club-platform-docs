# Dokumentvorlagen und Platzhalter — Phase 4

Die zentrale `PlaceholderRegistry` wird von LocalClient und HTTP-Client gemeinsam
verwendet. Desktop und Portal enthalten Platzhalterauswahl, explizite Kontextauswahl,
Vorschau ungespeicherter Entwürfe und Ausgabe gespeicherter Vorlagen als PDF.
Dokumente sind in Personen- und Organisationsakten erreichbar.

## Bedienung

1. Eine Akte öffnen und zum Reiter Dokumente wechseln, oder Dokumentvorlagen über
   Administration öffnen. Vorlage anlegen oder bearbeiten.
2. Geltungsbereich wählen: Person, Organisation, Mitgliedschaft oder global.
3. Platzhalter laden (Desktop: Dokumentwerkzeuge), auswählen und einfügen.
4. Kontext auswählen: etwa Person, Organisation oder Mitgliedschaft. Bei mehreren
   Anschriften/Kontakten/Funktionen den gewünschten Datensatz ausdrücklich auswählen.
   Die Suche und Auswahl verwenden die vorhandenen berechtigten Verwaltungslisten.
5. Vorschau öffnen. Sie speichert keine Vorlage. Nach dem Speichern kann die
   gespeicherte Version als PDF ausgegeben werden.

Unbekannte Platzhalter, unpassender Scope, mehrdeutige Auswahl und fehlende Rechte
werden abgewiesen. Bei Änderungen am Text erneut Vorschau ausführen. Eine PDF-Ausgabe
verwendet die gespeicherte Vorlage, nicht einen noch ungespeicherten Entwurf.

## Vertrag

Ein Deskriptor enthält `key`, `label_key`, `description_key`, `value_type`, `scope`,
`source`, `required_permission`, `format`, `module_id`. Die Liste wird für die
aktuelle Sitzung nach Rechten gefiltert. Die alten Aliase bleiben erhalten:

| Alias | Kanonischer Schlüssel |
|---|---|
| `given_name` | `person.given_name` |
| `family_name` | `person.family_name` |
| `date` | `document.date` |

Core-Namensräume: `document`, `person`, `organization`, `membership`, `department`,
`position`, `sender`, `recipient`. Enthalten sind unter anderem Namen, persönliche
Stammdaten, E-Mail/Telefon, Anschriften, Erziehungsberechtigte, Notfallkontakt,
Register-/Verbandsdaten, Mitgliedschaftsfristen und Funktionen. Die aktuelle
verbindliche Liste liefert der Discovery-Endpunkt.
Custom Fields erscheinen als `person.custom.<key>` bzw. `organization.custom.<key>`.

Vorlagen speichern `title`, `body`, `scope`, `language`, `locale`,
`template_group_id`. Titel höchstens 120 Zeichen, Text höchstens 12000 Zeichen.
Standard-Scope ist `person`; Sprache und Locale sind standardmäßig `inherit`.
Die optionale Vorlagengruppen-ID ist eine UUID. Schema 10 übernimmt vorhandene
Vorlagen mit diesen Defaults; alte Vorlagentexte müssen nicht umgeschrieben werden.

Der Renderkontext enthält Template-, Personen-, Organisations- und Mitgliedschafts-ID,
Dokumentdatum, Sprache und Locale. Eine Mitgliedschaft kann Person und Organisation
bestimmen; widersprüchliche Angaben werden abgewiesen. Optionale Auswahl-IDs:
`address_id`, `email_id`, `phone_id`, `position_id`, `extension_record_id`.
Fremde und archivierte Auswahlobjekte werden nicht übernommen. Ohne explizite Auswahl
wird nur ein eindeutiger aktiver Datensatz verwendet. Fehlende optionale Werte sind
leer; fehlende Rechte führen zum Fehler, nicht zu stiller Teilausgabe.

`current_user_id` stammt ausschließlich aus der Sitzung und darf nicht vom Client
gesetzt werden. `event_id`, `calendar_entry_id`, `finance_account_id` sind für spätere
Provider reserviert; belegte Werte werden derzeit abgewiesen.
Datum bleibt in dieser Phase ISO-formatiert. `document.datetime` ist der Beginn des
gewählten Dokumenttages (`T00:00:00`), kein Erstellungszeitstempel.
Sprache/Locale werden aus Vorlage oder Kontext übernommen, Fallback `de-DE`.
Vollständige sprachabhängige Formatierung und Sprachpakete folgen in Phase 5.

## Rechte und Modulprovider

Speichern, Vorschau und Ausgabe prüfen Scope und Rechte erneut. Feldrechte gelten
auch für Administratoren mit allgemeinem Wildcard-Recht. Ein Rechteentzug sperrt
damit ebenfalls bestehende gespeicherte Vorlagen.

Ein bereites V3-Modul kann `document.placeholder-provider` Version 1 anbieten.
Seine Manifest-Platzhalter benötigen Modulnamensraum, Label-/Beschreibungsschlüssel,
Typ, Scope und ein deklariertes Modulrecht. Der Host prüft zusätzlich `<module>.read`.
Ein optionaler eigener `record_type` bestimmt die ausgewählten Moduldatensätze.
Der Provider erhält den autorisierten Kontext und ausgewählte eigene Datensätze,
keine Sitzungstoken oder Datenbankverbindung. Rückgabe: `{ "value": "…" }`.
Werttyp und Länge werden validiert. Inaktive Module liefern keine Platzhalter.
Ausgaben werden nicht erneut als Vorlagensyntax interpretiert und als Klartext gerendert.

## HTTP unter `/api/v1`

| Methode und Route | Eingabe / Ergebnis |
|---|---|
| `GET /documents/placeholders?scope=person` | `{items: [descriptor,…]}` |
| `POST /documents/preview` | `{context: {...}, draft: {...}}` → `{title,body}` |
| `POST /documents/render` | Kontext mit `template_id` → `{title,body}`; Legacy-`date` bleibt gültig |
| `POST /extensions/{id}/state` | `{revision: "1", enabled: false}` → 204; `schema.manage` erforderlich |

Alle Aufrufe sind authentifiziert. Ungültige Eingaben: 400, fehlende Rechte: 403,
fehlender Datensatz: 404, Revisionskonflikt: 409. Vorschau und Ausgabe erzeugen
Audit-Ereignisse. Ohne erfolgreiche Validierung gibt es keine Dokumentausgabe.

## Prüfung und nächste Schritte

Tests umfassen Legacy-Kompatibilität, Scope, unbekannte Schlüssel, gefälschte
Benutzer-ID, Kontaktauswahl, Feldrechteentzug und nicht rekursive Modulwerte.
Client-Verträge laufen gegen lokalen Host und echte HTTP-API. Qt-Smoketests prüfen
lokale/Remote-Vorschau; Playwright prüft Picker/Vorschau bei Desktop- und Mobilbreite.
PostgreSQL führt dieselben neuen fachlichen Tests in der CI aus.
Phase 5 ergänzt vollständige I18n; Phase 6 den vollständigen Erweiterungsmanager
und Martial-V3-Migration. Dieser Stand ist keine vollständige 0.6.0-Freigabe.
