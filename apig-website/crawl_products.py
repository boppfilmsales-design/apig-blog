# -*- coding: utf-8 -*-
"""crawl aenmgroup.com product list + details -> products.json"""
import os, re, json, time, urllib.parse
import requests
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"})
BASE = "http://www.aenmgroup.com/En"

def get(url):
    for _ in range(3):
        try:
            r = S.get(url, timeout=25)
            r.raise_for_status()
            r.encoding = "utf-8"
            return r.text
        except Exception:
            time.sleep(1.2)
    return ""

def clean(t):
    return re.sub(r"\s+", " ", (t or "")).strip()

def name_from_a(a):
    # 优先 title 属性，其次 a 的文本，其次 img alt
    t = a.get("title") or ""
    if t:
        return clean(t)
    txt = clean(a.get_text())
    if txt:
        return txt
    img = a.find("img")
    if img and img.get("alt"):
        return clean(img.get("alt"))
    return ""

def collect_list():
    visited = set()
    found = {}
    order = []
    stack = [BASE + "/ProductClass.html"]
    while stack:
        url = stack.pop()
        if url in visited:
            continue
        visited.add(url)
        html = get(url)
        if not html:
            continue
        soup = BeautifulSoup(html, "lxml")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            full = urllib.parse.urljoin(url, href)
            m = re.match(r"^.*?Product-(\d+)\.html$", href)
            if m:
                pid = m.group(1)
                if pid not in found:
                    found[pid] = {"id": pid, "name": name_from_a(a), "url": full}
                    order.append(pid)
                continue
            m2 = re.match(r"^.*?ProductClass-(\d+)-(\d+)\.html$", href)
            if m2 and full not in visited:
                stack.append(full)
    return [found[p] for p in order]

def scrape_detail(p):
    html = get(p["url"])
    if not html:
        return p
    soup = BeautifulSoup(html, "lxml")
    # 产品名（页面 h1 / title 里的)
    h1 = soup.find(["h1", "h2"])
    if h1:
        n = clean(h1.get_text())
        if n and not p.get("name"):
            p["name"] = n
    # 字段行（Product No / Model / Price / Update / Manufacturer）
    fields = {}
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) >= 2:
            k = clean(tds[0].get_text()).replace("：", ":").replace(":", "").strip()
            v = clean(tds[1].get_text())
            if k and v:
                fields[k] = v
    p["fields"] = fields
    # 图片
    imgs = []
    for img in soup.find_all("img", src=True):
        src = img["src"]
        if "/upload/" in src:
            u = urllib.parse.urljoin(p["url"], src)
            if u not in imgs:
                imgs.append(u)
    p["images"] = imgs
    # 描述正文（去掉脚本/样式）
    for tag in soup(["script", "style", "nav", "footer", "table"]):
        tag.decompose()
    body = soup.get_text("\n")
    body = re.sub(r"\n+", "\n", body)
    lines = [l.strip() for l in body.split("\n") if l.strip()]
    p["text"] = " | ".join(lines[:40])
    return p

def main():
    items = collect_list()
    print("TOTAL listed:", len(items))
    results = []
    for i, p in enumerate(items, 1):
        p = scrape_detail(p)
        results.append(p)
        print(f"[{i}/{len(items)}] {p['id']} | {p.get('name','')[:60]}")
        time.sleep(0.3)
    with open(os.path.join(HERE, "products.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("SAVED products.json")

if __name__ == "__main__":
    main()