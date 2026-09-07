# Frontend integration

Frontends communicate with the central server over HTTPS. A frontend should never connect directly to PostgreSQL.

Typical calls include `/api/v1/me`, `/api/v1/members`, `/api/v1/appointments` and extension-specific resources. The server filters data according to the authenticated user's permissions.

See `examples/frontends/web-basic`.
