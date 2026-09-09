# Deklarative Oberflächenbeiträge

[Sprachstart](../README.md) · [Entwicklung](getting-started.md)

ABI 2 beschreibt Datensatztypen und Felder. Desktop und Portal erzeugen daraus
Reiter und Formulare in **Personenakten**. Ein Manifest definiert keine beliebigen
Menüs, Widgets oder Skripte. In der Organisationsakte werden native Typen dieses
Vertrags derzeit nicht automatisch eingebunden.

Ein Typ-`label` ist der sichtbare Reitername; Feld-`label` die Beschriftung.
`integer` wird als Ganzzahl behandelt, `date` wird für den Transport als ISO-Datum
gesendet. Die Darstellung folgt dem jeweiligen System-/Browsergebietsschema.
Optionale Felder sichtbar als optional kennzeichnen und beim Schreiben als leere
Zeichenkette mitsenden. Technische Schlüssel bleiben sprachneutral; Labels im
Manifest sind in 0.5.0 einfache Zeichenketten, keine Übersetzungstabellen.

Der Host prüft Berechtigungen erneut beim Lesen und Speichern. Fehlende Rechte
können deshalb auch nach Öffnen einer Akte zu einer Fehlermeldung führen.
Revisionen erhalten; `409` nicht durch erzwungenes Überschreiben umgehen.
Ein bloß sichtbarer Reiter bedeutet nicht, dass das Konto schreiben darf.

Prüfung eines neuen Moduls: als Administrator laden/aktivieren, Person öffnen,
Pflichtfelder ausfüllen und speichern; Akte schließen und wieder öffnen.
Danach ungültiges Datum und fachlich ungültigen Wert ausprobieren. Zuletzt mit
einer Leserrolle das Lesen erlauben und Schreiben verweigern. Beide Oberflächen
sowie schmale Fensterbreite prüfen. Das Kampfsportmodul demonstriert freie
Graduierungsbezeichnungen und die Prüfung von Stufen 1–30; diese Zahlen ersetzen
keine verbandsspezifische Graduierungsordnung.
