# Versionierung und belegter Funktionsstand

[Sprachstart](README.md)

Basis: Anwendung **0.5.0**, Commit `320a4c2709c13dd56455768a2f8819a815ad3997`,
Schema **8**, native ABI **2**, Dokumentationsausgabe **2026-09-09**.

| Ebene | Vertrag |
|---|---|
| Anwendung | Paket-/Produktversion 0.5.0 |
| Datenbank | Geordnete Migrationen; unbekannte oder veränderte Definitionen werden abgewiesen |
| Erweiterung | ABI 2 und eigenes Manifest mit dreiteiliger Versionsnummer |
| HTTP | Implementierte `/api`-Routen, separat `/health`; kein veröffentlichtes `/api/v1` |
| Dokumentation | Gleiche Kapitel und fachlicher Umfang in de/en/fr/es/ko |

R1.9 stellt den nativen Host bereit, R1.10 das Kampfsportmodul, R1.11 Vorlagen,
PDF-Ausgabe und CSV, R1.12 Betriebswerkzeuge und Pilotabläufe. „Pilot“ bedeutet
keine universellen signierten Installer oder bereits erfolgte Zielrechner-Abnahme.
Die Handbuchübersetzungen schalten die Anwendungssprache nicht um.

Der frühere öffentliche ABI-1-/`/api/v1`-Entwurf bleibt als historisch erkennbar;
seine Menü-, View- und REST-Callbacks sind keine zugesicherte Fähigkeit von 0.5.0.
Geplant bzw. nicht abgeschlossen sind unter anderem Termin-/Zahlungsabläufe,
Offline-Synchronisation, Mandantentrennung, freie Plugin-UI, automatische Updates
und vollständige Anwendungslokalisierung. Vor Erweiterungen oder Integrationen
Produktversion, ABI und tatsächliche Routen gemeinsam prüfen.

Nach Änderungen zuerst die englische Referenz und alle vier weiteren Sprachen
fachlich synchronisieren, den Implementierungsbezug aktualisieren und die
Dokumentationsprüfung ausführen. Quellcodekennungen, Feldschlüssel, URLs und
Befehlsoptionen niemals übersetzen. Die technische Sicherheit einer Integration
hängt nicht von ihrer gewählten Dokumentationssprache ab.
