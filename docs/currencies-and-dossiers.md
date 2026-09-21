# Währungen und Modulansichten in Personenakten

Stand: 19.09.2026, Datenbankschema 16. Finance und Calendar tragen Version 1.1.0.

## Bauen und ausprobieren

1. Den aktuellen Stand von `feature/calendar-events` abrufen und wie bisher bauen:
   `cmake --build --preset user-macos-vscode-debug --parallel`.
2. Desktop starten: `open build/user-macos-vscode-debug/apps/desktop/clubplatform-desktop.app`.
3. Unter **Erweiterungen** Finance und Calendar jeweils **Installieren / aktualisieren**.
   Die Module müssen lizenziert und aktiviert sein. Bei signierter Provisionierung
   die aktualisierten Pakete im Katalog bereitstellen; eine bestehende Generation
   hat Vorrang vor dem lokalen Modulverzeichnis.
4. Eine neue Organisation öffnen. Unter **Währung der Organisation** die gewünschte
   Währung wählen und speichern. Ohne eigene Einstellung gilt EUR.
5. Im Finanzbereich ein Konto für eine Person und diese Organisation anlegen.
   Eine Zahlung mit `12,50` erfassen. Anschließend das Konto erneut laden.
6. Die Person öffnen und **Personenkonten** wählen: Organisation, Währung, Saldo und
   Buchungshistorie erscheinen hier ebenfalls. Ein fehlendes Konto wird ausdrücklich
   angezeigt; die Ansicht legt kein Konto automatisch an.
7. Einen Termin dieser Person zuweisen. In der Personenakte **Zugeordnete Termine**
   wählen. Der Zeitraum ist anpassbar, maximal 366 Tage pro Abfrage. Standardmäßig
   wird das kommende Jahr angezeigt; vergangene Termine sind über das Startdatum
   erreichbar. Auch Veranstaltungen mit Verantwortung/Teilnahme und die bereits
   vorhandenen Ablaufprojektionen von Sportlerlizenzen werden angezeigt, soweit
   die betreffenden Module und Rechte verfügbar sind.

## Zahlungsbetrag und Kontosaldo

Das Personenkonto ist ein Forderungskonto. Eine Forderung erhöht den offenen
Betrag, eine Zahlung senkt ihn. Beispiel: Forderung 50,00 EUR, Zahlung 20,00 EUR,
Restforderung 30,00 EUR. Deshalb bleibt die **Saldenwirkung** der Zahlung negativ.
Der **Betrag** selbst wird positiv angezeigt, daneben stehen Buchungsart und
Saldenwirkung. Ein negativer Gesamtsaldo bedeutet Guthaben. Vorhandene Buchungen
werden weder umgebucht noch in eine andere Währung umgerechnet.

## Eingabe und unterstützte Währungen

Komma oder Punkt als Dezimaltrenner, keine Tausendertrennzeichen. Ungültige
Nachkommastellen werden zurückgewiesen und nicht still gerundet. Das gilt für
Zahlungen, Forderungen, Zuordnungen, Beitragshöhen, Mahngebühren, Produktpreise
und Veranstaltungsgebühren. Mengen, Monate und Rabatt-Basispunkte bleiben Zahlen.

- Zwei Nachkommastellen: EUR, USD, GBP, CHF, PLN, CZK, DKK, NOK, SEK, HUF, CAD,
  AUD, NZD, INR, BRL, ZAR.
- Keine Nachkommastellen: JPY, KRW.
- Drei Nachkommastellen: KWD, BHD, TND.

Die Währung gilt einheitlich pro Organisation. Sobald ein Konto, Beitragsplan,
Produkt oder eine Veranstaltung existiert, ist der Währungswechsel gesperrt.
Organisationen mit unterschiedlicher Währung bleiben getrennt; es gibt keinen
zusammengerechneten Saldo über mehrere Währungen.

## Module, API und Rechte

Die Organisation erhält kein dauerhaftes Währungsfeld im Kernformular. Finance
liefert seine Ansichten über `dossier_views` im Modulmanifest. Calendar liefert
auf dieselbe Weise die Terminübersicht. Beide Oberflächen zeigen die Ansichten
nur bei betriebsbereiten Modulen; der Server prüft den Modulstatus erneut.

`GET /api/v1/module-dossiers/finance/organization/{id}` liest die Einstellung.
`POST /api/v1/finance/commands/organization.currency` speichert
`organization_id`, `currency`, `revision` (Zeichenkette) und `source_id`.
Lesen benötigt `records.read` und `finance.read`, Schreiben `finance.write`.

`GET /api/v1/module-dossiers/finance/person/{id}` liest die Personenkonten.
Neben `finance.read` muss die Person dem Benutzer zugeordnet sein, oder es gilt
`finance.read.all`, oder `finance.read.organization` mit einer aktuell gültigen
Funktionärszuordnung. Im letzten Fall erscheinen nur Konten der eigenen
Organisationen. Diese Einschränkung betrifft die neue Personenansicht; die
bestehende zentrale Finanzverwaltung behält ihre bisherige Rechteprüfung.

`GET /api/v1/module-dossiers/calendar/person/{id}?from=...&until=...` verwendet
UTC-Epochsekunden und die bestehenden personenbezogenen Kalenderrechte.

Die REST-Geldbeträge bleiben ganzzahlige Zeichenketten in kleinsten Einheiten:
`"1250"` bedeutet 12,50 EUR, 1250 JPY oder 1,250 KWD. Clients müssen anhand der
Kontowährung umrechnen. Schema 16 übernimmt bestehende Finanz- und Kalenderdaten
transaktional, einschließlich IDs, Buchungsbeträgen, Zuordnungen und Stornos.
