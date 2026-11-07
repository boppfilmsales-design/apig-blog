# -*- coding: utf-8 -*-
import json, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw = json.load(open(os.path.join(HERE,"build","products_raw.json"), encoding="utf-8"))
print("products:", len(raw))
print("sample keys:", list(raw[0].keys()))
c = collections.Counter()
for p in raw[:3]:
    print("----", p.get("id"), p.get("name"))
    print("   items:", json.dumps(p.get("items", [])[:4], ensure_ascii=False)[:600])
    print("   desc:", str(p.get("description",""))[:300])
