# Installation und Erstinbetriebnahme

> Zielversion 0.6.0, Vorarbeit G0: HTTP-API `/api/v1` und gemeinsamer `Client` mit `LocalClient`/`RestClient`. Datenbankschema 8 und Extension ABI 2 bleiben bestehen. Alte `/api/...`-Pfade liefern 404. Server, Desktop, Portal und Proxy gemeinsam aktualisieren. Die folgenden Funktionsbeschreibungen stammen aus der 0.5.0-Basis und gelten weiterhin, soweit dieser Hinweis sie aktualisiert. Core Foundation II mit ABI V3 und sieben UI-Sprachen ist noch nicht abgeschlossen.


[Sprachstart](README.md) · [Betrieb und Wiederherstellung](operations.md)

## Vorbereitungen

Für eine bestehende Installation zuerst eine geprüfte Sicherung erstellen. Daten
und Konfiguration außerhalb des Programmverzeichnisses aufbewahren. Die Beispiele
verwenden Platzhalterpfade; diese an die eigene Installation anpassen. Niemals
Produktivdaten für einen Smoke-Test verwenden.

Ein Archiv ist kein vollständiger plattformunabhängiger Installer. Passende
Betriebssystembibliotheken und für den Desktop eine passende Qt-Laufzeit sind
notwendig. Ein Desktop-Paket kann vom Hersteller mit Qt-Deployment gebaut werden.
Quellcodebefehle in diesem Kapitel richten sich an Personen mit Zugriff auf das
Implementierungsrepository; das öffentliche Dokumentationsrepository enthält
keine proprietäre Anwendung.

## Entwicklerumgebungen

| System | Referenz des Projekts |
|---|---|
| Windows | Visual Studio 2026; für Qt MSVC v143/14.44 und Qt 6.11.2 `msvc2022_64`; IncrediBuild optionaler Buildpfad |
| macOS | Vollständiges Xcode, Apple Clang, VS Code, Ninja, ccache; Qt 6.11.2 `macos` |
| Linux | C++23-Compiler, CMake/Ninja, SQLite, libsodium, cpp-httplib, nlohmann-json; Qt nur für Desktop |
| Portal | Node.js 22.12 oder neuer innerhalb der unterstützten Node-22-Linie, npm |

Dies sind projektspezifische Referenzen, keine Aussage über die jeweils neueste
verfügbare Version. PostgreSQL-Builds benötigen zusätzlich libpq. `QT_ROOT` zeigt
auf das plattformspezifische SDK. Lokale `CMakeUserPresets.json` wird nicht committet.

macOS: Falls `xcodebuild -version` nur auf Command Line Tools verweist, eine
vorhandene vollständige Xcode-Installation auswählen:

```sh
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
sudo xcodebuild -runFirstLaunch
xcodebuild -version
export QT_ROOT="$HOME/Qt/6.11.2/macos"
```

Anschließend im Implementierungsrepository:

```sh
./scripts/init-dev-macos.sh
./scripts/verify-dev-macos.sh
cmake --preset user-macos-vscode-debug
cmake --build --preset user-macos-vscode-debug --parallel
ctest --preset user-macos-vscode-debug --output-on-failure
```

Windows: `QT_ROOT` etwa auf `C:\Qt\6.11.2\msvc2022_64` setzen, neues Terminal
öffnen und `scripts\init-dev-windows.ps1` sowie `scripts\verify-dev-windows.ps1`
ausführen. Das IncrediBuild-Skript unterstützt `-Configuration Debug -Desktop`.
Builds verschiedener Systeme niemals in dasselbe Buildverzeichnis kopieren.
Qt Quick 3D/Shader Tools sind für entsprechende Grafikfunktionen vorgesehen,
aber keine Voraussetzung für die normalen Verwaltungsabläufe. WebEngine ist
für das eigenständige Portal nicht erforderlich.

## Einzelplatz

```sh
clubplatform-desktop --database /pfad/club/data.sqlite \
  --extensions /pfad/club/extensions
```

Bei einer neuen Datenbank führt der Desktop durch die Administratoreinrichtung.
Ein Passwort mit mindestens zwölf Zeichen verwenden. Danach anmelden und unter
`Administration` die gewünschten Erweiterungen aktivieren. Die Bibliothek muss
bereits im übergebenen Verzeichnis liegen; Aktivierung lädt keine Datei herunter.

## Server und Remote-Desktop

Den Server zunächst lokal mit einer neuen Datenbank initialisieren:

```sh
clubplatform-server --sqlite /pfad/club/data.sqlite --init admin
clubplatform-server --sqlite /pfad/club/data.sqlite \
  --extensions /pfad/club/extensions \
  --portal-origin https://verwaltung.example
```

`--password-stdin` ist für kontrollierte Automatisierung vorgesehen; Geheimnisse
nicht als Befehlsargument, in Git oder in öffentliche Logs schreiben. Für
PostgreSQL `--postgres` verwenden und `CLUBPLATFORM_POSTGRESQL` über eine geschützte
Betriebskonfiguration bereitstellen. Genau einen Datenbankanbieter auswählen.

Der Remote-Desktop startet mit `--server https://verwaltung.example`. Sein lokaler
Datenbankpfad ist keine Offline-Kopie der Serverdaten. Auf dem Server müssen Konto,
Rechte und Erweiterungen eingerichtet sein. Außerhalb von Loopback ist HTTPS
vorgesehen. Die öffentliche Adresse muss über einen korrekt eingerichteten Proxy
auf den lokalen C++-Host führen.

## Webportal bereitstellen

Im Implementierungsrepository:

```sh
cd apps/portal
npm ci
npm run build
```

Den Inhalt von `dist/` in das Dokumentenverzeichnis des HTTPS-Webservers kopieren.
Kein Node-Prozess wird zum Ausliefern benötigt. `/api/v1/` an `127.0.0.1:8080`
weiterleiten; den Upstream-Header `Host` auf `127.0.0.1:8080` setzen und `Origin`
sowie `Authorization` erhalten. `--portal-origin` muss exakt zum Browser-Ursprung
passen, ohne abschließenden Schrägstrich. Der Portalpfad ist `/`; ein beliebiger
Unterpfad ist in 0.5.0 nicht als fertig konfigurierbar zu behandeln.

Für Entwicklung läuft Vite üblicherweise auf `http://127.0.0.1:5173`; genau diesen
Ursprung am Server freigeben. `CLUB_API` kann das Ziel des Entwicklungsproxys ändern.
`npm run dev` ist kein Produktions-Webserver.

## Abnahme

Mit einer Testperson Anmeldung, Speichern, erneutes Laden, Organisation und
Mitgliedschaft prüfen. Ein eingeschränktes Konto muss unberechtigte Schreibversuche
abweisen. Foto, Binärdatei, Graduierung, CSV und PDF ausprobieren. Anschließend
Sicherung tatsächlich in eine neue Datenbank wiederherstellen. Alte Sitzungen
müssen dort ungültig sein. Systemdialoge und PDF-Betrachter auf jedem Zielsystem
prüfen. Erfolgreicher Build allein ist keine fachliche Abnahme.

## Beispiel für den HTTPS-Reverse-Proxy

Die folgende Nginx-Konfiguration ergänzt den bestehenden TLS-Virtual-Host. Passe den Webroot an und konfiguriere Zertifikat und HTTPS-Listener in der Serverumgebung. `client_max_body_size` erlaubt den maximalen JSON-Upload; fachliche Dateigrenzen prüft weiterhin die Anwendung. Starte den Dienst mit der exakt gleichen öffentlichen Origin.

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
