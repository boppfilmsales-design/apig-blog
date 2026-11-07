# -*- coding: utf-8 -*-
"""Inventory of untranslated English in names, headings and spec values."""
import json, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE,"build"))
from site_data import ZH_TOKENS, ZH_PHRASES, ZH_NAME_OVERRIDE
raw = json.load(open(os.path.join(HERE,"build","products_raw.json"), encoding="utf-8"))

KEEP = {"BOPP","BOPET","CPP","BOPA","BOPS","TTR","PVC","PE","PP","PET","PVA","EVOH",
        "PVDC","MOPP","TPU","PS","EPS","ABS","HDPE","LDPE","LLDPE","API","ISO","OEM",
        "GSM","PSI","PA","PU","PI","MD","GM","UM"}
KNOWN_PHRASE = {p.lower() for p,_ in ZH_PHRASES}

name_tokens = collections.Counter()
value_texts = collections.Counter()
for p in raw:
    nm = p.get("name","")
    if p["id"] in ZH_NAME_OVERRIDE: continue
    # strip already-known phrases
    t = nm
    for ph,zh in sorted(ZH_PHRASES, key=lambda x:-len(x[0])):
        t = re.sub(r"\b"+re.escape(ph)+r"\b", " ", t, flags=re.I)
    for w in t.split():
        c = w.strip("(),.:;/[]")
        if not c or any(ch.isdigit() for ch in c): continue
        if c.upper() in KEEP: continue
        if c.upper() in ZH_TOKENS: continue
        name_tokens[c.upper()] += 1
    for it in p.get("items",[]):
        h = it.get("heading","")
        for w in h.split():
            c=w.strip("(),.:;/[]")
            if not c or any(ch.isdigit() for ch in c): continue
            if c.upper() in KEEP or c.upper() in ZH_TOKENS: continue
            name_tokens[c.upper()] += 1
        for k,v in it.get("specs",[]):
            for m in re.findall(r"[A-Za-z][A-Za-z'\-]*(?:[ ][A-Za-z'\-]+)*", v):
                if len(m) > 3: value_texts[m.strip().lower()] += 1

print("=== 未译产品名/标题词 (", len(name_tokens), ") ===")
for w,c in name_tokens.most_common(120):
    print(f"  {c:3d}  {w}")
