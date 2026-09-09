# Frontends und Webserver-Anbindung

> Zielversion 0.6.0, Vorarbeit G0: HTTP-API `/api/v1` und gemeinsamer `Client` mit `LocalClient`/`RestClient`. Datenbankschema 8 und Extension ABI 2 bleiben bestehen. Alte `/api/...`-Pfade liefern 404. Server, Desktop, Portal und Proxy gemeinsam aktualisieren. Die folgenden Funktionsbeschreibungen stammen aus der 0.5.0-Basis und gelten weiterhin, soweit dieser Hinweis sie aktualisiert. Core Foundation II mit ABI V3 und sieben UI-Sprachen ist noch nicht abgeschlossen.


[Sprachstart](../README.md) · [REST](../api/overview.md) · [Installation](../installation.md)

Das mitgelieferte Portal ist ein Verwaltungsfrontend mit React/TypeScript und
Tailwind 4. `npm ci` verwendet die festgeschriebene Abhängigkeitsauflösung;
`npm run build` erzeugt statische Dateien in `dist/`. PDF-Bibliothek und Fonts
werden beim Bedarf lokal aus dem Build geladen. Das Portal benötigt keine
externen CDN-Skripte. Das kleine Beispiel in `examples/frontends/web-basic`
zeigt nur Anmeldung und Personenliste, nicht den vollständigen Produktumfang.

## Transportvertrag

Browser und öffentliche API sollten über denselben HTTPS-Ursprung erreichbar
sein. `/api/v1/` wird vom Webserver an den Loopback-Server weitergereicht. Der
Upstream-`Host` muss `127.0.0.1:8080` sein; `Authorization` und `Origin` bleiben
erhalten. Der Serverstart enthält denselben exakten Ursprung als `--portal-origin`.
Ohne Freigabe werden Browseranfragen mit Origin abgewiesen. Niemals `*` als
Ersatz für eine passende Konfiguration verwenden.

Ein öffentliches Gesundheitsmonitoring muss `/health` separat konfigurieren;
die normale `/api/v1/`-Weiterleitung umfasst diese Route nicht. Reverse Proxy und
Server dürfen keine Passwort-/Token- oder Request-Body-Protokollierung betreiben.
Für HTTPS-Zertifikat, DNS und Betriebskonto gelten die örtlichen Betriebsverfahren.
Die Anwendung bringt keine automatische Zertifikatsverwaltung mit.

## Clientverhalten

Token nur im Arbeitsspeicher halten; weder in URLs noch Browser-Speichern ablegen.
Bei `401` persönliche Listen, Entwürfe und Sitzung entfernen und neu anmelden.
Bei `403` die fehlende Berechtigung erklären. Ein Netzwerkfehler beim Speichern
ist mehrdeutig: zuerst Serverstand neu lesen, keine automatische Schreibwiederholung.
Ein `409` erfordert einen Vergleich mit der aktuellen Revision.

Listen seitenweise lesen. Lange IDs nicht als alleinige Referenzbeschriftung
verwenden; `labels` oder zugehörige Namen anzeigen. Ungeprüften Servertext als
Text rendern, nicht als HTML. Dateiinhalte nur nach einer expliziten Benutzeraktion
herunterladen. Das Portal führt hochgeladene Dateien nicht als Plugins aus.

## Darstellung und Umfang

Die fünf Farblayouts Hell, Dunkel, Wald, Pflaume und hoher Kontrast ergänzen den
Systemmodus. Datumseingabe und Anzeige verwenden das Browsergebietsschema;
ISO-Werte bleiben im API-Vertrag. Auf kleinen Bildschirmen wird der Aktenbereich
über eine Auswahl geöffnet. Felddefinitionen und Feldrechte der Core-Custom-Fields
werden weiterhin im Desktop verwaltet. Das Portal bietet keine automatische
Selbstzuordnung eines Kontos zum eigenen Mitgliedsdatensatz.

Für eigene Clients die [OpenAPI-Datei](../../../openapi/club-platform.yaml) und
[Ressourcenreferenz](../../../reference/resources.md) gemeinsam verwenden.
Nicht vorhandene Endpunkte wie `/api/v1/appointments` nicht aus dem historischen
Entwurf übernehmen. API-Kompatibilität vor jedem Produktupdate erneut testen.
