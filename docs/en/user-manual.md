# User manual

[Language home](README.md) · [Installation](installation.md) · [Operations](operations.md)

**Edition:** 0.5.0 / 2026-09-09. For office staff, instructors and administrators.
Examples use fictional people. German captions below are the actual interface
labels, followed by explanations; visibility may depend on permissions and screen size.

## Contents

1. [Basic concepts](#basic-concepts)
2. [Signing in](#signing-in)
3. [Organisations and hierarchy](#organisations-and-hierarchy)
4. [Person dossiers](#person-dossiers)
5. [Memberships and positions](#memberships-and-positions)
6. [Photos and documents](#photos-and-documents)
7. [Martial arts](#martial-arts)
8. [Custom fields](#custom-fields)
9. [Templates and reports](#templates-and-reports)
10. [Appearance and help](#appearance-and-help)
11. [Administration](#administration)
12. [Troubleshooting and daily checks](#troubleshooting-and-daily-checks)

## Basic concepts

A **person** may be a member, instructor, contact or supporter. A **user** is a
login account. These are different records: you can manage a person without an
account, and the software does not automatically link an account to a person.

An **organisation** may be a school, club, federation or business. A **membership**
links a person to an organisation and holds the membership number, status and dates.
A **position** describes an organisational function; a **relationship** records
another contact or supporting role. Do not create duplicate people to represent
several memberships or functions.

A dossier brings related information together. Switching tabs does not change the
person or organisation. Access comes from your account, not from an organisation's
position in the hierarchy.

## Signing in

1. Open the desktop application or the administrator's HTTPS portal address.
2. Check whether the desktop is in standalone or server mode. Identical names in
   two databases do not imply synchronisation.
3. Enter username and password and select `Anmelden` (sign in).
4. Confirm that the expected dossiers are available.

A new standalone database offers `Administrator einrichten` (initial administrator
setup). This is not the normal workflow for adding colleagues. Server accounts are
provisioned by administration. Passwords require at least 12 characters. After
repeated failed attempts, wait briefly and check the credentials.

Reloading the portal requires login again. Default sessions expire after eight
hours at most or after 30 minutes idle. Save work before breaks and sign out;
an open browser is not a workstation lock. Change your password in the desktop
under `Administration → Passwort ändern`. The portal has no dedicated password-
change form in this release.

## Organisations and hierarchy

### Create an organisation

1. Open `Organisationen` and search for an existing record first.
2. Select `Neu anlegen` and enter the full name.
3. Choose its type: `Dachverband` (national/umbrella federation), `Landesverband`
   (regional federation), `Verein` (club), `Sportschule` (sports school),
   `Unternehmen` (business) or `Sonstige` (other).
4. Add known details: short name, registration data, founding date, website,
   email, phone, address and federation identifiers.
5. Select `Speichern`, reopen the dossier and verify the result.

Leave unavailable optional information empty instead of inventing registration
numbers. Organisation settings do not automatically grant account access.

### Build the hierarchy

Create the national federation first. Create a regional federation and choose the
national body as its parent; finally create the school or club with the regional
body as parent. Select an actual existing record in the reference picker: entering
a name alone does not create an association.

The desktop `Struktur` section shows child organisations. Additional affiliations
belong under `Verbandszugehörigkeit`, with a role and dates. An organisation cannot
be its own ancestor. If rejected, inspect the parent chain instead of creating a
second organisation with the same name.

`Abteilungen` holds departments and their sports. `Beiträge` holds fee groups,
currency and interval. Amounts are in **cents**: EUR 25.00 is entered as `2500`.
These are reference values, not payment instructions. Members, positions,
relationships, contacts, addresses and files can be accessed through the dossier;
some views differ between desktop and portal.

## Person dossiers

### Add a person

1. Open `Personen`; search first to avoid duplicates.
2. Create a person with given name and family name and save.
3. Open the record or select `Akte öffnen`.
4. Complete each relevant section and save it before moving on.

Search is literal and case-sensitive. If no match appears, shorten the text and
check further pages. A page contains at most 100 entries; it is not necessarily
the complete collection.

| Caption | Content |
|---|---|
| Übersicht | Given name, family name and identity |
| Persönlich | Birth date, salutation, gender, guardian and emergency contacts |
| Kontakt | Labelled phone numbers and email addresses |
| Anschriften | Clearly labelled addresses |
| Mitgliedschaften | Organisation, membership number, status and dates |
| Funktionen | Organisational positions and validity periods |
| Beziehungen | Other organisational/contact relationships |
| Dateien | Supporting files; profile photo remains in the header |
| Eigene Felder | Authorised Core custom fields in the desktop |
| Graduierungen / Prüfungshistorie | After activation of the martial-arts module |
| Dokumente / Dokumentvorlagen | Generate documents for this person |

Date controls follow system/browser formatting; APIs and technical exports may
show ISO dates such as `2026-09-08`. Do not force an unrelated format into a control
that already displays the local pattern.

On small portal screens, choose a section using `Aktenbereich`. The desktop can
retain a draft with `Entwurf behalten und schließen`; a dot marks an unsaved draft.
This is **not a database save**. In the portal, save or deliberately discard the
open edit before navigating. Never treat an unsaved draft as backed up data.

## Memberships and positions

In a person dossier, open `Mitgliedschaften → Neu anlegen`. The person is fixed by
the dossier; explicitly select the organisation. Enter membership number, status
and start date. Add membership type, department, fee group and leaving information
as appropriate. From an organisation dossier, the organisation is fixed and you
select the person instead.

An end date cannot precede the start. `Aktiv`, `Ruhend`, `Beendet` mean active,
paused and ended membership; they are not the account's enabled/disabled state.
For a departure, update the existing membership with its end date and reason.
Do not recreate the person. Automatic billing, reminders, direct debit and legal
notice-period calculations are not part of this release.

Under `Funktionen`, enter a position such as instructor or managing director and
its dates. A business position grants no software permissions: an instructor role
in the dossier does not replace `martial.write`. One person may hold several
memberships and positions.

## Photos and documents

Use the fixed dossier-header image for a person's photo or an organisation's logo.
Choose `Foto auswählen`, `Logo auswählen` or `Foto / Logo hochladen`. PNG and JPEG
are supported. The interface resizes images; extremely large or damaged images
may be rejected. A new profile image replaces the previous one for that record.

For agreements, certificates or supporting material, open `Dateien` or
`Unterlagen und Dateien`. Select `Datei hochladen`, choose the file and wait for
confirmation. Verify the filename and correct dossier. Maximum size is 5 MiB,
meaning 5 × 1,024 × 1,024 bytes. Use meaningful filenames. Do not use document
uploads to store access credentials or install executable modules.

Select a file or `Herunterladen` and choose the destination. Open it deliberately
with an appropriate program afterwards. Keep the original until upload and a
verification download succeed. Version 0.5.0 has no general delete interface;
contact administration if a file is attached to the wrong record. Not every file
list supports filename search.

## Martial arts

Administration must install the native library on the host and activate it.
`Graduierungen` and `Prüfungshistorie` then appear in person dossiers. Missing tabs
suggest checking activation and connection; access-denied messages also require
checking your module rights.

A graduation stores discipline/style, a stage from 1 to 30, a free designation,
award date and optional examiner. Example: `Taekwon-Do`, stage `8`, designation
`8. Kup`. These neutral numbers do not define a universal order across federations.
Use your own organisation's graduation rules.

An examination stores discipline, target stage, date, result, examiner and optional
notes. Enter exactly `passed` or `failed` for the result. Saving an examination
does not automatically create a graduation or certificate: carry out and verify
those steps separately. There is no automatic eligibility or examination-fee process.

## Custom fields

In the desktop, administration can define additional fields for a record type.
Available types are text, integer, decimal, boolean and date. Assign group-level
field rights before entering values in the dossier's `Eigene Felder` section.

With write-only access, the current value is hidden. An apparently empty field
therefore does not prove that no value exists. Back up and inspect data before a
type change: any unconvertible value rejects the entire migration. Core custom-field
definitions and field rights are not administered through the current portal.

## Templates and reports

Administrators create a title and plain-text body under `Dokumentvorlagen`.
The only supported placeholders are:

```text
Attendance confirmation

We confirm attendance by {{given_name}} {{family_name}}.
Issue date: {{date}}
```

Do not invent additional placeholders such as `{{member_number}}`; they are
rejected. Templates contain no executable code. Select the recipient by opening
the appropriate person dossier.

Desktop: open a saved template in `Dokumente`, choose
`Gespeicherte Vorlage als PDF öffnen`, select a destination and review it in the
system PDF viewer. Portal: select `PDF-Vorschau`. If the mobile browser cannot
embed a PDF, use `PDF öffnen` or `Herunterladen`. Check names, date, line breaks
and wording before distribution. There is no automatic email delivery. The template
date is currently inserted in ISO format.

For lists, first choose the resource and search filter, then `CSV exportieren` or
`Gefilterte Liste exportieren`. Exports may include up to 5,000 entries across all
pages. Avoid concurrent editing of that collection while exporting. In a spreadsheet
application, select UTF-8 and comma separation. A leading apostrophe before a
formula-like value is protective; do not remove it without understanding the effect.
If an export is empty, check filters and permissions before assuming a malfunction.

## Appearance and help

Desktop: `Einstellungen → Ansicht → Darstellung und Farben`. System mode follows
light/dark preference; five alternative layouts include high contrast. Custom
colours are also available in the desktop. Portal: `Einstellungen → Ansicht`,
with system, light, dark, forest, plum and high contrast; custom colour values are
not a separate portal feature yet.

Administrators configure login-screen images under `Einstellungen → Startbildschirm`
or the portal's corresponding settings. These images are visible **before login**;
use suitable non-confidential material. They are not a person's profile photo.

Desktop `Hilfe → Nach Updates suchen` checks stable releases. A private repository
may require appropriate access; a failed check is not proof that the installed
version is current. The check installs nothing. Coordinate upgrades with
administration using the operating procedure.

## Administration

Create a user, add the user to a group, assign a role to that group and grant the
required permissions to the role. Verify the entire chain. General reading requires
`records.read`; memberships additionally use `memberships.read`; martial arts
additionally use `martial.read`. Add write rights only when needed. Do not grant
`*` as a blanket workaround for unexplained errors.

The last active administrator cannot be disabled or stripped of its last admin
assignment. Password loss requires the documented local operator-recovery process;
there is no public administrator-reset API. Business positions are not security
roles. Custom fields also require their separate group grants.

## Troubleshooting and daily checks

| Symptom | Next action |
|---|---|
| No progress after entering a name | Check the save/create action and visible error; verify window size and installed build |
| Changes not visible | Confirm dossier and host mode, refresh and clear filters |
| Access denied | Ask administration to inspect the specific role and field/module grants |
| Record changed elsewhere | Preserve your intended edits, reload and merge differences deliberately |
| Network error after saving | Do not click again blindly; check whether the write already committed |
| Missing module | Have the host directory, activation and version checked |
| PDF will not open | Check the saved file and system viewer, or portal “PDF öffnen” |
| File too large | Create a suitable smaller file while keeping the original |

At the end of the day, resolve drafts, re-read important changes and sign out.
Backup monitoring and restore drills belong to administration. Support requests
should include version, mode, time, action and error, excluding passwords, tokens
and unnecessary personal data.
