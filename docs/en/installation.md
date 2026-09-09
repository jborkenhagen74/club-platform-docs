# Installation and initial setup

> Target version 0.6.0, preparatory G0 work: HTTP API `/api/v1` and shared `Client` with `LocalClient`/`RestClient`. Database schema 8 and extension ABI 2 remain unchanged. Old `/api/...` paths return 404. Upgrade server, desktop, portal and proxy together. The functional descriptions below originate from the 0.5.0 baseline and remain applicable except where this notice updates them. Core Foundation II with ABI V3 and seven UI languages is not complete.


[Language home](README.md) · [Operations and recovery](operations.md)

## Preparation

Back up an existing installation before changing it. Keep data and configuration
outside the program directory. Replace example paths with your installation's
paths and never run smoke tests against production data.

An archive is not a universal installer: operating-system libraries and a matching
Qt runtime for the desktop must be available. A desktop distribution can bundle
Qt through the product's deployment option. Source-build commands below require
access to the implementation repository. This public documentation repository
does not contain the proprietary application.

## Development environments

| System | Project reference |
|---|---|
| Windows | Visual Studio 2026; MSVC v143/14.44 and Qt 6.11.2 `msvc2022_64` for Qt; optional IncrediBuild workflow |
| macOS | Full Xcode, Apple Clang, VS Code, Ninja, ccache and Qt 6.11.2 `macos` |
| Linux | C++23 compiler, CMake/Ninja, SQLite, libsodium, cpp-httplib, nlohmann-json; Qt for desktop builds |
| Portal | Supported Node 22 release, at least 22.12, and npm |

These are project references, not claims about the newest available releases.
PostgreSQL builds also need libpq. `QT_ROOT` points to the platform SDK.
Machine-specific `CMakeUserPresets.json` must not be committed.

If macOS reports Command Line Tools instead of full Xcode, select the installed
full application:

```sh
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
sudo xcodebuild -runFirstLaunch
xcodebuild -version
export QT_ROOT="$HOME/Qt/6.11.2/macos"
```

Then, in the implementation repository:

```sh
./scripts/init-dev-macos.sh
./scripts/verify-dev-macos.sh
cmake --preset user-macos-vscode-debug
cmake --build --preset user-macos-vscode-debug --parallel
ctest --preset user-macos-vscode-debug --output-on-failure
```

On Windows, set `QT_ROOT`, for example to `C:\Qt\6.11.2\msvc2022_64`, open a new
terminal and run `scripts\init-dev-windows.ps1` and `scripts\verify-dev-windows.ps1`.
The IncrediBuild wrapper accepts `-Configuration Debug -Desktop`. Do not share
build output directories between operating systems. Quick 3D/Shader Tools are for
related graphics functionality, not prerequisites for routine administration.
WebEngine is unnecessary for the separate browser portal.

## Standalone desktop

```sh
clubplatform-desktop --database /path/club/data.sqlite \
  --extensions /path/club/extensions
```

A new database offers initial administrator setup. Use a password of at least
12 characters. Log in and activate required extensions from `Administration`.
The native library must already be in the configured directory; activation is
not a download operation.

## Server and connected desktop

Initialise the database locally, then start the service:

```sh
clubplatform-server --sqlite /path/club/data.sqlite --init admin
clubplatform-server --sqlite /path/club/data.sqlite \
  --extensions /path/club/extensions \
  --portal-origin https://management.example
```

`--password-stdin` supports controlled automation. Do not put passwords in command
arguments, Git or public logs. For PostgreSQL use `--postgres` and provide
`CLUBPLATFORM_POSTGRESQL` through protected operating configuration. Select exactly
one database provider.

Connect the desktop with `--server https://management.example`. A local database
path is not an offline replica of server data. Accounts, permissions and native
modules must exist on the server. Remote access uses HTTPS through a correctly
configured reverse proxy; HTTP is limited to loopback use.

## Deploying the portal

In the implementation repository:

```sh
cd apps/portal
npm ci
npm run build
```

Copy `dist/` contents to the HTTPS web server's document root. No Node process is
needed to serve them. Proxy `/api/v1/` to `127.0.0.1:8080`, set upstream `Host` to
`127.0.0.1:8080`, and preserve `Origin` and `Authorization`. The configured
`--portal-origin` must match the browser origin exactly, without a trailing slash.
Version 0.5.0 operates at `/`; arbitrary subpath deployment is not a completed
configuration feature.

For development, Vite normally serves `http://127.0.0.1:5173`; permit that exact
origin. `CLUB_API` changes the development proxy target. `npm run dev` is not a
production hosting command.

## Acceptance checks

Use test data to verify login, create/save/reload, an organisation and membership.
An account with restricted permissions must fail an unauthorised write. Check a
photo, binary file download, graduation, CSV and PDF. Restore a real backup into
a new database and verify that old sessions are invalid. Check native dialogs and
the PDF viewer on every target OS. A successful build alone is not acceptance.

## HTTPS reverse-proxy example

Add the following Nginx configuration to the existing TLS virtual host. Adjust the document root and configure the certificate and HTTPS listener in the server environment. The request-size limit accommodates the largest JSON upload; the application still enforces its decoded-file limits. Start the service with the exact same public origin.

```nginx
root /srv/club-platform/portal;
client_max_body_size 8m;

location / {
    try_files $uri $uri/ /index.html;
}

location /api/v1/ {
    proxy_pass http://127.0.0.1:8080;
    proxy_set_header Host 127.0.0.1:8080;
    proxy_set_header Origin $http_origin;
    proxy_set_header Authorization $http_authorization;
}
```
