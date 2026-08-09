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

> Bewusst **nicht** enthalten (gefährlich/niche): Factory-Reset, Firmware-Update,
> System-/WLAN-Konfiguration, Datei-Upload. Diese lassen sich bei Bedarf ergänzen.

## Verwendung

1. In Home Assistant: **Einstellungen → Automationen & Szenen → Skripte →
   Skript hinzufügen → (drei Punkte) → In YAML bearbeiten**.
2. Inhalt der gewünschten `.yaml` einfügen und speichern.
3. Das Skript per Dienst-Aufruf mit den Feldern nutzen (Automation, Dashboard-
   Button) oder in den **Entwicklerwerkzeugen → Aktionen** testen.

**Topic-Prefix:** Alle Skripte verwenden `awtrix` als MQTT-Prefix. Nutzt deine
NG-Uhr einen anderen Prefix (z. B. `awtrixNG`), in den `topic:`-Zeilen anpassen.

**Hinweis:** AWTRIX NG validiert Payloads strikt – ein ungültiger Key/Wert lässt
den **ganzen** Befehl scheitern. Deshalb sind optionale Felder in den Skripten
konditional aufgebaut. Effekt-/Palettennamen und verfügbare Sounds sind
geräteabhängig (siehe `GET /api/v1/capabilities` bzw. das Dateisystem der Uhr).

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
