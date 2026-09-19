# Vollständige Platzhalterreferenz

Stand: Schema 18 / Extension ABI V3. Diese Liste wurde aus der tatsächlichen Core-Registrierung und den mitgelieferten Modulmanifesten ermittelt. Die Nutzung erfolgt exakt als `{{person.full_name}}`, ohne Leerzeichen innerhalb der Klammern. Das Ergebnis hängt zusätzlich von den Daten und Rechten der jeweiligen Installation ab.

`records.read` ist stets erforderlich; Module benötigen außerdem ihre Leseberechtigung sowie eine gültige Lizenz, Installation und Aktivierung. `membership_id` legt Person und Organisation fest. Mehrere passende Adressen, E-Mails, Telefonnummern, Funktionen oder Moduleinträge erfordern eine explizite Auswahl über `address_id`, `email_id`, `phone_id`, `position_id` beziehungsweise `extension_record_id`. Mehrdeutigkeit wird abgewiesen.

`document.datetime` liefert derzeit das Dokumentdatum mit `T00:00:00`, keine aktuelle Uhrzeit. Datumswerte werden als ISO-Datum ausgegeben; `raw` bedeutet unveränderte Textausgabe. `person.age` wird am Dokumentdatum berechnet. Fehlende optionale Werte können leer sein; fehlende Rechte erzeugen einen Fehler.

| Placeholder | Type | Scope | Permission | Module | Format |
|---|---|---|---|---|---|
| `{{document.date}}` | date | global | `records.read` | core | iso |
| `{{document.datetime}}` | text | global | `records.read` | core | raw |
| `{{document.title}}` | text | global | `records.read` | core | raw |
| `{{document.language}}` | text | global | `records.read` | core | raw |
| `{{person.id}}` | text | person | `records.read` | core | raw |
| `{{person.given_name}}` | text | person | `records.read` | core | raw |
| `{{person.family_name}}` | text | person | `records.read` | core | raw |
| `{{person.full_name}}` | text | person | `records.read` | core | raw |
| `{{person.salutation}}` | text | person | `records.read` | core | raw |
| `{{person.birth_date}}` | date | person | `records.read` | core | iso |
| `{{person.gender}}` | text | person | `records.read` | core | raw |
| `{{person.age}}` | integer | person | `records.read` | core | raw |
| `{{person.email}}` | text | person | `records.read` | core | raw |
| `{{person.phone}}` | text | person | `records.read` | core | raw |
| `{{person.address.street}}` | text | person | `records.read` | core | raw |
| `{{person.address.postal_code}}` | text | person | `records.read` | core | raw |
| `{{person.address.city}}` | text | person | `records.read` | core | raw |
| `{{person.address.country}}` | text | person | `records.read` | core | raw |
| `{{person.address.full}}` | text | person | `records.read` | core | raw |
| `{{person.guardian.name}}` | text | person | `records.read` | core | raw |
| `{{person.guardian.contact}}` | text | person | `records.read` | core | raw |
| `{{person.emergency.name}}` | text | person | `records.read` | core | raw |
| `{{person.emergency.phone}}` | text | person | `records.read` | core | raw |
| `{{organization.id}}` | text | organization | `records.read` | core | raw |
| `{{organization.name}}` | text | organization | `records.read` | core | raw |
| `{{organization.short_name}}` | text | organization | `records.read` | core | raw |
| `{{organization.type}}` | text | organization | `records.read` | core | raw |
| `{{organization.founded_on}}` | date | organization | `records.read` | core | iso |
| `{{organization.address.street}}` | text | organization | `records.read` | core | raw |
| `{{organization.address.postal_code}}` | text | organization | `records.read` | core | raw |
| `{{organization.address.city}}` | text | organization | `records.read` | core | raw |
| `{{organization.address.country}}` | text | organization | `records.read` | core | raw |
| `{{organization.address.full}}` | text | organization | `records.read` | core | raw |
| `{{organization.email}}` | text | organization | `records.read` | core | raw |
| `{{organization.phone}}` | text | organization | `records.read` | core | raw |
| `{{organization.website}}` | text | organization | `records.read` | core | raw |
| `{{organization.registration_number}}` | text | organization | `records.read` | core | raw |
| `{{organization.registry_court}}` | text | organization | `records.read` | core | raw |
| `{{organization.association}}` | text | organization | `records.read` | core | raw |
| `{{organization.association_number}}` | text | organization | `records.read` | core | raw |
| `{{membership.id}}` | text | membership | `memberships.read` | core | raw |
| `{{membership.member_number}}` | text | membership | `memberships.read` | core | raw |
| `{{membership.status}}` | text | membership | `memberships.read` | core | raw |
| `{{membership.type}}` | text | membership | `memberships.read` | core | raw |
| `{{membership.start_date}}` | date | membership | `memberships.read` | core | iso |
| `{{membership.end_date}}` | date | membership | `memberships.read` | core | iso |
| `{{membership.notice_received_on}}` | date | membership | `memberships.read` | core | iso |
| `{{membership.termination_reason}}` | text | membership | `memberships.read` | core | raw |
| `{{department.name}}` | text | membership | `memberships.read` | core | raw |
| `{{department.sport}}` | text | membership | `memberships.read` | core | raw |
| `{{position.title}}` | text | person | `records.read` | core | raw |
| `{{position.start_date}}` | date | person | `records.read` | core | iso |
| `{{position.end_date}}` | date | person | `records.read` | core | iso |
| `{{sender.name}}` | text | organization | `records.read` | core | raw |
| `{{sender.address.full}}` | text | organization | `records.read` | core | raw |
| `{{sender.email}}` | text | organization | `records.read` | core | raw |
| `{{sender.phone}}` | text | organization | `records.read` | core | raw |
| `{{recipient.name}}` | text | person | `records.read` | core | raw |
| `{{recipient.address.full}}` | text | person | `records.read` | core | raw |
| `{{martial.graduation.discipline}}` | text | person | `martial.read` | martial | raw |
| `{{martial.graduation.rank}}` | integer | person | `martial.read` | martial | raw |
| `{{martial.graduation.designation}}` | text | person | `martial.read` | martial | raw |
| `{{martial.graduation.awarded_on}}` | date | person | `martial.read` | martial | raw |
| `{{martial.graduation.examiner}}` | text | person | `martial.read` | martial | raw |
| `{{martial.exam.discipline}}` | text | person | `martial.read` | martial | raw |
| `{{martial.exam.rank}}` | integer | person | `martial.read` | martial | raw |
| `{{martial.exam.examined_on}}` | date | person | `martial.read` | martial | raw |
| `{{martial.exam.result}}` | text | person | `martial.read` | martial | raw |
| `{{martial.exam.examiner}}` | text | person | `martial.read` | martial | raw |
| `{{martial.exam.notes}}` | text | person | `martial.read` | martial | raw |

## Dynamische Felder und Grenzen

- `{{person.custom.<key>}}` und `{{organization.custom.<key>}}`: pro tatsächlich definierter eigener Feldkennung; Datentyp gemäß Felddefinition, zusätzlich Feldleserecht erforderlich. `<key>` ist ein Muster, kein wörtlicher Platzhalter.
- Kompatible Kurzformen: `{{given_name}}` → `person.given_name`, `{{family_name}}` → `person.family_name`, `{{date}}` → `document.date`.
- Weitere installierte Module können eigene registrierte Platzhalter ergänzen. Die tatsächliche, berechtigungsgefilterte Liste liefert `GET /api/v1/documents/placeholders?scope=person` (auch `global`, `organization`, `membership`).
- Aktuell keine registrierten Platzhalter für Finance, Contributions, Purchases, Calendar, Events, Banking oder Sportlerlizenzen. Geplante Schlüssel werden nicht als verfügbar aufgeführt.
