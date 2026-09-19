# Lizenz mit allen verfügbaren Modulen erstellen

Diese Anleitung richtet sich an den Herausgeber. Die Befehle laufen im privaten
`club-platform`-Code-Repository auf macOS. Eine produktive Lizenz benötigt einen
eigenen erreichbaren HTTPS-Aktivierungsdienst; eine Beispieldomain reicht nicht.
Bereits verwendete Herausgeberschlüssel weiterverwenden, damit vorhandene
Kundenpakete neue Lizenzen prüfen können.

## 1. Signierwerkzeug bauen

```bash
cmake --preset user-macos-vscode-debug -DCLUBPLATFORM_BUILD_PUBLISHER_TOOLS=ON
cmake --build --preset user-macos-vscode-debug --parallel
```

Das Werkzeug liegt unter
`build/user-macos-vscode-debug/tools/distribution/clubplatform-sign`.

## 2. Schlüssel sicher bereitstellen

Nur bei einer **neuen Herausgeberinstallation** zwei Schlüsselpaare erzeugen.
Die Zielverzeichnisse dürfen noch nicht existieren. Private Schlüssel außerhalb
des Repositories verwahren und sichern:

```bash
umask 077
mkdir -p "$HOME/club-license-issuer"
build/user-macos-vscode-debug/tools/distribution/clubplatform-sign keygen \
  "$HOME/club-license-issuer/issuer"
build/user-macos-vscode-debug/tools/distribution/clubplatform-sign keygen \
  "$HOME/club-license-issuer/activation"
```

Je Verzeichnis entstehen `public.hex` und `secret.hex`. Den privaten
Aktivierungsschlüssel ausschließlich zum Aktivierungsdienst übertragen. Der
private Herausgeberschlüssel kann auf dem Herausgeberrechner bleiben.

## 3. Aktivierungsdienst einrichten

Die [Betreiberanleitung](../../tools/activation/README.md) beschreibt WSGI,
Datenbank, Dienstbenutzer und HTTPS-Proxy. Der Dienst braucht den öffentlichen
Herausgeberschlüssel sowie den privaten Aktivierungsschlüssel. Die tatsächlich
erreichbare URL endet beispielsweise auf `/v1/activation`.

## 4. Payload mit allen Modul-IDs erstellen

Die aktuell mitgelieferten IDs lauten:

| ID | Modul |
|---|---|
| martial | Kampfsport einschließlich Sportlerlizenzen |
| finance | Finanzkonten, Währungen und Buchungen |
| contributions | Beiträge |
| purchases | Käufe |
| calendar | Kalender |
| events | Veranstaltungen |
| banking | Bankkonten, CSV/CAMT-Import und Zahlungszuordnung |

Core und Sprachpakete benötigen keine zusätzliche Modul-ID. Eine Modullizenz
ersetzt weder Benutzerrechte noch die Installation der passenden Moduldatei.

Dieses Beispiel erzeugt **ein Jahr Laufzeit, ein Jahr Wartung und 20 Benutzer**.
Kundenkennung und Grenzen vor der Signatur anpassen. Für eine geänderte Lizenz
dieselbe Kunden-Lizenz-ID behalten und die neue signierte Fassung erneut beim
Dienst registrieren.

```bash
python3 - <<'PY'
import json, time
from pathlib import Path
now = int(time.time())
payload = {
    "license_id": "kunde-0001-alle-module",
    "edition": "all-modules",
    "not_before": now - 300,
    "expires_at": now + 365 * 86400,
    "maintenance_until": now + 365 * 86400,
    "max_users": 20,
    "modules": ["martial", "finance", "contributions", "purchases",
                "calendar", "events", "banking"]
}
path = Path.home() / "club-license-issuer" / "kunde-0001-payload.json"
with path.open("x", encoding="utf-8") as output:
    json.dump(payload, output, indent=2)
PY
```

Die Datei ist noch keine nutzbare Lizenz. Das Beispiel überschreibt keine
vorhandene Payload; vorhandene Dateien gezielt bearbeiten oder einen neuen
Ausgabename für eine neue Fassung verwenden.

## 5. Aktivierungsrichtlinie ergänzen und signieren

`DEINE-DOMAIN` durch den echten Dienst ersetzen:

```bash
export CLUBPLATFORM_ACTIVATION_URL="https://DEINE-DOMAIN/v1/activation"
export CLUBPLATFORM_ACTIVATION_PUBLIC_KEY="$(cat "$HOME/club-license-issuer/activation/public.hex")"
build/user-macos-vscode-debug/tools/distribution/clubplatform-sign sign license \
  "$HOME/club-license-issuer/issuer/secret.hex" \
  "$HOME/club-license-issuer/kunde-0001-payload.json" \
  "$HOME/club-license-issuer/kunde-0001-license.json"
```

Ohne explizites `activation`-Objekt ergänzt das Werkzeug eine Installation,
30 Tage Offline-Lease und `allow_offline: false`. Andere Grenzen gehören als
`activation`-Objekt **vor dem Signieren** in die Payload; siehe Betreiberanleitung.
Die fertige signierte Datei nicht nachträglich bearbeiten.

## 6. Lizenz beim Dienst registrieren

Die signierte Datei auf den Aktivierungsserver übertragen. Dort im privaten
Code-Repository mit den tatsächlichen Dienstpfaden ausführen:

```bash
.venv/bin/python tools/activation/service.py \
  --database /var/lib/club-activation/authority.sqlite \
  --secret /etc/club-activation/activation-secret.hex \
  --license-public-key /etc/club-activation/issuer-public.hex \
  register /sicher/kunde-0001-license.json
```

Die Datenbank und Schlüssel müssen dieselben sein, die der laufende Dienst
verwendet. Erst nach erfolgreicher Registrierung die Lizenz ausliefern.

## 7. Öffentlichen Herausgeberschlüssel im Kundenbuild festlegen

```bash
cmake --preset user-macos-vscode-debug \
  -DCLUBPLATFORM_PINNED_LICENSE_KEY="$(cat "$HOME/club-license-issuer/issuer/public.hex")"
cmake --build --preset user-macos-vscode-debug --parallel
```

Für Releasepakete die gleiche Option im Releaseprofil bzw. die Repository-Variable
`CLUBPLATFORM_PINNED_LICENSE_KEY` in Actions setzen. Das Debug-Preset hier dient dem
lokalen Funktionstest und ersetzt keine Release-Abnahme.

## 8. Importieren und prüfen

1. Die neu gebaute Anwendung starten. Ein macOS-App-Bundle mit `open` starten,
   beispielsweise `open build/user-macos-vscode-debug/apps/desktop/clubplatform-desktop.app`.
2. Unter **Erweiterungen** bzw. **Einstellungen → Lizenz und Module**
   `kunde-0001-license.json` importieren.
3. **Installation aktivieren** ausführen. Das Portal aktiviert die Serverinstallation.
4. Module aus dem signierten Katalog installieren oder die lokal gebauten Module
   installieren/aktualisieren. Für lokale Server alle Module aus
   `build/user-macos-vscode-debug/runtime-extensions` laden.
5. Bei jeder Modulzeile prüfen: lizenziert, installiert, aktiv und betriebsbereit.
6. Mit einem passend berechtigten Benutzer Kalender, Finanzen und Banking öffnen.

An Kunden gehen ausschließlich signierte Lizenz-/Paketdateien und öffentliche
Schlüssel, niemals `secret.hex`. Vor einem Rechnerwechsel die Installation
freigeben; Verfahren für verlorene Rechner siehe Betreiberanleitung.
