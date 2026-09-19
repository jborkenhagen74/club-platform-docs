# 전체 문서 자리표시자 목록

기준: 스키마 18 / ABI V3. 실제 코어 등록과 배포 모듈 매니페스트에서 추출했습니다. 내부 공백 없이 `{{person.full_name}}`처럼 정확히 입력하세요. 사용 가능 여부는 설치 데이터와 권한에 따라 달라집니다.

항상 `records.read`가 필요합니다. 모듈은 읽기 권한, 라이선스, 설치 및 활성화도 필요합니다. `membership_id`는 사람과 조직을 지정합니다. 주소, 이메일, 전화, 직책 또는 모듈 기록이 여러 개면 `address_id`, `email_id`, `phone_id`, `position_id`, `extension_record_id`로 명시적으로 선택해야 합니다. 모호한 문맥은 거부됩니다.

`document.datetime`은 현재 시각이 아니라 문서 날짜에 `T00:00:00`을 붙입니다. 날짜는 ISO 형식이며 `raw`는 원문입니다. 나이는 문서 날짜 기준으로 계산됩니다. 선택 값이 없으면 빈 문자열이 될 수 있으나 권한이 없으면 오류가 발생합니다.

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

## 동적 필드와 제한

- `{{person.custom.<key>}}`, `{{organization.custom.<key>}}`: 설정된 사용자 정의 필드마다 생성되며 해당 필드 형식 및 읽기 권한을 따릅니다. `<key>`는 패턴입니다.
- 이전 별칭: `{{given_name}}` → `person.given_name`, `{{family_name}}` → `person.family_name`, `{{date}}` → `document.date`.
- 실제 권한별 목록: `GET /api/v1/documents/placeholders?scope=person`. 다른 범위는 `global`, `organization`, `membership`입니다.
- Finance, Contributions, Purchases, Calendar, Events, Banking 및 선수 라이선스는 아직 문서 자리표시자를 등록하지 않습니다. 계획된 키를 사용 가능으로 표시하지 않습니다.
