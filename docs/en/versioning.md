# Versioning and supported scope

> Target version 0.6.0, preparatory G0 work: HTTP API `/api/v1` and shared `Client` with `LocalClient`/`RestClient`. Database schema 8 and extension ABI 2 remain unchanged. Old `/api/...` paths return 404. Upgrade server, desktop, portal and proxy together. The functional descriptions below originate from the 0.5.0 baseline and remain applicable except where this notice updates them. Core Foundation II with ABI V3 and seven UI languages is not complete.


[Language home](README.md)

Baseline: application **0.5.0**, commit `320a4c2709c13dd56455768a2f8819a815ad3997`,
schema **8**, native ABI **2**, documentation edition **2026-09-09**.

| Layer | Contract |
|---|---|
| Application | Product/package version 0.5.0 |
| Database | Ordered migrations; unknown or modified definitions are rejected |
| Extension | ABI 2 and a separate manifest with three-component version |
| HTTP | Implemented `/api/v1` routes and separate `/health`; no released `/api/v1` |
| Documentation | Equivalent chapters and functional scope in de/en/fr/es/ko |

R1.9 adds the native host, R1.10 martial arts, R1.11 templates/PDF/CSV and R1.12
pilot operations. Pilot status does not mean universally signed installers or
completed acceptance on every target computer. Translated manuals do not switch
the application's interface language.

The earlier ABI-1 and `/api/v1` proposal is historical. Its menu, view and REST
callbacks are not guaranteed capabilities of 0.5.0. Appointments, payment workflows,
offline sync, tenant isolation, arbitrary plugin UI, automatic updates and complete
interface localisation remain outside the implemented scope. Check product, ABI
and actual routes together before extending or integrating.

After a change, synchronise this reference and the other four languages, update
the implementation baseline and run documentation validation. Never translate
identifiers, field keys, URLs or command options. An integration's security contract
is independent of the language chosen to read about it.
