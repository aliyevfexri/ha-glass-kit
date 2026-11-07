# Adding a component for a new device type

Example: a light relay, a roller shade, a camera, a service status.

## Checklist
1. **One device type = one file** `templates/kit_<type>.yaml`, template name `kit_<type>`.
2. `template: kit_tile` first line; do not restyle `card` (surface, radius, blur come from the base).
3. **Entity in, variables for extras.** The main entity is `entity:`; every other entity is a variable with default `null`, and the component must work when it is missing.
4. Fill the slots: `icon`, `b` (badge), `v` (main value), `l` (label line), optional `c` (controls). Add a slot only by extending `grid-template-areas`, keep the order i/b, n, v, l, c.
5. Colours and sizes only from tokens, always with the dark fallback: `var(--kit-accent, #0a84ff)`. If a new colour is needed, add a token to the theme (both modes) first.
6. Actions: use `perform-action` with explicit `target.entity_id`; clamp numbers to the entity's min/max.
7. States: map the device's states to the vocabulary in `design-system.md` (working / idle / attention / unavailable).
8. Plain JavaScript in `[[[ ]]]` (no `?.` / `??`), handle `entity` missing, and never print `unavailable` / `unknown` / `none` as a value: skip it or show "—".
8a. YAML: quote `"on"`, `"off"`, `"Off"`, `"yes"`, `"no"` in state lists and maps; HA's YAML turns them into booleans.
9. Document it: header comment in the file (purpose, entity, variables), a row in `README.md`, a section in `docs/components.md`, a line in `CHANGELOG.md`.
10. Test: on, off, unavailable entity, phone width and tablet width, dark and light.

## Skeleton
```yaml
# kit_<type>: <one line purpose>. entity = <domain>. variables: <name>: <what> (optional)
kit_<type>:
  template: kit_tile
  icon: mdi:<icon>
  variables:
    extra: null
  styles:
    icon:
      - color: >
          [[[ return entity && entity.state === 'on' ? 'var(--kit-accent)' : 'var(--kit-off)'; ]]]
  custom_fields:
    b: '[[[ return entity ? (entity.state === "on" ? "On" : "Off") : ""; ]]]'
    v: '[[[ return entity ? entity.state : "—"; ]]]'
    l: '[[[ return variables.extra && states[variables.extra] ? states[variables.extra].state : ""; ]]]'
  tap_action:
    action: toggle
```

## Planned components (not written yet)
| Component | Entity | Notes |
|---|---|---|
| `kit_light` | `light.*` / `switch.*` | toggle on tap, brightness only if supported |
| `kit_shade` | `cover.*` | open / stop / close buttons, position % as value |
| `kit_camera` | `camera.*` | snapshot as background, tap = live view (core picture card inside) |
| `kit_service` | Uptime Kuma or other up/down sensors | up/down as badge, alert colour when down |
| `kit_room_summary` | several | per-room tile: temperature + lights on count + shades |
