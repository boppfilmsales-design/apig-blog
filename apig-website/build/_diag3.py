# -*- coding: utf-8 -*-
"""Inventory of English prose inside spec values (the main ZH leak source)."""
import json, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw = json.load(open(os.path.join(HERE,"build","products_raw.json"), encoding="utf-8"))

runs = collections.Counter()
for p in raw:
    for it in p.get("items",[]):
        for k,v in it.get("specs",[]):
            t = re.sub(r"[0-9][0-9.,~～×xX\-\/\s]*", " ", v)
            for m in re.findall(r"[A-Za-z][A-Za-z'\-\.&\/]*(?:[ ][A-Za-z][A-Za-z'\-\.&\/]*)*", t):
                m = m.strip(" .")
                if len(m.split()) >= 2:
                    runs[m.lower()] += 1
print("total distinct multi-word runs:", len(runs), " total occurrences:", sum(runs.values()))
for r,c in runs.most_common(90):
    print(f"  {c:3d}  {r}")
