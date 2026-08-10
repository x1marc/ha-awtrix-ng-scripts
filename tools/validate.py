#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validiert alle YAML-Dateien des Repos.

- Jede .yaml/.yml muss syntaktisch parsen (Home-Assistant-Tags wie
  !include_dir_named / !input werden toleriert).
- Jedes Einzelskript  awtrix_ng_*.yaml  (ausser dem Package) braucht
  'alias' und 'sequence'.
- Das Package  awtrix_ng_all_scripts.yaml  braucht einen 'script:'-Block,
  dessen Eintraege jeweils 'alias' + 'sequence' haben.

Exit-Code 1, wenn irgendetwas fehlschlaegt. Wird lokal und in der CI genutzt.
"""
import os
import sys
import glob
import yaml


def all_yaml_files(root):
    """Alle .yaml/.yml – inkl. versteckter Ordner wie .github, ohne .git."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for name in filenames:
            if name.endswith((".yaml", ".yml")):
                yield os.path.join(dirpath, name)

# HA-eigene Tags nicht als Fehler werten
yaml.add_multi_constructor("!", lambda loader, suffix, node: None,
                           Loader=yaml.SafeLoader)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []
checked = 0


def load(path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


# 1) Alle YAML-Dateien parsen
for path in all_yaml_files(ROOT):
    rel = os.path.relpath(path, ROOT)
    checked += 1
    try:
        load(path)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{rel}: YAML-Parsefehler: {exc}")

# 2) Einzelskripte strukturell pruefen
for path in glob.glob(os.path.join(ROOT, "awtrix_ng_*.yaml")):
    rel = os.path.relpath(path, ROOT)
    if rel == "awtrix_ng_all_scripts.yaml":
        continue
    try:
        doc = load(path)
    except Exception:  # bereits oben gemeldet
        continue
    if not isinstance(doc, dict) or "alias" not in doc or "sequence" not in doc:
        errors.append(f"{rel}: 'alias' und/oder 'sequence' fehlt")

# 3) Package pruefen
pkg = os.path.join(ROOT, "awtrix_ng_all_scripts.yaml")
if os.path.exists(pkg):
    try:
        doc = load(pkg)
        scripts = (doc or {}).get("script")
        if not isinstance(scripts, dict) or not scripts:
            errors.append("awtrix_ng_all_scripts.yaml: 'script:'-Block fehlt/leer")
        else:
            for name, body in scripts.items():
                if not isinstance(body, dict) or "alias" not in body \
                        or "sequence" not in body:
                    errors.append(
                        f"awtrix_ng_all_scripts.yaml: '{name}' ohne alias/sequence")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"awtrix_ng_all_scripts.yaml: {exc}")

print(f"Geprueft: {checked} YAML-Datei(en)")
if errors:
    print(f"\n{len(errors)} Problem(e):")
    for e in errors:
        print("  - " + e)
    sys.exit(1)
print("Alles in Ordnung.")
