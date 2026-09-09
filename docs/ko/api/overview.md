# REST 계약과 연동 규칙

> 목표 버전 0.6.0의 준비 작업 G0입니다. HTTP API는 `/api/v1`이며 공통 `Client` 계약을 `LocalClient`와 `RestClient`가 구현합니다. 데이터베이스 스키마 8과 확장 ABI 2는 그대로입니다. 기존 `/api/...` 경로는 404를 반환합니다. 서버, 데스크톱, 포털 및 프록시를 함께 업데이트하십시오. 아래 기능 설명은 0.5.0 기준에서 작성되었으며 이 안내로 변경된 부분 외에는 계속 적용됩니다. ABI V3 및 일곱 UI 언어를 포함한 Core Foundation II는 아직 완료되지 않았습니다.


[시작 페이지](../README.md) · [OpenAPI](../../../openapi/club-platform.yaml)

## 실제 경로

현재 개발 API는 `/api/v1`을 사용하며 `/health`는 이 접두사 밖에 있습니다. OpenAPI는 구현된 HTTP 작업을 설명합니다. 내부 메서드가 자동으로 HTTP 경로가 되는 것은 아닙니다.

| 영역 | 경로 |
|---|---|
| 세션 | `POST /api/v1/auth/login`, `GET /api/v1/auth/me`, `POST /api/v1/auth/logout`, `POST /api/v1/auth/password` |
| 사람 | `GET/POST /api/v1/persons`, `GET/PUT /api/v1/persons/{id}` |
| 관리 | `GET/POST /api/v1/management/{resource}` |
| 파일 | `GET/POST /api/v1/assets`, `GET /api/v1/assets/{id}`, 공개 `GET /api/v1/branding` |
| 확장 | `GET /api/v1/extensions`, `POST /api/v1/extensions/install` |
| 문서 | `POST /api/v1/documents/render`, `GET /api/v1/reports` |
| 권한·필드 | OpenAPI에 정의된 사용자, 그룹, 역할, 필드 작업 |

## 세션과 자료 표현

로그인은 `{"login":"…","password":"…"}`을 전송합니다. 응답은 `user_id`,
`login`, Unix 초 단위 `expires_at`, 토큰을 포함합니다. 이후 요청은
`Authorization: Bearer TOKEN`을 사용합니다. `401`이면 로컬 세션을 폐기하고
재로그인합니다. 비밀번호나 토큰을 브라우저 영구 저장소에 보관하지 않습니다.

JSON에는 `Content-Type: application/json`이 필요합니다. 일반 관리 값은
`"8"`, `"true"`, `"2026-09-08"` 같은 문자열입니다. 전용 권한 경로의 `enabled`,
`active`, `read`, `write`는 실제 JSON 불리언입니다. 리비전은 문자열이며,
ID는 대체로 UUID이지만 관계 테이블에는 복합 ID가 있습니다.

사람 생성 예제:

```json
{"given_name":"Erika","family_name":"Mustermann"}
```

`PUT /api/v1/persons/{id}` 수정 예제:

```json
{"revision":"1","given_name":"Erika","family_name":"Muster"}
```

일반 레코드 생성은 `{"id":"","revision":"0","values":{…}}`을 사용하고,
수정은 읽은 ID와 리비전을 재사용합니다. `persons`, `organization_children`은
일반 관리 API에서 읽기 전용 뷰입니다. 사람 수정은 전용 경로나 `person_identity`를
사용합니다. 관계 테이블은 별도의 활성화 의미를 갖습니다.

## 리소스와 페이지 처리

기록 리소스는 `organizations`, `person_profiles`, `contacts`, `addresses`,
`relationships`, `memberships`, `positions`, `departments`, `fee_groups`,
`organization_affiliations`입니다. 연락처·주소는 `entity_id`, 개인 데이터는
`person_id`, 조직 영역은 `organization_id`를 사용합니다. `owner`는 리소스별
기록 필터이며 권한을 부여하지 않습니다.

관리 리소스는 `users`, `groups`, `roles`, `group_members`, `group_roles`,
`role_permissions`, `field_definitions`, `field_permissions`, `field_values`입니다.
양식은 `document_templates`, 네이티브 데이터는 `ext:martial.graduation`,
`ext:martial.exam` 등입니다. 정확한 키는 [공통 필드 참조](../../../reference/resources.md)를
확인하십시오. `labels`는 표시용이고 저장에는 ID를 보냅니다. 일부 리소스는
필드 집합이 정확해야 하므로 알 수 없는 키를 추가하지 마십시오.

페이지당 최대 100개입니다. `after`는 마지막 커서, `q`는 대소문자를 구분하는
문자 그대로의 검색입니다. `next_cursor`가 있으면 `null`까지 이어 읽습니다.
파일 목록에는 이 값이 없으므로 100개가 반환되면 마지막 ID를 `after`로 전송하고
짧거나 빈 페이지에서 중단합니다. 현재 양식은 검색·owner 필터를 무시합니다.
모든 리소스가 모든 필터를 지원한다고 가정하지 마십시오.

## 파일, 문서와 오류

업로드는 `owner`, `purpose`, `filename`, `media_type`, Base64 `content`를
보냅니다. Data URI 접두사는 넣지 않습니다. `file`/`photo`는 사람 또는 조직용,
`logo`/`background`는 빈 owner와 `security.manage`를 사용합니다. 목록은 메타데이터,
단건 읽기는 내용을 포함합니다. 시작 화면 이미지는 로그인 전 공개되므로
기밀 내용을 넣으면 안 됩니다.

`/api/v1/documents/render`는 `template_id`, `person_id`, `date`를 받고 `title`,
`body`를 반환하며 **PDF를 반환하지 않습니다**. PDF는 클라이언트가 생성합니다.
전송 날짜는 ISO입니다. `/api/v1/reports`는 사람·조직·회원 소속·직책·네이티브
데이터의 UTF-8 BOM CSV를 반환합니다. 최대 5,000행이며 초과하면 필터를 좁힙니다.
페이지별 보고서는 트랜잭션 스냅샷이 아닙니다.

| 상태 | 처리 |
|---|---|
| 400 | JSON, 필드 집합, 자료형, 필수 값 확인 |
| 401 | 세션 폐기 후 재로그인 |
| 403 | 권한과 Host/Origin 설정 확인 |
| 404 | ID와 실제 리소스 확인 |
| 409 | 재조회·비교 후 새 리비전에 의도적으로 수정 |
| 500 | 무조건 재전송하지 말고 원인 조사 |

시간 초과된 쓰기가 이미 완료되었을 수 있으므로 먼저 재조회합니다. 일반적인
멱등성 키나 HTTP 배치 트랜잭션은 없습니다. 일반 JSON은 16 KiB, 파일 요청은
HTTP 8 MiB와 디코딩 내용 제한을 함께 적용합니다. 정확한 브라우저 출처 하나만
허용합니다. 프리플라이트는 `OPTIONS /api/v1/…`, 업스트림 Host는 `localhost` 또는
`127.0.0.1`과 선택적 포트입니다. 원격 클라이언트는 HTTPS 프록시를 사용합니다.
