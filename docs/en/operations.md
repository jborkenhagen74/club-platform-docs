# Operations, backups and updates

[Language home](README.md) · [Installation](installation.md)

> Windows builds and PostgreSQL restoration additionally require maintenance commit `cd765ba08bd2cd8c21969eb8fc20a52a9659e214`. It corrects the Windows SDK symbol `LOAD_LIBRARY_SEARCH_DEFAULT_DIRS` and adds `--file=-` when exporting SQL with `pg_restore`. This fix does not change the schema or API.

## Operational ownership

A dedicated service account owns the database file or PostgreSQL connection.
Separate program, native-module and data directories. Portal users must not be
able to write to the module directory. Backups contain personal records, files
and password hashes; restrict access and use a suitably protected backup location.

The `scripts/pilot-*.py` tools belong to the implementation distribution, not this
public documentation repository. They require Python 3.11 or later. Possession
of a backup file is not proof that recovery works.

## SQLite

```sh
python3 scripts/pilot-data.py backup data.sqlite backup-2026-09-09
python3 scripts/pilot-data.py diagnose backup-2026-09-09/database.sqlite
python3 scripts/pilot-data.py restore backup-2026-09-09 restored.sqlite
```

Online backup includes committed WAL data. The destination directory must not
already exist. Integrity, foreign keys, migration sequence and SHA-256 are checked.
A failed backup may leave an incomplete directory; it is not a valid backup without
a valid manifest.

Restore requires a **new** destination file. It checks the checksum and database
and revokes existing sessions. Stop the host before switching it to the verified
file. Retain the old file until functional checks succeed. Uploaded files are part
of the database backup; executable versions, certificates, configuration and
native modules require separate recovery arrangements.

## PostgreSQL

Use `pg_dump`, `pg_restore` and `psql` compatible with the server version. Configure
access through `pg_service.conf`, `.pgpass` or protected libpq settings. Create a
fresh empty restore database and a separate service definition; do not run a host
against that target during recovery.

```sh
python3 scripts/pilot-postgres.py backup --service club-production --directory pg-backup
python3 scripts/pilot-postgres.py restore --service club-restore --directory pg-backup
```

The tool produces a custom-format archive and checksum manifest. Existing user
tables block restoration. Restore and session revocation occur in one transaction.
Old ownership and ACL settings are not imported; prepare database operating roles
separately. Never attempt to restore over active production tables.

## Controlled update

1. Notify users, finish outstanding work and create a backup.
2. Place new binaries and matching modules in a separate version directory.
3. Restore the backup into a new test database. Start the new host there; migrations
   are checked and applied transactionally.
4. Verify login, edits, memberships, graduations, file downloads, CSV and PDF;
   include an account with restricted rights.
5. Stop production. Switch the program/configuration only after acceptance, and
   deploy the matching static portal version.
6. Reload browsers, sign in again and perform functional spot checks.
7. To roll back, use the old application **and its matching pre-migration backup**.
   Never run old binaries against an already upgraded database.

Changes since the backup may be lost on rollback and need deliberate treatment.
Checking for updates does not install them. Signing, notarisation and broad rollout
remain separate release steps.

## Diagnostics and incidents

`clubplatform-server --sqlite TESTFILE --diagnose` reports connectivity and migration
state without personal records. Opening the host checks **and applies** migrations.
For SQLite inspection without migration, use `pilot-data.py diagnose`. Record the
version, mode, paths, time and error; do not put tokens or passwords into tickets.

Git reporting “no tracking information” is fixed by selecting the intended branch
and setting `git branch --set-upstream-to=origin/feature/core-foundation
feature/core-foundation` once, then `git pull --ff-only`. Do not erase local edits
with a forced reset. Portal `403` requires checking roles and proxy/origin settings.
For missing modules, check path, architecture, ABI, installed manifest and activation.
Do not “repair” these issues by editing migration tables or persisted manifests.
