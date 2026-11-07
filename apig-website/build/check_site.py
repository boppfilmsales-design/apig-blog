# -*- coding: utf-8 -*-
"""Pre-deploy sanity checks for the generated bilingual site.

Verifies:
  * every internal link and image reference resolves to a real file
  * the English tree contains no Chinese body copy (and vice versa)
  * the current company details appear on every page
  * no legacy placeholder text survived
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ("en", "zh")

COMPANY_MARKERS = {
    "en": ["No.3399 Luzhou Ave.", "+0086-551-64687285", "+0086-551-64683490",
           "sales@boppfilmsales.com", "admin@apigcl.com", "asiapacificsale",
           "840715367", "0086-18919654871", "18919659471", "www.apigcl.com",
           "Asia Pacific Industry Group Co., Limited"],
    "zh": ["3399", "64687285", "64683490", "sales@boppfilmsales.com",
           "admin@apigcl.com", "asiapacificsale", "840715367",
           "18919654871", "18919659471", "www.apigcl.com"],
}

CJK = re.compile(r"[\u4e00-\u9fa5]")
LATIN_WORD = re.compile(r"[A-Za-z]{4,}")

SKIP_FILES = {"index.html"}


def html_files(lang):
    base = os.path.join(HERE, lang)
    out = []
    for root, _dirs, files in os.walk(base):
        for f in files:
            if f.endswith(".html"):
                out.append(os.path.join(root, f))
    return out


def main():
    problems = []
    stats = {}

    for lang in LANGS:
        files = html_files(lang)
        stats[lang] = {"pages": len(files), "broken_links": 0, "broken_images": 0,
                       "cjk_leak": 0, "missing_company": 0}
        for path in files:
            rel = os.path.relpath(path, HERE).replace("\\", "/")
            src = open(path, encoding="utf-8").read()
            page_dir = os.path.dirname(path)

            # --- links & images
            refs = []
            refs += [("a", l) for l in re.findall(r'<a[^>]+href="([^"]+)"', src)]
            refs += [("link", l) for l in re.findall(r'<link[^>]+href="([^"]+)"', src)]
            refs += [("img", l) for l in re.findall(r'<img[^>]+src="([^"]+)"', src)]
            refs += [("script", l) for l in re.findall(r'<script[^>]+src="([^"]+)"', src)]
            for kind, link in refs:
                if link.startswith(("http://", "https://", "mailto:", "data:", "#", "//")):
                    continue
                target = link.split("#")[0].split("?")[0]
                if not target:
                    continue
                # bare external domain such as www.apigcl.com
                if "/" not in target and "." in target and not target.endswith(
                        (".html", ".css", ".js", ".jpg", ".jpeg", ".png", ".webp", ".svg")):
                    continue
                resolved = os.path.normpath(os.path.join(page_dir, target))
                if not os.path.exists(resolved):
                    if kind == "img":
                        stats[lang]["broken_images"] += 1
                        problems.append(f"[{lang}] missing image  {rel} -> {link}")
                    else:
                        stats[lang]["broken_links"] += 1
                        problems.append(f"[{lang}] broken {kind:<6} {rel} -> {link}")

            # --- language purity (body copy only, not attributes/urls)
            body = re.sub(r"<head[\s\S]*?</head>", "", src, flags=re.I)
            body = re.sub(r"<script[\s\S]*?</script>", "", body, flags=re.I)
            body = re.sub(r"<style[\s\S]*?</style>", "", body, flags=re.I)
            # the language toggle legitimately shows the target language name
            body = re.sub(r'<span class="lang-switch">[\s\S]*?</span>', "", body, flags=re.I)
            text = re.sub(r"<[^>]+>", " ", body)
            text = re.sub(r"\s+", " ", text)
            if lang == "en":
                cjk = CJK.findall(text)
                # product names such as 丙烯 are not expected; flag any CJK run
                if cjk:
                    stats[lang]["cjk_leak"] += 1
                    snippet = " ".join(cjk[:12])
                    problems.append(f"[{lang}] Chinese text in English page {rel}: {snippet}")
            else:
                words = LATIN_WORD.findall(text)
                # allow technical tokens (BOPP, BOPET, ISO, Skype, WhatsApp ...)
                allowed = {"BOPP", "BOPET", "CPP", "BOPA", "BOPS", "TTR", "ISO", "OEM",
                           "API", "GPS", "PVC", "PET", "PVA", "EVOH", "Skype", "QQ",
                           "Whatsapp", "WhatsApp", "WeChat", "Tel", "Fax", "Add",
                           "Email", "Website", "Asia", "Pacific", "Industry",
                           "Group", "Limited", "Hefei", "Anhui", "China", "Product",
                           "No", "Mobile", "Online", "On", "line", "Home",
                           "Products", "Blog", "About", "Contact", "Search",
                           "Read", "Article", "All", "Related", "Technical",
                           "Specifications", "Overview", "Type", "Grade",
                           "Thickness", "Width", "Length", "Color", "Printing",
                           "Application", "Material", "Model", "Coating", "Core",
                           "Copyright", "rights", "reserved", "APIG", "BOPPFilm"}
                runs = re.findall(r"(?:[A-Za-z][A-Za-z'\-]*\s+){5,}[A-Za-z][A-Za-z'\-]*", text)
                if runs:
                    stats[lang]["cjk_leak"] += 1
                    problems.append(f"[{lang}] English sentence in Chinese page {rel}: "
                                    f"{' '.join(runs[0].split())[:90]}")

            # --- company details
            for marker in COMPANY_MARKERS[lang]:
                if marker not in src:
                    stats[lang]["missing_company"] += 1
                    problems.append(f"[{lang}] missing company marker '{marker}' in {rel}")
                    break

            # --- legacy leftovers
            for bad_text in ("Asia Pacific International Co", "International Co., Limited",
                             "Anhui Eastern Communication"):
                if bad_text in src:
                    problems.append(f"[{lang}] legacy company name in {rel}: {bad_text}")
                    break

    # ---------------------------------------------------------------- report
    print("=" * 68)
    for lang in LANGS:
        s = stats[lang]
        print(f"{lang.upper():>3}  pages={s['pages']:<5} broken_links={s['broken_links']:<4} "
              f"broken_images={s['broken_images']:<4} lang_leak={s['cjk_leak']:<4} "
              f"company_miss={s['missing_company']}")
    print("=" * 68)
    if problems:
        print(f"{len(problems)} issue(s):")
        for p in problems[:60]:
            print("  -", p)
        if len(problems) > 60:
            print(f"  ... and {len(problems) - 60} more")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
