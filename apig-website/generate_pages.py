# -*- coding: utf-8 -*-
"""generate product detail pages from products.json -> product-XXX.html"""
import os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = "https://objectstorage.us-phoenix-1.oraclecloud.com/n/axgggehgnfll/b/apig-blog-images/o/"

def clean(t):
    return re.sub(r"\s+", " ", (t or "")).strip()

def gen_html(p):
    pid = p["id"]
    name = clean(p.get("name", ""))
    short = name[:70]
    fields = p.get("fields", {})
    desc = clean(fields.get("Product Name", ""))[:300]
    # build spec table from field pairs (skip noise keys)
    skip = ["Home About US News Products Join US Download MemberCenter Cart Web map Guestbook Contact US", "Product Name", "Plain BOPP Film"]
    rows = ""
    for k, v in fields.items():
        kk = clean(k)
        vv = clean(v)
        if not kk or not vv or kk in skip or len(kk) > 30 or len(vv) > 200:
            continue
        if "Parameter" in kk or "Value" == kk:
            continue
        rows += "<tr><th>%s</th><td>%s</td></tr>\n" % (kk, vv)
    if not rows:
        rows = "<tr><th>Note</th><td>Detailed specification on request.</td></tr>"
    imgs = p.get("images", [])
    img_tags = ""
    if imgs:
        for i, u in enumerate(imgs):
            fname = "%s_%d.jpg" % (pid, i)
            img_tags += '<img src="%s%s" alt="%s" class="img-card mt-4">\n' % (IMG, fname, short)
    else:
        img_tags = '<div class="img-card mt-4 flex items-center justify-center text-gray-400">No image</div>'
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>@@SHORT@@ | Asia Pacific Industry Group</title>
<meta name="description" content="@@SHORT@@ - technical specification for global packaging.">
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Noto+Sans+SC:wght@400;700&display=swap" rel="stylesheet">
<style>
body{font-family:'Inter','Noto Sans SC',sans-serif}
.bg-green{background-color:#064e3b}
.text-green{color:#064e3b}
.btn-gold{background-color:#fbbf24;transition:all .3s ease}
.btn-gold:hover{background-color:#f59e0b}
.img-card{height:260px;object-fit:cover;width:100%;border-radius:16px;background:#f0f4f3}
table.spec{width:100%;border-collapse:collapse;font-size:14px}
table.spec th,table.spec td{border:1px solid #e5e7eb;padding:10px 14px;text-align:left;vertical-align:top}
table.spec th{background:#f3f4f6;font-weight:700;width:32%}
</style>
</head>
<body class="bg-gray-50 text-gray-900">

<nav class="bg-white shadow-sm">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between h-16 items-center">
    <a href="index.html" class="font-bold text-green text-lg">ASIA PACIFIC <span class="text-yellow-600">INDUSTRY</span></a>
    <div class="hidden md:flex space-x-8 text-sm font-medium text-gray-600">
      <a href="index.html" class="hover:text-green">Home</a>
      <a href="index.html#products" class="hover:text-green">Products</a>
      <a href="index.html#contact" class="hover:text-green">Contact</a>
    </div>
  </div>
</nav>

<section class="bg-green text-white">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
    <div class="text-sm text-yellow-400 font-semibold uppercase tracking-wider mb-2">Product No. @@PID@@</div>
    <h1 class="text-2xl md:text-3xl font-bold">@@NAME@@</h1>
  </div>
</section>

<section class="py-12">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-2 gap-10">
    <div>@@IMGS@@</div>
    <div>
      <h2 class="text-2xl font-bold text-green mb-6">Technical Specifications</h2>
      <table class="spec bg-white rounded-xl shadow overflow-hidden">
        <tbody>
@@ROWS@@        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="py-14 bg-green">
  <div class="max-w-4xl mx-auto px-4 text-center text-white">
    <h2 class="text-2xl font-bold mb-3">Need this film in your specification?</h2>
    <p class="text-white/80 mb-6">Send us your thickness, width and quantity for a fast quotation.</p>
    <a href="index.html#contact" class="btn-gold text-green px-8 py-3 rounded-full font-bold inline-block">Get a Quote</a>
  </div>
</section>

<footer class="py-8 bg-white border-t text-center text-gray-500 text-sm">
  &copy; 2026 Asia Pacific Industry Group Co., Limited. &middot; www.boppfilmsales.com
</footer>

</body>
</html>
"""
    html = html.replace("@@SHORT@@", short)
    html = html.replace("@@PID@@", pid)
    html = html.replace("@@NAME@@", name)
    html = html.replace("@@IMGS@@", img_tags)
    html = html.replace("@@ROWS@@", rows)
    return html

def main():
    with open(os.path.join(HERE, "products.json"), "r", encoding="utf-8") as f:
        products = json.load(f)
    n = 0
    for p in products:
        pid = p["id"]
        html = gen_html(p)
        path = os.path.join(HERE, "product-%s.html" % pid)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        n += 1
        print("generated product-%s.html" % pid)
    print("DONE. %d pages generated" % n)

if __name__ == "__main__":
    main()