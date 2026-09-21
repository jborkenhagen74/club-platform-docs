# Extension ABI V3 — Phase 3

Phase 3: Runtime, Abhängigkeiten, Lifecycle und Modulmigrationen implementiert.
Phase 4 ist ebenfalls implementiert: [Dokumentregistry und UI](document-placeholders.md).
Keine vollständige Core-Foundation-II-Freigabe.

Der öffentliche C-Vertrag ist `sdk/include/clubplatform/extension_v3.h`.
Der Host bevorzugt `clubplatform_extension_v3`; nur bei fehlendem V3-Symbol
wird V2 als Legacy geladen. Ein defekter V3-Deskriptor fällt nicht auf V2 zurück.
Strukturgröße und sämtliche Callback-Zeiger werden geprüft.

Callbacks werden serialisiert aufgerufen. Keine Exceptions oder externen
Seiteneffekte; Eingabezeiger dürfen nicht behalten werden. JSON-Rückgaben gehören
dem Modul, bleiben bis zum nächsten Aufruf gültig und werden sofort kopiert.
Ergebnis: 1=Erfolg, 0=Ablehnung, -1=Fehler; JSON-Fehler liefern nullptr.
Module laufen als vertrauenswürdiger nativer Code im Hostprozess.

Das Beispiel `sdk/examples/v3-extension` baut ohne Core-/Datenbanklink:

```sh
cmake -S sdk/examples/v3-extension -B build/v3-example -DCLUB_SDK=/path/to/installed/include
cmake --build build/v3-example
```

Es benötigt nlohmann-json. Der Standardfall ist ein Notizmodul; die
`V3_FIXTURE`-Varianten dienen ausschließlich den Regressionstests.

V3-Manifeste deklarieren `name_key`, Core-Versionsbereich (`minimum`, optional
`maximum_exclusive`), `schema_version`, lückenlose `migrations` mit unveränderlicher
`definition`, eigene `permissions`, `capabilities` als `{key,version}` und optionale
`dependencies` als `{id,minimum?,maximum_exclusive?,optional?}`. `requires` enthält
Capability-Abhängigkeiten `{module,key,version}`. Unterstützte Capability-Version
ist aktuell 1. Versionsstrings sind numerische Tripel ohne Prerelease-Suffix.

Auflösung und Initialisierung sind deterministisch und topologisch. Fehlercodes
umfassen `dependency_missing`, `dependency_cycle`, `version_mismatch`,
`capability_missing`, `capability_version_mismatch`, `lifecycle_failed`.
UI-/Platzhalter-Metadaten werden validiert; spätere Finanz-, Kalender- und
Übersetzungsprovider können denselben versionierten Dispatch verwenden.

Lifecycle: `load`, `install`, `upgrade`, `enable`, `disable`. Deaktivieren entlädt
keine Bibliothek. Native Updates erfordern einen Host-Neustart. Installation und
Migration sind eine Datenbanktransaktion einschließlich Manifest und Audit.
`migrate_record` transformiert die Werte bestehender hostverwalteter Moduldatensätze;
IDs bleiben erhalten. Eigene SQL-Schemata sind nicht Teil dieses Vertrags.
Historienmanipulation, Downgrades und Manifeständerungen ohne neue Migration werden
abgewiesen. V2-Datenübernahme benötigt `accepts_v2: true`.

Schema 10 ergänzt Modulzustände, Migrationshistorie und vorbereitende Vorlagenspalten.
Vor Aktualisierung Backup erstellen. Bestehende Migrationen bleiben unverändert.
Katalogwerte trennen geladen/installiert/aktiv/bereit/Legacy und liefern Diagnosen.
Lizenzierung wird seit Phase 7 geprüft (`license_status: licensed` oder `not_licensed`); siehe [Lizenzierung/Provisionierung](licensing-provisioning.md). Martial bleibt bis
Phase 6 V2.

Endgültiges Löschen von Personen/Organisationen benötigt von allen installierten
Modulen eine erfolgreiche `record.references`-Antwort `{referenced:false}`.
Übergeben werden Ziel-ID und sämtliche Moduldatensätze einschließlich archivierter
Einträge. Fehlende/deaktivierte Module oder unbekannte Referenzen sperren Löschen;
Archivierung bleibt möglich. Core-Fremdschlüssel werden zusätzlich geprüft.

Lokale Foundation-Tests prüfen V2→V3, erfolgreiche/fehlgeschlagene Migration,
Datenerhalt, Audit-Rollback, idempotente Installation, Revisionsschutz,
Manipulations- und Downgrade-Sperre sowie Loaderdiagnosen. Die PostgreSQL- und
Plattformabnahme erfolgt in der bestehenden CI-Matrix.
