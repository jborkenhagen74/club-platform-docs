# REST contract and integration rules

> Target version 0.6.0, preparatory G0 work: HTTP API `/api/v1` and shared `Client` with `LocalClient`/`RestClient`. Database schema 8 and extension ABI 2 remain unchanged. Old `/api/...` paths return 404. Upgrade server, desktop, portal and proxy together. The functional descriptions below originate from the 0.5.0 baseline and remain applicable except where this notice updates them. Core Foundation II with ABI V3 and seven UI languages is not complete.


[Language home](../README.md) · [OpenAPI](../../../openapi/club-platform.yaml)

## Real routes

The current development API uses `/api/v1`. `/health` is outside that prefix. OpenAPI describes the implemented HTTP operations; internal methods are not automatically HTTP endpoints.

| Area | Routes |
|---|---|
| Sessions | `POST /api/v1/auth/login`, `GET /api/v1/auth/me`, `POST /api/v1/auth/logout`, `POST /api/v1/auth/password` |
| People | `GET/POST /api/v1/persons`, `GET/PUT /api/v1/persons/{id}` |
| Management | `GET/POST /api/v1/management/{resource}` |
| Files | `GET/POST /api/v1/assets`, `GET /api/v1/assets/{id}`, public `GET /api/v1/branding` |
| Extensions | `GET /api/v1/extensions`, `POST /api/v1/extensions/install` |
| Documents | `POST /api/v1/documents/render`, `GET /api/v1/reports` |
| Security/fields | User, group, role and field operations specified in OpenAPI |

## Authentication and representations

Login sends `{"login":"…","password":"…"}` and returns `user_id`, `login`,
`expires_at` in Unix seconds and a token. Subsequent requests use
`Authorization: Bearer TOKEN`. Clients must not invent acting identities.
On `401`, discard the session and authenticate again. Do not persist the password
or token in browser storage.

JSON requests require `Content-Type: application/json`. Generic management values
are strings such as `"8"`, `"true"`, `"2026-09-08"`. Dedicated security routes use
actual JSON booleans for `enabled`, `active`, `read` and `write`. Revisions are
strings. Most IDs are UUIDs; association resources may return composite IDs.

Create a person:

```json
{"given_name":"Erika","family_name":"Mustermann"}
```

Update through `PUT /api/v1/persons/{id}`:

```json
{"revision":"1","given_name":"Erika","family_name":"Muster"}
```

Generic creation sends `{"id":"","revision":"0","values":{…}}`; an update
reuses the ID and revision returned by the server. Not every generic resource is
writable: `persons` and `organization_children` are read views. Edit people through
the dedicated API or `person_identity`. Assignment tables have their own enabling
semantics rather than ordinary versioned-record behaviour.

## Resources, fields and paging

Dossier resources are `organizations`, `person_profiles`, `contacts`, `addresses`,
`relationships`, `memberships`, `positions`, `departments`, `fee_groups` and
`organization_affiliations`. Contacts/addresses use `entity_id`; personal records
use `person_id`; organisation sections use `organization_id`. Memberships and
positions link both. `owner` filters by dossier according to the resource; it
never grants permission.

Administration resources are `users`, `groups`, `roles`, `group_members`,
`group_roles`, `role_permissions`, `field_definitions`, `field_permissions` and
`field_values`. Templates use `document_templates`; native records use resources
such as `ext:martial.graduation` and `ext:martial.exam`.
The [shared field reference](../../../reference/resources.md) lists exact keys.
Do not echo display-only `labels` back as values or blindly add unknown fields.
Some resources require an exact field set.

Pages contain at most 100 entries. `after` is the last cursor and `q` is a literal,
case-sensitive search. Where returned, follow `next_cursor` until `null`.
Asset lists have no `next_cursor`: after 100 entries, pass the last ID as `after`;
stop on a shorter or empty page. Templates currently ignore search/owner filters.
Do not assume every generic resource implements every filter.

## Assets and document rendering

Uploads send `owner`, `purpose`, `filename`, `media_type` and Base64 `content`
without a Data-URI prefix. `file`/`photo` belong to a person or organisation;
`logo`/`background` use an empty owner and require `security.manage`. Lists return
metadata; single-item reads include content. Branding is intentionally readable
before login, so its images must not contain confidential information.

`/api/v1/documents/render` receives `template_id`, `person_id`, `date` and returns
`title` and `body`, not a PDF. Clients generate PDFs. The input date remains ISO
regardless of display locale. `/api/v1/reports` returns UTF-8 CSV with BOM for people,
organisations, memberships, positions and native records. Narrow the filter for
results exceeding 5,000 records. Multi-page reports are not transactional snapshots.

## Errors and transport limits

| Status | Client action |
|---|---|
| 400 | Check JSON, field set, types and required values |
| 401 | Discard session and sign in again |
| 403 | Check permission and Host/Origin configuration |
| 404 | Verify ID and implemented resource |
| 409 | Re-read, compare and deliberately resubmit an edit |
| 500 | Investigate; never blindly replay writes |

A timed-out write may already have committed. Read the current state before
retrying. The contract provides no general idempotency keys or HTTP batch
transactions. Standard JSON requests are limited to 16 KiB. Asset requests also
face the 8-MiB HTTP limit and decoded-content limits. Only one exact configured
browser origin is permitted; preflight uses `OPTIONS /api/v1/…`. Upstream `Host` is
`localhost` or `127.0.0.1`, optionally with a port. Remote clients use the HTTPS proxy.
