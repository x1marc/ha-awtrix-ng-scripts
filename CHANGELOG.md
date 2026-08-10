# Changelog

Alle nennenswerten Änderungen an diesem Projekt werden hier dokumentiert.
Das Format orientiert sich an
[Keep a Changelog](https://keepachangelog.com/de/1.1.0/).

## [Unveröffentlicht]

## [2026-08-10]

### Hinzugefügt
- **Beispiel pro Skript** direkt in der README (kopierbare Automation/Aktion).
- **Importierbare Beispiel-Dateien** im Ordner `examples/` – eine Datei je
  Szenario, mit Kopf-Anleitung zum Einbinden.
- **Sehr ausführliche README**: Inhaltsverzeichnis, Begriffe einfach erklärt,
  Voraussetzungen-Checkliste, Schritt-für-Schritt-Installation, „erste Anzeige
  in 2 Minuten", Feld-Tabelle pro Skript, Icons/Farben/Effekte, Verlauf-
  Diagramme, Fehlerbehebung/FAQ, MQTT-Kurzreferenz.
- **CI**: GitHub-Action, die bei jedem Push/PR alle YAML-Dateien validiert
  (`tools/validate.py`).
- **Projekt-Hygiene**: `LICENSE` (MIT), dieses `CHANGELOG.md` und
  Issue-Vorlagen (Fehler melden / Skript-Wunsch).

### Geändert
- **Verständlichere Feld-Beschreibungen** in allen Skripten (konkrete Beispiele,
  „(Pflicht)"-Kennzeichnung); `prefix` überall mit Fundort erklärt.
- Package `awtrix_ng_all_scripts.yaml` aus den aktualisierten Einzelskripten neu
  gebaut.

## [Erstausgabe]

### Hinzugefügt
- Skript-Sammlung für **AWTRIX NG** (blueforcer/awtrix-ng): `new app`,
  `delete app`, `notify`, `dismiss notification`, `switch app`, `app order`,
  `display`, `moodlight`, `indicator`, `sound`, `radio`, `graph`,
  `settings (brightness)`, `reboot`, `firmware update`.
- Kombiniertes Home-Assistant-**Package** `awtrix_ng_all_scripts.yaml`.
- Beispiel **Solar-Verlauf** (`examples/`).
