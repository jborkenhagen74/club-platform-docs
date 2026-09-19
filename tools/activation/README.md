# Installationsgebundene Lizenzen

Der Aktivierungsdienst gehört zum Herausgeber, nicht auf Kundenrechner. Die
Lizenzprüfung im Kundenprogramm arbeitet mit Schema 17. Der Dienst wird separat
bereitgestellt; dieses Repository richtet keinen öffentlichen Server automatisch ein.

## 1. Zwei Schlüsselpaare verwenden

Den vorhandenen Lizenz-Herausgeberschlüssel behalten. Ein zusätzliches Schlüsselpaar
signiert ausschließlich Aktivierungen:

```sh
build/user-macos-vscode-debug/tools/distribution/clubplatform-sign keygen activation-keys
```

`activation-keys/secret.hex` liegt ausschließlich auf dem Aktivierungsserver.
Der private Lizenz-Herausgeberschlüssel bleibt beim Herausgeber und muss nicht auf
diesen Server. Kundenpakete enthalten keine privaten Herausgeberschlüssel.

## 2. Dienst bereitstellen

Auf einem eigenen Linux-Server einen dedizierten Benutzer und ein privates
Datenverzeichnis einrichten. Im ausgecheckten Repository:

```sh
python3 -m venv .venv
.venv/bin/pip install -r tools/activation/requirements.txt
```

Folgende Variablen im Dienstmanager setzen (Beispielpfade anpassen):

```sh
export CLUB_ACTIVATION_DATABASE=/var/lib/club-activation/authority.sqlite
export CLUB_ACTIVATION_SECRET=/etc/club-activation/activation-secret.hex
export CLUB_LICENSE_PUBLIC_KEY="$(cat issuer-keys/public.hex)"
umask 077
.venv/bin/gunicorn --chdir tools/activation --bind 127.0.0.1:8091 \
  --workers 2 --timeout 30 service:application
```

Davor einen HTTPS-Reverse-Proxy mit gültigem Zertifikat betreiben. Nur
`POST /v1/activation` weiterleiten; Request-Body auf 128 KiB begrenzen und
Rate-Limits konfigurieren. Der Dienst darf nicht direkt öffentlich auf Port 8091
lauschen. Das private Datenverzeichnis einschließlich Datenbank muss nur dem
Dienstkonto zugänglich sein. Keine Request-Bodies protokollieren.

Die öffentliche URL, beispielsweise `https://DEINE-DOMAIN/v1/activation`, wird
in die Lizenz signiert. Kunden benötigen für Aktivierung und Erneuerung Zugang
zu dieser URL. Weiterleitungen und unverschlüsseltes HTTP werden abgewiesen.

## 3. Geschützte Lizenz erstellen und registrieren

Die vorhandene Lizenz-Payload enthält weiterhin `license_id`, `edition`,
`not_before`, `expires_at`, `maintenance_until`, `max_users` und `modules`.

```sh
export CLUBPLATFORM_ACTIVATION_URL=https://DEINE-DOMAIN/v1/activation
export CLUBPLATFORM_ACTIVATION_PUBLIC_KEY="$(cat activation-keys/public.hex)"
build/user-macos-vscode-debug/tools/distribution/clubplatform-sign sign license \
  issuer-keys/secret.hex license-payload.json customer-license.json
```

Das Signierwerkzeug ergänzt standardmäßig eine erlaubte Installation, 30 Tage
Offline-Gültigkeit und `allow_offline: false`. Alternativ diese Einstellungen
explizit als `activation`-Objekt in der Payload angeben:

```json
{
  "url": "https://DEINE-DOMAIN/v1/activation",
  "public_key": "64_HEX_ZEICHEN_DES_AKTIVIERUNGSSCHLUESSELS",
  "max_installations": 1,
  "offline_days": 30,
  "allow_offline": false
}
```

Die Beispielobjekte und Platzhalter sind keine direkt nutzbare Lizenz. Die
Offline-Frist ist auf 1–90 Tage begrenzt. Eine neue Version derselben Lizenz-ID
muss erneut registriert werden; alte Payloads werden danach vom Dienst abgewiesen.

```sh
.venv/bin/python tools/activation/service.py \
  --database /var/lib/club-activation/authority.sqlite \
  --secret /etc/club-activation/activation-secret.hex \
  --license-public-key issuer-keys/public.hex register customer-license.json
```

Erst danach die Lizenzdatei an den Kunden geben. Die Lizenz selbst wird nicht
dauerhaft auf dem Aktivierungsserver gespeichert; dort liegen Lizenz-ID,
Payload-Hash, Installationsschlüssel, Status, Sequenz und Ablaufdaten sowie
kurzlebige Antwort-Caches. Keine Vereins- oder Personendaten werden übertragen.

## 4. Kundenpakete mit festem Vertrauensanker bauen

**Für Kundenauslieferungen zwingend den öffentlichen Lizenz-Herausgeberschlüssel
fest einbauen:**

```sh
cmake --preset user-macos-vscode-debug \
  -DCLUBPLATFORM_PINNED_LICENSE_KEY="$(cat issuer-keys/public.hex)"
cmake --build --preset user-macos-vscode-debug --parallel
```

Für GitHub Actions die Repository-Variable `CLUBPLATFORM_PINNED_LICENSE_KEY`
mit diesem öffentlichen Schlüssel setzen. Veröffentlichungen von `main` und
`release/*` brechen ohne diese Variable vor der Paketierung ab. PR-Prüfungen
und Develop-Snapshots verwenden weiterhin den Entwicklungsmodus.

Für manuelle Release-Pakete dieselbe CMake-Option im jeweiligen Release-Preset bzw.
CI-Build setzen. Der öffentliche Schlüssel ist kein Geheimnis. Bei gesetzter
Option ignoriert der Host den Umgebungswert `CLUBPLATFORM_LICENSE_PUBLIC_KEY`
und akzeptiert keine ungebundenen Alt-Lizenzen mehr.

Ohne gesetzten Schlüssel ist dies ausdrücklich ein Entwicklungsbuild mit
konfigurierbarem Vertrauensanker und Kompatibilität zu alten Testlizenzen.
`sign license-legacy` ist nur für isolierte Kompatibilitätstests vorgesehen.
Alte Produktionslizenzen müssen vor dem Wechsel auf geschützte Pakete neu
mit Aktivierungsrichtlinie ausgestellt und registriert werden.

## 5. Aktivieren und Rechner wechseln

Desktop: **Erweiterungen**, Portal: **Einstellungen → Lizenz und Module**.

1. Lizenzdatei importieren.
2. **Installation aktivieren** wählen. Die lokalen Fachmodule werden erst nach
   erfolgreicher Aktivierung freigeschaltet.
3. Der Host prüft stündlich, ob eine Erneuerung fällig ist, und erneuert normalerweise
   nach einem Tag, bei kurzen Leases bereits nach der halben Laufzeit. Er muss dafür laufen. Netzwerkausfälle verwerfen keine noch
   gültige Aktivierung. Nach Fristablauf bleiben die Daten erhalten, lizenzierte
   Module sind bis zur erfolgreichen Erneuerung gesperrt.
4. Vor einem Rechnerwechsel **Installation freigeben** bestätigen. Danach ist
   diese Installation lokal gesperrt und ein Platz beim Dienst frei.
5. Auf dem neuen Rechner die Lizenz importieren und aktivieren.

Bei defektem oder verlorenem Rechner kann der Herausgeber einen Platz freigeben:
mit denselben drei Verwaltungsparametern wie oben `list`, dann
`release LIZENZ_ID INSTALLATIONS_PUBLIC_KEY`. `revoke LIZENZ_ID` sperrt die Lizenz.
Verwaltungsbefehle sind ausschließlich lokal am Dienst verfügbar, nicht als
öffentliche HTTP-API. Eine freigegebene Identität kann sich nicht selbst erneut
aktivieren; für die nächste Installation entsteht eine neue Identität in einer
neuen Datenbank. Bei Datenbankübernahme auf einen anderen Rechner wird ein neuer lokaler Schlüssel
erzeugt; die bisherige Aktivierungsdatei ist dort ungültig. Erst nach Freigabe des
alten Platzes und erneuter Aktivierung ist der neue Host freigeschaltet.

## 6. Dauerhaft offline

Nur für ausdrücklich mit `allow_offline: true` ausgestellte Lizenzen:

1. Auf dem Kundenhost **Offline-Anfrage exportieren**.
2. Anfrage zum Herausgeber übertragen.
3. Herausgeber führt mit den Verwaltungsparametern aus:
   `offline activation-request.json activation.json`.
4. Kunde importiert `activation.json` über **Aktivierungsdatei importieren**.

Die Antwort bleibt an den Installationsschlüssel gebunden und gilt höchstens bis
zum Ablauf der Lizenz. Die Offline-Aktivierung belegt einen regulären Platz.
Sie lässt sich aus der Ferne nicht sofort sperren. Freigaben beim Herausgeber
können eine bereits ausgegebene, vollständig offline verwendete Datei nicht
rückwirkend ungültig machen.

## Speicherung und Grenzen

- macOS: nicht synchronisierter, gerätegebundener Schlüsselbund-Eintrag.
- Windows: mit DPAPI geschützte Schlüsseldatei im Benutzerprofil.
- Linux: Schlüsseldatei mit Modus 0600 in einem Verzeichnis mit Modus 0700.
  Diese Variante ist kein TPM-/Hardware-Schutz; wer auch Schlüssel und Zustand
  kopieren kann, kann eine Installation klonen.
- Standardverzeichnis außerhalb der Datenbank: unter Windows
  `%LOCALAPPDATA%/clubplatform/identities`, sonst
  `$XDG_STATE_HOME/clubplatform/identities` oder
  `$HOME/.local/state/clubplatform/identities`. Für Servicekonten kann der Betreiber
  `CLUBPLATFORM_IDENTITY_DIRECTORY` auf ein privates, persistentes Verzeichnis setzen.
  Unter macOS wird das Schlüsselmaterial ausschließlich im Schlüsselbund abgelegt.
- Ein kopiertes Datenbank-Backup enthält keinen privaten Installationsschlüssel.
  Am anderen Rechner ist eine erneute Aktivierung erforderlich. Der Slot darf
  nach Freigabe nur kontrolliert zurückgesetzt werden; Datenbank und Schlüssel
  niemals bei einem bloßen Verbindungsfehler automatisch ersetzen.
- Sequenznummern sperren ältere importierte Aktivierungsdateien nach Freigabe.
  Ein Zeitstempel erkennt deutliche Rückstellungen der Uhr. Ein vollständiges
  Zurücksetzen von Datenbank, Betriebssystemzustand und Uhr ist damit nicht
  manipulationssicher verhindert. Sperrungen greifen bei erreichbaren Hosts nach
  Erneuerung, ansonsten spätestens nach Ablauf des gültigen Lease – sofern die
  lokale Prüfung nicht manipuliert wurde.
- Der Dienst begrenzt registrierte Installationen, nicht Kopien eines vollständig
  geklonten Hosts. Gegen absichtlich modifizierte Programme gibt es keinen
  absoluten Schutz.

API: `POST /api/v1/license/activation/{activate|renew|deactivate|request|import}`,
mit authentifizierter Sitzung und `schema.manage`. Import akzeptiert
`{"envelope":"SIGNIERTE_JSON_DATEI"}`, andere Aktionen `{}`. Die exportierte
Anfrage enthält den öffentlichen Installationsschlüssel, Lizenz und Besitznachweis.
Private Schlüssel werden nie über diese API übertragen. Bei Remote-Desktop oder
Portal entsteht die Identität auf dem Server, nicht auf jedem Client.

Technische Referenzen:
[Apple Keychain](https://developer.apple.com/documentation/security/secitemcopymatching(_:_:)),
[Microsoft DPAPI](https://learn.microsoft.com/en-us/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata).
