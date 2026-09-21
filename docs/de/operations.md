# Betrieb und Integration

## Lokaler Test

Die Befehle gelten im privaten Code-Repository, nicht im Docs-Repository. Voraussetzungen: vorhandenes macOS-Preset mit Qt, ICU, libxml2 und den übrigen nativen Abhängigkeiten; Node.js 22 ab 22.12. `--init admin` nur einmal auf einer neuen Testdatenbank ausführen; das Passwort wird abgefragt. Danach bleibt der Server im ersten Terminal geöffnet. Die zweite Befehlsgruppe startet das Portal in einem zweiten Terminal ausgehend vom Projektverzeichnis. Beide Prozesse beendet Ctrl+C. Die Testdatenbank ist von Deinen Desktopdaten getrennt.

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

## Anmeldung und Freigabe

`POST /api/v1/auth/login` erhält `{"login":"…","password":"…"}` und liefert `token`, `user_id`, `login`, `expires_at`. Sende anschließend `Authorization: Bearer <token>`. Token nur im Arbeitsspeicher halten. `GET /api/v1/auth/me` prüft die Sitzung; `POST /api/v1/auth/logout` widerruft sie. Standard: acht Stunden absolute Laufzeit, 30 Minuten Inaktivität; fünf Fehlversuche führen zu 30 Sekunden Sperre. Benutzerrechte und Modulbereitschaft werden serverseitig geprüft.

Im Produktivbetrieb liefert ein HTTPS-Reverse-Proxy das Portal aus und leitet `/api/v1` an den nur auf Loopback lauschenden Server weiter. `--portal-origin` muss exakt zur Browser-Origin passen. Der Proxy muss den Backend-Host auf localhost/127.0.0.1 setzen und Origin erhalten. CORS ist keine kryptografische Portalanmeldung: Nicht-Browser können Origin weglassen. mTLS/BFF ist noch nicht implementiert. Keine geheimen Portalschlüssel im Browser hinterlegen.

## Lizenzen und Module

Die [Schritt-für-Schritt-Anleitung für alle Module](lizenz-alle-module.md) enthält
die vollständige Modul-ID-Liste, Payload-Erstellung, Signatur, Registrierung und
den Import in die Anwendung.

1. Herausgeber- und Aktivierungsschlüsselpaar außerhalb des Repositories erzeugen und sicher verwahren.
2. Eigenen Aktivierungsdienst hinter HTTPS bereitstellen. [Vollständige Betreiberanleitung](../../tools/activation/README.md).
3. Lizenzpayload mit Modul-IDs, Nutzerlimit, Gültigkeit und Aktivierungsrichtlinie erstellen. Banking benötigt zusätzlich `finance`; die Bankimport-Funktion verwendet `banking`.
4. Mit dem Herausgeberschlüssel signieren und beim Aktivierungsdienst registrieren. Nur öffentliche Schlüssel und signierte Dateien weitergeben.
5. Für Produktionspakete die öffentliche Repository-Variable `CLUBPLATFORM_PINNED_LICENSE_KEY` setzen. Entwicklungs-Legacy-Lizenzen sind keine produktive Kopierschutzlösung.
6. In der Anwendung Lizenz importieren und aktivieren, Module installieren/aktualisieren und freischalten. Im Portal ist die Serverinstallation gebunden, nicht jeder Browser.
7. Vor Rechnerwechsel die Installation freigeben; am neuen Host neu aktivieren. Offline-Ausgabe setzt ausdrückliche Erlaubnis in der Lizenz voraus. Sperrungen wirken bei Offline-Leases spätestens nach Ablauf, nicht sofort.

Schema 18 ergänzt Bankkonten und importierte Posten; 17 die Installationsaktivierung, 16 Organisationswährungen, 15 Benutzer-/Personenverknüpfung und 14 Kalender/Events. Vor Upgrade Server stoppen, geprüftes Backup erstellen und passende Server-/Client-/Moduleversionen bereitstellen. Backup-Restore auf einem anderen Rechner ersetzt die Lizenzaktivierung nicht.

## API, SDK und Dokumente

Die [API-Übersicht](../api/overview.md) verlinkt die Teilverträge. API-Beträge sind dezimale Zeichenketten mit ganzzahligen kleinsten Währungseinheiten; UI-Beträge sind formatiert. Revisionen und Quell-IDs schützen Änderungen und Wiederholungen. Bankimport wird zuerst geprüft und erst nach Bestätigung gespeichert; Details im [Banking-Vertrag](../banking.md).

ABI V3 verwendet einen stabilen C-Vertrag und Modulmanifeste. Native Module sind vertrauenswürdiger Code im Hostprozess, keine Sandbox. Datenbankzugriffe und Autorisierung bleiben im Host. Siehe [V3](../extension-v3.md) und [Platzhalter](placeholders.md). Die [Abnahmeübersicht](../status.md) trennt Implementierung von Releasefreigabe.


Historical supplementary backup and restore instructions: [0.6 G0 operations](operations-0.6-g0.md). Current schema and licensing rules above take precedence.
