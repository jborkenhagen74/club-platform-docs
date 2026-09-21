# Formularatlas

Diese Referenz führt sämtliche Felder der verfügbaren Finanz- und Terminaktionen auf. Öffne den Bereich, wähle den Vorgang und fülle die Felder aus. Prüfe die Auswahl vor Speichern/Bestätigen und lade danach die Ansicht neu. Leere Auswahlmenüs werden durch vorher angelegte Stammdaten und Neu laden befüllt. Ein Screenshot zeigt das echte Formular mit Testdaten, nicht die Bestätigung einer fachlichen Buchung.

[Zum ausführlichen Handbuch](bedienung.md) · [Screenshots](../images/pilot/README.md)

## Finanzen

### Konto anlegen

`finance` · `account.create`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Kontoinhaber (Person oder Organisation) | Auswahlliste | Pflicht |
| Organisation | Auswahlliste | Pflicht |

![Konto anlegen (DE)](../images/pilot/desktop/finance-operation-00.png)

### Forderung buchen

`finance` · `receivable.create`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Konto | Auswahlliste | Pflicht |
| Betrag | Betrag in Organisationswährung | Pflicht |
| Buchungsdatum | Datum | Pflicht |
| Fällig am | Datum | Pflicht |
| Beschreibung / Buchungstext | Text | Pflicht |

![Forderung buchen (DE)](../images/pilot/desktop/finance-operation-01.png)

### Zahlung erfassen

`finance` · `payment.create`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Konto | Auswahlliste | Pflicht |
| Betrag | Betrag in Organisationswährung | Pflicht |
| Buchungsdatum | Datum | Pflicht |
| Beschreibung / Buchungstext | Text | Pflicht |
| Zahlungsreferenz | Text | Pflicht |

![Zahlung erfassen (DE)](../images/pilot/desktop/finance-operation-02.png)

### Zahlung zuordnen

`finance` · `allocation.create`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Zahlung | Auswahlliste | Pflicht |
| Forderung | Auswahlliste | Pflicht |
| Betrag | Betrag in Organisationswährung | Pflicht |

![Zahlung zuordnen (DE)](../images/pilot/desktop/finance-operation-03.png)

### Buchung stornieren

`finance` · `entry.reverse`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Buchung | Auswahlliste | Pflicht |
| Buchungsdatum | Datum | Pflicht |
| Beschreibung / Buchungstext | Text | Pflicht |

![Buchung stornieren (DE)](../images/pilot/desktop/finance-operation-04.png)

### Beitragsplan anlegen

`contributions` · `plan.create`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Organisation | Auswahlliste | Pflicht |
| Name | Text | Pflicht |
| Betrag | Betrag in Organisationswährung | Pflicht |
| Intervall (1, 3, 6 oder 12 Monate) | Ganzzahl | Pflicht |
| Gültig ab | Datum | Pflicht |
| Gültig bis | Datum | Pflicht |
| Fälligkeitstag im Monat (1–31) | Ganzzahl | Pflicht |

![Beitragsplan anlegen (DE)](../images/pilot/desktop/finance-operation-05.png)

### Beitrag zuweisen

`contributions` · `assignment.create`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Mitgliedschaften | Auswahlliste | Pflicht |
| Beitragsplan | Auswahlliste | Pflicht |
| Konto | Auswahlliste | Pflicht |
| Gültig ab | Datum | Pflicht |
| Gültig bis | Datum | Pflicht |
| Individueller Betrag | Betrag in Organisationswährung | Optional |
| Rabatt (100 = 1 %, 10000 = 100 %) | Ganzzahl | Pflicht |

![Beitrag zuweisen (DE)](../images/pilot/desktop/finance-operation-06.png)

### Beitragszuweisung beenden

`contributions` · `assignment.end`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Beitragszuweisung | Auswahlliste | Pflicht |
| Gültig bis | Datum | Pflicht |

![Beitragszuweisung beenden (DE)](../images/pilot/desktop/finance-operation-07.png)

### Beiträge abrechnen

`contributions` · `contributions.bill`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Beitragszuweisung | Auswahlliste | Pflicht |
| Abrechnen bis einschließlich | Datum | Pflicht |

![Beiträge abrechnen (DE)](../images/pilot/desktop/finance-operation-08.png)

### Mahnstufe erfassen

`contributions` · `reminder.create`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Forderung | Auswahlliste | Pflicht |
| Mahndatum | Datum | Pflicht |
| Zahlungsfrist | Datum | Pflicht |
| Gebühr | Betrag in Organisationswährung | Pflicht |
| Beschreibung / Buchungstext | Text | Pflicht |

![Mahnstufe erfassen (DE)](../images/pilot/desktop/finance-operation-09.png)

### Produkt anlegen

`purchases` · `product.create`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Organisation | Auswahlliste | Pflicht |
| Name | Text | Pflicht |
| Beschreibung / Buchungstext | Text | Pflicht |
| Preis | Betrag in Organisationswährung | Pflicht |

![Produkt anlegen (DE)](../images/pilot/desktop/finance-operation-10.png)

### Produkt ändern

`purchases` · `product.update`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Produkt | Auswahlliste | Pflicht |
| Produktrevision | Ganzzahl | Pflicht |
| Name | Text | Pflicht |
| Beschreibung / Buchungstext | Text | Pflicht |
| Preis | Betrag in Organisationswährung | Pflicht |
| Aktiv | Ja/Nein | Pflicht |

![Produkt ändern (DE)](../images/pilot/desktop/finance-operation-11.png)

### Kauf buchen

`purchases` · `purchase.post`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Konto | Auswahlliste | Pflicht |
| Buchungsdatum | Datum | Pflicht |
| Fällig am | Datum | Pflicht |
| Beschreibung / Buchungstext | Text | Pflicht |

Kaufpositionen: Produkt · Anzahl · Position hinzufügen / Position entfernen.

![Kauf buchen (DE)](../images/pilot/desktop/finance-operation-12.png)

### Rückgabe buchen

`purchases` · `purchase.return`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Kaufposition | Auswahlliste | Pflicht |
| Anzahl | Ganzzahl | Pflicht |
| Buchungsdatum | Datum | Pflicht |
| Beschreibung / Buchungstext | Text | Pflicht |

![Rückgabe buchen (DE)](../images/pilot/desktop/finance-operation-13.png)

## Kalender und Veranstaltungen

### Kalendereintrag anlegen

`calendar` · `create`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Titel | Text | Pflicht |
| Beschreibung / Buchungstext | Text | Pflicht |
| Ort | Text | Pflicht |
| Zugeordnete Person oder Organisation | Auswahlliste | Pflicht |
| Beginn | Datum und Uhrzeit | Pflicht |
| Ende | Datum und Uhrzeit | Pflicht |
| Zeitzone | Text | Pflicht |
| Ganztägig | Ja/Nein | Pflicht |
| Doppelte Uhrzeit bei Zeitumstellung | earlier, later | Pflicht |
| Wiederholung | none, DAILY, WEEKLY, MONTHLY | Pflicht |
| Abstand der Wiederholungen | Ganzzahl | Pflicht |
| Anzahl Termine (höchstens 366) | Ganzzahl | Pflicht |

### Kalendertermin absagen

`calendar` · `cancel`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Termin | Auswahlliste | Pflicht |

### Erinnerung einrichten

`calendar` · `remind`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Termin | Auswahlliste | Pflicht |
| Erinnerung: Minuten vorher | Ganzzahl | Pflicht |

### Erinnerung erledigen

`calendar` · `acknowledge`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Erinnerung | Auswahlliste | Pflicht |

### Veranstaltung anlegen

`events` · `create`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Titel | Text | Pflicht |
| Beschreibung / Buchungstext | Text | Pflicht |
| Kategorie | Text | Pflicht |
| Ort | Text | Pflicht |
| Organisation | Auswahlliste | Pflicht |
| Verantwortliche Person | Auswahlliste | Pflicht |
| Beginn | Datum und Uhrzeit | Pflicht |
| Ende | Datum und Uhrzeit | Pflicht |
| Zeitzone | Text | Pflicht |
| Ganztägig | Ja/Nein | Pflicht |
| Doppelte Uhrzeit bei Zeitumstellung | earlier, later | Pflicht |
| Wiederholung | none, DAILY, WEEKLY, MONTHLY | Pflicht |
| Abstand der Wiederholungen | Ganzzahl | Pflicht |
| Anzahl Termine (höchstens 366) | Ganzzahl | Pflicht |
| Anmeldung ab | Datum und Uhrzeit | Pflicht |
| Anmeldeschluss | Datum und Uhrzeit | Pflicht |
| Plätze je Termin | Ganzzahl | Pflicht |
| Teilnahmegebühr | Betrag in Organisationswährung | Pflicht |
| Währung | Text | Pflicht |

### Teilnehmer anmelden / einladen

`events` · `register`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Termin | Auswahlliste | Pflicht |
| Person | Auswahlliste | Pflicht |
| Konto | Auswahlliste | Optional |
| Status | registered, invited | Pflicht |

### Teilnehmerstatus ändern

`events` · `participant`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Teilnehmer | Auswahlliste | Pflicht |
| Datensatzversion | Ganzzahl | Pflicht |
| Status | registered, confirmed, cancelled, attended, no_show | Pflicht |

### Platzzahl ändern

`events` · `capacity`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Termin | Auswahlliste | Pflicht |
| Bisherige Platzzahl | Ganzzahl | Pflicht |
| Plätze je Termin | Ganzzahl | Pflicht |

### Veranstaltungstermin absagen

`events` · `cancel`

| Feld | Eingabe | Pflicht |
|---|---|---|
| Termin | Auswahlliste | Pflicht |
