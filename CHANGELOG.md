# Changelog

All notable changes to this kit. Versions follow [Semantic Versioning](https://semver.org/); template names and variables are the public API.

## [Unreleased]

## [0.1.0] - 2026-11-07
First public release.

### Added
- Theme `glass` with dark and light modes; all design tokens as `--kit-*` variables, plus HA variables so core cards, top bar, sidebar and bubble-card footer match.
- Templates: `kit_tile` (base), `kit_button`, `kit_spacer`, `kit_heat_room`, `kit_sensor_room`, `kit_heat_overview`, `kit_appliance`, `kit_weather`, `kit_media`, `kit_stats`.
- `tools/build_ui.py`: inlines the templates into one dashboard for UI mode.
- Examples `minimal.yaml` and `full.yaml`; docs for components, design system, layout and new components; interactive layout mockup.
- CI: yamllint and a build of every example.
