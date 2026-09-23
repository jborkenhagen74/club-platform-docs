# Deutsche PDF-Anleitungen

Bearbeitbare Quellen:

- [Builds und Installer](../de/build-und-installer.md)
- [Modulentwicklung ohne Core-Quellcode](../de/module-entwicklung-ohne-core.md)

PDFs:

- [Builds und Installer](Club-Platform-Build-und-Installer-DE.pdf)
- [Modulentwicklung](Club-Platform-Modulentwicklung-DE.pdf)

Erzeugung im Stamm dieses Repositorys mit Python ab 3.9:

```bash
python3 -m venv .venv-docs
.venv-docs/bin/pip install -r scripts/requirements-pdf.txt
.venv-docs/bin/python scripts/render-guides.py
python3 scripts/check-docs.py
```

Unter Windows die Python-Datei unter `.venv-docs/Scripts/python.exe` verwenden.
Der Renderer benötigt DejaVu Sans (normal/fett) und DejaVu Sans Mono als TTF.
Standardverzeichnis unter Linux: `/usr/share/fonts/truetype/dejavu`.
Für einen anderen Ort `DOCS_FONT_DIR` auf das Verzeichnis mit diesen drei Dateien
setzen. Fonts und Python-Pakete werden nicht heimlich vom Renderer geladen.

Der Renderer unterstützt die in diesen Anleitungen verwendeten Überschriften,
Absätze, Listen, Tabellen, Links und Codeblöcke. Er erzeugt Inhaltsverzeichnis,
Lesezeichen, Seitenzahlen und einen gekürzten SHA-256 der Markdown-Quelle in der
Fußzeile. Bei einem neuen Dokumentstand das Datum in Quellen und Renderer anpassen.

Nach Änderungen beide PDFs neu erzeugen und alle Seiten visuell prüfen, etwa mit
`pdftoppm -png -r 100 DATEI.pdf AUSGABEPREFIX`. Besonders Tabellen, lange Befehle,
Seitenumbrüche und Umlaute kontrollieren. Die Linkprüfung allein ersetzt diese
Sichtprüfung nicht. Änderungen an Markdown und zugehörigen PDFs gemeinsam committen.

[Training, Wearables und lokale KI (Feature-Stand)](Club-Platform-Training-Wearables-KI-DE.pdf) – [Markdown](../de/training-wearables-ai.md).
