# Inventarverwaltung (Erweiterung `inventory`)

## Einordnung

Eigenständige ABI-V3-Erweiterung für Eigentum einer Organisation oder Person. Der Core enthält weder Inventartabellen noch Inventaroberflächen. Das Modul stellt einen nativen Companion-Service, Qt-Quick- und React-Ansichten und versionierte Modulmigrationen bereit.

### Inventar und Ausleihen

- Ein Gegenstand besitzt **genau einen** Eigentümer (`organization` oder `person`). Eine Ausleihe verändert den Eigentümer nicht.
- Stammdaten: Name, Kategorie, Inventarnummer, Seriennummer, Standort, Zustand, Notizen, Menge, verliehene Menge und verfügbare Menge.
- Seriennummern sind für einzelne Gegenstände vorgesehen. Ein Gegenstand mit Seriennummer muss Menge 1 besitzen.
- Ein Inventargegenstand ist bei seinem Eigentümer über die Inventarnummer eindeutig (aktive Einträge).
- Gegenstände können nach der Anlage bearbeitet und archiviert werden. Eine Übertragung oder Archivierung mit offenen Ausleihen wird verhindert.
- Ausleihen referenzieren den bestehenden Personendatensatz, die Menge, optional ein Rückgabedatum und den Zeitpunkt der Ausgabe. Die Rückgabe markiert eine Ausleihe als abgeschlossen.
- Alle Bestandsänderungen sind transaktional; `UPDATE ... RETURNING`, CHECK-Constraints und Versionsprüfung verhindern negative Bestände, Überbuchungen und doppelte Rückgaben.
- Keine automatische Verknüpfung mit Finanzbuchungen: Eigentum ist unabhängig vom Bank-/Finanzmodul.

### Berechtigungen und Schutz

Serverseitige Prüfung für **jede** Operation, nicht nur beim Öffnen der Oberfläche:

| Berechtigung | Bedeutung |
| --- | --- |
| `inventory.read` | Grundrecht zum Lesen |
| `inventory.read.all` | Leserecht für alle Eigentümer |
| `inventory.read.organization` | Leserecht für Personen gemäß bestehenden Personenscope-Regeln sowie Organisationen mit aktiver Funktion |
| `inventory.write` | Grundrecht zum Bearbeiten |
| `inventory.write.all` | Schreibrecht für alle Eigentümer |
| `inventory.write.organization` | Schreibrecht im bestehenden Organisations-/Personenscope |

Personen dürfen mit dem Grundrecht auf ihr eigenes Inventar zugreifen. Organisationsinventar setzt die passende Organisationsberechtigung und eine gültige Position in der jeweiligen Organisation oder ein übergeordnetes `.all`-Recht voraus.

Die Auswahl `owners` zeigt nur Eigentümer, auf deren Inventar die Sitzung Leserechte besitzt. Übertragungen prüfen ausdrücklich **beide** Eigentümer.

### Schnittstelle

Authentifizierter REST-Endpunkt mit unveränderter Core-Extension-API:

```text
POST /api/v1/extensions/inventory/commands/{operation}
```

| Operation | Eingabe (Auszug) | Ergebnis |
| --- | --- | --- |
| `owners` | `owner_type`, `search` | `owners` |
| `list`, `more` | `owner_type`, `owner_id`, `search`, `after` | `items`, `next_cursor` |
| `save` | Eigentümer, Stammdaten, `quantity`, bei Änderungen `id` und `revision` | `item` |
| `archive` | `item_id`, `revision` | `id` |
| `transfer` | `item_id`, `revision`, neuer `owner_type` und `owner_id` | `id` |
| `loans` | `item_id` | `loans` |
| `checkout` | `item_id`, `borrower_person_id`, `quantity`, optional `due_date` | `id`, `item` |
| `checkin` | `loan_id`, `revision` | `id`, `item` |

Ein fehlender Eigentümer wird nicht stillschweigend angelegt. Aktive Inventare und Ausleihen sind nicht automatisch öffentlich. Schreibaufrufe protokollieren Aktionen im bestehenden Core-Audit.

## Lizenzierung mit dem Publisher

Im Publisher **„Inventarverwaltung (Organisationen & Personen)“** aktivieren. Die signierte Lizenz enthält den Modulbezeichner `inventory` in der vorhandenen Liste `modules`. Es gibt keine erforderlichen anderen Module (auch nicht `finance`).

Die Standard-Lizenzprüfung, Aktivierung und Ablaufkontrolle gelten unverändert; der Core prüft `module_licensed("inventory")` über `require_module_ready` **vor** dem Aufruf des Extension-Dienstes.

### Inbetriebnahme

1. Native Extension mit den anderen Modulen bauen und in die konfigurierte Extension-Directory kopieren/installieren. Die bestehenden Entwicklungs-Sammelziele nehmen `inventory` automatisch auf.
2. Eine signierte Lizenz inklusive `inventory` ausgeben und im Host importieren/aktivieren.
3. Die Erweiterung als berechtigter Administrator installieren; die Moduleigenmigration erzeugt die Inventartabellen.
4. Der Rolle `inventory.read`, `inventory.write` sowie die geeigneten Scope-Rechte zuweisen.
5. Desktop oder Webportal neu laden und die Navigation `Inventarverwaltung` öffnen.

Mit einer Lizenz ohne `inventory` werden weder Modulnavigation noch Inventar-API freigeschaltet. Eine abgelaufene Lizenz verweigert weiterhin den Zugriff; vorhandene Inventardaten bleiben erhalten.

### Prüfplan

- Extension-Definition einschließlich Migration, deutscher und englischer Übersetzungen prüfen.
- Publisher-Test: isoliertes `inventory`-Lizenzmodul, keine automatisch ergänzten Finanzrechte.
- SQLite-Schema-Test: genau ein Eigentümer, gültige Fremdschlüssel, Seriennummer/Mengenregel, Inventarnummer-Eindeutigkeit.
- Transaktionstest: keine Überbuchung, Rückgabe nur einmal, Versionskonflikt und Ausleihsperre vor Archivierung/Transfer.
- Ende-zu-Ende lokal in Desktop und Web: mit gültiger Lizenz, ohne Modulberechtigung, mit eingeschränktem Scope sowie mit abgelaufener/nicht enthaltener Modulfreischaltung.
- Datenbanktests zusätzlich mit dem PostgreSQL-Adapter durchführen.
