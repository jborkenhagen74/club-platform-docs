# Resource field reference / Feldreferenz / Référence des champs / Referencia de campos / 필드 참조

[Deutsch](../docs/de/api/overview.md) · [English](../docs/en/api/overview.md) · [Français](../docs/fr/api/overview.md) · [Español](../docs/es/api/overview.md) · [한국어](../docs/ko/api/overview.md)

**0.5.0 · schema 8 · API `/api/v1`**

- **DE:** Die folgenden technischen Schlüssel werden nicht übersetzt. Alle `values` sind JSON-Zeichenketten. Sende bei normalen Datensätzen den vollständigen Feldsatz; optionale leere Werte sind `""`. Die Tabelle zeigt keine Bildschirmbeschriftungen. IDs referenzieren vorhandene Datensätze. Fachrollen und Organisationshierarchie gewähren keine Zugriffsrechte.
- **EN:** Technical keys below are not translated. All `values` are JSON strings. Send the complete normal-record field set; optional empty values are `""`. These are not UI captions. IDs reference existing records. Business positions and organisation hierarchy do not grant access rights.
- **FR:** Les clés techniques ci-dessous ne sont pas traduites. Toutes les `values` sont des chaînes JSON. Envoyez tous les champs du dossier normal; les valeurs facultatives vides sont `""`. Ce ne sont pas les libellés de l’interface. Les identifiants référencent des dossiers existants. Les fonctions et la hiérarchie ne donnent aucun droit d’accès.
- **ES:** Las claves técnicas no se traducen. Todas las `values` son cadenas JSON. Envía el conjunto completo de campos del registro normal; los valores opcionales vacíos son `""`. No son etiquetas de pantalla. Los identificadores apuntan a registros existentes. Los cargos y la jerarquía no conceden permisos.
- **KO:** 기술적 키는 번역하지 않습니다. 모든 `values`는 JSON 문자열입니다. 일반 기록의 전체 필드 집합을 보내고 선택적인 빈 값은 `""`로 지정합니다. 화면 표시명이 아니며 ID는 기존 기록을 참조합니다. 직책과 조직 계층은 접근 권한을 부여하지 않습니다.

## Core / Kern / Noyau / Núcleo / 코어

| Resource | Permission: GET / POST | `values` keys |
|---|---|---|
| `organization_affiliations` | `records.read / records.write` | `organization_id`, `target_organization_id`, `role`, `start_date`, `end_date` |
| `organizations` | `records.read / records.write` | `name`, `short_name`, `registration_number`, `registry_court`, `founded_on`, `website`, `email`, `phone`, `street`, `postal_code`, `city`, `country`, `association`, `association_number`, `organization_type`, `parent_organization_id` |
| `contacts` | `records.read / records.write` | `entity_id`, `kind`, `label`, `value` |
| `addresses` | `records.read / records.write` | `entity_id`, `label`, `street`, `postal_code`, `city`, `country` |
| `relationships` | `records.read / records.write` | `person_id`, `organization_id`, `role`, `start_date`, `end_date` |
| `memberships` | `memberships.read / memberships.write` | `person_id`, `organization_id`, `member_number`, `status`, `start_date`, `end_date`, `membership_type`, `department_id`, `fee_group_id`, `notice_received_on`, `termination_reason` |
| `positions` | `memberships.read / memberships.write` | `person_id`, `organization_id`, `title`, `start_date`, `end_date` |
| `person_profiles` | `records.read / records.write` | `person_id`, `birth_date`, `salutation`, `gender`, `guardian_name`, `guardian_contact`, `emergency_name`, `emergency_phone` |
| `departments` | `records.read / records.write` | `organization_id`, `name`, `sport` |
| `fee_groups` | `memberships.read / memberships.write` | `organization_id`, `name`, `amount_cents`, `currency`, `interval` |

`persons`: GET → `given_name`, `family_name`; POST uses `/api/v1/persons` instead.
`person_identity`: POST → `given_name`, `family_name`, existing ID + revision.
`organization_children`: GET view of `organizations`, `owner` = parent ID.

## Values / Werte / Valeurs / Valores / 값

| Key | Allowed values / Zulässige Werte / Valeurs admises / Valores admitidos / 허용 값 |
|---|---|
| `organization_type` | `federation`, `regional_federation`, `club`, `sports_school`, `company`, `other`; compatibility default `unspecified` |
| `status` (membership) | `active`, `paused`, `ended` |
| `membership_type` | `regular`, `youth`, `family`, `supporting`, `honorary`, `""` |
| `gender` | `female`, `male`, `diverse`, `unspecified`, `""` |
| `kind` (contact) | `email`, `phone` |
| `interval` | `monthly`, `quarterly`, `half_yearly`, `yearly` |
| `currency` | Three uppercase letters, e.g. `EUR` |
| `amount_cents` | Nonnegative integer string: `"2500"` = EUR 25.00 when currency is EUR |
| Date / Datum / Date / Fecha / 날짜 | ISO `YYYY-MM-DD`; optional empty date `""` |
| Boolean / Boolesch / Booléen / Booleano / 불리언 | Management: `"true"` / `"false"`; dedicated security endpoints: JSON `true` / `false` |

**DE:** `organizations` benötigt `name`; weitere Felder können bei Erstellung fehlen. Neuere optionale Felder werden bei einem Update ohne Angabe erhalten. Bei Mitgliedschaften sind `membership_type`, `department_id`, `fee_group_id`, `notice_received_on`, `termination_reason` optional; im Personenprofil alle Felder außer `person_id`. Andere Feldsätze müssen vollständig sein. `end_date`, `label`, `postal_code` dürfen leer sein. Ein beendeter Mitgliedsdatensatz benötigt dennoch `end_date`. Startdatum und Referenzen müssen gültig sein, Enddatum ≥ Startdatum. Abteilung und Beitragsgruppe gehören zur gewählten Organisation. Mitgliedsnummern sind je Organisation eindeutig. Die meisten Fachwerte haben maximal 512 UTF-8-Bytes.

**EN:** `organizations` requires `name`; other fields may be omitted on creation. Omitted newer optional fields retain their previous value on update. Membership optional keys are `membership_type`, `department_id`, `fee_group_id`, `notice_received_on`, `termination_reason`; profile keys except `person_id` are optional. Other field sets must be complete. `end_date`, `label`, `postal_code` may be empty, but an ended membership requires `end_date`. Start date and references must be valid, end ≥ start. Department and fee group must belong to the selected organisation. Member numbers are unique per organisation. Most business values are limited to 512 UTF-8 bytes.

**FR:** `organizations` exige `name`; les autres champs peuvent être omis à la création. Les nouveaux champs facultatifs omis conservent leur valeur lors d’une modification. Pour l’adhésion: `membership_type`, `department_id`, `fee_group_id`, `notice_received_on`, `termination_reason` sont facultatifs; pour le profil, tous sauf `person_id`. Les autres ensembles doivent être complets. `end_date`, `label`, `postal_code` peuvent être vides, mais une adhésion terminée exige `end_date`. Les dates et références doivent être valides; fin ≥ début. Section et groupe de cotisation appartiennent à l’organisation sélectionnée. Le numéro d’adhérent est unique par organisation. La plupart des valeurs métier sont limitées à 512 octets UTF-8.

**ES:** `organizations` requiere `name`; los demás campos pueden omitirse al crear. Los nuevos campos opcionales omitidos conservan su valor al actualizar. En afiliaciones son opcionales `membership_type`, `department_id`, `fee_group_id`, `notice_received_on`, `termination_reason`; en perfiles, todos salvo `person_id`. Los otros conjuntos deben estar completos. `end_date`, `label`, `postal_code` pueden estar vacíos, pero una afiliación terminada requiere `end_date`. Fechas y referencias deben ser válidas; fin ≥ inicio. Departamento y grupo de cuotas pertenecen a la organización elegida. El número de socio es único por organización. La mayoría de valores admiten 512 bytes UTF-8 como máximo.

**KO:** `organizations`에는 `name`이 필수이며 생성 시 나머지는 생략할 수 있습니다. 새 선택 필드를 업데이트에서 생략하면 이전 값이 유지됩니다. 회원 자격의 선택 필드는 `membership_type`, `department_id`, `fee_group_id`, `notice_received_on`, `termination_reason`이며 프로필에서는 `person_id` 외의 필드가 선택 사항입니다. 다른 필드 집합은 완전해야 합니다. `end_date`, `label`, `postal_code`는 빈 문자열이 가능하지만 종료된 회원 자격에는 `end_date`가 필요합니다. 날짜와 참조는 유효해야 하고 종료일은 시작일 이후여야 합니다. 부서와 회비 그룹은 선택 조직에 속해야 합니다. 회원 번호는 조직 내에서 고유하며 대부분의 업무 값은 UTF-8 512바이트로 제한됩니다.

## Administration / Verwaltung / Administration / Administración / 관리

| Resource | GET permission | POST permission | Create / update keys |
|---|---|---|---|
| `users` | `security.manage` | `security.manage` | Create: `login`, `password`; update: `active` |
| `groups`, `roles` | `security.manage` | `security.manage` | Create: `name`; rename unsupported |
| `group_members` | `security.manage` | `security.manage` | `group_id`, `user_id`, `enabled` |
| `group_roles` | `security.manage` | `security.manage` | `group_id`, `role_id`, `enabled` |
| `role_permissions` | `security.manage` | `security.manage` | `role_id`, `permission`, `enabled` |
| `field_definitions` | `schema.manage` | `schema.manage` | Create: `record_type`, `key`, `value_type`; update: `value_type` |
| `field_permissions` | `security.manage` | `security.manage` | `field_id`, `group_id`, `can_read`, `can_write` |
| `field_values` | `records.read` + field read or write grant | `records.write` + field write grant | `entity_id`, `type`, `value`, `clear`; row ID = field ID |
| `document_templates` | `records.read` | `schema.manage` | `title`, `body` |

`field_values` GET metadata: `entity_id`, `key`, `type`, `can_read`, `can_write`,
`has_value`, `value` (subject to read grant). POST returns no echoed field values.
Assignment row IDs use `first_id/second_id_or_permission`; do not parse all IDs as UUIDs.
`clear` is a management string boolean; it removes the stored field value, not its definition.
Passwords are accepted only during user creation and never returned in lists.
Template title ≤ 120 bytes; body ≤ 12000 bytes. Placeholders:
`{{given_name}}`, `{{family_name}}`, `{{date}}`.

## Extensions / Erweiterungen / Extensions / Extensiones / 확장

| Resource | Permissions | Complete `values` keys |
|---|---|---|
| `ext:martial.graduation` | `records.read/write` + `martial.read/write` | `person_id`, `discipline`, `rank`, `designation`, `awarded_on`, `examiner` |
| `ext:martial.exam` | `records.read/write` + `martial.read/write` | `person_id`, `discipline`, `rank`, `examined_on`, `result`, `examiner`, `notes` |
| `ext:attendance.session` (public example) | `records.read/write` + `attendance.read/write` | `person_id`, `attended_on`, `course` |

`rank`: integer string `"1"` … `"30"`; `result`: `passed` / `failed`.
Graduation `examiner` and examination `notes` may be `""`; all keys remain present.
Native record owners are people. Activation requires `schema.manage`.

## Example / Beispiel / Exemple / Ejemplo / 예시

`POST /api/v1/management/organizations`:

```json
{"id":"","revision":"0","values":{"name":"Example Sports School","organization_type":"sports_school"}}
```

`POST /api/v1/management/field_values` (replace IDs with actual field/person IDs):

```json
{"id":"e32d76cb-fd1a-435a-9cd0-62adcb959b70","revision":"0","values":{"entity_id":"d92d76cb-fd1a-435a-9cd0-62adcb959b70","type":"integer","value":"8","clear":"false"}}
```

[OpenAPI request and response schemas](../openapi/club-platform.yaml)
