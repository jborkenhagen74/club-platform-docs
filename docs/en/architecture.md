# Architecture and security model

The desktop controller uses only the shared `Client` interface. `LocalClient` connects to authenticated core services in process; `RestClient` performs the same operations through `/api/v1`. The application selects the implementation at startup. The UI controller has no build dependency on host, application, or persistence.

> Target version 0.6.0, preparatory G0 work: HTTP API `/api/v1` and shared `Client` with `LocalClient`/`RestClient`. Database schema 8 and extension ABI 2 remain unchanged. Old `/api/...` paths return 404. Upgrade server, desktop, portal and proxy together. The functional descriptions below originate from the 0.5.0 baseline and remain applicable except where this notice updates them. Core Foundation II with ABI V3 and seven UI languages is not complete.


[Language home](README.md) · [User manual](user-manual.md)

## Scope

This edition describes **Club Platform 0.5.0**, implementation commit
`320a4c2709c13dd56455768a2f8819a815ad3997`, database schema 8 and extension ABI 2.
Product version, migration sequence and ABI are separate contracts. Five translated
manuals do not imply that the application's predominantly German interface has
already been translated into five languages.

The product manages people, organisations, memberships, positions, contacts,
files and sport-specific records. A person can belong to several organisations.
A user account is a login identity; creating a person does not create an account
or automatically link that person to the current user. Organisations may be
national or regional federations, clubs, sports schools, businesses or other bodies.

## Hosts and responsibilities

| Mode | Interface | Processing and storage |
|---|---|---|
| Standalone | Qt Quick/QML | Local host, SQLite, shared application services |
| Connected desktop | Qt Quick/QML | HTTPS REST; the server owns the database connection |
| Web portal | React/TypeScript, Tailwind 4 | Static web files and an HTTPS proxy to the C++ server |

The application resolves the session and checks permissions for each operation.
A client must not supply the acting user's identity: HTTP objects containing
`actor` or `actor_id` are rejected. The C++ server binds to `127.0.0.1`; a reverse
proxy provides TLS and public access. Client integrations must not access the
server database directly. SQLite and PostgreSQL are alternative providers, not
a pair of automatically synchronised stores.

The connected desktop has no offline write cache. The portal keeps its token in
memory only and requires a fresh login after a reload. Only the appearance choice
is stored locally in the browser.

## Records and relationships

UUIDs identify records independently of names and membership numbers. Mutable
records carry revisions. An update submits the revision previously read; conflicts
prevent lost updates. REST revisions are decimal **strings**, avoiding accidental
rounding of large integers in JavaScript.

A person dossier groups identity, personal details, contact methods, addresses,
relationships, memberships, positions, custom fields and files. Membership links
a person to an organisation, with optional department and fee-group assignments.
A fee group is reference data, not an automatic payment, invoicing or SEPA engine.

The parent-organisation field forms a hierarchy, for example national federation
→ regional federation → sports school. Additional affiliations are separate
relationships. A hierarchy does not grant permissions and is not a tenant or
row-level security boundary. Parent cycles are rejected.

Custom fields have definitions, types, group permissions and values. Reading and
writing are separate rights. A write-only field does not expose its current value.
A type change must convert every existing value successfully; otherwise the whole
change is rolled back.

## Authentication and authorisation

Passwords use Argon2id hashes; server-side session tokens are also stored as hashes.
Defaults are eight hours absolute lifetime, 30 minutes idle timeout and a
30-second lock interval after five failed login attempts. Clients should explain
failures instead of creating rapid retry loops.

The permission chain is user → groups → roles → permission keys. Default is deny.
`records.read/write` cover general records; `memberships.read/write` cover
memberships and positions. `security.manage` controls accounts and branding;
`schema.manage` controls field definitions, templates and extension installation.
`audit.read` belongs to the application API; 0.5.0 exposes no dedicated audit HTTP
route. `*` is comprehensive administrator access. At least one active administrator
must remain.

Field permissions are additional checks, not replacements for general permissions.
Martial-arts records also require `martial.read` or `martial.write`. The current
release does not automatically restrict users to their own person or organisation.
The portal is an authorised administration frontend, not a completed member
self-service portal.

## Files, transactions and limitations

Files, including their contents, are stored in the database. They do not require
a separate media-folder backup. Ordinary files are limited to 5 MiB; photos and
branding to 2 MiB at the service boundary. Interfaces resize PNG/JPEG images and
limit their area to 16 megapixels. A new profile image replaces the old image for
that record. Document uploads never install native modules.

Changes and their audit entries are transactional. SQLite serialises writes;
PostgreSQL uses its transaction and locking mechanisms. A paginated CSV report
is still not a point-in-time database snapshot.

Do not assume completed support for signed installers, automatic update
installation, billing/payment runs, appointments, offline synchronisation,
tenant isolation, automatic document delivery or arbitrary plugin menus/REST
callbacks. [Versioning](versioning.md) separates implemented features from proposals.
