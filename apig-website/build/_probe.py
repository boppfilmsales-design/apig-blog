# -*- coding: utf-8 -*-
import re, requests, collections
S = requests.Session()
S.headers.update({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0 Safari/537.36"})
BASE="http://www.aenmgroup.com/En"
SORTS=[1,3,4,5,13,17,18,20,22,23,24,25,26,27,29,31,36,37]
found=collections.OrderedDict()
per_sort={}
for sid in SORTS:
    url=f"{BASE}/ProductList.asp?SortID={sid}"
    try:
        r=S.get(url,timeout=25); r.encoding="gb18030"
        html=r.text
    except Exception as e:
        print("ERR",sid,e); continue
    ids=re.findall(r"Product-(\d+)\.html",html)
    ids=[i for i in dict.fromkeys(ids)]
    per_sort[sid]=len(ids)
    for i in ids: found[i]=sid
    # detect pagination
    pg=re.findall(r"[?&](?:page|Page|PageIndex)=(\d+)",html)
    print(f"SortID={sid:>3}  products={len(ids):>3}  page-params={sorted(set(pg))[:6]}  sample={ids[:5]}")
print("TOTAL unique products:",len(found))
