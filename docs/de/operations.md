# Betrieb, Sicherung und Updates

> Zielversion 0.6.0, Vorarbeit G0: HTTP-API `/api/v1` und gemeinsamer `Client` mit `LocalClient`/`RestClient`. Datenbankschema 8 und Extension ABI 2 bleiben bestehen. Alte `/api/...`-Pfade liefern 404. Server, Desktop, Portal und Proxy gemeinsam aktualisieren. Die folgenden Funktionsbeschreibungen stammen aus der 0.5.0-Basis und gelten weiterhin, soweit dieser Hinweis sie aktualisiert. Core Foundation II mit ABI V3 und sieben UI-Sprachen ist noch nicht abgeschlossen.


[Sprachstart](README.md) · [Installation](installation.md)

> Für Windows-Builds und die PostgreSQL-Wiederherstellung wird zusätzlich der Fehlerkorrektur-Commit `6ebb363ec28ab8631fb82a88051351f87659b523` benötigt. Er korrigiert das Windows-SDK-Symbol `LOAD_LIBRARY_SEARCH_DEFAULT_DIRS` und ergänzt beim SQL-Export von `pg_restore` die Option `--file=-`. Schema und API bleiben bei diesem Fix unverändert. Vor dem Sitzungswiderruf wird außerdem der konfigurierte Suchpfad wiederhergestellt, den die Dump-Ausgabe zuvor geleert hat. Ein Regressionstest prüft, dass bei fehlgeschlagenem Widerruf auch die wiederhergestellten Tabellen zurückgerollt werden.

## Betriebsverantwortung

Ein separates Betriebskonto besitzt die Datenbankdatei bzw. den PostgreSQL-Zugang.
Programme, native Module und Daten haben getrennte Verzeichnisse. Normale
Portalnutzer erhalten keine Schreibrechte auf das Modulverzeichnis. Sicherungen
enthalten Personen-, Datei- und Zugangsdaten einschließlich Passworthashes;
Zugriff beschränken und ein geeignet geschütztes Sicherungsziel verwenden.

Die hier genannten `scripts/pilot-*.py` gehören zum Implementierungspaket,
nicht zum öffentlichen Dokumentationsrepository. Python 3.11 oder neuer ist
vorausgesetzt. Eine lesbare Sicherungsdatei ist noch kein nachgewiesener Restore.

## SQLite

```sh
python3 scripts/pilot-data.py backup daten.sqlite sicherung-2026-09-09
python3 scripts/pilot-data.py diagnose sicherung-2026-09-09/database.sqlite
python3 scripts/pilot-data.py restore sicherung-2026-09-09 wiederhergestellt.sqlite
```

Die Online-Backup-API schließt bestätigte WAL-Daten ein. Das Zielverzeichnis darf
noch nicht existieren. Integrität, Fremdschlüssel, Migrationsfolge und SHA-256
werden geprüft. Bei einem fehlgeschlagenen Backup kann ein unvollständiges
Verzeichnis zurückbleiben; nicht ohne gültiges Manifest als Sicherung behandeln.

Restore benötigt eine **neue** Zieldatei. Prüfsumme und Datenbank werden kontrolliert;
vorhandene Sitzungen werden widerrufen. Den Host anschließend stoppen und erst dann
auf die geprüfte Datei umstellen. Alte Datei bis zum erfolgreichen Abgleich behalten.
Dateiuploads liegen in der Datenbank und sind Teil dieser Sicherung. Programmdateien,
Zertifikate, Konfiguration und native Module müssen separat wiederherstellbar sein.

## PostgreSQL

`pg_dump`, `pg_restore` und `psql` in einer zum Server passenden Version verwenden.
Zugriff über `pg_service.conf` und `.pgpass` bzw. geschützte libpq-Konfiguration.
Für die Wiederherstellung eine neue leere Datenbank und einen separaten Service
anlegen; keinen Host parallel auf dieses Ziel starten.

```sh
python3 scripts/pilot-postgres.py backup --service club-production --directory pg-backup
python3 scripts/pilot-postgres.py restore --service club-restore --directory pg-backup
```

Das Werkzeug verwendet ein Custom-Format-Archiv und ein Prüfsummenmanifest.
Vorhandene Benutzertabellen verhindern den Restore. Wiederherstellung und
Sitzungswiderruf erfolgen in einer Transaktion. Eigentümer-/ACL-Einstellungen
werden nicht aus dem alten System übertragen; Rollen und Berechtigungen des
Datenbankbetriebs separat bereitstellen. Keine Wiederherstellung direkt über
laufende Produktivtabellen versuchen.

## Geprüftes Updateverfahren

1. Anwender informieren, offene Arbeiten abschließen und Sicherung erstellen.
2. Neue Binärdateien und passende Module in ein eigenes Versionsverzeichnis legen.
3. Sicherung in eine neue Testdatenbank wiederherstellen. Neuen Host damit starten;
   Migrationen werden geprüft und transaktional angewendet.
4. Anmeldung, Datensatzänderung, Mitgliedschaft, Graduierung, Datei-Download,
   CSV und PDF prüfen; eingeschränktes Konto mitprüfen.
5. Produktivhost stoppen. Nur nach erfolgreicher Prüfung Programmversion und
   zugehörige Konfiguration umstellen. Statische Portaldateien passend mitwechseln.
6. Browser neu laden, neu anmelden und fachliche Stichprobe durchführen.
7. Bei Rückkehr zur alten Version auch die **passende Sicherung vor der Migration**
   verwenden. Eine ältere Binärdatei darf keine bereits migrierte Datenbank öffnen.

Änderungen seit der Sicherung können bei Rollback verloren gehen; diese vor einer
Rückkehr fachlich behandeln. Eine Suche nach Updates installiert nichts automatisch.
Signierung, Notarisierung und ein breiter Rollout bleiben eigene Freigabeschritte.

## Diagnose und Störungsbehandlung

`clubplatform-server --sqlite TESTDATEI --diagnose` meldet Verbindung und
Migrationsstand ohne Personendaten. Achtung: Öffnen des Hosts prüft **und wendet**
Migrationen an. Für eine SQLite-Prüfung ohne Migration `pilot-data.py diagnose`
verwenden. Pfade, verwendete Produktversion, Uhrzeit und Fehlermeldung notieren;
keine Token oder Passwörter in Tickets kopieren.

„Keine Tracking-Informationen“ in Git: den richtigen bestehenden Branch wählen
und einmalig `git branch --set-upstream-to=origin/feature/core-foundation
feature/core-foundation` setzen; danach `git pull --ff-only`. Nicht mit einem
Force-Reset lokale Änderungen überschreiben. `403` im Portal verlangt Prüfung von
Rollen **und** Proxy-/Origin-Konfiguration. Bei fehlendem Modul Verzeichnis, CPU,
ABI, gespeichertes Manifest und Aktivierung prüfen. Nicht durch manuelle Änderung
von Migrationstabellen oder Modulmanifesten „reparieren“.
