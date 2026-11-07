# Contributing

Thanks for helping. Issues and pull requests are welcome: bugs, new components, theme fixes, docs.

## Reporting a bug
Open an issue with: Home Assistant version, button-card / bubble-card versions, browser and device, the card YAML you used (with your entity ids replaced if you prefer), what you expected and what you saw. A screenshot helps.

## Pull requests
1. Fork, branch from `main`, keep the change focused.
2. Follow the rules in [docs/design-system.md](docs/design-system.md) and, for a new device type, the checklist in [docs/new-component.md](docs/new-component.md):
   - one component per file, `template: kit_tile` first, tokens only (with the dark fallback), no hard-coded entity ids;
   - plain JavaScript in `[[[ ]]]` (no `?.` or `??`) so older Safari keeps working;
   - quote `"on"` / `"off"` / `"yes"` / `"no"` in YAML.
3. Document it: header comment in the template, a row in `README.md`, a section in `docs/components.md`, a line under `[Unreleased]` in `CHANGELOG.md`.
4. Run the checks CI runs:
   ```sh
   pip install pyyaml yamllint
   yamllint --strict .
   for f in examples/*.yaml; do python3 tools/build_ui.py "$f" > /dev/null; done
   ```
5. Test in Home Assistant: entity on, off and unavailable; phone and laptop width; dark and light mode.

## Licence and originality
By contributing you agree your work is released under the [MIT licence](LICENSE). Only submit code you wrote yourself or that carries a compatible licence; do not copy unlicensed dashboard code from forums or other repos.
