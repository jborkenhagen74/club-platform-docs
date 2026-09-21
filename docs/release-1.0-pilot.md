# Club Platform 1.0.0 Pilot

Stand: 21.09.2026. Produktversion: **1.0.0**. Veröffentlichungskanal: **pilot**.
Datenbankschema: **18**. Öffentliche HTTP-API: **/api/v1**. Native Extension-ABI: **V3**.

Dieser Stand bündelt die bisherigen Featurezweige auf develop und main und ist für
kontrollierten Pilotbetrieb vorgesehen. Die Versionssetzung ist kein Nachweis einer
abgeschlossenen Produktionsabnahme. Historische Prüfprotokolle gelten nur für ihre
jeweils genannten Commits. Aktuell fehlgeschlagene GitHub-Jobs ohne Prüfschritte
liefern keinen neuen nativen Abnahmenachweis.

## Builds und Veröffentlichung

`VERSION` enthält die numerische Version für CMake, Pakete und Vertrauensprüfungen.
`RELEASE_CHANNEL` enthält `pilot`. Native Installer und Archive tragen `-pilot`
im Dateinamen; die Desktop-Versionsanzeige nennt den Pilotstatus. Der main-Workflow
veröffentlicht erst nach seinen vorhandenen erfolgreichen Prüfgates eine GitHub-
Vorabversion mit Tag `v1.0.0-pilot.<Runnummer>` und `latest=false`. Ein Pilot wird
nicht als stabile 1.0.0 veröffentlicht. develop bleibt ein unabhängiger Debug-/
Diagnosebuild mit Snapshot, main ein unabhängiger optimierter Build.

Eine spätere stabile Freigabe benötigt eine bewusste Änderung von
`RELEASE_CHANNEL` auf `stable` und eine erfolgreiche Abnahme. Die Updateprüfung
fragt weiterhin ausschließlich stabile GitHub-Releases ab; Pilotupdates werden
über die Release-Seite verteilt.

## Upgrade aus 0.6

Vorher Datenbank und zur Installation gehörende Module sichern und den Restore
auf einer separaten Testinstallation prüfen. Danach Host und gebündelte Module
zusammen aktualisieren. Die mitgelieferten V3-Module deklarieren nun den Corebereich
`>= 1.0.0, < 2.0.0`. Ihre eigenen Modulversionen bleiben separat:

| Modul | Modulversion | Modul-Schema |
|---|---|---|
| Martial | 1.2.1 | 3 |
| Finanzen, Kalender | 1.1.1 | 3 |
| Beiträge, Käufe, Banking, Veranstaltungen | 1.0.1 | 2 |

Die bisherige Migrationshistorie bleibt unverändert. Ein zusätzlicher datenerhaltender
Migrationsschritt protokolliert die geänderte Kompatibilität. Nach dem Start als
Administrator unter Erweiterungen **Installieren / aktualisieren** ausführen.
Ein geändertes Manifest ohne Migration würde bei bestehenden Datenbanken abgewiesen.
Bei katalogverwalteten Installationen neue Deskriptoren und Kataloge passend zu den
1.0-Modulen signieren und über den Katalog installieren; alte 0.6-Kataloge sind nicht
für Core 1.0 gültig. Externe Module benötigen ebenfalls eine ausdrückliche
Kompatibilitätsprüfung und gegebenenfalls eine neue signierte Paketversion.

Der Herausgeberschlüssel bleibt unverändert. Bestehende Lizenzen werden durch den
Versionssprung nicht automatisch ersetzt; Signatur, Laufzeit, Module und gegebenenfalls
Installationsaktivierung gelten weiterhin. Keine Datenbank oder Geräteschlüssel löschen,
um eine Aktivierung oder Migration zu umgehen.

## Pilotabnahme

- Installation und Start auf den tatsächlich angebotenen OS-/CPU-Kombinationen.
- Anmeldung, Rollen, lokale und Server-/Portalverwendung mit getrennten Testkonten.
- Standalone-Lizenz und gebundene Aktivierung einschließlich Erneuerung prüfen.
- Modulupgrade mit vorhandenen Daten, Fachfunktionen und Berechtigungen prüfen.
- Backup/Restore und kontrollierte Rückkehr zum gesicherten Ausgangsstand erproben.

Die ausführlichen Build- und Modulentwicklerhandbücher einschließlich PDFs liegen im
[öffentlichen Doku-Repository](https://github.com/jborkenhagen74/club-platform-docs).
