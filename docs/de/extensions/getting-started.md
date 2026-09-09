# Native Erweiterungen entwickeln

[Sprachstart](../README.md) · [UI-Vertrag](ui.md) · [Beispiel](../../../examples/extensions/hello-extension/README.md)

## Kompatibilität und Vertrauen

Der laufende Host 0.5.0 erwartet **ABI 2**. `sdk/extension_api.h` bleibt als
historischer ABI-1-Entwurf erhalten; dessen Lifecycle-/Menü-/REST-Callbacks sind
kein verwendbarer Vertrag dieses Hosts. Für neue Module `sdk/extension_v2.h`
verwenden. Die C-Grenze vermeidet STL-Objekte und fremde Speicherfreigaben;
die Bibliothek muss dennoch zum Betriebssystem und zur CPU-Architektur passen.

Native Bibliotheken führen vertrauenswürdigen Code mit den Hostrechten aus.
Es gibt keinen Plugin-Sandboxprozess. Modulverzeichnis administrativ schützen,
Bibliotheken vor Freigabe prüfen und nie Upload-Verzeichnisse danach durchsuchen.
Module werden beim Hoststart geladen, nicht zur Laufzeit ausgetauscht.

## Paket und Manifest

Ein Modul exportiert `clubplatform_extension_v2`. Der Rückgabewert verweist auf
eine dauerhaft gültige Struktur aus ABI-Nummer, UTF-8-Manifest und Validator.
Manifeststrings bleiben Eigentum des Moduls. Der Validator nimmt Datensatztyp
und JSON-Zeichenkette entgegen und liefert genau `1` bei Erfolg; Ausnahmen dürfen
die C-Grenze nicht überschreiten. Keine Datenbankhandles werden herausgegeben.

Das Manifest enthält `id`, `name`, `version` und `types`. Die Version hat drei
numerische Komponenten. Modul-ID ohne Punkt; Typen beginnen mit `modul.`.
Typen besitzen `key`, `label`, `fields`; Felder `key`, `label`, `type` und optional
`required:false`. Unterstützt: `text`, `integer`, `decimal`, `boolean`, `date`.
Schlüssel beginnen mit Kleinbuchstaben und verwenden Kleinbuchstaben, Ziffern,
Unterstriche und für Typen Punkte. Duplikate und fremde Namensräume werden abgewiesen.

Der Host verlangt alle deklarierten Feldschlüssel, auch optionale Felder mit
leerem Wert. Unbekannte Felder werden verworfen durch Ablehnung des Vorgangs.
Er validiert Typen und Pflichtwerte vor dem Modulvalidator; Textwerte maximal
512 UTF-8-Bytes gemäß aktueller Validierung. Das Beispiel fügt Trainingsteilnahmen
hinzu und benötigt beim Bauen nur den veröffentlichten Header.

```sh
cmake -S examples/extensions/hello-extension -B build/hello-extension -DCMAKE_BUILD_TYPE=Release
cmake --build build/hello-extension --config Release
```

Die erzeugte Bibliothek in ein eigenes Erweiterungsverzeichnis kopieren. Bei
Visual Studio den Konfigurationsunterordner beachten. Den Host mit
`--extensions /absoluter/pfad` starten oder `CLUBPLATFORM_EXTENSIONS` setzen.
Ein Remote-Desktop lädt serverseitige Module nicht nochmals lokal.

## Installation und Datenzugriff

Nach dem Laden muss ein angemeldeter Administrator `Erweiterungen aktivieren`
ausführen oder `POST /api/extensions/install` mit `{}` senden. Dafür ist
`schema.manage` notwendig. Typregistrierung und Manifest werden transaktional
persistiert und auditiert. `GET /api/extensions` zeigt geladene Manifeste und
`installed`. Eine Wiederholung mit identischem Manifest ist zulässig.

Native Einträge gehören derzeit zu Personen. Beispielroute:
`/api/management/ext:attendance.session`. Die Verwaltungswerte enthalten zusätzlich
`person_id`; der Host entfernt diese Zuordnung, bevor der fachliche Validator
aufgerufen wird. `attendance.read/write` ergänzen `records.read/write`.
Berechtigungen sind Rollen zuzuweisen; UI-Sichtbarkeit ersetzt keine Serverprüfung.

Ein abweichendes bereits gespeichertes Manifest wird beim Laden abgewiesen.
Versionsnummer erhöhen allein migriert keine Daten. Eine explizite Migration und
geprüfte Sicherung sind vor Schemaänderungen erforderlich. Nicht unterstützt:
Hot Reload, frei definierte REST-Routen, Hintergrundjobs oder mitgebrachte QML-/JS-
Ausführung über diesen ABI-Vertrag. Solche Ideen sind Zukunftsplanung.
