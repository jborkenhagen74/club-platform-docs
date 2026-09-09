# Frontends and web-server integration

> Target version 0.6.0, preparatory G0 work: HTTP API `/api/v1` and shared `Client` with `LocalClient`/`RestClient`. Database schema 8 and extension ABI 2 remain unchanged. Old `/api/...` paths return 404. Upgrade server, desktop, portal and proxy together. The functional descriptions below originate from the 0.5.0 baseline and remain applicable except where this notice updates them. Core Foundation II with ABI V3 and seven UI languages is not complete.


[Language home](../README.md) · [REST](../api/overview.md) · [Installation](../installation.md)

The product portal uses React/TypeScript and Tailwind 4. `npm ci` follows the lockfile;
`npm run build` creates static `dist/` files. PDF code and fonts are loaded from the
build only when needed, with no required CDN scripts. The small
`examples/frontends/web-basic` example demonstrates login and a people list,
not the full application.

## Transport

Serve the browser and API through the same public HTTPS origin. Proxy `/api/v1/` to
the loopback host. Set upstream `Host` to `127.0.0.1:8080` and preserve `Authorization`
and `Origin`. Start the service with that exact public origin in `--portal-origin`.
Without configuration, browser requests carrying an Origin are denied. Do not
replace correct configuration with wildcard access.

Configure `/health` separately if public health monitoring is required; the usual
`/api/v1/` proxy does not include it. Do not log request bodies, passwords or tokens.
DNS, certificates and service accounts follow local operating procedures; the
application does not automatically manage TLS certificates.

## Client behaviour

Keep tokens in memory, never in URLs or persistent browser stores. On `401`, clear
personal lists, drafts and the session, then request login. Explain `403` as an
authorisation/configuration failure. A network error after a write is ambiguous:
read the server state before deciding to retry. Compare the current revision after
`409` rather than automatically replaying the edit.

Read lists in pages. Show human-readable reference names using `labels` or related
records, while submitting IDs. Render untrusted strings as text, not HTML. Download
files only following an explicit user action. Uploaded files are never executed
as extensions by the portal.

## Appearance and scope

Light, dark, forest, plum and high-contrast layouts supplement system mode.
Date inputs and displays use browser locale; API dates remain ISO. Small screens
select dossier sections through `Aktenbereich`. Core custom-field definitions
and field permissions are still administered in the desktop application. The
portal does not automatically map a login to the user's own membership record.

Use the [OpenAPI contract](../../../openapi/club-platform.yaml) together with the
[field reference](../../../reference/resources.md). Do not reuse nonexistent draft
routes such as `/api/v1/appointments`. Test compatibility before product updates.
