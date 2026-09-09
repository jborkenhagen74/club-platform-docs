# Minimal browser integration

[Deutsch](../../../docs/de/frontends/getting-started.md) · [English](../../../docs/en/frontends/getting-started.md) · [Français](../../../docs/fr/frontends/getting-started.md) · [Español](../../../docs/es/frontends/getting-started.md) · [한국어](../../../docs/ko/frontends/getting-started.md)

Serve this directory from the same HTTPS origin as the reverse-proxied `/api/v1`.
Configure the server's exact allowed portal origin and rewrite the upstream Host to
`127.0.0.1:8080`. Use the deployment configuration in the translated installation
chapters. Opening `index.html` as `file://` or merely starting a static server without
an API proxy is insufficient.

Create an account on the application host and grant `records.read`. Enter its real
credentials; the example ships no default password. It signs in, lists people with
cursor pagination and signs out. Tokens stay in memory, a reload requires login,
and user-supplied names are rendered as text. A failed logout drops the browser token
but cannot guarantee server revocation if the server was unreachable.

This intentionally small example does not replace the React/Tailwind administration
portal in the implementation repository. It has no editing, membership management,
branding, files or PDF interface. The translated chapters explain the full portal.
