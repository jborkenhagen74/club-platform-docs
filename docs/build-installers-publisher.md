# Builds, Installer und grafische Lizenzerstellung

Die Skripte bauen auf dem jeweiligen Zielsystem: Windows auf Windows, macOS auf
macOS und Linux auf Linux. Ein Mac erzeugt keine Windows-EXE. Die Architektur
folgt dem ausgewählten Compiler/Qt-SDK bzw. dem optionalen CMake-Preset.

## Voraussetzungen

Für die Skripte: Python 3.9 oder neuer sowie CMake/CTest/CPack im PATH. Für den
Code: C++23-Compiler und die vorhandenen Projektabhängigkeiten. Desktop und
Herausgeberoberfläche benötigen Qt 6.5 oder neuer; Referenz-SDK ist Qt 6.11.2.
Das Herausgeberwerkzeug benötigt Qt Widgets aus Qt Base, kein zusätzliches
Python auf dem Rechner, auf dem das fertige Lizenztool verwendet wird.

- **Windows:** Visual Studio 2026 mit C++-Werkzeugen, passendes Qt-MSVC-SDK,
  `VCPKG_ROOT` wie in der Entwicklungsanleitung. Für EXE-Installer zusätzlich
  NSIS 3.03 oder neuer (`makensis` im PATH bzw. regulär installiert).
- **macOS:** Xcode/Command Line Tools, CMake, Ninja nach Bedarf sowie die
  Homebrew-Abhängigkeiten der Entwicklungsanleitung. `QT_ROOT` auf
  `$HOME/Qt/6.11.2/macos` setzen; `ICU_ROOT` bei Bedarf auf den Homebrew-ICU-Prefix.
  `productbuild` und `pkgbuild` gehören zu den macOS-Werkzeugen.
- **Linux:** C++23-Compiler, Qt und Entwicklungspakete für SQLite, libsodium,
  cpp-httplib, nlohmann-json, curl, ICU und libxml2. DEB benötigt `dpkg-deb` und
  `dpkg-shlibdeps` (dpkg-dev), RPM zusätzlich `rpmbuild`.
- `--with-portal` benötigt zusätzlich das bereits im Projekt verwendete Node/npm.

Die Skripte installieren keine Compiler, verändern keine Systemrechte und laden
keine privaten Schlüssel herunter. Normale Buildfehler stoppen den Ablauf sofort.

## Einstieg: vier Befehle

| Zweck | Windows PowerShell | macOS / Linux |
|---|---|---|
| Desktop-Debugbuild mit Tests | `./scripts/build.ps1` | `./scripts/build.sh` |
| Grafisches Lizenztool bauen | `./scripts/build-publisher.ps1 --config Release` | `./scripts/build-publisher.sh --config Release` |
| Kunden-Installer erstellen | `./scripts/create-installer.ps1 --public-key C:/Keys/issuer/public.hex` | `./scripts/create-installer.sh --public-key /sicher/issuer/public.hex` |
| Separaten Herausgeber-Installer erstellen | `./scripts/create-publisher-installer.ps1` | `./scripts/create-publisher-installer.sh` |

Alle Wrapper rufen denselben Python-Treiber auf und reichen Argumente unverändert
weiter. Alternativ: `python3 scripts/build.py --help`, unter Windows
`py -3 scripts/build.py --help`. Die Befehle funktionieren unabhängig vom
aktuellen Arbeitsverzeichnis. Pfade mit Leerzeichen in Anführungszeichen setzen.

Beispiel auf Deinem Mac:

```bash
export QT_ROOT="$HOME/Qt/6.11.2/macos"
export ICU_ROOT="$(brew --prefix icu4c)"
./scripts/build-publisher.sh --config Release
./scripts/create-publisher-installer.sh
```

Beispiel unter Windows:

```powershell
$env:QT_ROOT = 'C:\Qt\6.11.2\msvc2022_64'
./scripts/build-publisher.ps1 --config Release --generator 'Visual Studio 18 2026'
./scripts/create-publisher-installer.ps1 --generator 'Visual Studio 18 2026'
```

Ein vorhandenes Benutzerpreset kann mit `--preset user-macos-vscode-release`
bzw. `--preset user-windows-vs2026-release` als Werkzeugkonfiguration dienen.
Die Profile des Skripts überschreiben Buildtyp, Test-, GUI- und Lizenzoptionen.
Die bisherigen IncrediBuild-Skripte bleiben für verteilte Builds verfügbar;
die neuen Wrapper aktivieren IncrediBuild nicht automatisch.

## Profile, Optionen und Ausgabe

- `--profile desktop`: Desktop und Server samt Fachmodulen.
- `--profile server`: Server und Fachmodule ohne Qt-Oberfläche.
- `--profile publisher`: natives Lizenztool; signierte Lizenzen direkt erstellen.
- `--config Debug`: Diagnoseinformationen; `Release`: Optimierungen.
- `--qt-root PFAD`: Alternative zu `QT_ROOT`.
- `--toolchain DATEI`, `--generator NAME`, `--preset NAME`: vorhandene Toolchain.
- `--jobs 4`: Zahl paralleler Buildjobs (Standard maximal acht).
- `--with-portal`: npm-Installation/Build; im Installer unter
  `share/clubplatform/portal`. Das konfiguriert noch keinen Webserver.
- `--skip-tests`: Tests ausdrücklich überspringen. Kein Abnahmenachweis.
- `--dry-run`: geplante Befehle prüfen, ohne Build oder Dateiänderungen.
- `--output PFAD`: anderes Ausgabeverzeichnis für Installer.

Buildbäume liegen unter `build/<system>-<profil>-<konfiguration>/`, Pakete unter
`out/installers/`. Ein öffentlicher Produktionsschlüssel führt für native Tests
zu einem separaten `-verification`-Build mit dem Test-Vertrauensanker; der finale
Kundenbuild enthält ausschließlich den fest eingebauten Produktions-Public-Key.
Ein Herausgeberbuild enthält keinen vordefinierten privaten Schlüssel.

| System | Standard-Installer | Weitere Formate |
|---|---|---|
| Windows | NSIS `.exe` | `--format ZIP`, `--format TGZ` |
| macOS | `productbuild` `.pkg` | `--format ZIP`, `--format TGZ` |
| Linux | `.deb` | `--format RPM`, `--format TGZ`, `--format ZIP` |

Installer erzwingen Release. Kunden-Installer erfordern `--public-key`; eine
128-stellige private Schlüsseldatei wird hier abgewiesen. Herausgeberpakete
brauchen keinen Kunden-Vertrauensanker. In jedem Fall wird ein frisches
Stagingverzeichnis verwendet. Paketiert werden ausschließlich CMake-Installations-
artefakte, niemals der Quellbaum oder lokal erzeugte Lizenz-/Schlüsselverzeichnisse.

Windows verwendet getrennte Installationsverzeichnisse und Startmenüeinträge
für Desktop und Lizenztool. macOS installiert nach `/Applications/ClubPlatform`
bzw. `/Applications/ClubPlatformPublisher`. Linux installiert nach
`/opt/club-platform-<profil>`; Programmstart über das dortige `bin`-Verzeichnis.
ZIP/TGZ sind portable Verzeichnisarchive, keine nativen Installer.

Qt-Runtime-Deployment wird bei der Paketierung aktiviert, soweit es das verwendete
Qt-SDK auf der Plattform unterstützt. Linux-Pakete ermitteln native Bibliotheks-
abhängigkeiten. Serverpakete und Archivpakete benötigen gegebenenfalls zusätzliche
Systembibliotheken. Prüfe jedes Paket auf einer sauberen Zielmaschine.
Apple-Codesignierung/Notarisierung und Windows-Authenticode-Signierung sind hier
noch nicht automatisiert; die erstellten Installer sind ohne separate Signierung.

## Das Lizenztool verwenden

Nach dem Build heißt das Programm `clubplatform-license-tool`. Unter Windows
liegt es gewöhnlich in `tools/publisher/Release`, unter Linux in
`tools/publisher`; unter macOS entsteht dort `clubplatform-license-tool.app`.
Das installierte Paket enthält diese Oberfläche und den integrierten Signierer.
Der bisherige separate CLI-Signierer bleibt im Quellprojekt verfügbar.

### Einmalige Einrichtung

1. Im Reiter **Einrichtung** den vorhandenen privaten Lizenzschlüssel auswählen.
   Hast Du noch keinen, erzeugt **Neues Herausgeber-Schlüsselpaar erstellen** ein
   neues privates Verzeichnis mit `secret.hex` und `public.hex`.
2. Diesen Schlüssel beibehalten und privat sichern. Ein neuer Herausgeberschlüssel
   passt nicht zu bereits mit dem alten Public-Key gebauten Kundenprogrammen.
3. HTTPS-Adresse des Aktivierungsdienstes und dessen **öffentliche** Schlüsseldatei
   auswählen. Der private Aktivierungsschlüssel verbleibt auf dem Diensthost.
4. Optional einen vorhandenen SSH-Host-Alias und die dortigen Pfade für Python,
   `service.py`, Datenbank, Aktivierungsschlüssel und Lizenz-Public-Key eintragen.
5. **Einrichtung speichern**. Gespeichert werden Pfade und öffentliche Einstellungen;
   keine Kopie des privaten Signierschlüssels und kein SSH-Passwort.

Der Aktivierungsdienst muss separat eingerichtet sein, siehe
[Aktivierungsanleitung](../tools/activation/README.md). Für automatische Registrierung
benötigt er die neue CLI-Operation `register-stdin`. Der SSH-Zugang muss bereits
mit bekanntem Hostschlüssel und Schlüssel/SSH-Agent funktionieren. Das Tool
schaltet Hostprüfungen nicht aus und fragt keine SSH-Passwörter ab.

### Eine neue Lizenz ausstellen

1. Im Reiter **Lizenz** die Lizenz-ID, Edition und Laufzeit eintragen. Die
   vorbelegte UUID ist eine neue eindeutige ID. Für eine Verlängerung dieselbe
   bisherige Lizenz-ID verwenden, für einen anderen Kunden eine andere ID.
2. Enddatum und Wartungsdatum gelten jeweils **einschließlich dieses UTC-Tages**.
3. Benutzerlimit, Installationszahl und Erneuerungsfrist festlegen.
4. Gewünschte Module auswählen. Beiträge/Käufe/Banking ergänzen Finanzen;
   Veranstaltungen ergänzen Finanzen und Kalender automatisch.
5. **Lizenz erstellen und beim Dienst registrieren** wählen und den Zielnamen
   bestimmen. Die Oberfläche erzeugt JSON und Signatur und überträgt ausschließlich
   die signierte Lizenz per SSH-Standardeingabe an den Dienst.
6. Erst bei **erstellt und registriert** ausliefern. Wird eine bereits registrierte
   Lizenz-ID verwendet, ersetzt die Registrierung ihre bisherige Payload und
   gibt eine zuvor gesperrte Lizenz wieder frei; dies wird vorher bestätigt.

**Nur signierte Lizenzdatei erstellen** funktioniert ohne SSH. Die Registrierung
steht dann ausdrücklich noch aus. Bei einem Registrierungsfehler bleibt die Datei
erhalten. Nach Korrektur der Dienstkonfiguration über **Vorhandene Lizenz beim
Dienst registrieren** wiederholen; die Lizenz muss nicht neu signiert werden.

Vorhandene Ausgabedateien werden nicht überschrieben. Die vollständige Datei an
Kunden übergeben; `payload` und `signature` nicht manuell bearbeiten. Private
Schlüssel niemals mitgeben. Die Wahl „dauerhaft offline“ erlaubt anschließend den
separaten an die Installation gebundenen Offline-Aktivierungsablauf; die Lizenzdatei
allein aktiviert auch in diesem Modus noch keine Kundeninstallation.

## Prüfstand

Automatisiert vorgesehen: Buildplanung für alle drei Systeme, Schlüsselgrenzen,
Datum/Modulvalidierung, eingebetteter Signierer und sichere CLI-Registrierung.
Die Qt-CI baut das Herausgeberwerkzeug und führt dessen native Tests aus.
Lokal geprüft: Python-Tests und Paketstruktur mit synthetischem Inhalt.
Die neuen nativen Builds, GUI-Bedienung und plattformspezifischen Installer sind
noch nicht abgenommen: die aktuellen GitHub-Jobs scheitern vor dem ersten Schritt.
Dieser Status ersetzt weder einen erfolgreichen CI-Lauf noch einen Installationstest.
