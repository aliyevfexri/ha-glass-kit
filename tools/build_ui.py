#!/usr/bin/env python3
"""Build a dashboard for Home Assistant's UI mode from a kit dashboard YAML.

UI-mode dashboards (the default kind, edited in the browser) have no `!include`,
so the kit templates must be pasted inline. This script reads your dashboard
YAML, replaces `button_card_templates: !include_dir_merge_named ...` with the
contents of every template file, and prints one YAML document you can paste
into the dashboard's raw configuration editor.

usage:
  python3 tools/build_ui.py examples/full.yaml > out.yaml
  python3 tools/build_ui.py my-dashboard.yaml --templates templates -o out.yaml

Needs PyYAML (`pip install pyyaml`).
"""
import argparse
import glob
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEMPLATES = os.path.join(HERE, "..", "templates")
MARK = "__KIT_TEMPLATES__"


class Loader(yaml.SafeLoader):
    pass


# The include path inside the dashboard is ignored: templates come from --templates.
Loader.add_constructor("!include_dir_merge_named", lambda loader, node: MARK)


class Dumper(yaml.SafeDumper):
    pass


def _str(dumper, data):
    # Multi-line strings (button-card JavaScript) as literal blocks, so the output stays readable.
    style = "|" if "\n" in data else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


Dumper.add_representer(str, _str)


def load_templates(tpl_dir):
    templates = {}
    paths = sorted(glob.glob(os.path.join(tpl_dir, "*.yaml")))
    if not paths:
        sys.exit(f"error: no *.yaml templates in {tpl_dir}")
    for p in paths:
        with open(p, encoding="utf-8") as f:
            data = yaml.load(f, Loader=Loader) or {}
        for name in data:
            if name in templates:
                sys.exit(f"error: template {name} defined twice ({p})")
        templates.update(data)
    return templates


def build(dash_path, tpl_dir):
    with open(dash_path, encoding="utf-8") as f:
        dash = yaml.load(f, Loader=Loader)
    if not isinstance(dash, dict) or "views" not in dash:
        sys.exit(f"error: {dash_path} is not a dashboard (no `views:`)")
    current = dash.get("button_card_templates")
    templates = load_templates(tpl_dir)
    if current == MARK or current is None:
        dash["button_card_templates"] = templates
    elif isinstance(current, dict):
        # Your own templates win over kit templates with the same name.
        merged = dict(templates)
        merged.update(current)
        dash["button_card_templates"] = merged
    # Keep button_card_templates first, like HA writes it.
    ordered = {"button_card_templates": dash.pop("button_card_templates")}
    ordered.update(dash)
    return ordered


def main():
    ap = argparse.ArgumentParser(description="Inline kit templates into a dashboard for UI mode.")
    ap.add_argument("dashboard", help="dashboard YAML that uses the kit templates")
    ap.add_argument("--templates", default=DEFAULT_TEMPLATES, help="templates directory (default: the kit's templates/)")
    ap.add_argument("-o", "--output", help="write to this file instead of stdout")
    args = ap.parse_args()
    out = build(args.dashboard, args.templates)
    text = yaml.dump(out, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=1000)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
