# Components

Every component is a `custom:button-card` template. Use it with `type: custom:button-card` and `template: <name>`. Standard button-card options (`name`, `icon`, `tap_action`, `hold_action`, `styles`...) work on every component and override the template. Kit-specific options go under `variables:`.

All variables are optional unless marked **required**. A missing or unavailable entity never breaks a tile: values show "—", the tile dims, and its buttons do nothing.

Sizes: `grid_options: {columns: 6, rows: auto}` for a normal tile, `columns: 12` for a wide one. Always `rows: auto`.

- [kit_heat_room](#kit_heat_room)
- [kit_sensor_room](#kit_sensor_room)
- [kit_heat_overview](#kit_heat_overview)
- [kit_appliance](#kit_appliance)
- [kit_toggle](#kit_toggle)
- [kit_setpoint](#kit_setpoint)
- [kit_weather](#kit_weather)
- [kit_media](#kit_media)
- [kit_youtube_header / kit_youtube_row](#kit_youtube_header--kit_youtube_row)
- [kit_stats](#kit_stats)
- [kit_spacer](#kit_spacer)
- [kit_tile](#kit_tile)
- [kit_button](#kit_button)

---

## kit_heat_room
One heated room with a thermostat. Big number = current temperature. − / + change the target by the entity's `target_temp_step` (default 0.5), clamped to `min_temp` / `max_temp`. The icon turns orange while `hvac_action` is `heating`.

**Entity** (**required**): a `climate.*` entity (generic thermostat, TRV, smart thermostat).

| Variable | Type | Default | Meaning |
|---|---|---|---|
| `humidity` | entity id | `null` | Humidity sensor shown on the label line |
| `next_step` | entity id | `null` | Sensor whose state is the next schedule step text, shown as "Next: …" |
| `sensor` | entity id | `null` | The temperature sensor behind the thermostat. When it is `unavailable` / `unknown` the badge says **Sensor offline** and the icon turns red. Recommended: a thermostat keeps the last reading and hides a dead sensor |

Badge: Heating / Idle / Off / Sensor offline.

```yaml
type: custom:button-card
template: kit_heat_room
entity: climate.living_room
name: Living room
variables:
  humidity: sensor.living_room_humidity
  sensor: sensor.living_room_temperature
grid_options: {columns: 6, rows: auto}
```

## kit_sensor_room
A room with a temperature sensor but no heating control. No buttons, so nothing to press by mistake.

**Entity** (**required**): a temperature `sensor.*`.

| Variable | Type | Default | Meaning |
|---|---|---|---|
| `humidity` | entity id | `null` | Humidity sensor |
| `battery` | entity id | `null` | Battery % sensor, shown as "Battery 87%" |
| `note` | text | `Not heated` | Badge text; `""` hides it |

```yaml
type: custom:button-card
template: kit_sensor_room
entity: sensor.office_temperature
name: Office
variables:
  humidity: sensor.office_humidity
  battery: sensor.office_battery
grid_options: {columns: 6, rows: auto}
```

## kit_heat_overview
All heated rooms in one wide tile: a row per room with current → target and a dot when it is heating, plus an optional boiler relay badge.

**Entity**: none needed. Set `tap_action` to open a pop-up with the thermostats.

| Variable | Type | Default | Meaning |
|---|---|---|---|
| `rooms` | list of `{name, climate}` | `[]` | Rooms in display order |
| `boiler` | entity id | `null` | Boiler relay `switch.*`; badge shows "Boiler on" / "Boiler off" |

```yaml
type: custom:button-card
template: kit_heat_overview
variables:
  rooms:
    - {name: Living room, climate: climate.living_room}
    - {name: Bedroom, climate: climate.bedroom}
  boiler: switch.boiler
tap_action:
  action: navigate
  navigation_path: "#heating"
grid_options: {columns: 12, rows: auto}
```

## kit_appliance
Any appliance or two-state device: washer, dryer, dishwasher, oven, fridge, a door. The main value is the state (prettified or renamed), the label line collects details. Active states colour the icon blue, alert states red.

**Entity** (**required**): the appliance's main state entity (any domain). Set `icon:` to match the device.

| Variable | Type | Default | Meaning |
|---|---|---|---|
| `active_states` | list | `["on", running, run]` | States that mean "working" (lower case) |
| `alert_states` | list | `[open, finished, done]` | States that need attention (lower case) |
| `state_names` | map | `{}` | Rename states, e.g. `{"on": Open, "off": Closed}` |
| `detail` | entity id | `null` | One extra entity on the label line |
| `detail_unit` | text | `''` | Appended to `detail` |
| `details` | list of `{entity, unit, label}` | `[]` | More extras, e.g. freezer temperature |
| `progress` | entity id | `null` | Percent sensor, shown while active ("70%") |
| `finish` | entity id | `null` | Timestamp sensor, shown while active ("ready 14:20") |
| `alert` | entity id | `null` | Extra entity that raises the alert look while it is `on` (e.g. an `input_boolean` "washer done" set by an automation) |
| `alert_text` | text | `null` | Text of the red status pill; empty shows `Done` while `alert` is on and `Alert` for `alert_states` |
| `popup` | text | `null` | bubble-card pop-up hash (e.g. `"#oven"`); tapping the tile opens it instead of more-info |
| `toggle` | entity id | `null` | Light / switch for the round quick button (e.g. oven lamp); tap toggles it |
| `toggle_icon` | icon | `mdi:lightbulb` | Quick button icon |
| `toggle_color` | CSS colour | `var(--kit-sun)` | Quick button colour while on |

Layout: icon (top left) + red status pill (only when something needs attention), name, value with the quick button beside it, label line, progress bar while active. Rows are fixed and the label line and progress bar always keep their space, so tiles in one row have the same height whether or not they have a button, label or progress. Binary sensors on the label line use HA's own words (door: Open / Closed). Quote colours with a `#` (`"var(--kit-cool, #64d2ff)"`), or YAML reads the rest as a comment.

Quote `"on"`, `"off"`, `"yes"`, `"no"` in lists and maps, or YAML turns them into booleans.

```yaml
# Washer
type: custom:button-card
template: kit_appliance
entity: sensor.washer_state
name: Washer
icon: mdi:washing-machine
variables:
  active_states: [run, running]
  alert_states: [finished, done]
  progress: sensor.washer_progress
  finish: sensor.washer_completion_time
grid_options: {columns: 6, rows: auto}
```
```yaml
# Fridge door + temperatures
type: custom:button-card
template: kit_appliance
entity: binary_sensor.fridge_door
name: Fridge
icon: mdi:fridge-outline
variables:
  active_states: []
  alert_states: ["on"]
  state_names: {"on": Open, "off": Closed}
  details:
    - {entity: sensor.fridge_temperature, unit: " °C"}
    - {entity: sensor.freezer_temperature, unit: " °C", label: freezer}
grid_options: {columns: 6, rows: auto}
```

```yaml
# Oven with a light button that opens a pop-up
type: custom:button-card
template: kit_appliance
entity: sensor.oven_machine_state
name: Oven
icon: mdi:stove
variables:
  popup: "#oven"
  toggle: light.oven_light
  active_states: [running]
  state_names: {ready: "Off", running: Cooking}
grid_options: {columns: 6, rows: auto}
```

## kit_toggle
One on/off control as a full-width glass row: icon, name, optional note, On/Off pill. Tap toggles. Made for pop-ups (oven light, Power Cool, "laundry waiting").

**Entity** (**required**): anything `homeassistant.toggle` understands (light, switch, input_boolean, fan...).

| Variable | Type | Default | Meaning |
|---|---|---|---|
| `on_color` | CSS colour | `var(--kit-accent)` | Icon and pill colour while on |
| `note` | text | `''` | Small text under the name |
| `square` | bool | `false` | Square tile instead of a row: icon, small name, big On/Off stacked and centred (112 px high, same as `kit_value`). Put two side by side in a 2-column `grid`, like the SmartThings app |

```yaml
type: custom:button-card
template: kit_toggle
entity: switch.fridge_power_cool
name: Power Cool
icon: mdi:snowflake
variables:
  on_color: "var(--kit-cool, #64d2ff)"
  note: Fast cooling of the fridge
```

## kit_setpoint
A number setting as a glass row with − / +. Step, min and max come from the entity's attributes; the note line shows the range unless you set `note`.

**Entity** (**required**): a `number.*` or `input_number.*` entity.

| Variable | Type | Default | Meaning |
|---|---|---|---|
| `note` | text | `''` | Replaces the "Range a to b" line |

```yaml
type: custom:button-card
template: kit_setpoint
entity: number.fridge_temperature
name: Fridge temperature
icon: mdi:fridge-top
```

## kit_banner
Coloured header for a pop-up: two or three big numbers side by side on a gradient (fridge / freezer temperature, oven now / target). Read-only; tap does nothing.

**Entity**: none; list the values in `items`.

| Variable | Type | Default | Meaning |
|---|---|---|---|
| `items` | list of `{label, entity, unit}` | `[]` | Values to show; unavailable shows `—` |
| `gradient` | CSS background | blue gradient | e.g. `"linear-gradient(135deg, #ff9f0a 0%, #ff6b35 100%)"` for an oven |
| `note` | text | `''` | Small line under the values |

```yaml
type: custom:button-card
template: kit_banner
variables:
  items:
    - {label: Fridge, entity: sensor.fridge_temperature, unit: "°C"}
    - {label: Freezer, entity: sensor.freezer_temperature, unit: "°C"}
```

## kit_value
Square info tile: centred icon, small name, big value. For settings and states shown two per row in a pop-up (washer temperature and spin, oven mode, door). 112 px high, same as a square `kit_toggle`. Tap opens more-info (a `select` can be changed there).

**Entity** (**required**): any entity; its state is the value (binary sensors use HA's wording).

| Variable | Type | Default | Meaning |
|---|---|---|---|
| `unit` | text | `''` | Appended to the value, e.g. `" rpm"` |
| `state_names` | map | `{}` | Rename states |
| `icon_color` | CSS colour | `var(--kit-accent)` | Icon colour |

```yaml
type: grid
columns: 2
square: false
cards:
  - type: custom:button-card
    template: kit_value
    entity: select.washer_water_temperature
    name: Temp.
    icon: mdi:thermometer
    variables: {unit: "°C", icon_color: "var(--kit-alert, #ff453a)"}
  - type: custom:button-card
    template: kit_value
    entity: select.washer_spin_level
    name: Spin
    icon: mdi:autorenew
    variables: {unit: " rpm"}
```

## kit_weather
Current weather: coloured condition icon, temperature, condition name, humidity and wind. No forecast: HA only returns forecasts through the `weather.get_forecasts` action, which a tile cannot call.

**Entity** (**required**): a `weather.*` entity (e.g. Met.no `weather.home`). No variables.

```yaml
type: custom:button-card
template: kit_weather
entity: weather.home
grid_options: {columns: 12, rows: auto}
```

## kit_media
A speaker or media player. Shows title and artist while playing or paused, volume as the badge, and round buttons for volume −, play/pause, volume +.

**Entity** (**required**): a `media_player.*`. No variables. Works best full width (`columns: 12`) so long titles fit.

```yaml
type: custom:button-card
template: kit_media
entity: media_player.living_room_speaker
name: Speaker
grid_options: {columns: 12, rows: auto}
```

## kit_youtube_header / kit_youtube_row
YouTube search results inside a speaker pop-up: a status line ("Searching…", "8 results for …") and up to 8 result rows (thumbnail, title, channel · length). Tapping a row plays the video's **audio** on the speaker. Needs a backend with this contract (the author's is a small yt-dlp based custom integration called `yt_audio`, not part of the kit): a sensor whose attribute `results` is a list of `{id, title, channel, duration}` (and optional `now_playing: {<player>: {id}}`), and an action `yt_audio.play` with `entity_id` + `video_id`. The player is best a Music Assistant player (seek bar, AirPlay 2 to HomePods). The row for the video that this speaker plays shows "▶ Playing".

**Entity** (**required**, both): the results sensor `sensor.youtube_results`.

| Template | Variable | Default | Meaning |
|---|---|---|---|
| `kit_youtube_header` | `search_entity` | `input_text.youtube_search` | the text field people type into |
| `kit_youtube_row` | `index` (**required**) | `0` | which result, 0..7 |
| `kit_youtube_row` | `player` (**required**) | — | `media_player.*` that plays (Music Assistant player) |

```yaml
# inside a bubble-card pop-up, one per speaker
- type: media-control                 # now playing + seek bar
  entity: media_player.kitchen_speaker
- type: entities
  entities:
    - entity: input_text.youtube_search
      name: Search YouTube
- type: custom:button-card
  template: kit_youtube_header
  entity: sensor.youtube_results
- type: custom:button-card
  template: kit_youtube_row
  entity: sensor.youtube_results
  variables: {index: 0, player: media_player.kitchen_speaker}
# ... repeat the row with index 1..7
```

## kit_stats
Two or three numbers side by side with small captions. Non-numeric values show "—".

**Entity**: optional, only used for the tap (more-info).

| Variable | Type | Default | Meaning |
|---|---|---|---|
| `items` | list of `{name, entity, unit, decimals}` | `[]` | One cell per item. `unit` defaults to the entity's unit, `decimals` to 0 |

```yaml
type: custom:button-card
template: kit_stats
name: Energy
icon: mdi:lightning-bolt
variables:
  items:
    - {name: Power, entity: sensor.house_power, unit: W}
    - {name: Today, entity: sensor.house_energy_today, unit: kWh, decimals: 1}
grid_options: {columns: 6, rows: auto}
```

## kit_spacer
Empty, invisible block whose height is the `--kit-bottom-space` token (110 px). Put it last in a full-width last section when the view has a fixed footer bar, so the last row can scroll above it. No options.

```yaml
type: custom:button-card
template: kit_spacer
grid_options: {columns: 12, rows: auto}
```

## kit_tile
The base of every component: glass surface, slot grid, dimmed unavailable state. You can use it directly for a simple read-only tile, or extend it in your own template (see [new-component.md](new-component.md)).

Slots (grid areas): `i` icon, `b` badge (top right), `n` name, `v` main value, `l` label line. Fill `b`, `v`, `l` with `custom_fields`.

```yaml
type: custom:button-card
template: kit_tile
entity: sensor.co2
name: CO₂
icon: mdi:molecule-co2
custom_fields:
  v: '[[[ return entity ? entity.state + " ppm" : "—"; ]]]'
grid_options: {columns: 6, rows: auto}
```

## kit_button
Round 44 px outlined button, used inside components for − / + and media controls. Set `icon` and `tap_action` where you use it.

```yaml
type: custom:button-card
template: kit_button
icon: mdi:lightbulb-group
tap_action:
  action: perform-action
  perform_action: light.toggle
  target:
    entity_id: light.living_room
```
