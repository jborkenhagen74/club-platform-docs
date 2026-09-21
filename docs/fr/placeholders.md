# Référence complète des variables

Référence : schéma 18 / ABI V3. Liste extraite du registre réel et des manifestes livrés. Utilisez exactement `{{person.full_name}}`, sans espaces internes. Les données et droits de l'installation déterminent la disponibilité.

`records.read` est toujours requis. Les modules exigent aussi leur droit de lecture, licence, installation et activation. `membership_id` fournit personne et organisation. Plusieurs adresses, courriels, téléphones, fonctions ou entrées exigent `address_id`, `email_id`, `phone_id`, `position_id` ou `extension_record_id` ; les contextes ambigus sont refusés.

`document.datetime` renvoie la date du document suivie de `T00:00:00`, pas l'heure actuelle. Les dates sont au format ISO ; `raw` conserve le texte. L'âge est calculé à la date du document. Une valeur facultative absente peut être vide ; un droit manquant provoque une erreur.

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

## Champs dynamiques et limites

- `{{person.custom.<key>}}` et `{{organization.custom.<key>}}` dépendent des champs configurés et de leur type ; le droit de lecture du champ est requis. `<key>` est un modèle.
- Alias : `{{given_name}}` → `person.given_name`, `{{family_name}}` → `person.family_name`, `{{date}}` → `document.date`.
- Catalogue réel autorisé : `GET /api/v1/documents/placeholders?scope=person` ; autres portées : `global`, `organization`, `membership`.
- Aucun marqueur enregistré actuellement pour Finance, Contributions, Purchases, Calendar, Events, Banking ou licences sportives. Les clés prévues ne sont pas annoncées disponibles.
