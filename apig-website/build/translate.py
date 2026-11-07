# -*- coding: utf-8 -*-
"""Rebuild clean, bilingual specification values from the noisy legacy data.

The legacy catalogue stores a whole technical data sheet inside a single
spreadsheet-like cell, e.g.

    "350~1600 mm Customized dimensions and specifications are available upon
     request. Tech Data ( Physical Properties) For Customer Reference : BOPP
     PLAIN FILM"

`structure_value()` cuts that down to the meaningful part and `en_value()` /
`zh_value()` then present it in the page language while keeping every number,
unit and standard reference intact.
"""
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from glossary import ACRONYMS, JUNK_EN, PHRASE_ZH, TERM_ZH, UNIT_ZH

# ---------------------------------------------------------------------------
# Canonical specification keys.  Anything that is not on this list is a
# garbled scrape artefact and gets dropped instead of being published.
CANON_KEYS = [
    "basic material", "base material", "material", "thickness", "caliper",
    "width", "length", "size", "sizes", "core", "color", "colour", "printing",
    "surface treatment", "corona treatment", "coating", "heat seal",
    "tensile strength", "elongation", "density", "opacity", "haze", "brightness",
    "gloss", "standard", "grade", "type", "model", "application", "use",
    "usage", "packing", "packaging", "packing style", "weight", "net weight",
    "gross weight", "adhesive", "feature", "features", "capacity", "appearance",
    "remark", "note", "item", "unit", "value", "quantity", "certificate",
    "certification", "msl", "paper", "roll", "tolerance", "specification",
    "product name", "product description", "style", "whiteness",
    "transparency", "light transmission", "seal strength", "printability",
    "surface tension", "coefficient of friction", "elongation at break",
    "tear strength", "impact resistance", "heat resistance", "thermal shrinkage",
    "shrinkage rate", "storage", "shelf life", "code", "logo", "printing side",
]

# Garbled keys produced by the legacy scraper (leading characters were cut).
GARBLED_KEYS = {
    "idth of bopet thermal transfer basic film": "width",
    "ngth of bopet thermal transfer basic film": "length",
    "ture of bopet thermal transfer basic film": "feature",
    "thickness of bopet thermal transfer film": "thickness",
    "ion of bopet thermal transfer basic film": "application",
    "rmal transfer film product applications": "application",
    "llent machinability technical performance": "feature",
    "mm 350-550 note": "width",
    "wo side(s) with a detailed description of": "feature",
    "aracteristics of a host transmission part": "feature",
    "bility quickly . the central control unit": "feature",
    "automatically . the operation panel parts": "feature",
    "ctly on the screen . motor control system": "feature",
    "th . . the cut volumes positioning system": "feature",
    "itioning action . feed positioning system": "feature",
    "automatic round knife angle adjustment": "feature",
    "fficiency . quick changeover shaft device": "feature",
    "rnal label with the following information": "remark",
    "h) 245 204 184 note": "color",
    "opes 1) material of self adhesive tear tape": "material",
    "vmopp. 2) width of tear tape rolls": "width",
    "mm ( such as": "size",
    "mm..) 3) run length of tear tape rolls": "length",
    "m/spool 4) color of tear tape rolls": "color",
    "using pallets. 4.) others": "packing",
    "th . normal produce ribbon specifications": "specification",
    "ypropylene safety capacitor film features": "feature",
    "of blast-proof capacitor. film thickness": "thickness",
    "um-15um electrode design": "feature",
    "has the following four characteristics": "feature",
    "bring more results. include the following": "feature",
    "ng soft-touch film laminating temperature": "temperature",
    "could be about 6000 mts the core diameter": "length",
    "standard exporting package 1. package": "packing",
    "stretch film 9 rolls / pallet 2. package": "packing",
    "hermal transfer film product applications": "application",
    "nning or for seal tape. specifications are": "application",
    "rf card": "application",
    "contactless ic card": "application",
    "n of printed materials is not easy. usage": "usage",
    "small heat shrinkage. typical properties": "typical properties",
    "astm d 1003 note": "standard",
    "gta/gt specifications": "specification",
    "inches) 152mm (6 inches) in sheets note": "size",
    "requirements. product characteristic": "feature",
    "ions is beyond our control. product usage": "usage",
    "bops sheets size": "size",
    "with sizes": "size",
    "opet polyester film thermal transfer film": "material",
    "ning or for seal tape. specifications are ": "application",
    "value units test optical haze": "haze",
}

# Markers that introduce a pasted technical table inside a value cell.
TABLE_MARKERS = [
    "tech data", "typical properties", "typical property", "physical properties",
    "for customer reference", "refer to the following", "as follows",
    "item standard value", "property thickness value",
]

# English boilerplate that is worth keeping even when it sits past a marker.
KEEP_SENTENCES = [
    "customized dimensions and specifications are available upon request",
    "customized size and specification are available upon request",
    "standard export package",
]


def _normalise(text):
    text = (text or "").replace("\ufffd", " ").replace("\xa0", " ")
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\uff5e", "~").replace("\u3000", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def strip_junk(text):
    low = text.lower()
    for junk in JUNK_EN:
        if junk in low:
            idx = low.find(junk)
            text = text[:idx] + text[idx + len(junk):]
            low = text.lower()
    return re.sub(r"\s+", " ", text).strip()


def structure_value(value):
    """Cut the pasted data-sheet tail off a legacy value cell.

    Returns a cleaned English value; the Chinese version is derived from it.
    """
    text = _normalise(value)
    if not text:
        return ""
    text = strip_junk(text)
    text = re.sub(r"\s*\(\s*\)\s*", " ", text)
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    text = re.sub(r"([,;:])\s*([,.;:])", r"\1", text)

    # cut at the first pasted table marker (keep the meaningful prefix)
    low = text.lower()
    cut = None
    for marker in TABLE_MARKERS:
        idx = low.find(marker)
        if idx == -1:
            continue
        if cut is None or idx < cut:
            cut = idx
    prefix = text[:cut] if cut is not None and cut > 12 else text

    # keep a useful boilerplate sentence even when it sat past the marker
    extra = []
    low_full = text.lower()
    for sent in KEEP_SENTENCES:
        if sent in low_full and sent not in prefix.lower():
            extra.append(sent)

    out = prefix.strip(" .;,")
    if extra:
        out = out + ". " + ". ".join(extra)
    out = re.sub(r"\s+", " ", out).strip()
    # drop a dangling trailing enumeration marker such as "5)" or "3)"
    out = re.sub(r"[\s,;]*\d+\s*\)\s*$", "", out)
    out = re.sub(r"[\s,;]*\d+\s*$", lambda m: m.group(0) if "." in out else "", out)
    if len(out) > 300:
        out = out[:300].rsplit(" ", 1)[0].rstrip(" ,;.") + "…"
    return out


# --------------------------------------------------------------- key work ---
def canonical_key(key):
    """Map a legacy/garbled spec key onto a canonical one ('' = drop)."""
    k = _normalise(key).strip(" .:;*#")
    low = k.lower()
    if not low:
        return ""
    if low in GARBLED_KEYS:
        return GARBLED_KEYS[low]
    if low in CANON_KEYS:
        return low
    # a canonical key embedded in the raw text ("width of bopet film")
    for canon in CANON_KEYS:
        if re.search(r"\b" + re.escape(canon) + r"\b", low):
            return canon
    # truncated leading characters ("idth", "ngth", "ture")
    for frag, canon in (("idth", "width"), ("ngth", "length"),
                         ("ture", "feature"), ("ical", "material")):
        if low.startswith(frag):
            return canon
    return ""


def en_key(key):
    canon = canonical_key(key)
    if not canon:
        return ""
    return canon.capitalize() if canon not in ("iso. opacity", "brightness(iso)") else canon


def zh_key(key):
    canon = canonical_key(key)
    if not canon:
        return ""
    from generate_site import SPEC_KEY_ZH
    return SPEC_KEY_ZH.get(canon, canon)


# ------------------------------------------------------------ value work ---
def _protect(text):
    """Replace acronyms with placeholders so they survive the rewrite."""
    placeholders = {}

    def sub(m):
        key = "\x00%d\x00" % len(placeholders)
        placeholders[key] = m.group(0)
        return key

    pattern = r"\b[A-Za-z][A-Za-z0-9/\-]{1,12}\b"
    tokens = re.findall(pattern, text)
    for tok in sorted(set(tokens), key=len, reverse=True):
        if tok.lower() in ACRONYMS:
            text = re.sub(r"\b" + re.escape(tok) + r"\b", sub, text)
    return text, placeholders


def _restore(text, placeholders):
    for key, value in placeholders.items():
        text = text.replace(key, value)
    return text


def zh_value(value):
    """Chinese rendering of a legacy specification value."""
    text = structure_value(value)
    if not text:
        return ""
    text = _normalise(text)

    # 1. full phrases (longest first) - must run before acronym protection,
    #    because a phrase may itself contain an acronym ("bopp film ...").
    for en, zh in sorted(PHRASE_ZH, key=lambda x: -len(x[0])):
        pattern = r"(?<![A-Za-z])" + re.escape(en) + r"(?![A-Za-z])"
        text = re.sub(pattern, " " + zh + " ", text, flags=re.I)

    # 2. protect acronyms so they survive the rewrite
    text, placeholders = _protect(text)

    # 3. measurement units attached to numbers
    unit_alt = "|".join(sorted((re.escape(u) for u in UNIT_ZH), key=len, reverse=True))
    text = re.sub(r"(\d[\d.,~/\-]*)\s*(" + unit_alt + r")\b",
                  lambda m: m.group(1) + " " + UNIT_ZH[m.group(2).lower()], text, flags=re.I)
    # a bare "m" after a number is a metre
    text = re.sub(r"(?<=\d)\s*m\b", " 米", text, flags=re.I)
    # a bare "um" written without a space
    text = re.sub(r"(?<=\d)um\b", " 微米", text)

    # 4. technical terms (multi word first)
    for en in sorted(TERM_ZH, key=len, reverse=True):
        zh = TERM_ZH[en]
        pattern = r"(?<![A-Za-z])" + re.escape(en) + r"(?![A-Za-z])"
        text = re.sub(pattern, " " + zh + " ", text, flags=re.I)

    # 5. strip whatever English survived
    text = re.sub(r"[A-Za-z][A-Za-z'\-\.]*", " ", text)

    # 6. tidy up
    text = _restore(text, placeholders)
    text = re.sub(r"\(\s*\)", "", text)
    text = re.sub(r"\s*\(\s*", "（", text)
    text = re.sub(r"\s*\)\s*", "）", text)
    text = re.sub(r"\s+（", "（", text)
    text = re.sub(r"）\s*", "）", text)
    # legacy enumeration markers such as "6 )" or "3)" carry no meaning
    text = re.sub(r"[\s,、]*\d+\s*）", "", text)
    text = re.sub(r"[\s,、]*\d+\s*\)", "", text)
    text = re.sub(r"[\s,、]*\d+\.\s*）", "", text)
    text = re.sub(r"[:：]\s*$", "", text)
    text = re.sub(r"\s+", " ", text)
    # numeric lists use the Chinese enumeration comma, thousands keep ","
    def _sep(m):
        rest = m.string[m.end():]
        return "," if re.match(r"\d{3}(?!\d)", rest) else "、"
    # a comma that is not preceded by a digit is a list separator
    text = re.sub(r"(?<!\d),\s*", "、", text)
    text = re.sub(r"(?<=\d),(?=\d)", _sep, text)
    text = re.sub(r"\s*;\s*", "；", text)
    # sentence stops: only a real full stop, never a decimal point
    text = re.sub(r"(?<!\d)\.(?!\d)\s*", "。", text)
    text = re.sub(r"(?<!\d)\.(?!\d)$", "。", text)
    text = re.sub(r"[，；。]\s*$", "", text)
    text = re.sub(r"^\s*[，；。、]\s*", "", text)
    text = re.sub(r"，+", "，", text)
    text = re.sub(r"。+", "。", text)
    text = re.sub(r"、{2,}", "、", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"^\s*[，；。、]\s*", "", text)
    if len(text) > 260:
        text = text[:260].rstrip("，；。 ") + "…"
    return text


def en_value(value):
    """English rendering of a legacy specification value."""
    text = structure_value(value)
    if not text:
        return ""
    text = re.sub(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def zh_heading(text):
    """Translate a legacy item heading into Chinese."""
    text = _normalise(text)
    if not text:
        return ""
    if re.search(r"[\u4e00-\u9fff]", text):
        return text
    translated = zh_value(text)
    if translated:
        return translated
    return ""
