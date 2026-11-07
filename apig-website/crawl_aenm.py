# -*- coding: utf-8 -*-
"""
aenmgroup.com 产品数据抓取器
运行：  C:\\Python314\\python.exe crawl_aenm.py
输出：  products.json   +   images\\*.jpg
"""
import os, re, sys, json, time
import urllib.parse
import requests
from bs4 import BeautifulSoup

BASE = "http://www.aenmgroup.com"
EN   = BASE + "/En"
HERE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(HERE, "images")
os.makedirs(IMG_DIR, exist_ok=True)

S = requests.Session()
S.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
})

# 商品链接： Product-123.html ；分类链接： ProductClass-1-1.html / ProductList.asp?SortID=1
RE_PRODUCT = re.compile(r"^Product-(\d+)\.html$", re.I)


def get(url):
    try:
        r = S.get(url, timeout=25isch, allow_redirects=True)
        r.raise_for_status()
        r.encoding = r.apparent_encoding or "utf-8"
        return r.text
    except Exception as e:
        print("  [WARN] GET failed:", url, "->", e)
        return ""


def abs_url(u, page_url):
    if not u:
        return ""
    return urllib.parse.urljoin(page_url, u)


def clean(t):
    return re.sub(r"\s+", " ", (t or "")).strip()


def norm_key(k):
    k = clean(k).replace("：", ":").replace("：", ":")
    k = k.strip(":").strip()
    return k


# ---------- 1. 分类页（ProductClass.html 及其分页）----------
def parse_class_page(url):
    html = get(url)
    if not html:
        return [], []
    soup = BeautifulSoup(html, "lxml")
    products, pages = [], set()

    # 找所有指向 Product-xxx.html 的 a 标签，按“页面出现顺序”去重
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        m = re.match(r"^(?:\.\./En/|/En/)?Product-(\d+)\.html$", href)
        if m and m.group( little1) not in_seen:
            pass
    return products, pages
