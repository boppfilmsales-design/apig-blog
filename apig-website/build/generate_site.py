# -*- coding: utf-8 -*-
"""Build the bilingual APIG site (EN + ZH) from the scraped legacy catalogue.

Layout produced at the project root:

    index.html            language gateway (auto-detects the visitor)
    en/ , zh/             two fully independent language sites
    assets/               css, js and the processed product imagery
    _redirects            legacy URLs -> new product URLs (301)
"""
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from articles import ARTICLES
from site_data import (CATEGORIES, CATEGORY_CONTENT, COMPANY, NAV, ZH_NAME_OVERRIDE,
                       ZH_PHRASES, ZH_TOKENS)
from site_render import (Ctx, UI, contact_info_card, cta_band, document, esc,
                         inquiry_form, page_head, pillar_block, post_card,
                         product_card, section_head, stat_block)
import translate as tr
import infer
from glossary import PHRASE_ZH as GLOSSARY_PHRASES

# one merged phrase table for product names and for spec values
MERGED_PHRASES = list(GLOSSARY_PHRASES)
_seen = {en.lower() for en, _ in MERGED_PHRASES}
for _en, _zh in ZH_PHRASES:
    if _en.lower() not in _seen:
        MERGED_PHRASES.append((_en, _zh))
        _seen.add(_en.lower())

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# products the site already featured -> used for the homepage line-up
FEATURED = ["522", "521", "513", "517", "504", "505", "506", "511", "512",
            "515", "519", "516", "507", "508", "509"]

KEEP_UPPER = {"BOPP", "BOPET", "CPP", "BOPA", "BOPS", "TTR", "PVC", "PE", "PP",
              "PET", "PVA", "EVOH", "PVDC", "MOPP", "TPU", "PS", "EPS", "ABS",
              "HDPE", "LDPE", "LLDPE", "API", "ISO", "OEM", "GSM", "PSI", "PA",
              "PU", "PI", "MD", "GM", "UM"}

SPEC_KEY_ZH = {
    "thickness": "厚度", "width": "宽度", "length": "长度", "color": "颜色",
    "colour": "颜色", "printing": "印刷", "basic material": "基材",
    "base material": "基材", "material": "基材", "application": "应用领域",
    "tensile strength": "抗拉强度", "elongation": "伸长率", "model": "型号",
    "surface treatment": "表面处理", "corona treatment": "电晕处理",
    "heat seal": "热封性能", "coating": "涂层", "core": "纸芯",
    "type": "类型", "use": "用途", "feature": "产品特点", "advantage": "优点",
    "capacity": "产能", "packing": "包装形式", "grade": "牌号",
    "appearance": "外观", "standard": "执行标准", "remark": "备注",
    "basic materl": "基材", "product name": "产品名称", "item": "项目",
    "customer": "适用领域", "packing style": "包装形式", "note": "备注",
    "caliper": "厚度", "size": "尺寸", "sizes": "尺寸", "weight": "重量",
    "net weight": "净重", "gross weight": "毛重", "adhesive": "粘合剂",
    "features": "产品特点", "packaging": "包装形式", "density": "密度",
    "opacity": "不透明度", "haze": "雾度", "brightness": "亮度",
    "gloss": "光泽度", "certification": "认证", "specification": "规格说明",
    "usage": "用途", "paper": "纸张", "roll": "卷材", "tolerance": "公差",
    "product description": "产品描述", "style": "型号", "whiteness": "白度",
    "transparency": "透明度", "light transmission": "透光率",
    "seal strength": "热封强度", "printability": "印刷适性",
    "surface tension": "表面张力", "coefficient of friction": "摩擦系数",
    "elongation at break": "断裂伸长率", "tear strength": "撕裂强度",
    "impact resistance": "抗冲击性", "heat resistance": "耐热性",
    "thermal shrinkage": "热收缩率", "shrinkage rate": "收缩率",
    "storage": "储存条件", "shelf life": "保质期", "code": "编码",
    "logo": "商标", "printing side": "印刷面", "unit": "单位",
    "value": "数值", "quantity": "数量", "certificate": "证书",
    "msl": "湿敏等级", "typical properties": "典型性能",
    "temperature": "温度", "elongation at break (md)": "断裂伸长率（MD）",
    "elongation at break (td)": "断裂伸长率（TD）",
    "tensile strength (md)": "抗拉强度（MD）",
    "tensile strength (td)": "抗拉强度（TD）",
    "brightness(iso)": "亮度（ISO）", "iso. opacity": "不透明度（ISO）",
}

SPEC_ORDER = ["base material", "basic material", "material", "thickness", "width",
              "length", "type", "grade", "color", "colour", "printing",
              "surface treatment", "corona treatment", "coating", "heat seal",
              "tensile strength", "elongation", "application", "core", "remark"]

DROP_SPEC_KEYS = {"price", "was price", "now price", "clicks", "last update",
                  "manufacturer", "product name", "product no", "model",
                  "product description", "buy", "inquiry", "quotation",
                  "moq", "delivery", "payment terms", "port", "certification"}


# --------------------------------------------------------------- helpers ---
def smart_title(name):
    """Tidy legacy ALL-CAPS names into readable title case."""
    name = re.sub(r"\s+", " ", (name or "").strip())
    if not name:
        return name

    def fix(word):
        core = word.strip("(),.:;/-[]")
        if not core:
            return word
        if any(ch.isdigit() for ch in core):
            return word
        if core.upper() in KEEP_UPPER:
            return word.replace(core, core.upper())
        if core.isupper() and len(core) > 3:
            return word.replace(core, core.capitalize())
        return word

    out = " ".join(fix(w) for w in name.split(" "))
    out = re.sub(r"\s+([,.;:)])", r"\1", out)
    return out.strip()


ACRONYM_RE = re.compile(r"^[A-Z0-9][A-Z0-9\-/&]*$")


def _join_zh(parts):
    """Join translated name parts: space only around acronyms / latin words."""
    out = ""
    for part in parts:
        if not out:
            out = part
            continue
        prev = out.split(" ")[-1]
        acronym = (ACRONYM_RE.match(part) or ACRONYM_RE.match(prev))
        both_latin = re.search(r"[A-Za-z]", part) and re.search(r"[A-Za-z]", prev)
        if acronym or both_latin:
            out += " " + part
        else:
            out += part
    return out


def translate_name(name):
    """EN -> ZH product name. Phrases first (longest match), then tokens."""
    text = re.sub(r"\s+", " ", name or "").strip()
    # split a unit or a word glued to a number: "12MICRONS", "film3.8"
    text = re.sub(r"(\d)\s*(MICRONS|MICRON|MIC|UM|GSM|CM|MM)\b", r"\1 \2", text,
                  flags=re.I)
    text = re.sub(r"([A-Za-z])(?=\d)", r"\1 ", text)
    text = re.sub(r"(?<=\d)([A-Za-z])", r" \1", text)
    for phrase, zh in sorted(MERGED_PHRASES, key=lambda x: -len(x[0])):
        text = re.sub(r"\b" + re.escape(phrase) + r"\b", zh, text, flags=re.I)
    parts = []
    for word in text.split(" "):
        core = word.strip("(),.:;/[]")
        if not core:
            if word.strip():
                parts.append(word)
            continue
        up = core.upper()
        if up in KEEP_UPPER:
            parts.append(up)
        elif up in ZH_TOKENS:
            parts.append(ZH_TOKENS[up])
        else:
            parts.append(word)
    out = _join_zh(parts).strip()
    out = re.sub(r"\s+([,.;:)])", r"\1", out)
    out = re.sub(r"\.$", "", out)
    # keep the parentheses balanced
    if out.count("(") > out.count(")"):
        out = re.sub(r"\s*\(", " ", out)
    elif out.count(")") > out.count("("):
        out = re.sub(r"\s*\)", " ", out)
    return out.strip()


def clean_text(text):
    text = (text or "").replace("\ufffd", " ").replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def spec_sort_key(item):
    key = item[0].strip().lower()
    return (SPEC_ORDER.index(key) if key in SPEC_ORDER else len(SPEC_ORDER), key)


def clean_specs(pairs):
    out = []
    seen = set()
    for k, v in pairs:
        k = clean_text(k).strip(" .:;")
        v = clean_text(v).strip(" .;")
        if not k or not v:
            continue
        if k.lower() in DROP_SPEC_KEYS:
            continue
        if len(k) > 46 or len(v) > 600:
            continue
        if not re.search(r"[A-Za-z\u4e00-\u9fff]", k):
            continue
        lk = k.lower()
        if lk in seen:
            continue
        seen.add(lk)
        out.append((k, v))
    out.sort(key=spec_sort_key)
    return out


def summary_from(product, lang):
    """Short product description for cards and meta tags."""
    intro = clean_text(product.get("intro"))
    if intro:
        text = intro
    else:
        text = ""
        for item in product.get("items", []):
            if item.get("text"):
                text = clean_text(item["text"])
                break
            if item.get("specs"):
                text = "; ".join(f"{k}: {v}" for k, v in item["specs"][:3])
                break
    if not text:
        text = product["name"]
    if len(text) > 190:
        text = text[:190].rsplit(" ", 1)[0] + "…"
    return text


SUMMARY_KEYS = ("厚度", "宽度", "长度", "纸芯", "颜色", "基材", "表面处理",
                "热封性能", "材质", "克重")


def summary_zh(product):
    """Chinese summary: category headline plus the leading technical parameters."""
    cat = CATEGORY_CONTENT.get(product["cat_slug"], {}).get("zh", {})
    base = cat.get("highlights", [""])
    parts = []
    for item in product.get("items_zh", product.get("items", [])):
        for k, v in item.get("specs", []):
            if k not in SUMMARY_KEYS or len(v) > 44:
                continue
            parts.append(f"{k} {v}")
        if parts:
            break
    text = base[0] if base else product.get("name_zh", "")
    if parts:
        text = text + "（" + "；".join(parts[:3]) + "）"
    text = clean_text(text)
    if len(text) > 200:
        text = text[:200].rsplit(" ", 1)[0] + "…"
    return text


def feature_block(ctx, product):
    cat = CATEGORY_CONTENT.get(product["cat_slug"], {})
    content = cat.get(ctx.lang, {})
    return content.get("highlights", []), content.get("applications", [])


# ------------------------------------------------------------- pipeline ---
def load_products():
    raw_path = os.path.join(HERE, "build", "products_raw.json")
    with open(raw_path, "r", encoding="utf-8") as fh:
        raw = json.load(fh)
    with open(os.path.join(HERE, "build", "images.json"), "r", encoding="utf-8") as fh:
        images = json.load(fh)

    products = []
    for item in raw:
        pid = item["id"]
        cat = CATEGORIES.get(item.get("sort"), None)
        if cat is None:
            continue
        stem = None
        for key in images:
            if key.split("_")[0] == pid:
                stem = key
                break
        name_en = smart_title(item.get("name")) or f"Product {pid}"
        name_en = name_en if len(name_en) <= 118 else name_en[:118].rsplit(" ", 1)[0] + "…"
        name_zh = ZH_NAME_OVERRIDE.get(pid) or translate_name(name_en)
        products.append({
            "id": pid,
            "sort": item.get("sort"),
            "cat_slug": cat["slug"],
            "cat_name": cat["en"],
            "cat_name_zh": cat["zh"],
            "name": name_en,
            "name_zh": name_zh,
            "model": clean_text(item.get("model")),
            "product_no": clean_text(item.get("product_no")),
            "updated": clean_text(item.get("updated")),
            "intro": clean_text(item.get("intro")),
            "items": [{"heading": clean_text(i.get("heading")),
                       "specs": clean_specs(i.get("specs", [])),
                       "text": clean_text(i.get("text"))[:600]}
                      for i in item.get("items", [])],
            "image_main": ((images.get(stem, {}) or {}).get("main", "") or "").replace("assets/", "") if stem else "",
            "image_thumb": ((images.get(stem, {}) or {}).get("thumb", "") or "").replace("assets/", "") if stem else "",
            "image_stems": sorted([k for k in images if k.split("_")[0] == pid]),
        })
    return products, images


CJK_RE = re.compile(r"[\u4e00-\u9fff]")


def has_cjk(text):
    return bool(CJK_RE.search(text or ""))


def strip_cjk(text):
    """Drop Chinese fragments the legacy English pages carried over."""
    if not has_cjk(text):
        return clean_text(text)
    out = re.sub(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]+", " ", text)
    out = re.sub(r"\(\s*\)|\uff08\s*\uff09|\[\s*\]", " ", out)
    return clean_text(out)


def build_summary_en(p):
    """English summary: never contains Chinese."""
    txt = p.get("intro_en", "")
    if not txt:
        for it in p.get("items_en", []):
            if it.get("specs"):
                txt = "; ".join(f"{k}: {v}" for k, v in it["specs"][:3])
                break
            if it.get("text"):
                txt = it["text"]
                break
    if not txt:
        txt = p["name_en"]
    txt = clean_text(txt)
    if len(txt) > 190:
        txt = txt[:190].rsplit(" ", 1)[0] + "\u2026"
    return txt


def model_display(model):
    """Legacy 'model' field -> (english label, chinese label).

    The field mixes API product codes ("API-PP-03"), bare numbers and
    product-name-like strings.  Pure numbers carry no information and are
    dropped; API codes stay as they are in both languages.
    """
    text = clean_text(model)
    if not text:
        return "", ""
    if re.fullmatch(r"[\d\.\s]+", text):
        return "", ""
    en = strip_cjk(text)
    if not en:
        return "", ""
    if re.fullmatch(r"API[-–_ ]?[A-Za-z0-9\-]*", en):
        return en, en
    zh = translate_name(en)
    if re.search(r"[A-Za-z]{4,}", zh) and not re.search(r"[\u4e00-\u9fff]", zh):
        zh = tr.zh_value(en)
    return en, zh


def prepare_products(products, images):
    """Attach language-specific display fields."""
    for p in products:
        items_en = []
        items_zh = []
        for it in p["items"]:
            # ---- English block
            specs = []
            for k, v in it["specs"]:
                key = tr.en_key(k)
                if not key:
                    continue
                val = tr.en_value(v)
                if not val:
                    continue
                specs.append((key, val))
            text_en = strip_cjk(it["text"])
            if text_en:
                text_en = tr.structure_value(text_en)
            if specs or text_en:
                items_en.append({"heading": strip_cjk(it["heading"]),
                                 "specs": specs,
                                 "text": "" if specs else text_en})

            # ---- Chinese block
            specs_zh = []
            for k, v in it["specs"]:
                key = tr.zh_key(k)
                if not key:
                    continue
                val = tr.zh_value(v)
                if not val:
                    continue
                specs_zh.append((key, val))
            heading_zh = tr.zh_heading(it["heading"])
            if specs_zh or heading_zh:
                items_zh.append({"heading": heading_zh,
                                 "specs": specs_zh,
                                 "text": "" if specs_zh else ""})

        p["items_en"] = items_en
        p["items_zh"] = items_zh

        # --- facts that the legacy pages only mention in prose
        inf_en, inf_zh = infer.infer_specs(p)
        have_en = {k.lower() for it in items_en for k, _ in it["specs"]}
        have_zh = {k.lower() for it in items_zh for k, _ in it["specs"]}
        extra_en = [(k, v) for k, v in inf_en if k.lower() not in have_en]
        extra_zh = [(k, v) for k, v in inf_zh if k.lower() not in have_zh]

        # every product states its typical end use, taken from its category
        cat_en = CATEGORY_CONTENT.get(p["cat_slug"], {}).get("en", {})
        cat_zh = CATEGORY_CONTENT.get(p["cat_slug"], {}).get("zh", {})
        apps_en = cat_en.get("applications", [])
        apps_zh = cat_zh.get("applications", [])
        if apps_en and "application" not in have_en:
            extra_en.append(("Application", "; ".join(apps_en[:3])))
        if apps_zh and "应用领域" not in have_zh:
            extra_zh.append(("应用领域", "；".join(apps_zh[:3])))

        if extra_en:
            items_en.append({"heading": "Product characteristics",
                             "specs": extra_en, "text": ""})
        if extra_zh:
            items_zh.append({"heading": "产品特点",
                             "specs": extra_zh, "text": ""})

        p["name_en"] = strip_cjk(p["name"]) or p["name"]
        p["model_en"], p["model_zh"] = model_display(p["model"])
        p["intro_en"] = strip_cjk(p["intro"])
        p["summary_en"] = build_summary_en(p)
        p["summary_zh"] = summary_zh(p)
        p["search_text"] = " ".join([
            p["name_en"], p["name_zh"], p["id"], p["model_en"], p["model_zh"],
            p["cat_name"], p["cat_name_zh"], p["summary_en"][:200],
            " ".join(k for it in p["items_en"] for k, _ in it["specs"]),
        ]).lower()
    return products


def related_for(product, products, limit=4):
    same = [p for p in products if p["cat_slug"] == product["cat_slug"] and p["id"] != product["id"]]
    if len(same) < limit:
        extra = [p for p in products if p["cat_slug"] != product["cat_slug"] and p["id"] != product["id"]]
        same += extra
    return same[:limit]


# --------------------------------------------------------------- pages ----
def render_home(ctx, products):
    t = ctx.t
    c = COMPANY[ctx.lang]
    ctx.current = f"{ctx.lang}/index.html"
    featured = [p for p in products if p["id"] in FEATURED]
    featured.sort(key=lambda p: FEATURED.index(p["id"]))
    cards = "".join(product_card(ctx, p) for p in featured)
    posts = "".join(post_card(ctx, a) for a in ARTICLES[:3])
    lede = ("Asia Pacific Industry Group manufactures BOPP, BOPET and CPP films — heat-seal, "
            "lamination, metallised, tear-tape and thermal-transfer grades supplied to packaging "
            "and printing converters in more than 80 countries."
            if ctx.lang == "en" else
            "亚太工业集团生产 BOPP、BOPET 与 CPP 薄膜，涵盖热封、复合、镀铝、易撕胶带与热转印等牌号，"
            "供应全球 80 多个国家的包装与印刷转换企业。")
    body = f"""
<section class="hero">
  <div class="shell hero-inner">
    <span class="eyebrow">{esc(c['legal_name'])}</span>
    <h1>{'Engineered ' if ctx.lang == 'en' else '精密制造的'}<em>{'BOPP, BOPET & CPP ' if ctx.lang == 'en' else 'BOPP、BOPET 与 CPP '}</em>{'films for packaging and labelling' if ctx.lang == 'en' else '薄膜'}</h1>
    <p class="hero-sub">{lede}</p>
    <div class="hero-actions">
      <a class="btn btn-gold" href="{ctx.page('products.html')}">{esc(t['products_cta'])}</a>
      <a class="btn btn-line" href="{ctx.page('blog.html')}">{esc(t['blog_cta'])}</a>
    </div>
  </div>
</section>

<section class="section dark">
  <div class="shell">{stat_block(ctx)}</div>
</section>

<section class="section">
  <div class="shell">
    {section_head(ctx, t['products'] if ctx.lang == 'en' else 'PRODUCTS', t['featured'], t['featured_sub'])}
    <div class="grid grid-3">{cards}</div>
    <div style="text-align:center;margin-top:38px">
      <a class="btn btn-outline" href="{ctx.page('products.html')}">{esc(t['products_cta'])} &rarr;</a>
    </div>
  </div>
</section>

<section class="section tint">
  <div class="shell split">
    <div>{pillar_block(ctx)}</div>
    <div>
      {section_head(ctx, t['why'], t['why'] if ctx.lang == 'en' else 'Why us', '', center=False)}
      <p style="color:var(--muted);font-size:15px">{esc(c['tagline'])}</p>
      <div style="margin-top:26px">{cta_band(ctx)}</div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    {section_head(ctx, t['blog'], t['latest_posts'], t['latest_posts_sub'])}
    <div class="grid grid-3">{posts}</div>
    <div style="text-align:center;margin-top:38px">
      <a class="btn btn-outline" href="{ctx.page('blog.html')}">{esc(t['blog_cta'])} &rarr;</a>
    </div>
  </div>
</section>

<section class="section tint">
  <div class="shell">
    <div class="contact-layout">
      {contact_info_card(ctx)}
      {inquiry_form(ctx)}
    </div>
  </div>
</section>
"""
    return document(ctx, t["home"], lede, body)


def render_catalogue(ctx, products):
    t = ctx.t
    ctx.current = f"{ctx.lang}/products.html"
    cats = []
    used = {}
    for p in products:
        used.setdefault(p["cat_slug"], p["cat_name_zh"] if ctx.lang == "zh" else p["cat_name"])
    for slug, name in used.items():
        cats.append(f'<button type="button" data-cat="{esc(slug)}">{esc(name)}</button>')
    buttons = f'<button type="button" class="on" data-cat="all">{esc(t["all"])}</button>' + "".join(cats)
    cards = "".join(product_card(ctx, p) for p in products)
    body = f"""
{page_head(ctx, [(t['home'], ctx.home()), (t['products'], '')], t['catalogue'], t['catalogue_sub'])}
<section class="section">
  <div class="shell">
    <div class="filter-bar" data-filter-root>
      {buttons}
      <input class="search-box" type="search" data-search placeholder="{esc(t['search_ph'])}">
    </div>
    <p style="color:var(--muted);font-size:13.5px"><span data-count>{len(products)}</span> {esc(t['results'])}</p>
    <div class="grid grid-3" style="margin-top:20px">{cards}</div>
    <p class="empty" data-empty style="display:none">{esc(t['no_results'])}</p>
  </div>
</section>
<section class="section tint">
  <div class="shell">{cta_band(ctx)}</div>
</section>
"""
    return document(ctx, t["products"], t["catalogue_sub"], body)


def render_product(ctx, p, products):
    t = ctx.t
    ctx.current = f"{ctx.lang}/products/{p['id']}.html"
    name = p["name_en"] if ctx.lang == "en" else p["name_zh"]
    summary = p["summary_en"] if ctx.lang == "en" else p["summary_zh"]
    summary = clean_text(summary)[:240]
    # Detail pages show the full product description; the short summary is
    # kept for meta tags and catalogue cards only.
    full_desc = clean_text(p["intro_en"]) if ctx.lang == "en" else summary
    if not full_desc:
        full_desc = summary
    source_items = p["items_en"] if ctx.lang == "en" else p["items_zh"]
    highlights, applications = feature_block(ctx, p)
    cat_name = p["cat_name"] if ctx.lang == "en" else p["cat_name_zh"]

    # --- specification blocks
    blocks = []
    for idx, item in enumerate(source_items):
        specs = item["specs"]
        if not specs:
            if item["text"]:
                blocks.append(
                    f'<div class="spec-block"><h3>{esc(item["heading"]) or esc(t["overview"])}</h3>'
                    f'<p style="font-size:14.5px;color:var(--ink-soft)">{esc(item["text"])}</p></div>')
            continue
        heading = item["heading"]
        rows = []
        for k, v in specs:
            rows.append(f"<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>")
        blocks.append(
            f'<div class="spec-block"><h3>{esc(heading) or esc(t["overview"])}</h3>'
            f'<div class="spec-wrap"><table class="spec-table"><tbody>{"".join(rows)}</tbody></table></div></div>')

    if not blocks:
        blocks.append(f'<div class="spec-block"><p style="color:var(--muted)">{esc(t["specs_sub"])}</p></div>')

    # --- gallery
    thumbs = ""
    main_src = p["image_main"]
    if p["image_stems"]:
        for i, stem in enumerate(p["image_stems"]):
            src = f"img/{stem}.jpg"
            thumbs += (f'<img src="{ctx.asset(src)}" alt="{esc(name)}" data-gallery-thumb '
                       f'data-src="{ctx.asset(src)}" data-alt="{esc(name)}" class="{"on" if i == 0 else ""}">')
    gallery = f"""<div class="gallery" data-gallery>
  <div class="gallery-main"><img data-gallery-main src="{ctx.asset(main_src)}" alt="{esc(name)}"></div>
  <div class="gallery-thumbs">{thumbs}</div>
</div>""" if main_src else ""

    no_label = "Product No." if ctx.lang == "en" else "产品编号"
    chips = f'<span class="chip">{esc(cat_name)}</span>'
    chips += f'<span class="chip gold">{esc(no_label)} {esc(p["id"])}</span>'
    model = p["model_en"] if ctx.lang == "en" else p["model_zh"]
    if model:
        chips += f'<span class="chip">{esc(model)}</span>'

    feat_html = "".join(f"<li>{esc(x)}</li>" for x in highlights)
    app_html = "".join(f"<li>{esc(x)}</li>" for x in applications)

    related = related_for(p, products)
    rel_html = "".join(product_card(ctx, r) for r in related)

    body = f"""
{page_head(ctx, [(t['home'], ctx.home()), (t['products'], ctx.page('products.html')), (name, '')], name, full_desc)}
<section class="section">
  <div class="shell">
    <div class="product-layout">
      {gallery}
      <div class="product-head">
        <div class="product-tags">{chips}</div>
        <h1>{esc(name)}</h1>
        <p style="font-size:15.5px;color:var(--ink-soft)">{esc(full_desc)}</p>
        {f'<h2 style="font-size:16px;margin-top:26px">{esc(t["features"])}</h2><ul class="feature-list">{feat_html}</ul>' if highlights else ''}
        {f'<h2 style="font-size:16px;margin-top:26px">{esc(t["applications"])}</h2><ul class="app-list">{app_html}</ul>' if applications else ''}
        <div class="product-cta">
          <a class="btn btn-solid" href="{ctx.page('contact.html')}">{esc(t['quote_cta'])}</a>
          <a class="btn btn-outline" href="{ctx.page('products.html')}">{esc(t['products_cta'])}</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section tint">
  <div class="shell">
    {section_head(ctx, t['specs'], t['specs'], t['specs_sub'], center=False)}
    {''.join(blocks)}
  </div>
</section>

<section class="section">
  <div class="shell">
    {section_head(ctx, t['products'], t['related'], t['related_sub'])}
    <div class="related">{rel_html}</div>
  </div>
</section>

<section class="section tint">
  <div class="shell">{cta_band(ctx)}</div>
</section>
"""
    return document(ctx, name, summary, body)


def render_blog_index(ctx):
    t = ctx.t
    ctx.current = f"{ctx.lang}/blog.html"
    cards = "".join(post_card(ctx, a) for a in ARTICLES)
    body = f"""
{page_head(ctx, [(t['home'], ctx.home()), (t['blog'], '')], t['blog'], t['blog_sub'])}
<section class="section">
  <div class="shell">
    <div class="grid grid-3">{cards}</div>
  </div>
</section>
<section class="section tint">
  <div class="shell">{cta_band(ctx)}</div>
</section>
"""
    return document(ctx, t["blog"], t["blog_sub"], body)


def render_article(ctx, article):
    t = ctx.t
    ctx.current = f"{ctx.lang}/blog/{article['slug']}.html"
    title = article["title"][ctx.lang]
    body_parts = []
    for block in article["body"][ctx.lang]:
        if block.startswith("## "):
            body_parts.append(f"<h2>{esc(block[3:])}</h2>")
        elif block.startswith("- "):
            items = "".join(f"<li>{esc(line[2:])}</li>" for line in [block])
            body_parts.append(f"<ul>{items}</ul>")
        else:
            body_parts.append(f"<p>{esc(block)}</p>")
    points = "".join(f"<li>{esc(x)}</li>" for x in article["key_points"][ctx.lang])
    others = [a for a in ARTICLES if a["slug"] != article["slug"]][:3]
    rel = "".join(post_card(ctx, a) for a in others)
    body = f"""
{page_head(ctx, [(t['home'], ctx.home()), (t['blog'], ctx.page('blog.html')), (title, '')], title, article['excerpt'][ctx.lang])}
<section class="section">
  <div class="shell">
    <div class="article-body">
      <div class="article-meta">
        <span class="cat" style="color:var(--green-500);font-weight:700">{esc(article['category'][ctx.lang])}</span>
        <span>{esc(article['date'])}</span>
        <span>{article['minutes']} {esc(t['minutes'])}</span>
      </div>
      <div class="key-points"><h4>{esc(t['key_points'])}</h4><ul>{points}</ul></div>
      <div class="prose">{''.join(body_parts)}</div>
      <div style="margin-top:36px">{cta_band(ctx)}</div>
    </div>
  </div>
</section>
<section class="section tint">
  <div class="shell">
    {section_head(ctx, t['blog'], t['related_posts'], '')}
    <div class="grid grid-3">{rel}</div>
  </div>
</section>
"""
    return document(ctx, title, article["excerpt"][ctx.lang], body)


def render_about(ctx, products):
    t = ctx.t
    ctx.current = f"{ctx.lang}/about.html"
    c = COMPANY[ctx.lang]
    if ctx.lang == "en":
        intro = ("Asia Pacific Industry Group Co., Limited is a Chinese manufacturer of flexible "
                 "packaging films, established in Hefei, Anhui Province. The company operates "
                 "BOPP, BOPET and CPP film lines together with coating, slitting and converting "
                 "capacity, and supplies converters, printers and brand owners in more than 80 "
                 "countries. The film business sits alongside the group company "
                 "www.apigcl.com, which serves the wider industrial and trading community.")
        story = ("The company grew out of a packaging-materials trading operation and progressively "
                 "moved upstream into film manufacturing. That history still shapes how it works: "
                 "a great deal of the business is technical problem-solving for converters who need "
                 "a specific grade running reliably on their own equipment, rather than a catalogue "
                 "purchase. Production is organised around audited lines with in-line gauge and "
                 "defect control, so a specification agreed once keeps holding over repeat orders.")
        capability = ("We produce biaxially oriented polypropylene, biaxially oriented polyester and "
                      "cast polypropylene, plus coating, metallising partners, printing and converting "
                      "support. In-house capability covers corona treatment selection, coating, "
                      "slitting, rewinding and finished-roll conversion. Typical output serves flexible "
                      "packaging, labelling and thermal transfer ribbon converters, print-and-lamination "
                      "houses and trading partners who supply them.")
        quality = ("Quality management operates under an ISO-certified system covering incoming raw "
                   "material, in-process gauging, defect inspection, finished-reel testing and "
                   "traceability. Every reel carries a production identity that can be traced back to "
                   "the line and the raw material lot. Food-contact declarations, REACH and RoHS "
                   "statements and certificates of analysis are available per grade, and documentation "
                   "is agreed before production rather than assembled afterwards.")
        cap_title = "Manufacturing and supply scope"
        qual_title = "Quality, compliance and documentation"
    else:
        intro = ("亚太工业集团有限公司是中国合肥的柔性包装薄膜制造企业。公司拥有 BOPP、BOPET 与 CPP "
                 "生产线，并具备涂布、分切与转换加工能力，产品供应全球 80 多个国家的转换商、印刷企业与品牌商。"
                 "薄膜业务与集团公司 www.apigcl.com 并行，后者服务于更广泛的工业与贸易客户群体。")
        story = ("公司由包装材料贸易起步，逐步向上游延伸至薄膜制造。这段经历至今仍影响着公司的做事方式："
                 "大量业务是为转换商解决技术问题——让特定牌号在他们自己的设备上稳定运行——而不是简单的目录采购。"
                 "生产围绕经过审核的产线组织，配备在线测厚与缺陷检测，因此一次确认的规格可以在重复订单中长期保持。")
        capability = ("我们生产双向拉伸聚丙烯、双向拉伸聚酯与流延聚丙烯薄膜，并提供涂布、镀铝协作、"
                      "印刷与转换加工支持。自有能力覆盖电晕处理选择、涂布、分切、复卷与成品卷转换。"
                      "典型产出服务于软包装、标签与热转印转换企业、印刷复合企业，以及为其供货的贸易伙伴。")
        quality = ("质量管理体系通过 ISO 认证，覆盖原料进厂、在制测厚、缺陷检验、成品卷测试与可追溯性。"
                   "每一卷都带有可回溯至产线与原料批次的生产标识。每个牌号均可提供食品接触声明、REACH 与 RoHS "
                   "声明及检测报告，相关文件在生产前即确认，而非事后补齐。")
        cap_title = "制造与供应范围"
        qual_title = "质量、合规与文件"

    pillars = "".join(
        f'<div class="pillar"><div class="ico">{i:02d}</div><div><h4>{esc(title)}</h4><p>{esc(text)}</p></div></div>'
        for i, (title, text) in enumerate([
            (t["our_story"], story),
            (cap_title, capability),
            (qual_title, quality),
        ], 1)
    )
    cats = {}
    for p in products:
        cats.setdefault(p["cat_slug"], p["cat_name"] if ctx.lang == "en" else p["cat_name_zh"])
    cat_html = "".join(f'<span class="chip">{esc(v)}</span>' for v in cats.values())

    body = f"""
{page_head(ctx, [(t['home'], ctx.home()), (t['about'], '')], t['about'], intro)}
<section class="section">
  <div class="shell split">
    <div>{pillars}</div>
    <div>
      <h2 style="font-size:22px">{esc(t['capability'])}</h2>
      <p style="color:var(--muted);font-size:15px">{esc(intro)}</p>
      <div style="margin-top:22px;display:flex;flex-wrap:wrap;gap:9px">{cat_html}</div>
      <div style="margin-top:30px">{cta_band(ctx)}</div>
    </div>
  </div>
</section>
<section class="section tint">
  <div class="shell">
    <div class="contact-layout">
      {contact_info_card(ctx)}
      <div>
        <h2 style="font-size:20px;margin-bottom:14px">{esc(t['contact'])}</h2>
        {inquiry_form(ctx)}
      </div>
    </div>
  </div>
</section>
"""
    return document(ctx, t["about"], intro, body)


def render_contact(ctx):
    t = ctx.t
    ctx.current = f"{ctx.lang}/contact.html"
    c = COMPANY[ctx.lang]
    body = f"""
{page_head(ctx, [(t['home'], ctx.home()), (t['contact'], '')], t['contact'], c['tagline'])}
<section class="section">
  <div class="shell contact-layout">
    {contact_info_card(ctx)}
    {inquiry_form(ctx)}
  </div>
</section>
"""
    return document(ctx, t["contact"], c["tagline"], body)


def render_gateway():
    """Root index: pick a language, then leave.
    Matches the live gateway page (canonical/OG tags, remembered
    language choice via localStorage, English default)."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Asia Pacific Industry Group Co., Limited | BOPP, BOPET &amp; CPP Films</title>
<meta name="description" content="Asia Pacific Industry Group Co., Limited - BOPP, BOPET and CPP packaging films from Hefei, Anhui, China. Technical blog, product catalogue and contact details.">
<link rel="canonical" href="https://blog.boppfilmsales.com/en/">
<link rel="alternate" hreflang="en" href="https://blog.boppfilmsales.com/en/">
<link rel="alternate" hreflang="zh-CN" href="https://blog.boppfilmsales.com/zh/">
<link rel="alternate" hreflang="x-default" href="https://blog.boppfilmsales.com/en/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Asia Pacific Industry Group Co., Limited">
<meta property="og:title" content="Asia Pacific Industry Group Co., Limited | BOPP, BOPET &amp; CPP Films">
<meta property="og:description" content="BOPP, BOPET and CPP packaging films from Hefei, Anhui, China. Flexible packaging and labelling films for more than 80 countries.">
<meta property="og:url" content="https://blog.boppfilmsales.com/">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
<meta name="theme-color" content="#064e3b">
<script>
(function () {
  // The English site is the default entry point for the bare domain. The
  // Chinese site stays reachable at /zh/ and through the language switcher;
  // a visitor only lands there again after picking it explicitly.
  var stored = null;
  try { stored = localStorage.getItem('apig_lang'); } catch (e) {}
  location.replace(stored === 'zh' ? 'zh/' : 'en/');
})();
</script>
</head>
<body>
<main id="main">
  <section class="hero" style="min-height:82vh;display:grid;place-items:center;text-align:center">
    <div class="shell hero-inner">
      <span class="eyebrow" style="justify-content:center">Asia Pacific Industry Group Co., Limited</span>
      <h1>BOPP, BOPET &amp; CPP Films</h1>
      <p class="hero-sub" style="margin-left:auto;margin-right:auto">Hefei, Anhui, China &middot; Flexible packaging and labelling films for more than 80 countries.</p>
      <div class="hero-actions" style="justify-content:center">
        <a class="btn btn-gold" href="en/" onclick="try{localStorage.setItem('apig_lang','en')}catch(e){}">English site</a>
        <a class="btn btn-line" href="zh/" onclick="try{localStorage.setItem('apig_lang','zh')}catch(e){}">中文网站</a>
      </div>
      <noscript><p style="margin-top:26px"><a href="en/" style="color:var(--gold)">English</a> &middot; <a href="zh/" style="color:var(--gold)">中文</a></p></noscript>
    </div>
  </section>
</main>
</body>
</html>
"""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Asia Pacific Industry Group Co., Limited | BOPP, BOPET &amp; CPP Films</title>
<meta name="description" content="Asia Pacific Industry Group Co., Limited - BOPP, BOPET and CPP packaging films from Hefei, Anhui, China. Technical blog, product catalogue and contact details.">
<link rel="alternate" hreflang="en" href="/en/">
<link rel="alternate" hreflang="zh-CN" href="/zh/">
<link rel="alternate" hreflang="x-default" href="/en/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
<script>
(function () {
  var zh = /^zh/i.test(navigator.language || '') || /^zh/i.test(navigator.userLanguage || '');
  location.replace(zh ? 'zh/' : 'en/');
})();
</script>
</head>
<body>
<main id="main">
  <section class="hero" style="min-height:82vh;display:grid;place-items:center;text-align:center">
    <div class="shell hero-inner">
      <span class="eyebrow" style="justify-content:center">Asia Pacific Industry Group Co., Limited</span>
      <h1>BOPP, BOPET &amp; CPP Films</h1>
      <p class="hero-sub" style="margin-left:auto;margin-right:auto">Hefei, Anhui, China &middot; Flexible packaging and labelling films for more than 80 countries.</p>
      <div class="hero-actions" style="justify-content:center">
        <a class="btn btn-gold" href="en/">English site</a>
        <a class="btn btn-line" href="zh/">中文网站</a>
      </div>
      <noscript><p style="margin-top:26px"><a href="en/" style="color:var(--gold)">English</a> &middot; <a href="zh/" style="color:var(--gold)">中文</a></p></noscript>
    </div>
  </section>
</main>
</body>
</html>
"""


def write(path, content):
    full = os.path.join(HERE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    # Repo stores generated pages with CRLF line endings (Windows origin);
    # keep that format so regenerations do not rewrite every file.
    with open(full, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write(content)


def main():
    products, images = load_products()
    products = prepare_products(products, images)
    print("products ready:", len(products))
    total = 0
    for lang in ("en", "zh"):
        ctx0 = Ctx(lang, 0)
        ctx1 = Ctx(lang, 1)
        write(f"{lang}/index.html", render_home(ctx0, products))
        write(f"{lang}/products.html", render_catalogue(ctx0, products))
        write(f"{lang}/blog.html", render_blog_index(ctx0))
        write(f"{lang}/about.html", render_about(ctx0, products))
        write(f"{lang}/contact.html", render_contact(ctx0))
        for p in products:
            write(f"{lang}/products/{p['id']}.html", render_product(ctx1, p, products))
        for a in ARTICLES:
            write(f"{lang}/blog/{a['slug']}.html", render_article(ctx1, a))
        total += len(products) + len(ARTICLES) + 5
        print(f"  {lang}: {len(products)} products, {len(ARTICLES)} articles")
    write("index.html", render_gateway())

    # legacy URLs -> new locations
    lines = []
    for p in products:
        lines.append(f"/product-{p['id']}.html  /en/products/{p['id']}  301")
    for legacy in ("bopet", "bops", "heatseal", "lamination"):
        lines.append(f"/{legacy}.html  /en/products.html  301")
    lines.append("/product-*.html  /en/products.html  301")
    write("_redirects", "\n".join(lines) + "\n")
    print("pages written:", total + 1)


if __name__ == "__main__":
    main()
