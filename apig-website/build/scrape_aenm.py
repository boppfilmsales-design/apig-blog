# -*- coding: utf-8 -*-
"""Scrape aenmgroup.com product catalogue (English section) into structured JSON.

Source pages : http://www.aenmgroup.com/En/ProductList.asp?SortID=<n>
Detail pages : http://www.aenmgroup.com/En/Product-<id>.html
Encoding     : GBK / GB18030 (decoded with gb18030 + errors='ignore')

Output        build/products_raw.json
Images        build/raw_images/<id>_<n>.jpg

The legacy pages are badly encoded and inconsistently formatted, so the
technical-parameter blob is parsed against a whitelist of the field names the
old site actually uses (Thickness, Width, Length, ...).  A generic fallback
regex handles the odd product that uses a different wording.
"""
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_JSON = os.path.join(HERE, "build", "products_raw.json")
IMG_DIR = os.path.join(HERE, "build", "raw_images")
BASE = "http://www.aenmgroup.com"
EN = BASE + "/En"

SORTS = [1, 3, 4, 5, 13, 17, 18, 20, 22, 23, 24, 25, 26, 27, 29, 31, 36, 37]

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

S = requests.Session()
S.headers.update({"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})

# field names used by the legacy catalogue
CANON_KEYS = [
    "Basic material", "Base material", "Surface treatment", "Corona treatment",
    "Sealing temperature", "Sealing time", "Tensile strength", "Shrink ratio",
    "Melting point", "Heat seal", "Material", "Structure", "Composition",
    "Thickness", "Width", "Length", "Colour", "Color", "Printing", "Grade",
    "Type", "Application", "Capacity", "Appearance", "Standard", "Remark",
    "Customer", "Weight", "Density", "Caliper", "Adhesive", "Style", "Packing",
    "Packaging", "Model", "Core", "Item", "Use", "Size", "Gloss", "Hardness",
    "Stiffness", "Feature", "Advantage", "Specification", "Requirement",
    "Coating", "Print", "Delivery", "Port", "Certification",
]
CANON_RE = re.compile(
    r"(?<![A-Za-z])(" + "|".join(re.escape(k) for k in sorted(CANON_KEYS, key=len, reverse=True)) + r")\s*[:：]\s*",
    re.I,
)
GENERIC_RE = re.compile(r"([A-Za-z][A-Za-z0-9 \-/()\.]{1,40}?)\s*[:：]\s*")
ITEM_RE = re.compile(r"(Item\s*\d+\s*[.、:：]?\s*)", re.I)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def new_session():
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
    return s


def get(url, tries=3):
    s = new_session()
    for i in range(tries):
        try:
            r = s.get(url, timeout=30)
            r.raise_for_status()
            r.encoding = "gb18030"
            return r.text
        except Exception:  # noqa: BLE001
            if i == tries - 1:
                return ""
            time.sleep(1.2 * (i + 1))
    return ""


def strip_tags(html):
    txt = TAG_RE.sub(" ", html or "")
    txt = (txt.replace("&nbsp;", " ").replace("&amp;", "&")
              .replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">"))
    return WS_RE.sub(" ", txt).strip()


def parse_kv(text):
    """Turn 'Basic material : X  Thickness : Y ...' into [(k, v), ...]."""
    parts = list(CANON_RE.finditer(text))
    if len(parts) < 2:
        parts = list(GENERIC_RE.finditer(text))
    out = []
    for i, m in enumerate(parts):
        key = WS_RE.sub(" ", m.group(1)).strip(" ,;.-")
        if len(key) < 2 or len(key) > 45:
            continue
        end = parts[i + 1].start() if i + 1 < len(parts) else len(text)
        val = WS_RE.sub(" ", text[m.end():end]).strip(" ,;.")
        if not val:
            continue
        out.append((key, val))
    return out


def parse_detail(raw_text):
    """Split the description blob into items with their own spec lists."""
    raw_text = raw_text.replace("&nbsp;", " ").replace("&amp;", "&")
    marks = [(m.start(), m.group(1)) for m in ITEM_RE.finditer(raw_text)]
    items = []
    if not marks:
        specs = parse_kv(raw_text)
        return [{"heading": "", "specs": specs, "text": "" if specs else raw_text.strip()}]
    for i, (pos, marker) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(raw_text)
        chunk = WS_RE.sub(" ", raw_text[pos + len(marker):end]).strip(" .:：;")
        specs = parse_kv(chunk)
        heading = ""
        if specs:
            head_txt = WS_RE.sub(" ", chunk[:chunk.find(specs[0][0])]) if specs[0][0] in chunk else ""
            heading = head_txt.strip(" ,;.-")
            if len(heading) > 90:
                heading = heading[:90].rsplit(" ", 1)[0] + "…"
        items.append({"heading": heading, "specs": specs, "text": "" if specs else chunk})
    return [it for it in items if it["specs"] or it["text"]]


def parse_product(pid, html):
    img_urls = []
    m = re.search(r'href="(\.\./upload/[^"]+\.(?:jpg|jpeg|png|gif))"[^>]*title="zoom"', html, re.I)
    if m:
        img_urls.append(m.group(1))
    else:
        for mm in re.finditer(r'src="(\.\./upload/[^"]+\.(?:jpg|jpeg|png|gif))"', html, re.I):
            u = mm.group(1)
            if u not in img_urls:
                img_urls.append(u)

    def field(label):
        mm = re.search(re.escape(label) + r"\s*[:：]\s*(.*?)</td>", html, re.S | re.I)
        return strip_tags(mm.group(1)) if mm else ""

    name = field("Product Name")
    product_no = field("Product No")
    model = field("Model")
    updated = field("Last update")
    manufacturer = field("Manufacturer")

    dpos = html.find("产品详细介绍")
    if dpos < 0:
        dpos = html.find("Product Detail")
    detail_html = ""
    if dpos > 0:
        tail = html[dpos + 6:]
        cut = tail.find("Contact Us")
        if cut < 0:
            cut = tail.find("CopyRight")
        detail_html = tail[:cut] if cut > 0 else tail[:8000]
    detail_text = strip_tags(detail_html)
    items = parse_detail(detail_text) if detail_text else []

    head = ITEM_RE.split(detail_text)[0].strip() if detail_text else ""
    if len(head) > 320:
        head = head[:320].rsplit(" ", 1)[0] + "…"

    return {
        "id": pid,
        "name": name,
        "product_no": product_no,
        "model": model,
        "updated": updated,
        "manufacturer": manufacturer,
        "intro": head,
        "items": items,
        "images": [BASE + u.replace("../", "/", 1) for u in img_urls],
    }


def download(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 3000:
        return True
    s = new_session()
    for i in range(3):
        try:
            r = s.get(url, timeout=40)
            if r.status_code == 200 and len(r.content) > 1500:
                with open(path, "wb") as fh:
                    fh.write(r.content)
                return True
        except Exception:  # noqa: BLE001
            pass
        time.sleep(1.0 * (i + 1))
    return False


def collect_catalogue():
    catalogue = {}
    for sid in SORTS:
        html = get(f"{EN}/ProductList.asp?SortID={sid}")
        if not html:
            continue
        for pid in dict.fromkeys(re.findall(r"Product-(\d+)\.html", html)):
            catalogue.setdefault(pid, sid)
    return catalogue


def handle(pid, sid):
    html = get(f"{EN}/Product-{pid}.html")
    if not html:
        return None
    p = parse_product(pid, html)
    p["sort"] = sid
    files = []
    for i, u in enumerate(p["images"]):
        ext = os.path.splitext(u)[1].split("?")[0].lower() or ".jpg"
        if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
            ext = ".jpg"
        rel = f"{pid}_{i}{ext}"
        if download(u, os.path.join(IMG_DIR, rel)):
            files.append(rel)
    p["image_files"] = files
    return p


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    catalogue = collect_catalogue()
    print("catalogue ids:", len(catalogue), flush=True)

    products = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(handle, pid, sid): pid for pid, sid in catalogue.items()}
        for n, fut in enumerate(futures, 1):
            pass
        for n, (fut, pid) in enumerate(futures.items(), 1):
            p = fut.result()
            if p:
                products.append(p)
            specs = sum(len(it["specs"]) for it in p["items"]) if p else 0
            head = (p["name"][:48] if p else "FAIL")
            print(f"  [{n}/{len(catalogue)}] {pid} specs={specs} :: {head}", flush=True)

    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(products, fh, ensure_ascii=False, indent=1)
    print("saved:", OUT_JSON, "products:", len(products))


if __name__ == "__main__":
    main()
