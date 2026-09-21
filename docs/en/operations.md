# Operations and integration

## Local test

Run these commands in the private implementation repository, not this documentation repository. Prerequisites: the existing macOS preset with Qt, ICU, libxml2 and other native dependencies; Node.js 22.12 or later in the 22 series. Run `--init admin` only once for a new test database; enter the password at its prompt. Keep the server running in the first terminal. Run the second command block in a second terminal starting at the project root. Ctrl+C stops each process. This database is separate from existing desktop data.

```bash
cmake --preset user-macos-vscode-debug
cmake --build --preset user-macos-vscode-debug --parallel
mkdir -p build/portal-test
./build/user-macos-vscode-debug/apps/server/clubplatform-server \
  --sqlite build/portal-test/data.sqlite --init admin
./build/user-macos-vscode-debug/apps/server/clubplatform-server \
  --sqlite build/portal-test/data.sqlite \
  --extensions "$PWD/build/user-macos-vscode-debug/runtime-extensions" \
  --port 8080 --portal-origin http://127.0.0.1:5173
```

```bash
cd apps/portal
npm ci
npm run dev -- --port 5173 --strictPort
```

http://127.0.0.1:5173

## Authentication and deployment

`POST /api/v1/auth/login` accepts `{"login":"…","password":"…"}` and returns `token`, `user_id`, `login`, `expires_at`. Send `Authorization: Bearer <token>`; keep the token in memory. `GET /api/v1/auth/me` checks the session; `POST /api/v1/auth/logout` revokes it. Defaults: eight-hour absolute lifetime, 30-minute idle timeout, 30-second lock after five failed attempts. The server checks user permissions and module readiness.

In production an HTTPS reverse proxy serves the portal and forwards `/api/v1` to the loopback-only server. Set `--portal-origin` to the exact browser origin. Forward the backend Host as localhost/127.0.0.1 and preserve Origin. CORS is not cryptographic portal authentication; non-browser clients may omit Origin. mTLS/BFF is not implemented. Never embed portal secrets in browser code.

## Licenses and modules

1. Generate publisher and activation keypairs outside the repository and protect the private keys.
2. Deploy the activation authority behind HTTPS. See the [operator guide](../../tools/activation/README.md).
3. Prepare the license payload with modules, user limit, validity and activation policy. Banking requires both `finance` and `banking`.
4. Sign with the publisher key and register the signed license at the authority. Distribute only public keys and signed files.
5. Set repository variable `CLUBPLATFORM_PINNED_LICENSE_KEY` for production packages. Development legacy licenses are not production copy protection.
6. Import and activate the license; install/update and enable modules. Portal activation binds the server installation, not individual browsers.
7. Release the installation before moving hosts, then activate the new host. Offline issuance must be permitted in the license. Offline revocation takes effect no later than lease expiry, not immediately.

Schema 18 adds bank accounts and imported entries; 17 installation activation; 16 organization currencies; 15 user/person linking; 14 calendar/events. Before upgrading, stop the server, take a verified backup and deploy matching server, client and module versions. Restoring a backup on another host does not replace license activation.

## API, SDK and documents

See the [API index](../api/overview.md). API money values are integer minor-unit decimal strings; UI values are formatted. Revisions and source IDs protect updates and retries. Banking preview precedes explicit import confirmation; see the [banking contract](../banking.md).

ABI V3 uses a stable C boundary and manifests. Native extensions are trusted in-process code, not sandboxed. Persistence and authorization belong to the host. See [V3](../extension-v3.md), [placeholders](placeholders.md) and [acceptance status](../status.md).



Historical supplementary backup and restore instructions: [0.6 G0 operations](operations-0.6-g0.md). Current schema and licensing rules above take precedence.
