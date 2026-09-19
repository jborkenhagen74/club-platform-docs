# Frontend integration

Frontends communicate with the central server over HTTPS. A frontend should never connect directly to PostgreSQL.

Authenticate with `POST /api/v1/auth/login` using `{login,password}`. Keep the returned
`token` in memory and send `Authorization: Bearer <token>` for protected requests.
Current principal: `GET /api/v1/auth/me`; logout: `POST /api/v1/auth/logout`.
This implementation does not use authentication cookies. Never put publisher keys
or a supposed shared portal secret into JavaScript. See [local setup and security](../en/operations.md).

Persons use `/api/v1/persons`; scheduling and finance use their module APIs.
License readiness and user permissions are separate server-side checks.

See `examples/frontends/web-basic`.
