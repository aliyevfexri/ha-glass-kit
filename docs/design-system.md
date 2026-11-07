# Design system

The kit has three layers. Change things in the lowest layer that can do it.

1. **Tokens** (`theme/glass.yaml`): colours, blur, radius, spacing, font sizes. The only place values live.
2. **Base tile** (`templates/kit_tile.yaml`): surface, slot grid, unavailable state. Uses tokens only.
3. **Components** (`templates/kit_*.yaml`): one per device type. Extend `kit_tile`, fill slots, use tokens only. No hard-coded colours, sizes in px only for touch targets (44 px) and icons.

## Tokens
| Token | Use |
|---|---|
| `--kit-bg` | Page background (layered gradients, no image): must be colourful, see "Why it looks like glass" |
| `--kit-surface`, `--kit-surface-strong` | Tile glass, buttons on a tile |
| `--kit-stroke` | 1 px tile border |
| `--kit-shadow` | Light top edge (inset highlight) + soft drop shadow |
| `--kit-button-stroke` | Outline of round buttons |
| `--kit-sun` | Sunny weather icon |
| `--kit-bottom-space` | Height of `kit_spacer` |
| `--kit-blur` | `backdrop-filter` of tiles (with `-webkit-` prefix for Safari) |
| `--kit-radius`, `--kit-radius-small` | Tile and inner element corners |
| `--kit-pad`, `--kit-gap` | Tile padding, spacing between inner elements |
| `--kit-text`, `--kit-text-dim` | Primary and secondary text |
| `--kit-accent` | Active/on (lights on, appliance running) |
| `--kit-heat` / `--kit-cool` | Heating / cooling right now |
| `--kit-ok` / `--kit-alert` | Good / needs attention |
| `--kit-off` | Off or idle icons |
| `--kit-font` | System font stack (SF Pro on Apple, Roboto/Segoe elsewhere) |
| `--kit-size-value`, `--kit-size-name`, `--kit-size-label` | Main number, tile name, small label |

Templates always write tokens with a fallback, `var(--kit-stroke, rgba(255, 255, 255, 0.24))` (the dark value), so the kit renders without the theme. When a token changes in the theme, update the fallbacks too (a sed over `templates/` is enough).

## Why it looks like glass
Frosted glass only shows when there is something colourful behind it to blur. Draft 1 had a near-black page, so `backdrop-filter` had nothing to work with and tiles read as flat grey boxes. What makes it work (2026-11-07):
1. **Background with colour and shape**: deep blue base, a light glow at the top, a thin light arc, a teal glow bottom right, dark corners. Layered CSS gradients, no image.
2. **Surface is a light gradient, not a flat tint**: white 17 % top-left to 5 % bottom-right.
3. **Edges**: 1 px light border plus an inset top highlight (`--kit-shadow`) so the tile edge catches light, and a soft drop shadow to lift it.
4. **Blur with little saturation**: `blur(28px) saturate(115%)`. High saturation turns the tiles into solid blue buttons.
5. **Outlined round buttons** instead of filled ones.
HA's top bar and sidebar only follow the theme when a device picks it (Profile → Theme → glass); a view `theme:` does not reach them. Footer pills follow the theme (`bubble-main-background-color`). Bubble-card pop-ups ignore theme variables for their backdrop: set `bg_color`, `bg_opacity`, `bg_blur` on each pop-up card.

Dark and light mode are both defined; HA picks by device setting unless the theme mode is forced.

## Tile anatomy
```
┌─────────────────────────┐
│ [i]               [b]   │  i = icon (state colour)   b = badge: short status ("Heating", "Not heated")
│                         │
│ n  Name                 │  n = name (room or device)
│ v  21.5°                │  v = main value (the one thing to read at a glance)
│ l  45% humidity · …     │  l = label line (secondary facts, joined with " · ")
│ c  [-]   22°   [+]      │  c = controls (optional, only components that act)
└─────────────────────────┘
```
Rules:
- One main value per tile. If you need two big numbers, it is two tiles.
- Icon colour carries the state: `--kit-heat` heating, `--kit-accent` active, `--kit-alert` needs attention, `--kit-off` otherwise.
- Badge text is one or two words.
- Tap on the tile = more-info (default). Controls are explicit buttons, never a hidden long-press.
- Unavailable/unknown entity: the tile dims (opacity 0.45) and values show "—". Never hide a broken tile.

## Sizes (sections grid, 12 columns per section)
| Size | `grid_options` | Use |
|---|---|---|
| Small | `columns: 6, rows: auto` | Appliance, simple sensor |
| Room | `columns: 6, rows: auto` | Room with controls |
| Wide | `columns: 12, rows: auto` | Overviews (heating, cameras later) |
Use `rows: auto`: button-card sizes itself, a fixed row count leaves empty gaps. Sections reflow by themselves: 1 column on a phone, 2–3 on a tablet or laptop (`max_columns` on the view). Do not set fixed widths.

## States vocabulary
| Meaning | Icon colour | Badge examples |
|---|---|---|
| Working now (heating, running, on) | heat / accent | Heating, Running, On |
| Idle / off | off | Idle, Off |
| Needs attention | alert | Open, Finished, Low battery |
| Unavailable | dimmed tile | — |

## Old and small browsers
Use `-webkit-backdrop-filter` next to `backdrop-filter`; avoid `:has()`, container queries and other new CSS in templates. JavaScript templates stay plain (no optional chaining `?.`, no `??`) so older Safari keeps working where HA itself still loads.
