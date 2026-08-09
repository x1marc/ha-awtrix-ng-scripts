# HA AWTRIX NG Scripts

Sammlung von [Home Assistant](https://www.home-assistant.io/)-**Skripten** für
[AWTRIX NG](https://blueforcer.github.io/awtrix-ng/) (blueforcer/awtrix-ng).
Jedes Skript kapselt einen MQTT-Befehl der NG-Firmware in ein bequemes,
wiederverwendbares HA-Skript mit Eingabefeldern.

> Für **Blueprints** (Alexa-Timer, Wetter-Overlay, Bodenfeuchte) siehe das
> separate Repo [ha-blueprints](https://github.com/x1marc/ha-blueprints).

## Skripte

| Skript | Datei | Zweck |
|---|---|---|
| **new app** | [`awtrix_ng_new_app.yaml`](awtrix_ng_new_app.yaml) | Pushed App anlegen/aktualisieren (Text, Icon, Farbe/Rainbow, Dauer, Lifetime, Fortschritt, sofort anzeigen) |
| **delete app** | [`awtrix_ng_delete_app.yaml`](awtrix_ng_delete_app.yaml) | Pushed App löschen |
| **notify** | [`awtrix_ng_notify.yaml`](awtrix_ng_notify.yaml) | Notification senden (hold, stack, blink, Sound, Effekt, Farbe/Rainbow …) |
| **dismiss notification** | [`awtrix_ng_dismiss_notification.yaml`](awtrix_ng_dismiss_notification.yaml) | Aktuelle oder benannte Notification verwerfen |
| **switch app** | [`awtrix_ng_switch_app.yaml`](awtrix_ng_switch_app.yaml) | Zu App springen bzw. `next` / `previous` |
| **app order** | [`awtrix_ng_app_order.yaml`](awtrix_ng_app_order.yaml) | App-Reihenfolge & deaktivierte Apps setzen |
| **display** | [`awtrix_ng_display.yaml`](awtrix_ng_display.yaml) | Display an/aus + globales Overlay |
| **moodlight** | [`awtrix_ng_moodlight.yaml`](awtrix_ng_moodlight.yaml) | Panel-Flutlicht (Farbe/Kelvin) an/aus |
| **indicator** | [`awtrix_ng_indicator.yaml`](awtrix_ng_indicator.yaml) | Status-LEDs 1–3 (Farbe, Blinken, Faden) |
| **sound** | [`awtrix_ng_sound.yaml`](awtrix_ng_sound.yaml) | Melodie / RTTTL / Builtin abspielen oder stoppen |
| **radio** | [`awtrix_ng_radio.yaml`](awtrix_ng_radio.yaml) | Radio abspielen/stoppen (Station/Index/URL) |
| **settings (brightness)** | [`awtrix_ng_settings.yaml`](awtrix_ng_settings.yaml) | Helligkeit & Auto-Helligkeit |
| **reboot** | [`awtrix_ng_reboot.yaml`](awtrix_ng_reboot.yaml) | Uhr neu starten |
| **firmware update** | [`awtrix_ng_firmware_update.yaml`](awtrix_ng_firmware_update.yaml) | `.bin` per HTTP hochladen (kein MQTT – [Setup nötig](#firmware-update-http-kein-mqtt)) |

> Bewusst **nicht** enthalten (gefährlich/niche): Factory-Reset,
> System-/WLAN-Konfiguration, Datei-Upload. Diese lassen sich bei Bedarf ergänzen.

## Verwendung

### Alle Skripte auf einmal (empfohlen)

Die Datei [`awtrix_ng_all_scripts.yaml`](awtrix_ng_all_scripts.yaml) enthält
**alle** Skripte als Home-Assistant-**Package**:

1. Datei nach `config/packages/awtrix_ng.yaml` kopieren (z. B. via File-Editor
   oder Studio Code Server).
2. Falls Packages noch nicht aktiv sind, in `configuration.yaml`:
   ```yaml
   homeassistant:
     packages: !include_dir_named packages
   ```
3. **Entwicklerwerkzeuge → YAML → „Skripte neu laden"** (oder HA neu starten).

Danach erscheinen alle Skripte unter **Einstellungen → Skripte**. Bei dir das
**`prefix`-Feld auf `awtrixng`** setzen.

### Einzeln

1. **Einstellungen → Automationen & Szenen → Skripte → Skript hinzufügen →
   (drei Punkte) → In YAML bearbeiten**.
2. Inhalt der gewünschten `.yaml` einfügen und speichern.
3. Per Dienst-Aufruf mit den Feldern nutzen oder in **Entwicklerwerkzeugen →
   Aktionen** testen.

**Topic-Prefix:** Jedes Skript hat ein Feld **`prefix`** (Standard `awtrix`).
Trag dort das MQTT-Prefix deiner NG-Uhr ein (z. B. `awtrixng`). Das Prefix
findest du in der Weboberfläche der Uhr bzw. per MQTT-Auto-Discovery; ist es
leer, nutzt NG die 12-stellige MAC. (Nur `awtrix_ng_firmware_update` nutzt statt
MQTT die Geräte-`ip`.)

**Hinweis:** AWTRIX NG validiert Payloads strikt – ein ungültiger Key/Wert lässt
den **ganzen** Befehl scheitern. Deshalb sind optionale Felder in den Skripten
konditional aufgebaut. Effekt-/Palettennamen und verfügbare Sounds sind
geräteabhängig (siehe `GET /api/v1/capabilities` bzw. das Dateisystem der Uhr).

## Firmware-Update (HTTP, kein MQTT)

AWTRIX NG kennt für Firmware-Updates **keinen MQTT-Befehl** und kein OTA-per-URL –
die Firmware wird als `.bin` per **HTTP-Multipart** hochgeladen (`POST /update`).
Das fehlgeschlagene Image wird in einen Reserve-Slot geschrieben und erst nach
vollständiger Prüfung aktiviert – ein abgebrochener Upload ist also ungefährlich.

**Manuell** (von jedem PC) oder über die Web-Oberfläche der Uhr:
```bash
curl -X POST http://<ip>/update -F "firmware=@firmware-awtrix-ng.bin"
```

**Aus Home Assistant** (Skript [`awtrix_ng_firmware_update.yaml`](awtrix_ng_firmware_update.yaml)):

1. Firmware-`.bin` auf den HA-Host legen, z. B. `/config/firmware-awtrix-ng.bin`.
2. In `configuration.yaml` ergänzen:
   ```yaml
   shell_command:
     awtrix_ng_firmware_update: >-
       curl -sS -X POST "http://{{ ip }}/update" -F "firmware=@{{ file }}"
   ```
3. Home Assistant neu starten (oder YAML neu laden), dann das Skript importieren.
4. Skript mit `ip` (z. B. `192.168.1.50`) und `file` (Pfad zur `.bin`) aufrufen.

> **Voraussetzung:** `curl` muss in der HA-Umgebung verfügbar sein (bei HA OS /
> Container meist vorhanden). Fehlt es, den Upload von einem PC oder über das
> Add-on **„Advanced SSH & Web Terminal"** ausführen. Lade die passende Datei –
> `firmware-awtrix-ng.bin` für ein Gerät, das bereits NG läuft.

## AWTRIX NG – MQTT-Kurzreferenz

| Zweck | Topic | Payload |
|---|---|---|
| Pushed App anlegen/ändern | `<prefix>/cmd/apps/pushed/<name>` | App-JSON |
| Pushed App löschen | `<prefix>/cmd/apps/pushed/<name>` | *(leer)* oder `{}` |
| App wechseln | `<prefix>/cmd/apps/switch` | `{"name":"..","fast":true}` |
| Nächste / Vorherige App | `<prefix>/cmd/apps/next` · `<prefix>/cmd/apps/previous` | *(leer)* |
| App-Reihenfolge | `<prefix>/cmd/apps/order` | `{"order":[..],"disabled":[..]}` |
| Notification | `<prefix>/cmd/notify` | Notify-JSON |
| Notification verwerfen | `<prefix>/cmd/notify/dismiss[/<name>]` | *(leer)* |
| Display / Overlay | `<prefix>/cmd/display` | `{"power":true,"overlay":"rain"}` |
| Moodlight | `<prefix>/cmd/display/moodlight` | `{"color":[..],"brightness":120}` / *(leer)* = aus |
| Indicators | `<prefix>/cmd/indicators/1..3` | `{"color":[..],"blinkMs":500}` / `{}` = aus |
| Sound | `<prefix>/cmd/sounds/play` · `<prefix>/cmd/sounds/stop` | `{"name":".."}` / `{"rtttl":".."}` / `{"builtin":".."}` |
| Radio | `<prefix>/cmd/radio/play` · `<prefix>/cmd/radio/stop` | `{"station":".."}` / `{"index":0}` / `{"url":".."}` |
| Einstellungen | `<prefix>/cmd/settings` | `{"brightness":120,"autoBrightness":false}` |
| Neustart | `<prefix>/cmd/device/reboot` | *(leer)* |

Doku: <https://blueforcer.github.io/awtrix-ng/>
