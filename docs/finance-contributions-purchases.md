# Phasen 9–11: Finanzen, Beiträge und Käufe

Stand: 19.09.2026. Siehe auch [Währungen und Personenakten](currencies-and-dossiers.md). Schema 13 ergänzt den gemeinsamen Ledger und die nativen
ABI-V3-Module `finance`, `contributions` und `purchases`. Die Anwendungs- und
ABI-Kompatibilitätsversion bleibt 0.6.0; dies ist kein Release-Tag.

## Lokal auf dem Mac testen

Das bisherige persönliche Preset bleibt verwendbar:

```sh
cmake --preset user-macos-vscode-debug -DCLUBPLATFORM_BUILD_PUBLISHER_TOOLS=ON
cmake --build --preset user-macos-vscode-debug --parallel
ctest --test-dir build/user-macos-vscode-debug --output-on-failure
```

Der Build erzeugt `runtime-extensions` mit Kampfsport und den drei neuen Modulen.
Die getrennten Verzeichnisse `extensions` und `financial-extensions` dienen
weiterhin den isolierten Modultests. Installationspakete enthalten alle Module
im regulären Verzeichnis `extensions`.

Eine gültige Lizenz muss **alle drei** IDs enthalten:
`["finance","contributions","purchases"]`; für Kampfsport zusätzlich `"martial"`.
Lizenzdatei importieren und die Module im Erweiterungsmanager installieren.
Herstellerschlüssel, Signieren und Kataloge sind unter
[Lizenzierung und Provisionierung](licensing-provisioning.md) beschrieben.
Für einen getrennten Entwicklertest kann das vorhandene Signierwerkzeug einen
eigenen Test-Vertrauensanker erzeugen:

```sh
mkdir -p build/finance-demo
build/user-macos-vscode-debug/tools/distribution/clubplatform-sign keygen build/finance-demo/keys
python3 - <<'PY'
import json, time
from pathlib import Path
now = int(time.time())
payload = dict(license_id="local-finance-demo", edition="development",
               not_before=now-60, expires_at=now+30*86400,
               maintenance_until=now+30*86400, max_users=10,
               modules=["martial", "finance", "contributions", "purchases"])
Path("build/finance-demo/payload.json").write_text(json.dumps(payload))
PY
build/user-macos-vscode-debug/tools/distribution/clubplatform-sign sign license-legacy \
  build/finance-demo/keys/secret.hex build/finance-demo/payload.json build/finance-demo/license.json
export CLUBPLATFORM_LICENSE_PUBLIC_KEY="$(cat build/finance-demo/keys/public.hex)"
export CLUBPLATFORM_INITIAL_LICENSE="$PWD/build/finance-demo/license.json"
build/user-macos-vscode-debug/apps/desktop/clubplatform-desktop.app/Contents/MacOS/clubplatform-desktop \
  --database "$PWD/build/finance-demo/demo.sqlite" \
  --extensions "$PWD/build/user-macos-vscode-debug/runtime-extensions"
```

Das Signierwerkzeug überschreibt vorhandene Schlüssel oder Lizenzdateien nicht.
Bei späteren Starts nur die beiden Umgebungsvariablen und den Startbefehl wiederholen.
Eine bereits provisionierte, signierte Modulgeneration hat Vorrang vor
`--extensions`; die separate Demo-Datenbank vermeidet eine Vermischung damit.
Die Demo-Schlüssel gehören ausschließlich zu dieser Testinstallation.

## Bedienung

1. Administrator einrichten, die lizenzierten Erweiterungen installieren und eine
   Person sowie Organisation anlegen. Für Beiträge außerdem eine aktive
   Mitgliedschaft mit passendem Gültigkeitszeitraum anlegen.
2. **Finanzen, Beiträge und Käufe** öffnen, **Neu laden** wählen und **Konto
   anlegen** ausführen. Kontoinhaber und Organisation werden über Listen ausgewählt.
3. Neu laden, Konto auswählen und **Suchen** wählen. Dies lädt den Saldo und die
   Buchungen sowie die Auswahl für Zahlungszuordnungen, Mahnungen und Stornos.
4. Beträge in der Währung des Kontos eingeben: `12,50` oder `12.50` entspricht 12,50 EUR. Buchung bestätigen.
   Nach Änderungen das Konto erneut laden. Positive Salden sind Forderungen,
   negative Salden Guthaben. Der Saldo umfasst Beiträge, Käufe und Zahlungen.
5. **Beitragsplan anlegen**: Betrag, Gültigkeit, Monatsintervall 1/3/6/12 und
   Fälligkeitstag 1–31. **Beitrag zuweisen** verbindet Mitgliedschaft, Plan und Konto.
   Optionaler individueller Betrag ersetzt den Planbetrag; danach wirkt der Rabatt
   in Basispunkten (`5000` = 50 %). **Beiträge abrechnen** bucht bis zum Stichtag.
6. **Mahnstufe erfassen** dokumentiert eine fällige, offene Beitragsforderung,
   eine neue Zahlungsfrist und gegebenenfalls eine Gebühr. Die erste Stufe kann
   als gebührenfreie Zahlungserinnerung verwendet werden. Es wird keine Nachricht
   automatisch versandt.
7. **Produkt anlegen**, anschließend neu laden. **Kauf buchen** unterstützt bis
   zu 100 Positionen mit ganzzahliger Menge. **Rückgabe buchen** schreibt die
   ausgewählte Position zum historischen Preis gut. **Produkt ändern** lädt beim
   Auswählen die aktuelle Revision und Werte.
8. **Zahlung zuordnen** gleicht eine Forderung ganz oder teilweise aus.
   **Buchung stornieren** erzeugt eine Gegenbuchung; gebuchte Historie bleibt erhalten.

Desktop lokal, Remote-Desktop und Portal verwenden dieselbe Fachlogik.
Im Portal öffnet der gleichnamige Button den Finanzbereich.
Alle neuen Formulartexte stehen in Deutsch, Englisch, Französisch, Italienisch,
Spanisch, Koreanisch und Türkisch bereit.

## Fachliche Regeln

* Ein Konto je Inhaber, Organisation und Währung. Die Organisation definiert die Währung
  im Finanzmodul; bestehende Konten sperren einen Wechsel. Intern und über REST bleiben
  Geldwerte Ganzzahlen bis 1.000.000.000.000 kleinsten Währungseinheiten als Zeichenketten.
  Die Oberfläche übernimmt die exakte Dezimalumrechnung. Keine Wechselkursumrechnung.
* Jeder Schreibauftrag benötigt eine stabile `source_id`. Gleiche Modul-ID,
  Source-ID und Nutzdaten liefern das ursprüngliche Ergebnis. Abweichende Nutzdaten
  liefern Konflikt. Die Oberflächen behalten den Schlüssel bei unverändertem
  Formular nach einem Transportfehler; nach Erfolg wird das Formular zurückgesetzt.
  Bei Bankimporten später die stabile Importzeilen-ID als Source-ID verwenden:
  `external_reference` allein erzwingt noch keine Dublettenprüfung.
* Zuordnungen überschreiten weder verfügbaren Zahlungsbetrag noch offene
  Forderung und verbinden nur dasselbe Konto. Storno und Rückgabe lösen betroffene
  Zuordnungen durch Gegenbelege auf; Zahlungen sind danach erneut zuzuordnen.
* Beitragspläne sind unveränderliche Versionen. Ein Wechsel erfolgt durch
  Beenden der alten Zuweisung und eine neue, nicht überlappende Zuweisung.
  Bereits abgerechnete Zeiträume verhindern ein rückwirkendes Verkürzen.
* Die erste Beitragsperiode beginnt am Zuweisungsbeginn; weitere Perioden beginnen
  am ersten Tag des jeweiligen Intervallmonats. Keine taggenaue anteilige Berechnung.
  Gültigkeitsgrenzen sind einschließlich. Ein Fälligkeitstag 31 wird im Februar
  auf dessen letzten Tag begrenzt. Rabatt wird pro Beitrag einmal kaufmännisch
  auf die kleinste Einheit der Kontowährung gerundet. Nullbeiträge erzeugen keine Forderung.
* Abrechnung prüft erneut Mitgliedschaftsstatus, Archivierung und Zeitraum.
  Wiederholte Abrechnung erzeugt auch mit neuer Source-ID keine zweite Forderung
  für dieselbe Zuweisung und Periode. Höchstens 1200 Perioden pro Durchlauf.
* Mahnstufen steigen von 1 bis 10; eine weitere Stufe setzt den Ablauf der letzten
  Zahlungsfrist voraus. Gebühr und Mahnbeleg entstehen atomar.
* Kaufpositionen speichern Bezeichnung und Preis. Produktänderungen beeinflussen
  alte Käufe nicht. Rückgaben überschreiten die gekaufte Restmenge nicht.
  Vollstorno nach Teilrückgabe ist gesperrt; die restliche Menge kann zurückgegeben
  werden. Stornos von Stornos sowie direkte Stornos von Rückgaben sind gesperrt.
* Finanzdaten, Source-Quittung und Audit werden gemeinsam bestätigt oder vollständig
  zurückgerollt. Schreibaufträge werden über eine Datenbanksperre serialisiert.

## Rechte, Datenbank und API

`finance.read` erlaubt Kontoübersicht und Ledger, `finance.write` Buchungen.
Beiträge benötigen zusätzlich `contributions.write`, Käufe `purchases.write`.
Optionale Auswahldaten benötigen das jeweilige Leserecht und eine betriebsbereite
lizenzierte Erweiterung. Die Rechte gelten unabhängig von der Modullizenz.
Kontoinhaber-Auswahldaten gehören zur Finanzleseberechtigung.

Schema 13 wird durch die vorhandene Migration angewandt. Bestehende Migrationen
werden nicht verändert. Fremdschlüssel erhalten die Beziehungen zu Personen,
Organisationen und Mitgliedschaften. Daten vor einem Update sichern; keine
Downgrade-Migration auf Schema 12 vorhanden.

* `GET /api/v1/finance/accounts/`: Auswahldaten.
* `GET /api/v1/finance/accounts/{id}`: gemeinsamer Saldo und Buchungen.
* `POST /api/v1/finance/commands/{operation}`: atomarer Fachauftrag.

Der [OpenAPI-Vertrag](api/finance.openapi.json) beschreibt alle 14 Vorgänge.
Auswahllisten sind derzeit auf 1000 Datensätze begrenzt; die Kontoansicht liefert
die gesamte Buchungshistorie. Suche und Pagination für große Finanzbestände sind
noch auszubauen. Steuerberechnung, Rechnungsdruck, Bankimport und automatischer
Mahnversand gehören nicht zu diesem Stand.

## Verifikation und verbleibende Abnahme

Die gemeinsame Foundation-Suite prüft Beiträge, Rabatt/Schaltjahr, Mahnfristen,
Zahlungszuordnung, Rückgaben zum historischen Preis, Storno, Lizenzentzug,
Rechte und Audit-Rollback. Sie läuft in der CI gegen SQLite und PostgreSQL.
Der neue HTTP-Test prüft zusätzlich konkurrierende Wiederholung desselben Auftrags.
Der Portaltest bedient Kontoanlage und Zahlung gegen einen echten Host mit eigens
signierter Testlizenz. Sprachprüfungen prüfen Schlüssel, Platzhalter und die
Formulardefinitionen; die Screenshot-Texte sind als Regression abgesichert.

Lokal sind nativer Build, SQLite-/HTTP-Tests, Sprachprüfung und Portal-Build prüfbar.
Chromium startet in der Work-Umgebung wegen einer Socket-Beschränkung nicht;
Qt/macOS und PostgreSQL müssen im CI-Lauf bzw. auf den Zielsystemen abgenommen
werden. Die vollständige Migration aller älteren UI-Texte bleibt ein offener
I18n-Abnahmepunkt; ergänzt sind insbesondere Personenübersicht, Suchhinweise,
Auswahllisten, Verwaltungsbuttons und die neuen Finanzformulare.
