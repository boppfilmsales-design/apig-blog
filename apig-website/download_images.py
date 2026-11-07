# -*- coding: utf-8 -*-
"""download product images listed in products.json -> images/"""
import os, re, json, time, urllib.parse
import requests
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(HERE, "images")
os.makedirs(IMG_DIR, exist_ok=True)
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"})

def dl(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 2000:
        return True
    for _ in range(3):
        try:
            r = S.get(url, timeout=30)
            if r.status_code == 200 and len(r.content) > 1000:
                with open(path, "wb") as f:
                    f.write(r.content)
                return True
        except Exception:
            time.sleep(1.0)
    return False

def main():
    with open(os.path.join(HERE, "products.json"), "r", encoding="utf-8") as f:
        products = json.load(f)
    total_ok = 0
    total_fail = 0
    for p in products:
        pid = p["id"]
        imgs = p.get("images", [])
        if not imgs:
            continue
        for i, u in enumerate(imgs):
            ext = os.path.splitext(urllib.parse.urlparse(u).path)[1] or ".jpg"
            name = "%s_%d%s" % (pid, i, ext)
            path = os.path.join(IMG_DIR, name)
            if dl(u, path):
                total_ok += 1
            else:
                total_fail += 1
                print("FAIL:", pid, name, u)
    print("DONE. ok=", total_ok, "fail=", total_fail)

if __name__ == "__main__":
    main()