> Seit Schema 17: Für neue Lizenzdateien Aktivierungs-URL und Aktivierungs-Public-Key konfigurieren. Kundenpakete erhalten einen fest eingebauten Herausgeber-Schlüssel. Siehe [Aktivierungsanleitung](../tools/activation/README.md). Die bisherigen ungebundenen Lizenzdateien gelten nur noch in Entwicklungsbuilds; für geschützte Produktionspakete müssen sie neu ausgestellt werden.

# Phase 7 und 8: Lizenzierung und Modulinstallation

Stand: 17.09.2026. Aufbauend auf Phase 5/6, Datenbankschema **12**.
Die noch offenen I18n-/Loader-Abnahmepunkte von Phase 5/6 bleiben eigenständig.

## Bedienung

Im Desktop unter **Erweiterungen** und im Webportal unter **Einstellungen →
Lizenz und Module** kann ein Administrator eine signierte Lizenzdatei importieren.
Im Portal zuerst „Lizenzstatus anzeigen“ wählen. Anschließend „Module aus Katalog
installieren“ wählen und den zum Produkt gehörenden signierten Katalog öffnen.
Der Host lädt die freigeschalteten Pakete, prüft sie und installiert ihre
Datenbankmigrationen. Bei Erfolg erscheint ein Neustarthinweis. Den Desktop
im Einzelplatzbetrieb bzw. den Server im Client-Server-Betrieb neu starten.
Remote-Desktops und Browser installieren niemals native Pakete auf dem Client.

Die Oberfläche verwendet gemeinsame Übersetzungsschlüssel für DE, EN, FR, IT,
ES, KO und TR. Die Edition stammt als Produktkennung aus der Lizenz.

Die administrative Berechtigung ist `schema.manage`. Lizenzentitlements und
Benutzerrechte sind unabhängige Voraussetzungen. Eine Lizenz verleiht keine
Schreibrechte und ein Administratorrecht ersetzt keine Modullizenz.

## Lizenzregeln

* Signatur: Ed25519 über die **unveränderten UTF-8-Bytes**
  `clubplatform/license/v1\n` plus `payload`.
* Pflichtfelder: `license_id`, `edition`, `not_before`, `expires_at`,
  `maintenance_until`, `max_users`, `modules`.
* Zeiten sind ganzzahlige UTC-Unixsekunden; Gültigkeit ist
  `not_before <= jetzt < expires_at`.
* Gezählt werden **aktive Benutzerkonten**, keine Sitzungen. Anlage und
  Reaktivierung werden innerhalb derselben DB-Transaktion wie die Limitprüfung
  durchgeführt. Ein kleineres Limit deaktiviert vorhandene Benutzer nicht
  automatisch: `over_limit` wird im API-Status geliefert, weitere Aktivierungen bleiben gesperrt.
* Ohne gültige Lizenz: Basisbetrieb mit einem aktiven Benutzerlimit, keine
  freigeschalteten Erweiterungen. Bestehende Konten bleiben für Verwaltung und
  Reparatur erreichbar. Kein vorhandener Datensatz wird wegen Lizenzablauf gelöscht.
* Entzogene/abgelaufene Modullizenzen sperren die Moduloperationen auch bei bereits
  angemeldeten Benutzern. Nach erneuter Freischaltung sind die Daten wieder verfügbar.
* Wartungsende begrenzt **neue Paketversionen** anhand von `released_at`;
  es beendet nicht selbst die Laufzeit einer noch gültigen Lizenz.
* Offline-Lizenzen benötigen keinen Kontakt zu einem Lizenzserver. Eine zentrale
  Online-Sperrliste oder ein Abonnement-/Zahlungsdienst gehört nicht zu diesem Stand.

Beispiel des unsignierten Hersteller-Eingabedokuments:

```json
{
  "license_id": "customer-0001",
  "edition": "sports-school",
  "not_before": 1789603200,
  "expires_at": 1821139200,
  "maintenance_until": 1821139200,
  "max_users": 20,
  "modules": ["martial"]
}
```

Alle notwendigen Abhängigkeitsmodule müssen ebenfalls in den Entitlements stehen.
Sprachpakete des Core werden nicht lizenziert. Die bestehenden Modulübersetzungen
werden durch den Translation Provider des jeweiligen nativen Moduls geliefert.

## Vertrauensanker und Installationspfade

Diese Werte setzt ausschließlich der Betreiber/Installer in der Prozessumgebung:

| Variable | Bedeutung |
|---|---|
| `CLUBPLATFORM_LICENSE_PUBLIC_KEY` | 32-Byte Ed25519-Public-Key als 64 Hexzeichen |
| `CLUBPLATFORM_CATALOG_PUBLIC_KEY` | separater Public-Key für Katalog und Paketdeskriptoren |
| `CLUBPLATFORM_MODULE_STORE` | persistentes Verzeichnis für vorbereitete Generationen |
| `CLUBPLATFORM_OFFLINE_PACKAGES` | optionales Verzeichnis für signierte Offline-Pakete |
| `CLUBPLATFORM_INITIAL_LICENSE` | optionaler Pfad einer **nur erstmalig** eingelesenen Lizenz |

Ein späterer Lizenzwechsel wird niemals durch die initiale Lizenzdatei überschrieben.
HTTP-Anfragen dürfen weder Trust Keys noch Installationspfade vorgeben. Private
Signierschlüssel gehören ausschließlich in die Herstellerumgebung.

Nach einer erfolgreichen Provisionierung hat die in der Datenbank referenzierte
Generation Vorrang vor `--extensions`/`CLUBPLATFORM_EXTENSIONS`. Vor ihrem Laden
werden Katalogsignatur, Plattform, Core-Kompatibilität, Dateien und Hashes erneut
geprüft. Der Katalog darf für einen bereits installierten Stand abgelaufen sein;
sein Ablauf verhindert neue Installationen, nicht den Start bestehender Pakete.

Das Modulverzeichnis muss für das Hostkonto beschreibbar sein. Alte Generationen
bleiben erhalten; es gibt keine automatische Bereinigung. Im Mehrhostbetrieb
müssen alle Hosts denselben Modulstand sehen und nach der Installation kontrolliert
neu gestartet werden. Gemischte Architekturen benötigen getrennte Installationen.

## Herstellerwerkzeuge

```sh
cmake -S . -B build -DCLUBPLATFORM_BUILD_PUBLISHER_TOOLS=ON
cmake --build build --target clubplatform-sign
build/tools/distribution/clubplatform-sign keygen /sicher/neue-lizenzschluessel
build/tools/distribution/clubplatform-sign sign license \
  /sicher/neue-lizenzschluessel/secret.hex license-payload.json license.json
```

Unter Windows entsprechend `clubplatform-sign.exe` aus dem gewählten Buildprofil
verwenden. Das Werkzeug überschreibt keine vorhandenen Ausgabedateien. Die
Signierwerkzeuge werden nicht in Kundenpakete installiert. Für automatisierte Tests
werden sie ebenfalls gebaut; deren eigener Trust Key ist ausschließlich Testmaterial.

Die Ausgabe für Lizenz und Katalog ist ein JSON-Envelope:

```json
{"payload":"...JSON als Zeichenkette...","signature":"128 Hexzeichen"}
```

`payload` anschließend nicht neu formatieren: Die Signatur gilt für seine exakten
Bytes. Für Paketdeskriptoren signiert das Werkzeug das mit nlohmann/json kompakt
serialisierte Objekt ohne `signature`; anschließend wird die Signatur hinzugefügt.

## Katalog und Pakete

Katalogpayload: `issued_at`, `expires_at`, `packages`. Jeder Paketdeskriptor enthält:

```json
{
  "module_id": "martial",
  "version": "1.0.0",
  "platform": "linux",
  "architecture": "x64",
  "core_range": {"minimum":"0.6.0", "maximum_exclusive":"0.7.0"},
  "released_at": 1789603200,
  "download_location": "https://packages.example.org/martial-1.0.0.so",
  "sha256": "SHA256-DER-DATEIBYTES",
  "dependencies": [],
  "manifest": {},
  "signature": "SIGNATUR-DES-DESKRIPTORS"
}
```

`manifest` muss das vollständige, tatsächlich eingebettete Manifest enthalten.
Der Beispielwert `{}` ist nicht installierbar. Mit
`clubplatform-sign manifests VERTRAUTES_MODULVERZEICHNIS manifests.json` lassen sich
Herstellermodule prüfen und ihre Manifeste ausgeben. Dieses Herstellerkommando lädt
nativen Code; nur eigene/vertraute Buildartefakte verwenden.

1. Das native Modul pro Zielplattform bauen: `windows`, `macos`, `linux`,
   Architektur `x64` bzw. `arm64`.
2. SHA-256 der unveränderten Bibliothek ermitteln, Manifest und Metadaten ergänzen.
3. Deskriptor signieren:
   `clubplatform-sign sign package CATALOG_SECRET descriptor.json package.json`.
4. Signierte Deskriptoren in `packages` einfügen.
5. Katalog signieren:
   `clubplatform-sign sign catalog CATALOG_SECRET catalog-payload.json catalog.json`.

Pakete sind in diesem Stand **einzelne native Bibliotheken**, keine ZIP-Archive.
Dies vermeidet Archivpfad-/Symlink-Extraktion. Fremde zusätzliche Laufzeitbibliotheken
müssen mit dem Grundprodukt bereitgestellt oder statisch eingebunden werden.
Downloads verwenden HTTPS mit Zertifikatsprüfung, keine Weiterleitungen, maximal
256 MiB je Paket und begrenzte Zeit. Für Offlineinstallation ist
`offline:DATEINAME` erlaubt, ausschließlich aus dem konfigurierten Offlineverzeichnis.
Relative Unterverzeichnisse und ein Verlassen dieses Verzeichnisses werden abgelehnt.

## Ablauf und Fehlerverhalten

1. Sitzung und `schema.manage` prüfen; Lizenzrevision lesen.
2. Lizenz und Katalog prüfen; Versionen, Plattform, Wartung und Abhängigkeiten lösen.
   Gemeinsame Versionsbedingungen werden mit begrenzter Rückwärtssuche gelöst;
   Zyklen, fehlende Entitlements und widersprüchliche Bereiche werden abgelehnt.
3. Dateien in eine neue Generation laden; Hash und signierte Deskriptoren prüfen.
4. Native ABI und eingebettete Manifeste gegen den Katalog prüfen.
5. Sitzung, Rechte und Lizenzrevision erneut prüfen.
6. Migrationen und aktiven Generationsverweis in **einer DB-Transaktion** speichern.
7. Anwendung/Server neu starten. Alte native Bibliotheken werden im laufenden Host
   nicht durch neue ersetzt; schemaabhängige Operationen können bis dahin gesperrt sein.

Downloads halten die Datenbank nicht gesperrt. Parallel geänderte Lizenzen und
Installationen führen zu einem Revisionskonflikt. Bei kontrollierten Fehlern vor
Commit bleibt der aktive Verweis unverändert; die unvollständige Generation wird
entfernt. Native Lifecycle-Hooks dürfen keine nichttransaktionalen externen
Seiteneffekte ausführen. Ein Prozessabbruch kann eine unreferenzierte Generation
hinterlassen. Alte Binärdateien allein sind nach einer DB-Migration kein vollständiges
Rollback: dafür Datenbanksicherung und dazugehörigen Modulstand gemeinsam wiederherstellen.

Ein Lizenzimport wird unabhängig von der anschließenden Provisionierung gespeichert.
Scheitert ein Download, bleibt die neue Lizenz gültig und die Paketinstallation kann
wiederholt werden. Dadurch wird kein erfolgreich importiertes Entitlement verworfen.

## Unbeaufsichtigter Server-/Installerweg

Nach Installation des Grundprodukts und Konfiguration der Umgebungsvariablen:

```sh
clubplatform-server --sqlite /daten/club.sqlite --init admin
clubplatform-server --sqlite /daten/club.sqlite --operator admin \
  --license license.json --catalog catalog.json
```

Das Passwort wird verdeckt abgefragt; für Automatisierung steht `--password-stdin`
zur Verfügung. Anschließend den normalen Server starten. Bei einer laufenden
Installation denselben Ablauf über die angemeldete Administrationsoberfläche
verwenden. Vorprüfung einer bereits importierten Lizenz ohne Paketinstallation:

```sh
clubplatform-server --sqlite /daten/club.sqlite --operator admin \
  --catalog catalog.json --plan
```

`--plan` importiert keine Lizenz und schreibt keine Pakete. Sitzungs-/Auditverwaltung
kann wie bei anderen authentifizierten Leseoperationen trotzdem DB-Schreibzugriffe auslösen.

## API und Prüfungen

* `GET /api/v1/license`: Status, Edition, Limits, Entitlements, Revision und Neustartbedarf.
* `POST /api/v1/license`: `{ "envelope": "...", "revision": "2" }`.
* `POST /api/v1/modules/provision`: `{ "catalog": "...", "apply": false, "revision": "3" }`.
  `apply:true` führt dieselbe geprüfte Planung aus und installiert sie.

Revisionen werden in den Request-Bodies wie andere Core-Revisionswerte als
Dezimalzeichenketten gesendet. Alle drei Endpunkte benötigen eine Sitzung und
`schema.manage`. Authentifizierung/Rechte: 401/403, ungültige Eingabe: 400,
Revisionskonflikt: 409. Schreibantworten niemals nach einem Transportabbruch blind
wiederholen; erst Lizenzstatus und Revision neu lesen.

Tests decken echte signierte Lizenzen und native Pakete ab: ungültige Signatur,
Ablauf, fehlende Rechte, Benutzeranlage/Reaktivierung über beide API-Wege,
Entitlemententzug ohne Datenverlust, Wartungsgrenze, Plattformabweichung,
Hashfehler, Abhängigkeiten, falsche Manifeste, Neustart und manipulierte Generationen.
SQLite läuft lokal; PostgreSQL sowie Windows/macOS und Qt-Desktop bleiben zusätzlich
an die bestehende CI-/Zielplattformabnahme gebunden.
