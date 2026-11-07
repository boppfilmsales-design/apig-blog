# -*- coding: utf-8 -*-
"""Generate product pages using built-in professional spec data."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = "https://objectstorage.us-phoenix-1.oraclecloud.com/n/axgggehgnfll/b/apig-blog-images/o/"

# Built-in professional spec data keyed by product id.
SPECS = {
"522": {
  "title": "4.5um BOPET Thermal Transfer Ribbon Film",
  "desc": "Ultra-thin BOPET base film for thermal transfer ribbons (TTR). High surface smoothness, consistent caliper and excellent coating anchorage for wax and resin ribbons.",
  "rows": [
    ("Thickness", "4.5 / 5.0 / 6.0 micron"),
    ("Type", "Thermal transfer ribbon (TTR) base film"),
    ("Surface", "Clear, high-smoothness coated side"),
    ("Width", "300 - 1600 mm"),
    ("Tensile strength (MD/TD)", "Min. 230 / 230 MPa"),
    ("Elongation at break", "120 / 130 %"),
    ("COF (dynamic)", "0.4 - 0.6"),
    ("Heat shrinkage (150°C, 15min)", "MD ≤ 2.0% / TD ≤ 1.0%"),
    ("Core", "76 mm / 152 mm"),
    ("Application", "Wax, resin and mixed thermal transfer ribbons"),
  ],
  "cat": "BOPET FILM",
},
"521": {
  "title": "Plain BOPP Film (Printing & Lamination)",
  "desc": "Bi-axially oriented polypropylene film with superior clarity, moisture resistance and mechanical strength. For printing, lamination and metallization.",
  "rows": [
    ("Thickness", "Printing 20-52um; Lamination 10-18um"),
    ("Width", "350 - 1600 mm"),
    ("Length", "2000 / 3000 / 4000 / 7000 / 8000 / 9000 m"),
    ("Corona treated", "Single or double side"),
    ("Heat sealable", "Non-heatsealable"),
    ("Dimensional stability", "≤ 3.0% (after 5 min @ 120°C)"),
    ("COF (dynamic)", "≤ 0.5"),
    ("Haze", "≤ 2.0%"),
    ("Application", "Printing, lamination, aluminium metallization"),
    ("Core", "76 mm / 152 mm"),
  ],
  "cat": "BOPP FILM",
},
"519": {
  "title": "Polypropylene Film",
  "desc": "Versatile polypropylene packaging film offering excellent transparency, moisture barrier and dimensional stability for general packaging and bag making.",
  "rows": [
    ("Thickness", "12 / 15 / 18 / 20 / 25 / 30 um"),
    ("Width", "300 - 1500 mm"),
    ("Type", "Plain, matte or metallized available"),
    ("Tensile strength", "MD ≥ 120 MPa / TD ≥ 200 MPa"),
    ("Elongation", "MD ≥ 120% / TD ≥ 40%"),
    ("Heat sealable", "Optional single or double side"),
    ("Application", "Food, textile, stationery and general packaging"),
    ("Core", "76 mm / 152 mm"),
  ],
  "cat": "BOPP FILM",
},
"517": {
  "title": "BOPP Tape-grade Film",
  "desc": "BOPP film specially designed as the base substrate for adhesive packing tape, with high tensile strength and consistent corona treatment.",
  "rows": [
    ("Thickness", "23 / 25 / 28 um"),
    ("Width", "400 - 1300 mm"),
    ("Length", "4000 / 7000 / 8000 m"),
    ("Corona treated", "Single side (tape side)"),
    ("Tensile strength (MD)", "≥ 125 MPa"),
    ("Elongation", "MD ≥ 140%"),
    ("Haze", "≤ 2.5%"),
    ("Application", "Adhesive packing tape, stationery tape jumbo rolls"),
    ("Core", "76 mm / 152 mm"),
  ],
  "cat": "BOPP FILM",
},
"516": {
  "title": "BOPP Flower Wrapping Film (Clear & Printed)",
  "desc": "High-clarity BOPP film for flower and gift wrapping. Crystal clear or with printed logos, excellent gloss and flexibility.",
  "rows": [
    ("Thickness", "18 / 25 / 30 / 35 / 40 um"),
    ("Width", "500 - 1200 mm"),
    ("Length", "30 / 60 / 100 / 120 / 150 / 200 m"),
    ("Color", "Super clear, colored or printed private logo"),
    ("Inner core", "1.5 / 1.8 / 2 / 3 inches"),
    ("Gloss", "≥ 90%"),
    ("Haze", "≤ 2.0%"),
    ("Application", "Flower, gift and bouquet wrapping"),
  ],
  "cat": "BOPP FILM",
},
"515": {
  "title": "BOPP Flower Wrapping Film Mini-rolls",
  "desc": "Compact mini-rolls and sheets of BOPP flower wrapping film for retail bouquet wrapping. Super clear or printed with customer logos.",
  "rows": [
    ("Thickness", "18 / 25 / 30 / 35 / 40 um"),
    ("Mini-roll width", "500 / 600 / 700 / 800 / 1000 / 1200 mm"),
    ("Mini-roll length", "30 / 60 / 100 / 120 / 150 / 180 / 200 m"),
    ("Sheet size", "0.24M - 1.2M width, 0.5M - 1.2M length"),
    ("Color", "Clear, red, pink, green, white, purple, blue or printed"),
    ("Core", "1.5 / 1.8 / 2 / 3 inches"),
    ("Package", "4 or 6 rolls / carton; 200-500 sheets / pack"),
    ("Application", "Florist, gift shop and supermarket wrapping"),
  ],
  "cat": "BOPP FILM",
},
"513": {
  "title": "BOPP Thermal Laminating Film",
  "desc": "Coated BOPP film for thermal lamination of printed materials. Crystal clear, high gloss and strong adhesion for document and packaging protection.",
  "rows": [
    ("Thickness", "12 / 15 / 20 / 25 / 30 / 38 um"),
    ("Width", "320 - 1600 mm"),
    ("Length", "1000 - 16000 m"),
    ("Adhesive", "EVA hot-melt thermal coating"),
    ("Gloss", "≥ 85%"),
    ("Haze", "≤ 2.0%"),
    ("Application", "Book covers, packaging boxes, cards, maps"),
    ("Core", "76 mm / 152 mm"),
  ],
  "cat": "BOPP FILM",
},
"512": {
  "title": "Velvet Soft-touch Film (EVA Adhesive)",
  "desc": "Matte soft-touch film with EVA adhesive coating, delivering a silky velvet feel and premium finish for luxury packaging and print.",
  "rows": [
    ("Thickness", "25 / 30 / 38 um"),
    ("Width", "320 - 1600 mm"),
    ("Adhesive", "EVA hot-melt"),
    ("Finish", "Matte velvet soft-touch"),
    ("Application", "Premium boxes, book covers, cosmetic packaging"),
    ("Core", "76 mm / 152 mm"),
  ],
  "cat": "LAMINATION FILM",
},
"511": {
  "title": "BOPP Crystal Tape Jumbo Rolls",
  "desc": "Crystal-clear BOPP adhesive tape in jumbo rolls for slitting into finished packing tape. High clarity and strong adhesion.",
  "rows": [
    ("Thickness", "38 / 40 / 43 / 45 um (film + adhesive)"),
    ("Width (jumbo)", "1000 / 1280 mm"),
    ("Length", "2000 - 10000 m"),
    ("Adhesive", "Water-based acrylic"),
    ("Adhesion strength", "≥ 1.6 N/cm"),
    ("Application", "Slitting into finished packing tape"),
  ],
  "cat": "TAPE",
},
"509": {
  "title": "BOPP Tape Semi-finished (Water-base Clear)",
  "desc": "Semi-finished clear BOPP adhesive tape with water-based acrylic coating, ready for slitting into finished transparent packing tape.",
  "rows": [
    ("Thickness", "38 / 40 / 43 / 45 um"),
    ("Width (jumbo)", "1280 / 1000 mm"),
    ("Adhesive", "Water-based acrylic"),
    ("Adhesion strength", "≥ 1.5 N/cm"),
    ("Tensile strength", "≥ 110 N/cm"),
    ("Application", "Transparent packing tape manufacture"),
  ],
  "cat": "TAPE",
},
"508": {
  "title": "Cigarette Adhesive Tear Tape",
  "desc": "BOPP tear tape with release coating for cigarette carton and package opening. Uniform width and consistent release strength.",
  "rows": [
    ("Thickness", "20 / 22 / 25 um"),
    ("Width", "1.5 / 2 / 2.5 / 3 / 4 mm"),
    ("Type", "Clear or colored, printed"),
    ("Release", "Low-tack release coating"),
    ("Application", "Cigarette packs, boxes and cartons"),
  ],
  "cat": "TEAR TAPE",
},
"507": {
  "title": "Cigarette Tear Tape",
  "desc": "High-strength BOPP tear tape for cigarette pack opening. Uniform slitting and reliable tear performance.",
  "rows": [
    ("Thickness", "20 / 25 um"),
    ("Width", "1.5 - 5 mm"),
    ("Type", "Clear, metallic, printed"),
    ("Tensile strength", "≥ 90 N/cm"),
    ("Application", "Cigarette packs, tea boxes, cartons"),
  ],
  "cat": "TEAR TAPE",
},
"506": {
  "title": "BOPP Adhesive Tape (Machine Lines)",
  "desc": "High-performance BOPP packing tape produced on machine lines. Strong adhesion, high tensile strength and reliable unwinding.",
  "rows": [
    ("Thickness", "38 / 40 / 43 / 45 / 48 um"),
    ("Width", "12 - 1000 mm (finished tape)"),
    ("Length", "50 - 500 m (finished rolls)"),
    ("Adhesive", "Water-based acrylic"),
    ("Adhesion strength", "≥ 1.6 N/cm"),
    ("Tensile strength", "≥ 45 N/cm"),
    ("Application", "Carton sealing, bundling, general packing"),
  ],
  "cat": "TAPE",
},
"505": {
  "title": "CPP Film",
  "desc": "Cast polypropylene film with excellent clarity, heat sealability and dimensional stability for flexible food packaging and lamination.",
  "rows": [
    ("Thickness", "15 / 18 / 20 / 25 / 30 / 40 um"),
    ("Width", "300 - 1500 mm"),
    ("Heat sealable", "Single or double side"),
    ("COF", "0.2 - 0.5"),
    ("Haze", "≤ 2.0%"),
    ("Application", "Food packaging, lamination, bags, labels"),
    ("Core", "76 mm / 152 mm"),
  ],
  "cat": "CPP FILM",
},
"504": {
  "title": "BOPET Tear Tape",
  "desc": "BOPET-based tear tape with high strength and clear release for easy opening of packaging and cigarette cartons.",
  "rows": [
    ("Thickness", "20 / 25 um"),
    ("Width", "1.5 - 5 mm"),
    ("Type", "Clear, printed, metallic"),
    ("Tensile strength", "≥ 130 N/cm"),
    ("Application", "Cigarette packs, cartons, easy-open packaging"),
  ],
  "cat": "BOPET FILM",
},
}

CATS = {
  "BOPP FILM": "BOPP Film",
  "BOPET FILM": "BOPET Film",
  "CPP FILM": "CPP Film",
  "LAMINATION FILM": "Lamination Film",
  "TAPE": "Adhesive Tape",
  "TEAR TAPE": "Tear Tape",
}

def rows_html(rows):
    out = []
    for k, v in rows:
        out.append("<tr><th>%s</th><td>%s</td></tr>" % (k, v))
    return "\n".join(out)

def gen(pid, data):
    r = rows_html(data["rows"])
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>@@TITLE@@ | Asia Pacific Industry Group</title>
<meta name="description" content="@@TITLE@@ - @@DESC@@">
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Noto+Sans+SC:wght@400;700&display=swap" rel="stylesheet">
<style>
body{font-family:'Inter','Noto Sans SC',sans-serif}
.bg-green{background-color:#064e3b}
.text-green{color:#064e3b}
.btn-gold{background-color:#fbbf24;transition:all .3s ease}
.btn-gold:hover{background-color:#f59e0b}
.img-card{height:300px;object-fit:contain;width:100%;border-radius:16px;background:#f0f4f3;padding:10px}
table.spec{width:100%;border-collapse:collapse;font-size:14px}
table.spec th,table.spec td{border:1px solid #e5e7eb;padding:10px 14px;text-align:left;vertical-align:top}
table.spec th{background:#f3f4f6;font-weight:700;width:34%}
</style>
</head>
<body class="bg-gray-50 text-gray-900">

<nav class="bg-white shadow-sm">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between h-16 items-center">
    <a href="index.html" class="font-bold text-green text-lg">ASIA PACIFIC <span class="text-yellow-600">INDUSTRY</span></a>
    <div class="hidden md:flex space-x-8 text-sm font-medium text-gray-600">
      <a href="index.html" class="hover:text-green">Home</a>
      <a href="index.html#products" class="hover:text-green">Products</a>
      <a href="index.html#about" class="hover:text-green">About</a>
      <a href="index.html#contact" class="hover:text-green">Contact</a>
    </div>
  </div>
</nav>

<section class="bg-green text-white">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
    <div class="text-sm text-yellow-400 font-semibold uppercase tracking-wider mb-2">Product No. @@PID@@ &middot; @@CAT@@</div>
    <h1 class="text-2xl md:text-3xl font-bold">@@TITLE@@</h1>
    <p class="text-white/80 mt-3 max-w-3xl">@@DESC@@</p>
  </div>
</section>

<section class="py-12">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-2 gap-10">
    <div>
      <img src="@@IMGURL@@" alt="@@TITLE@@" class="img-card">
    </div>
    <div>
      <h2 class="text-2xl font-bold text-green mb-6">Technical Specifications</h2>
      <table class="spec bg-white rounded-xl shadow overflow-hidden">
        <tbody>
@@ROWS@@
        </tbody>
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
    html = html.replace("@@TITLE@@", data["title"])
    html = html.replace("@@PID@@", pid)
    html = html.replace("@@CAT@@", data.get("cat", ""))
    html = html.replace("@@DESC@@", data["desc"])
    html = html.replace("@@ROWS@@", r)
    html = html.replace("@@IMGURL@@", IMG + pid + "_0.jpg")
    return html

def main():
    for pid, data in SPECS.items():
        html = gen(pid, data)
        with open(os.path.join(HERE, "product-%s.html" % pid), "w", encoding="utf-8") as f:
            f.write(html)
        print("generated product-%s.html" % pid)
    print("DONE. %d pages" % len(SPECS))

if __name__ == "__main__":
    main()