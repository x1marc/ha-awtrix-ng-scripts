# HA AWTRIX NG Scripts

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-x1marc-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/x1marc)

Fertige **[Home Assistant](https://www.home-assistant.io/)-Skripte** für die
Pixel-Uhr **[AWTRIX NG](https://blueforcer.github.io/awtrix-ng/)**
(blueforcer/awtrix-ng). Jedes Skript verpackt einen Uhr-Befehl in ein bequemes
Formular mit Eingabefeldern – **du musst also kein MQTT und kein YAML können**,
um Text, Icons, Farben, Töne oder Diagramme auf die Uhr zu bringen.

> **Du hast noch die alte AWTRIX 3 (awtrix-light)?** Dann sind *diese* Skripte
> nicht die richtigen – NG spricht andere Befehle. Für AWTRIX 3 / Blueprints
> (Alexa-Timer, Wetter-Overlay) siehe das Repo
> [ha-blueprints](https://github.com/x1marc/ha-blueprints).

> 💡 **Willst du nur einen Sensorwert anzeigen?** Dann brauchst du nicht einmal
> ein Skript – nimm den Blueprint
> [Sensor → AWTRIX NG App](https://github.com/x1marc/ha-blueprints/blob/main/sensor_to_awtrix_ng_app.yaml):
> importieren, Sensor wählen, App benennen, fertig.

---

## Inhalt

1. [Was ist das und was kann ich damit?](#was-ist-das-und-was-kann-ich-damit)
2. [Voraussetzungen](#voraussetzungen)
3. [Wichtige Begriffe – einfach erklärt](#wichtige-begriffe--einfach-erklärt)
4. [Installation](#installation)
5. [Deine erste Anzeige in 2 Minuten](#deine-erste-anzeige-in-2-minuten)
6. [Wie rufe ich ein Skript auf?](#wie-rufe-ich-ein-skript-auf)
7. [Skript-Referenz (jedes Feld erklärt)](#skript-referenz-jedes-feld-erklärt)
8. [Icons finden & auf die Uhr bringen](#icons-finden--auf-die-uhr-bringen)
9. [Farben, Effekte & Paletten](#farben-effekte--paletten)
10. [Diagramme & Verläufe (Historie)](#diagramme--verläufe-historie)
11. [Beispiele](#beispiele)
12. [Firmware-Update](#firmware-update-http-kein-mqtt)
13. [Fehlerbehebung / FAQ](#fehlerbehebung--faq)
14. [MQTT-Kurzreferenz (für Fortgeschrittene)](#mqtt-kurzreferenz-für-fortgeschrittene)

---

## Was ist das und was kann ich damit?

AWTRIX NG ist die Software auf einer kleinen **32×8-Pixel-Uhr** (LED-Matrix).
Sie kann Uhrzeit, Wetter, Text, kleine Bilder (Icons), Diagramme und mehr
anzeigen. Home Assistant (HA) steuert die Uhr über **MQTT** (eine Art
Nachrichten-Post).

Damit du nicht jedes Mal von Hand eine MQTT-Nachricht bauen musst, gibt es hier
für jeden Befehl ein **Skript**. Ein Skript ist in HA eine kleine „Aktion" mit
einem **Formular**: Du füllst Felder aus (Text, Farbe, Dauer …) und drückst auf
Ausführen – oder baust es in eine **Automation** ein (z. B. „wenn Briefkasten
offen → Text auf die Uhr").

**Beispiele, was möglich ist:**

- „**21.5 °C**" mit Thermometer-Icon dauerhaft als eigene App anzeigen
- Eine **Benachrichtigung** „Post da!" mit Ton einblenden
- Die **Solarleistung der letzten Stunde** als Balken-Diagramm zeigen
- Die **Status-LEDs** rot blinken lassen, wenn ein Fenster offen ist
- Die **Helligkeit** der Uhr abends automatisch senken
- Das ganze Panel als **Stimmungslicht** in einer Farbe leuchten lassen

---

## Voraussetzungen

Hake der Reihe nach ab:

- [ ] **Eine Uhr mit AWTRIX-NG-Firmware.** (Nicht AWTRIX 3 – siehe Hinweis oben.)
- [ ] **Home Assistant** läuft.
- [ ] **Ein MQTT-Broker** in HA (Add-on **„Mosquitto broker"**) und die
      **MQTT-Integration** ist eingerichtet.
- [ ] **Die Uhr ist mit demselben MQTT-Broker verbunden.** In der
      AWTRIX-Weboberfläche unter **Settings → MQTT** stehen Broker-Adresse,
      Benutzer/Passwort und der **Prefix** (merken – den brauchst du gleich).

**Kurz-Test, ob HA und Uhr über MQTT reden:** in HA
**Entwicklerwerkzeuge → MQTT → Nachrichten anhören**, als Thema `#` eintragen,
„Start listening" – wenn die Uhr sendet, tauchen Nachrichten mit deinem Prefix
auf (z. B. `awtrixng/stats/...`). Sieht man nichts, ist die MQTT-Verbindung der
Uhr das Problem, nicht diese Skripte.

> Du brauchst **kein HACS** und **keine Extra-Integration** – nur MQTT.

---

## Wichtige Begriffe – einfach erklärt

| Begriff | Was es bedeutet |
|---|---|
| **Prefix** | Der „Vorname" deiner Uhr im MQTT. Steht in der Weboberfläche unter **Settings → MQTT**. Fast immer **`awtrixng`**. Jedes Skript hat ein Feld `prefix` – der Standard passt meist, du lässt es also in Ruhe. Hast du mehrere Uhren, unterscheiden sie sich über den Prefix. |
| **App** | Eine dauerhafte Kachel, die im normalen Durchlauf der Uhr mitrotiert (z. B. „Wetter", „Solar"). Bleibt, bis du sie änderst oder löschst. → Skript **new app**. |
| **Notification** | Eine einmalige Einblendung, die kurz „dazwischenfunkt" (z. B. „Post da!") und dann wieder verschwindet. → Skript **notify**. |
| **App-Name** (`topicname`) | Der frei wählbare Name **einer** App, z. B. `wetter` oder `solar`. **Wichtig:** Pro App einen eigenen Namen. Rufst du **new app** zweimal mit demselben Namen auf, wird die App **überschrieben** (aktualisiert) – das ist praktisch für Werte, die sich ändern. |
| **Icon** | Eine kleine Nummer, die für ein Bildchen auf der Uhr steht (z. B. `2422`). Das Bild muss **auf der Uhr gespeichert** sein. → [Icons finden](#icons-finden--auf-die-uhr-bringen). |
| **Farbe** | Wird als Farbrad gewählt (intern RGB, z. B. `[255,0,0]` = Rot). |
| **MQTT** | Der Nachrichtenweg zwischen HA und Uhr. Musst du nicht verstehen – die Skripte erledigen das. |

---

## Installation

Du hast **zwei Wege**. Variante A bringt alle Skripte auf einmal und ist
empfohlen.

### Variante A – alle Skripte auf einmal (empfohlen)

Die Datei **[`awtrix_ng_all_scripts.yaml`](awtrix_ng_all_scripts.yaml)** enthält
alle Skripte als HA-**Package**.

1. **Datei auf den HA-Server legen:** nach `config/packages/awtrix_ng.yaml`
   kopieren. Am einfachsten mit dem Add-on **„Studio Code Server"** oder
   **„File editor"**. (Den Ordner `packages` im `config`-Verzeichnis ggf. neu
   anlegen.)
2. **Packages aktivieren** (nur einmalig nötig): in `configuration.yaml`
   ergänzen –
   ```yaml
   homeassistant:
     packages: !include_dir_named packages
   ```
3. **Neu laden:** **Entwicklerwerkzeuge → YAML → „Skripte neu laden"** (oder HA
   neu starten).

Danach findest du alle Skripte unter **Einstellungen → Automationen & Szenen →
Skripte**. Das `firmware update`-Skript ist bewusst **nicht** dabei (braucht
Extra-Setup, siehe [Firmware-Update](#firmware-update-http-kein-mqtt)).

### Variante B – einzelne Skripte

Wenn du nur ein oder zwei Skripte willst:

1. **Einstellungen → Automationen & Szenen → Skripte → Skript hinzufügen**.
2. Oben rechts **⋮ (drei Punkte) → In YAML bearbeiten**.
3. Den Inhalt der gewünschten `awtrix_ng_*.yaml`-Datei einfügen, **Speichern**.
4. Fertig – das Skript taucht in der Liste auf.

### Prefix prüfen (einmalig)

Öffne ein Skript, klicke **Ausführen** mit Testwerten. Passiert nichts, prüfe
das Feld **`prefix`**: Es muss exakt dem Prefix aus **Settings → MQTT** deiner
Uhr entsprechen (Standard `awtrixng`).

---

## Deine erste Anzeige in 2 Minuten

1. **Entwicklerwerkzeuge → Aktionen** (früher „Dienste").
2. Aktion suchen: **`awtrix ng - notify`**.
3. Auf **„In YAML-Modus wechseln"** oder einfach das Feld **text** ausfüllen mit
   `Hallo!`.
4. **Aktion ausführen**.

Auf der Uhr sollte kurz **„Hallo!"** erscheinen. 🎉 Klappt das, funktioniert die
ganze Kette (HA → MQTT → Uhr) und du kannst loslegen.

---

## Wie rufe ich ein Skript auf?

Es gibt drei typische Wege. In allen dreien heißt das Skript
`script.<name>` (z. B. `script.awtrix_ng_notify`) und die Formularfelder stehen
unter `data:`.

**1. Zum Testen (Entwicklerwerkzeuge → Aktionen):**
```yaml
action: script.awtrix_ng_new_app
data:
  topicname: wetter
  text: "21.5°C"
  icon: "2422"
  duration: 6
```

**2. Als Knopf im Dashboard (Button-Karte):**
```yaml
type: button
name: Gruß anzeigen
tap_action:
  action: perform-action
  perform_action: script.awtrix_ng_notify
  data:
    text: "Hallo!"
```

**3. In einer Automation (automatisch bei einem Ereignis):**
```yaml
alias: Post-Benachrichtigung
triggers:
  - trigger: state
    entity_id: binary_sensor.briefkasten
    to: "on"
actions:
  - action: script.awtrix_ng_notify
    data:
      text: "Post da!"
      icon: "1242"
      sound: "beep"
```

> **Tipp für Nicht-ITler:** Du musst dieses YAML nicht abtippen. Wähle das Skript
> im **Menü** aus (Automation → „Aktion hinzufügen" → „Skript ausführen") und
> fülle die Felder im **Formular** aus – HA baut das YAML selbst.

---

## Skript-Referenz (jedes Feld erklärt)

**Zu allen Tabellen:** Jedes Skript hat zusätzlich ein Feld **`prefix`**
(Standard `awtrixng`) – normalerweise **einfach so lassen**. Es wird unten nur
erwähnt, wenn nötig. **Pflicht** = muss ausgefüllt werden; alles andere ist
optional und hat einen sinnvollen Standard.

Unter jeder Tabelle steht ein **fertiges Beispiel zum Kopieren**. Der Übersicht
halber ist `prefix` darin weggelassen (Standard `awtrixng`) – hat deine Uhr einen
anderen Prefix, ergänze eine Zeile `prefix: deinprefix`. Entitäten wie
`sensor.balkonkraftwerk_kwh_tag` oder `binary_sensor.briefkasten` sind Platzhalter
– durch deine eigenen ersetzen.

### 📝 Text & Apps

#### `new app` — dauerhafte App anlegen/aktualisieren · [`awtrix_ng_new_app.yaml`](awtrix_ng_new_app.yaml)
Legt eine eigene, im Durchlauf mitrotierende App an. Gleicher `topicname` =
App wird aktualisiert (ideal für sich ändernde Werte).

| Feld | Was du einträgst | Beispiel | Pflicht? |
|---|---|---|---|
| `topicname` | Frei wählbarer App-Name (pro App eindeutig). Nur Buchstaben/Zahlen/`_`/`-`. | `wetter` | **Ja** |
| `text` | Der anzuzeigende Text. Zu lang → scrollt automatisch. | `21.5°C` | **Ja** |
| `icon` | Icon-Nummer, die auf der Uhr liegt. Leer = kein Icon. | `2422` | Nein |
| `iconmode` | Icon fest / einmal wegschieben / mitscrollen. | fest | Nein |
| `scrollspeed` | Scroll-Tempo für langen Text (kleiner = langsamer). | `80` | Nein |
| `effect` | Hintergrund-Effekt (Liste unten). | kein Effekt | Nein |
| `palette` | Text als Farbverlauf (statt einfarbig). | keine | Nein |
| `scrollmode` | Wie der Text läuft (Standard/static/wrap/loop/bounce). | Standard | Nein |
| `repeat` | Wie oft langer Text durchläuft. `0` = stattdessen Dauer nutzen. | `0` | Nein |
| `rainbow` | Text in Regenbogenfarben (an/aus). | aus | Nein |
| `lifetime` | Nach X Sekunden verschwindet die App. `0` = bleibt. | `0` | Nein |
| `duration` | Wie lange pro Durchlauf sichtbar (Sekunden). | `5` | Nein |
| `textcase` | 0 = wie global, 1 = ALLES GROSS, 2 = wie eingegeben. | `0` | Nein |
| `showimmediately` | An = Uhr springt sofort zu dieser App. | aus | Nein |
| `textcolor` | Textfarbe (Farbrad). Ignoriert bei Rainbow/Palette. | Weiß | Nein |
| `progress` | Zusätzlicher Fortschrittsbalken 0–99. `0` = keiner. | `0` | Nein |

**Beispiel — Tages-PV-Ertrag alle 27 Min aktualisieren** (aus einem
kWh-Sensor; gleicher `topicname` → App wird jedes Mal überschrieben):
```yaml
alias: Tages-PV-Ertrag auf AWTRIX NG
description: Aktualisiert den Balkonkraftwerk-Tagesertrag alle 27 Minuten.
triggers:
  - trigger: time_pattern
    minutes: /27
actions:
  - action: script.awtrix_ng_new_app
    data:
      topicname: TagesPV_Ertrag
      text: "{{ states('sensor.balkonkraftwerk_kwh_tag') | round(1) }} kWh"
      icon: "55972"
      iconmode: push
      textcolor: [255, 255, 255]
      duration: 15
      lifetime: 30
mode: single
```

#### `delete app` — App löschen · [`awtrix_ng_delete_app.yaml`](awtrix_ng_delete_app.yaml)

| Feld | Was du einträgst | Beispiel | Pflicht? |
|---|---|---|---|
| `topicname` | Name der App, die weg soll (wie beim Anlegen). | `wetter` | **Ja** |

**Beispiel — die PV-App nachts entfernen** (tagsüber baut die obige Automation
sie neu auf):
```yaml
alias: PV-App nachts entfernen
triggers:
  - trigger: time
    at: "23:30:00"
actions:
  - action: script.awtrix_ng_delete_app
    data:
      topicname: TagesPV_Ertrag
mode: single
```

#### `notify` — einmalige Einblendung · [`awtrix_ng_notify.yaml`](awtrix_ng_notify.yaml)
Funkt kurz dazwischen und verschwindet wieder (oder bleibt bei `hold`).

| Feld | Was du einträgst | Beispiel | Pflicht? |
|---|---|---|---|
| `text` | Der Benachrichtigungstext. | `Post da!` | **Ja** |
| `icon` | Icon-Nummer (optional). | `1242` | Nein |
| `iconmode` | Icon fest / wegschieben / mitscrollen. | fest | Nein |
| `scrollspeed` | Scroll-Tempo. | `80` | Nein |
| `duration` | Anzeigedauer in Sekunden (ohne `hold`). | `7` | Nein |
| `hold` | An = bleibt stehen, bis du sie wegwischst (→ `dismiss`). | aus | Nein |
| `stack` | An = einreihen; Aus = laufende Meldung ersetzen. | an | Nein |
| `wakeup` | An = schaltet das Display ein, falls aus. | aus | Nein |
| `center` | An = kurzer Text mittig. | aus | Nein |
| `blink` | An = Text blinkt. | aus | Nein |
| `rainbow` | Regenbogen-Text. | aus | Nein |
| `textcolor` | Textfarbe (bei Rainbow/Palette ignoriert). | Weiß | Nein |
| `effect` | Hintergrund-Effekt. | kein Effekt | Nein |
| `sound` | Melodie-Name, der auf der Uhr liegt (optional). | `beep` | Nein |
| `palette` | Text als Farbverlauf. | keine | Nein |
| `scrollmode` | Wie der Text läuft. | Standard | Nein |
| `repeat` | Wie oft langer Text durchläuft. | `0` | Nein |

**Beispiel — Post-Benachrichtigung mit Ton**, wenn der Briefkasten-Sensor
auslöst:
```yaml
alias: Post-Benachrichtigung auf AWTRIX NG
triggers:
  - trigger: state
    entity_id: binary_sensor.briefkasten
    to: "on"
actions:
  - action: script.awtrix_ng_notify
    data:
      text: "Post da!"
      icon: "1242"
      sound: "beep"
      textcolor: [0, 255, 0]
      duration: 8
mode: single
```

#### `dismiss notification` — Einblendung wegwischen · [`awtrix_ng_dismiss_notification.yaml`](awtrix_ng_dismiss_notification.yaml)

| Feld | Was du einträgst | Beispiel | Pflicht? |
|---|---|---|---|
| `name` | Name einer benannten Notification. **Leer** = aktuelle wegwischen. | *(leer)* | Nein |

**Beispiel — offene Einblendungen wegwischen**, sobald niemand mehr zu Hause ist
(leeres `name` = aktuelle Meldung):
```yaml
alias: Einblendung wegwischen, wenn niemand da
triggers:
  - trigger: state
    entity_id: group.family
    to: not_home
actions:
  - action: script.awtrix_ng_dismiss_notification
mode: single
```

#### `switch app` — zu einer App springen · [`awtrix_ng_switch_app.yaml`](awtrix_ng_switch_app.yaml)

| Feld | Was du einträgst | Beispiel | Pflicht? |
|---|---|---|---|
| `target` | App-Name, oder `next` / `previous`. | `wetter` | **Ja** |
| `fast` | An = sofort umschalten (ohne Animation). | an | Nein |

**Beispiel — morgens automatisch die Wetter-App zeigen:**
```yaml
alias: Morgens Wetter anzeigen
triggers:
  - trigger: time
    at: "06:45:00"
actions:
  - action: script.awtrix_ng_switch_app
    data:
      target: weather
      fast: true
mode: single
```

#### `app order` — Reihenfolge & Deaktivierte · [`awtrix_ng_app_order.yaml`](awtrix_ng_app_order.yaml)
> ⚠️ Nur die in `order` gelisteten Apps bleiben sichtbar. Namen genau treffen!

| Feld | Was du einträgst | Beispiel | Pflicht? |
|---|---|---|---|
| `order` | Reihenfolge, App-Namen mit Komma. | `Time, weather, solar` | Nein |
| `disabled` | Auszublendende Apps, mit Komma. | `Battery` | Nein |

**Beispiel — Reihenfolge einmalig festlegen** (Entwicklerwerkzeuge → Aktionen,
kein Trigger nötig):
```yaml
action: script.awtrix_ng_app_order
data:
  order: "Time, weather, TagesPV_Ertrag"
  disabled: "Battery"
```

### 💡 Anzeige & Licht

#### `display` — Display an/aus + Overlay · [`awtrix_ng_display.yaml`](awtrix_ng_display.yaml)

| Feld | Was du einträgst | Beispiel | Pflicht? |
|---|---|---|---|
| `power` | Display an / aus / beibehalten. | an | Nein |
| `overlay` | Wetter-Overlay übers ganze Bild (siehe unten) oder „aus". | rain | Nein |

**Beispiel — Regen-Overlay automatisch** übers Display legen, wenn das Wetter auf
„regnerisch" steht (sonst aus):
```yaml
alias: Regen-Overlay bei Regen
triggers:
  - trigger: state
    entity_id: weather.home
actions:
  - action: script.awtrix_ng_display
    data:
      overlay: "{{ 'rain' if is_state('weather.home','rainy') else 'off' }}"
mode: single
```

#### `moodlight` — Panel als Stimmungslicht · [`awtrix_ng_moodlight.yaml`](awtrix_ng_moodlight.yaml)

| Feld | Was du einträgst | Beispiel | Pflicht? |
|---|---|---|---|
| `mode` | an / aus. | an | Nein |
| `color` | Farbe (ignoriert, wenn `kelvin` > 0). | Warmweiß | Nein |
| `kelvin` | Farbtemperatur statt Farbe (0 = aus). | `2700` | Nein |
| `brightness` | Helligkeit 0–255. | `120` | Nein |

**Beispiel — zum Sonnenuntergang warmes Stimmungslicht** einschalten:
```yaml
alias: Moodlight zum Sonnenuntergang
triggers:
  - trigger: sun
    event: sunset
actions:
  - action: script.awtrix_ng_moodlight
    data:
      mode: "on"
      kelvin: 2700
      brightness: 80
mode: single
```

#### `indicator` — die 3 seitlichen Status-LEDs · [`awtrix_ng_indicator.yaml`](awtrix_ng_indicator.yaml)

| Feld | Was du einträgst | Beispiel | Pflicht? |
|---|---|---|---|
| `id` | Welche LED (1, 2 oder 3). | `1` | Nein |
| `mode` | setzen / aus. | setzen | Nein |
| `color` | Farbe der LED. | Rot | Nein |
| `blink` | Blink-Tempo in Millisekunden (0 = aus). | `500` | Nein |
| `fade` | Pulsieren in Millisekunden (0 = aus). | `0` | Nein |

**Beispiel — LED 1 rot blinken lassen, wenn ein Fenster offen ist**, und wieder
ausschalten, wenn es zu ist:
```yaml
alias: Fenster-Status als LED
triggers:
  - trigger: state
    entity_id: binary_sensor.fenster_wohnzimmer
actions:
  - choose:
      - conditions: "{{ is_state('binary_sensor.fenster_wohnzimmer','on') }}"
        sequence:
          - action: script.awtrix_ng_indicator
            data:
              id: 1
              mode: set
              color: [255, 0, 0]
              blink: 500
    default:
      - action: script.awtrix_ng_indicator
        data:
          id: 1
          mode: clear
mode: single
```

### 🔊 Töne

#### `sound` — Melodie/Ton abspielen · [`awtrix_ng_sound.yaml`](awtrix_ng_sound.yaml)

| Feld | Was du einträgst | Beispiel | Pflicht? |
|---|---|---|---|
| `mode` | abspielen / stoppen. | abspielen | Nein |
| `type` | Quelle: gespeicherte Melodie (`name`), Inline-`rtttl` oder `builtin`. | name | Nein |
| `value` | Der Datei-/Ton-Name bzw. RTTTL-String. | `beep` | Nein |

**Beispiel — morgens einen kurzen Weck-Ton** abspielen:
```yaml
alias: Wecker-Ton auf AWTRIX NG
triggers:
  - trigger: time
    at: "07:00:00"
actions:
  - action: script.awtrix_ng_sound
    data:
      mode: play
      type: builtin
      value: "beep"
mode: single
```

#### `radio` — Webradio (falls unterstützt) · [`awtrix_ng_radio.yaml`](awtrix_ng_radio.yaml)

| Feld | Was du einträgst | Beispiel | Pflicht? |
|---|---|---|---|
| `mode` | abspielen / stoppen. | abspielen | Nein |
| `by` | Auswahl per Station, Index oder URL. | station | Nein |
| `value` | Stationsname / Index / Stream-URL. | `SWR3` | Nein |

**Beispiel — Radio per Dashboard-Knopf starten** (ein zweiter Knopf mit
`mode: stop` hält es an):
```yaml
type: button
name: SWR3 an
tap_action:
  action: perform-action
  perform_action: script.awtrix_ng_radio
  data:
    mode: play
    by: station
    value: "SWR3"
```

### 📊 Diagramme

#### `graph` — Balken-/Linien-Diagramm · [`awtrix_ng_graph.yaml`](awtrix_ng_graph.yaml)
Zeichnet **fertige Zahlen**, die du übergibst (max. 16). Für einen echten
**Verlauf über Zeit** brauchst du einen Sammel-Speicher – siehe
[Diagramme & Verläufe](#diagramme--verläufe-historie).

| Feld | Was du einträgst | Beispiel | Pflicht? |
|---|---|---|---|
| `topicname` | App-Name (eindeutig pro Graph). | `solar` | **Ja** |
| `charttype` | Balken / Linie / Fortschritt. | Balken | Nein |
| `values` | Zahlenreihe mit Komma (max. 16). | `3,5,8,4,9` | Ja* |
| `progress` | Nur bei Typ „Fortschritt": Füllstand 0–100. | `75` | Ja* |
| `text` | Optionaler kurzer Text daneben. | `PV` | Nein |
| `icon` | Optionale Icon-Nummer. | `54211` | Nein |
| `color` | Farbe der Balken/Linie. | Gelb | Nein |
| `autoscale` | An = passt sich dem größten Wert an (empfohlen). | an | Nein |
| `duration` | Anzeigedauer (Sekunden). | `8` | Nein |
| `lifetime` | Nach X Sek. verschwinden (0 = bleibt). | `0` | Nein |

\* Je nach `charttype`: `values` bei Balken/Linie, `progress` bei Fortschritt.

**Beispiel — Solar-Verlauf als Balken** senden. Die fertige Zahlenreihe kommt aus
einem Sammel-Sensor (`series`-Attribut, siehe [Beispiele](#beispiele)):
```yaml
alias: Solar-Verlauf als Balken
triggers:
  - trigger: state
    entity_id: sensor.solar_verlauf
actions:
  - action: script.awtrix_ng_graph
    data:
      topicname: solar
      charttype: bar
      values: "{{ state_attr('sensor.solar_verlauf','series') }}"
      color: [255, 190, 0]
      autoscale: true
      duration: 8
mode: single
```

### ⚙️ System

#### `settings (brightness)` — Helligkeit · [`awtrix_ng_settings.yaml`](awtrix_ng_settings.yaml)

| Feld | Was du einträgst | Beispiel | Pflicht? |
|---|---|---|---|
| `autobrightness` | Automatische Helligkeit (Sensor) an/aus. | aus | Nein |
| `brightness` | Feste Helligkeit 0–255 (wenn Auto aus). | `120` | Nein |

**Beispiel — die Uhr abends dunkler** stellen und morgens wieder hell (ein
Trigger für Sonnenuntergang, einer für Sonnenaufgang):
```yaml
alias: AWTRIX nachts dunkler
triggers:
  - trigger: sun
    event: sunset
  - trigger: sun
    event: sunrise
actions:
  - action: script.awtrix_ng_settings
    data:
      autobrightness: false
      brightness: "{{ 30 if trigger.event == 'sunset' else 150 }}"
mode: single
```

#### `reboot` — Uhr neu starten · [`awtrix_ng_reboot.yaml`](awtrix_ng_reboot.yaml)
Nur das Feld `prefix`. Startet die Uhr neu.

**Beispiel — die Uhr jeden Sonntag um 04:00 neu starten:**
```yaml
alias: AWTRIX wöchentlich neu starten
triggers:
  - trigger: time
    at: "04:00:00"
conditions:
  - condition: time
    weekday:
      - sun
actions:
  - action: script.awtrix_ng_reboot
mode: single
```

#### `firmware update` — neue Firmware · [`awtrix_ng_firmware_update.yaml`](awtrix_ng_firmware_update.yaml)
Sonderfall (kein MQTT) – siehe [eigener Abschnitt](#firmware-update-http-kein-mqtt).

| Feld | Was du einträgst | Beispiel | Pflicht? |
|---|---|---|---|
| `ip` | IP/Host der Uhr. | `192.168.1.50` | **Ja** |
| `file` | Pfad zur `.bin` auf dem HA-Server. | `/config/firmware-awtrix-ng.bin` | **Ja** |

**Beispiel — Firmware aufspielen** (einmalig, Entwicklerwerkzeuge → Aktionen;
Voraussetzung: der `shell_command` aus dem [Firmware-Abschnitt](#firmware-update-http-kein-mqtt)):
```yaml
action: script.awtrix_ng_firmware_update
data:
  ip: "192.168.1.50"
  file: "/config/firmware-awtrix-ng.bin"
```

> Bewusst **nicht** enthalten (gefährlich/selten): Factory-Reset,
> WLAN-/System-Konfiguration, Datei-Upload.

---

## Icons finden & auf die Uhr bringen

Icons sind **Nummern**. Das Bild zur Nummer muss **auf der Uhr gespeichert** sein.

1. Nummer aussuchen auf **<https://developer.lametric.com/icons>** (dort steht
   unter jedem Bildchen eine Zahl, z. B. `2422`).
2. In der **AWTRIX-Weboberfläche → Icons** das Icon per Nummer laden/hochladen,
   damit es auf der Uhr liegt.
3. Diese Nummer als `icon` im Skript eintragen.

> Wird ein Icon **nicht angezeigt**, liegt es meist nicht auf der Uhr – erst dort
> hochladen. Ein falscher/fehlender Icon-Wert kann die ganze Anzeige verhindern.

---

## Farben, Effekte & Paletten

**Farbe:** über das **Farbrad** wählen (oder als `[R,G,B]`, z. B. `[255,0,0]`
für Rot).

**Effekte** (Hintergrund, Feld `effect`) – 19 Stück:
`Fade`, `MovingLine`, `BrickBreaker`, `PingPong`, `Radar`, `Checkerboard`,
`Fireworks`, `PlasmaCloud`, `Ripple`, `Snake`, `Pacifica`, `TheaterChase`,
`Plasma`, `Matrix`, `SwirlIn`, `SwirlOut`, `LookingEyes`, `TwinklingStars`,
`ColorWaves`.

**Paletten** (Text-Farbverlauf, Feld `palette`) – 8 Stück:
`Rainbow`, `Cloud`, `Lava`, `Ocean`, `Forest`, `Stripe`, `Party`, `Heat`.

**Overlays** (Wetter über das ganze Bild, Skript `display`):
`rain`, `snow`, `drizzle`, `storm`, `thunder`, `frost`.

> Effekt-/Palettennamen und verfügbare Sounds sind **geräteabhängig**. Was deine
> Uhr kann, zeigt `GET /api/v1/capabilities` bzw. das Dateisystem der Uhr.

---

## Diagramme & Verläufe (Historie)

Das **`graph`-Skript zeichnet nur Zahlen, die du ihm gibst** (max. 16). Es kennt
die Vergangenheit eines Sensors **nicht** – und HA-Vorlagen können die
Sensor-Historie leider nicht direkt auslesen.

**Willst du einen echten Verlauf** („Solar der letzten Stunde"), brauchst du
einen kleinen **Sammel-Speicher**, der alle paar Minuten einen Wert ablegt.
Zwei erprobte Wege:

1. **Template-Sensor mit rollender Liste** (siehe [Beispiele](#beispiele)):
   ein Sensor, der die letzten *N* Werte im Attribut `series` hält; eine
   Automation schickt `series` an `graph`.
2. **`input_text`-Helfer als Puffer:** eine Automation hängt alle paar Minuten
   den aktuellen Wert an und übergibt die Liste an `graph`.

Beides läuft in HA. (Wer die Uhr selbst sammeln lassen will – ganz ohne
HA-Helfer – kann ein On-Device-**Berry-Script** nutzen; das ist Bastelei auf dem
Gerät und hier bewusst nicht im Repo.)

**Merke:** ohne Speicher kein Verlauf. Für einen **Momentanwert** reicht dagegen
`graph` mit Typ **Fortschritt** (`progress`) oder eine einfache `new app`.

---

## Beispiele

**Jedes Beispiel aus der [Skript-Referenz](#skript-referenz-jedes-feld-erklärt)
liegt auch als fertige Datei im Ordner [`examples/`](examples)** zum Kopieren
bzw. Importieren – oben in jeder Datei steht kurz, wie man sie einbindet
(Automation, Aktion oder Dashboard-Karte).

Ein größeres, mehrteiliges Beispiel:

| Beispiel | Dateien | Was es macht |
|---|---|---|
| **Solar-Verlauf** | [`solar_verlauf_sensor.yaml`](examples/solar_verlauf_sensor.yaml) + [`solar_verlauf_automation.yaml`](examples/solar_verlauf_automation.yaml) | Zeigt die Solarleistung der letzten Stunde als **Balkendiagramm** über `graph`. |

**Solar-Verlauf einrichten:**
1. Inhalt von `solar_verlauf_sensor.yaml` in die `configuration.yaml` unter
   `template:` einfügen (rollender Puffer, alle 5 Min ein Wert, letzte 12 =
   1 Stunde) → HA neu starten / Template-Entitäten neu laden. Ergibt
   `sensor.solar_verlauf` mit Attribut `series`.
2. `solar_verlauf_automation.yaml` als Automation importieren – sie schickt die
   Reihe bei jeder Aktualisierung ans `graph`-Skript.

> Anpassen: `sensor.solar_leistung_watt` durch deinen Sensor ersetzen; `[-12:]`
> bzw. `minutes: "/5"` für einen anderen Zeitraum; `charttype: line` für Linie;
> `color` für die Balkenfarbe.

---

## Firmware-Update (HTTP, kein MQTT)

AWTRIX NG kennt für Firmware-Updates **keinen MQTT-Befehl** und kein OTA-per-URL –
die Firmware wird als `.bin` per **HTTP-Multipart** hochgeladen (`POST /update`).
Das neue Image wird erst nach vollständiger Prüfung aktiviert – ein abgebrochener
Upload ist also ungefährlich.

**Manuell** (von jedem PC) oder über die Weboberfläche der Uhr:
```bash
curl -X POST http://<ip>/update -F "firmware=@firmware-awtrix-ng.bin"
```

**Aus Home Assistant** (Skript [`awtrix_ng_firmware_update.yaml`](awtrix_ng_firmware_update.yaml)):
1. Firmware-`.bin` auf den HA-Server legen, z. B. `/config/firmware-awtrix-ng.bin`.
2. In `configuration.yaml` ergänzen:
   ```yaml
   shell_command:
     awtrix_ng_firmware_update: >-
       curl -sS -X POST "http://{{ ip }}/update" -F "firmware=@{{ file }}"
   ```
3. HA neu starten (oder YAML neu laden), dann das Skript importieren.
4. Skript mit `ip` (z. B. `192.168.1.50`) und `file` (Pfad zur `.bin`) aufrufen.

> **Voraussetzung:** `curl` muss in der HA-Umgebung verfügbar sein (bei HA OS /
> Container meist vorhanden). Fehlt es, den Upload von einem PC oder über das
> Add-on **„Advanced SSH & Web Terminal"** ausführen. Lade die passende Datei –
> `firmware-awtrix-ng.bin` für ein Gerät, das bereits NG läuft.

---

## Fehlerbehebung / FAQ

**Es passiert gar nichts auf der Uhr.**
- Stimmt der **`prefix`** (Settings → MQTT der Uhr, meist `awtrixng`)?
- Redet die Uhr überhaupt per MQTT? → Test unter
  [Voraussetzungen](#voraussetzungen) (Thema `#` mithören).
- Ist die **MQTT-Integration** in HA eingerichtet und der Broker online?

**„Das Skript hat einen Fehler beim Ausführen" / nichts erscheint, obwohl gesendet.**
AWTRIX NG prüft die Nachricht **streng**: ein einziger ungültiger Wert lässt den
**ganzen** Befehl scheitern. Häufigste Ursache: ein **Icon**, das nicht auf der
Uhr liegt, oder ein **Effekt-/Sound-Name**, den deine Uhr nicht hat. Erst ohne
Icon/Effekt testen, dann ergänzen.

**Der Text ist abgeschnitten.**
Er scrollt automatisch, wenn er zu lang ist. Prüfe `scrollmode`/`scrollspeed`,
oder kürze den Text.

**Meine App erscheint nicht im Durchlauf.**
Hast du `app order` benutzt? Dann sind **nur** die dort gelisteten Apps sichtbar –
deine neue App mit in die `order` aufnehmen. Oder `showimmediately: an` bei
`new app`, um direkt hinzuspringen.

**Umlaute (ä/ö/ü) sehen komisch aus.**
Die Pixel-Schrift ist sehr klein; nutze wo möglich `ae/oe/ue` oder kurze Texte.

**Ich habe zwei Uhren.**
Jede hat einen eigenen `prefix`. Rufe das Skript einfach zweimal auf (einmal je
Prefix) oder baue zwei Automationen.

**Wo sehe ich, was rausgeht?**
**Entwicklerwerkzeuge → MQTT → Nachrichten anhören**, Thema `awtrixng/#`. Dort
siehst du live die Befehle, die die Skripte senden.

---

## MQTT-Kurzreferenz (für Fortgeschrittene)

Was die Skripte intern senden – nützlich zum Debuggen oder für eigene Automationen.

| Zweck | Topic | Payload |
|---|---|---|
| Pushed App anlegen/ändern | `<prefix>/cmd/apps/pushed/<name>` | App-JSON |
| Pushed App löschen | `<prefix>/cmd/apps/pushed/<name>` | *(leer)* oder `{}` |
| App wechseln | `<prefix>/cmd/apps/switch` | `{"name":"..","fast":true}` |
| Nächste / Vorherige App | `<prefix>/cmd/apps/next` · `.../apps/previous` | *(leer)* |
| App-Reihenfolge | `<prefix>/cmd/apps/order` | `{"order":[..],"disabled":[..]}` |
| Notification | `<prefix>/cmd/notify` | Notify-JSON |
| Notification verwerfen | `<prefix>/cmd/notify/dismiss[/<name>]` | *(leer)* |
| Display / Overlay | `<prefix>/cmd/display` | `{"power":true,"overlay":"rain"}` |
| Moodlight | `<prefix>/cmd/display/moodlight` | `{"color":[..],"brightness":120}` / *(leer)* = aus |
| Indicators | `<prefix>/cmd/indicators/1..3` | `{"color":[..],"blinkMs":500}` / `{}` = aus |
| Sound | `<prefix>/cmd/sounds/play` · `.../sounds/stop` | `{"name":".."}` / `{"rtttl":".."}` / `{"builtin":".."}` |
| Radio | `<prefix>/cmd/radio/play` · `.../radio/stop` | `{"station":".."}` / `{"index":0}` / `{"url":".."}` |
| Einstellungen | `<prefix>/cmd/settings` | `{"brightness":120,"autoBrightness":false}` |
| Neustart | `<prefix>/cmd/device/reboot` | *(leer)* |

Offizielle Doku: <https://blueforcer.github.io/awtrix-ng/>

---

## Mitmachen & Lizenz

- **Fehler gefunden oder Skript-Wunsch?** Öffne ein
  [Issue](https://github.com/x1marc/ha-awtrix-ng-scripts/issues/new/choose) –
  es gibt fertige Vorlagen (Fehler melden / Skript-Wunsch).
- **Änderungen** stehen im [CHANGELOG.md](CHANGELOG.md).
- Jeder Push wird per **GitHub-Action** automatisch auf YAML-Fehler geprüft
  (`tools/validate.py` – lokal ausführbar mit `python tools/validate.py`).
- Lizenz: [MIT](LICENSE).
