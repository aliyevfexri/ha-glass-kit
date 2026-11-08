# Changelog

All notable changes to this kit. Versions follow [Semantic Versioning](https://semver.org/); template names and variables are the public API.

## [Unreleased]

### Added
- `kit_youtube_header`, `kit_youtube_row`: YouTube search status line and result rows for a speaker pop-up (tap plays the audio on that speaker; needs the `yt_audio` integration and a Music Assistant player).
- `kit_toggle`: on/off control as a row (light, switch, input_boolean), for pop-ups.
- `kit_setpoint`: number setting with − / + as a row (`number.*`, `input_number.*`), for pop-ups.
- `kit_appliance`: `popup` (tap opens a bubble-card pop-up instead of the history graph), `toggle` / `toggle_icon` / `toggle_color` (round quick button, e.g. oven light), `alert` / `alert_text` (red status pill driven by a helper), progress bar while active.
- `kit_banner`: coloured pop-up header with big numbers side by side.
- `kit_value`: square info tile (icon, name, big value), two per row in pop-ups.
- `kit_toggle`: `square: true` for a square tile with a big On/Off, matching `kit_value` height.
- Theme: icon colours for HA's own pages in both modes (sidebar icons, area and tile icons, summary colours); dark mode no longer keeps HA's light-mode icon tokens (navy icons on navy).

### Changed
- `kit_appliance` layout: status pill top right, quick button beside the value; binary sensors on the label line use HA's wording (Open / Closed instead of on / off). Existing configs keep working.
- `kit_appliance`: fixed grid rows, icon top left, label line and progress bar always reserve their space, so appliance tiles in one row are the same height.

### Fixed
- `kit_appliance`: `alert_text` default is now empty, so the `Alert` fallback for `alert_states` shows (it was always `Done`).

## [0.1.0] - 2026-11-07
First public release.

### Added
- Theme `glass` with dark and light modes; all design tokens as `--kit-*` variables, plus HA variables so core cards, top bar, sidebar and bubble-card footer match.
- Templates: `kit_tile` (base), `kit_button`, `kit_spacer`, `kit_heat_room`, `kit_sensor_room`, `kit_heat_overview`, `kit_appliance`, `kit_weather`, `kit_media`, `kit_stats`.
- `tools/build_ui.py`: inlines the templates into one dashboard for UI mode.
- Examples `minimal.yaml` and `full.yaml`; docs for components, design system, layout and new components; interactive layout mockup.
- CI: yamllint and a build of every example.
