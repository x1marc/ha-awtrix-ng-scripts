# HA AWTRIX NG Scripts

Sammlung von [Home Assistant](https://www.home-assistant.io/)-**Skripten** für
[AWTRIX NG](https://blueforcer.github.io/awtrix-ng/) (blueforcer/awtrix-ng).
Die Skripte kapseln die MQTT-Befehle der NG-Firmware in bequeme, wiederverwendbare
HA-Skripte mit Eingabefeldern.

> Für **Blueprints** (Alexa-Timer, Wetter-Overlay, Bodenfeuchte) siehe das
> separate Repo [ha-blueprints](https://github.com/x1marc/ha-blueprints).

## Inhalt

| Skript | Datei | Zweck |
|---|---|---|
| **awtrix ng - new app** | [`awtrix_ng_new_app.yaml`](awtrix_ng_new_app.yaml) | Erstellt/aktualisiert eine Pushed App (Text, Icon, Farbe/Rainbow, Dauer, Lifetime, Fortschritt, sofort anzeigen). |

*(weitere folgen)*

## Verwendung

1. In Home Assistant: **Einstellungen → Automationen & Szenen → Skripte →
   Skript hinzufügen → (drei Punkte) → In YAML bearbeiten**.
2. Den Inhalt der gewünschten `.yaml` einfügen und speichern.
3. Das Skript per `action:`/Dienst mit den Feldern aufrufen (z. B. aus einer
   Automation) oder direkt in den Entwicklerwerkzeugen testen.

**Topic-Prefix:** Die Skripte verwenden `awtrix` als MQTT-Prefix. Falls deine
NG-Uhr einen anderen Prefix nutzt (z. B. `awtrixNG`), in den `topic:`-Zeilen
anpassen.

## AWTRIX NG – MQTT-Kurzreferenz

| Zweck | Topic |
|---|---|
| Pushed App anlegen/ändern | `<prefix>/cmd/apps/pushed/<name>` |
| Pushed App löschen | dasselbe Topic mit leerem Payload oder `{}` |
| App sofort anzeigen | `<prefix>/cmd/apps/switch` → `{"name":"<name>","fast":true}` |
| Notification | `<prefix>/cmd/notify` |
| Notification verwerfen | `<prefix>/cmd/notify/dismiss` |
| Display/Overlay | `<prefix>/cmd/display` → `{"overlay":"rain"}` (`null` = aus) |

Doku: <https://blueforcer.github.io/awtrix-ng/>
