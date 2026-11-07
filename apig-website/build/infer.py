# -*- coding: utf-8 -*-
"""Derive the technical facts that the legacy pages only mention in prose.

37 of the 173 catalogue entries carry no structured parameter table at all -
their data is buried in a paragraph ("Plain bag-grade BOPP film with corona
treated").  Rather than inventing numbers, this module *extracts* the facts
that are actually written in the source text and turns them into proper
specification rows, in both languages.
"""
import re

# (en key, zh key, regex, en value, zh value)
FEATURE_RULES = [
    ("Surface treatment", "表面处理",
     r"corona\s*(?:treat\w*|treatment)", "Corona treated", "电晕处理"),
    ("Heat seal", "热封性能",
     r"two\s+sides?\s+heat\s+seal\w*|both\s+sides?\s+heat\s+seal\w*",
     "Heat sealable on two sides", "双面可热封"),
    ("Heat seal", "热封性能",
     r"one\s+side\s+heat\s+seal\w*|single\s+side\s+heat\s+seal\w*",
     "Heat sealable on one side", "单面可热封"),
    ("Heat seal", "热封性能",
     r"heat\s+seal\w*", "Heat sealable", "可热封"),
    ("Coating", "涂布方式",
     r"water\s*[- ]?based", "Water-based coating", "水性涂布"),
    ("Coating", "涂布方式",
     r"solvent\s*[- ]?based", "Solvent-based coating", "溶剂型涂布"),
    ("Coating", "涂布方式",
     r"wax\s*/?\s*resin", "Wax-resin coated", "蜡/树脂涂布"),
    ("Coating", "涂布方式",
     r"wax\s*(?:coat\w*|based)", "Wax coated", "蜡涂布"),
    ("Coating", "涂布方式",
     r"pvdc\s*(?:coat\w*|coating)", "PVDC coated", "PVDC 涂布"),
    ("Adhesive", "胶粘剂",
     r"acrylic\s+adhesive|acrylic\s+glue", "Acrylic adhesive", "丙烯酸胶粘剂"),
    ("Adhesive", "胶粘剂",
     r"hot\s*melt\s+adhesive", "Hot-melt adhesive", "热熔胶粘剂"),
    ("Feature", "产品特点",
     r"anti\s*[- ]?static", "Anti-static", "防静电"),
    ("Feature", "产品特点",
     r"anti\s*[- ]?fog", "Anti-fog", "防雾"),
    ("Feature", "产品特点",
     r"metalli[sz]ed", "Metallized", "镀铝"),
    ("Feature", "产品特点",
     r"perforated", "Perforated", "打孔"),
    ("Feature", "产品特点",
     r"holographic", "Holographic", "全息"),
    ("Feature", "产品特点",
     r"laser", "Laser", "镭射"),
    ("Feature", "产品特点",
     r"pearli[sz]ed", "Pearlized", "珠光"),
    ("Feature", "产品特点",
     r"soft\s*[- ]?touch", "Soft-touch", "软触感"),
    ("Feature", "产品特点",
     r"matte\b", "Matte finish", "哑光"),
    ("Feature", "产品特点",
     r"glossy\b", "Glossy finish", "光面"),
    ("Feature", "产品特点",
     r"shrink\w*", "Shrinkable", "可收缩"),
    ("Feature", "产品特点",
     r"cling", "Cling film", "缠绕成膜"),
    ("Feature", "产品特点",
     r"bi\s*[- ]?axially\s+oriented|biaxial", "Biaxially oriented", "双向拉伸"),
    ("Feature", "产品特点",
     r"cast\s+film|cast\s+polypropylene", "Cast film", "流延膜"),
    ("Feature", "产品特点",
     r"uncoat\w*", "Uncoated", "不涂布"),
    ("Printing", "印刷",
     r"printable|pre-?printed|for\s+printing", "Printable / printable grades",
     "可印刷"),
    ("Application", "应用领域",
     r"plastic\s+zipper|with\s+zipper", "Pouches with plastic zipper",
     "带塑料拉链的包装袋"),
    ("Application", "应用领域",
     r"food\s*(?:packaging|grade|contact)", "Food packaging", "食品包装"),
    ("Application", "应用领域",
     r"bar\s*code", "Label / barcode application", "标签与条码应用"),
]

# base material, derived from the polymer named in the product title
BASE_MATERIAL = [
    (r"\bBOPET\b|\bPET\b|POLYESTER|THERMAL\s+TRANSFER|\bTTR\b",
     ("Polyester (PET)", "聚酯（PET）")),
    (r"\bBOPS\b|POLYSTYRENE|\bPS\b",
     ("Polystyrene (PS)", "聚苯乙烯（PS）")),
    (r"\bBOPA\b|POLYAMIDE|\bPA\b",
     ("Polypropylene with PA tie layer", "聚丙烯（PA 粘结层）")),
    (r"\bCPP\b|POLYPROPYLENE|\bPP\b|\bBOPP\b",
     ("Polypropylene (PP)", "聚丙烯（PP）")),
    (r"\bHDPE\b", ("High-density polyethylene (HDPE)", "高密度聚乙烯（HDPE）")),
    (r"\bLDPE\b|\bLLDPE\b|\bPE\b|POLYETHYLENE",
     ("Polyethylene (PE)", "聚乙烯（PE）")),
    (r"\bPVC\b", ("Polyvinyl chloride (PVC)", "聚氯乙烯（PVC）")),
    (r"\bEVOH\b", ("EVOH barrier layer", "EVOH 阻隔层")),
]

STANDARD_RE = re.compile(
    r"(?:GB/?T?\s*\d+(?:\.\d+)?(?:\s*[-–]\s*\d+)?"
    r"|ASTM\s*[A-Z]?\s*\d+(?:\.\d+)?"
    r"|QB/?T?\s*\d+(?:\.\d+)?"
    r"|DIN\s*\d+(?:\.\d+)?"
    r"|JIS\s*[A-Z]?\s*\d+(?:\.\d+)?"
    r"|ISO\s*\d+(?:\.\d+)?)", re.I)

# Equipment and specialty lines are named after what they are; turn that into
# an explicit category row so the page is never left without a table.
NAME_RULES = [
    (r"SLITTING\s+MACHINE", "Equipment type", "Slitting machine",
     "设备类型", "分切机"),
    (r"COATING\s+MACHINE", "Equipment type", "Coating machine",
     "设备类型", "涂布机"),
    (r"PRINTING\s+MACHINE", "Equipment type", "Printing machine",
     "设备类型", "印刷机"),
    (r"PACKING\s+MACHINE", "Equipment type", "Packing machine",
     "设备类型", "包装机"),
    (r"MACHINE\s+PARTS", "Equipment type", "Machine spare parts",
     "设备类型", "设备零部件"),
    (r"PRODUCTION\s+LINES", "Equipment type", "Production line",
     "设备类型", "生产线"),
    (r"RIBBONS?\s+SLITTER", "Equipment type", "Ribbon slitter",
     "设备类型", "色带分切机"),
    (r"ADHESIVE\s+TAPE\s+CUTTER", "Equipment type", "Adhesive tape cutter",
     "设备类型", "胶带切割机"),
    (r"HOT\s+CODING\s+FOIL", "Product type", "Hot coding foil",
     "产品类型", "热打码箔"),
    (r"HOT\s+INK\s+ROLLER", "Product type", "Hot ink roller",
     "产品类型", "热转印墨辊"),
    (r"ZIPPER\s+BAGS?", "Product type", "Zipper bags",
     "产品类型", "拉链袋"),
    (r"RC\s+PHOTO\s+PAPER", "Product type", "RC photo paper",
     "产品类型", "涂布相纸"),
    (r"WOODFREE\s+COPY\s+PAPER|COPY\s+PAPER", "Product type", "Copy paper",
     "产品类型", "复印纸"),
    (r"ELECTRONIC\s+RELAY|RELAY", "Product type", "Electronic relay",
     "产品类型", "电子继电器"),
    (r"CLEAN\s+FILM\s+CAPACITORS|FILM\s+CAPACITORS",
     "Product type", "Film capacitors", "产品类型", "薄膜电容器"),
    (r"ELECTRONIC\s+THIN\s+FILM", "Product type", "Electronic thin film",
     "产品类型", "电子薄膜"),
    (r"SMD", "Product type", "SMD component film", "产品类型", "SMD 贴片元件膜"),
    (r"\bHC\b", "Product type", "HC capacitor film", "产品类型", "HC 电容器膜"),
    (r"UM-1|S-39|S-38|S-26", "Product type", "Designated film series",
     "产品类型", "指定规格系列"),
]



def _norm(text):
    return re.sub(r"\s+", " ", (text or "").replace("\ufffd", " ")).strip()


def collect_text(product):
    """All prose the legacy page carries for one product."""
    chunks = [product.get("name", ""), product.get("intro", "")]
    for item in product.get("items", []):
        chunks.append(item.get("heading", ""))
        chunks.append(item.get("text", ""))
        for k, v in item.get("specs", []):
            chunks.append(str(k))
            chunks.append(str(v))
    return _norm(" ".join(c for c in chunks if c))


def infer_specs(product):
    """Return (rows_en, rows_zh) derived from the legacy prose."""
    text = collect_text(product)
    low = text.lower()
    name_en = _norm(product.get("name", ""))

    rows_en, rows_zh = [], []
    seen_en = set()

    def add(en_key, en_val, zh_key, zh_val):
        if en_key.lower() in seen_en:
            return
        seen_en.add(en_key.lower())
        rows_en.append((en_key, en_val))
        rows_zh.append((zh_key, zh_val))

    # --- base material
    for pattern, (en_val, zh_val) in BASE_MATERIAL:
        if re.search(pattern, name_en, re.I):
            add("Basic material", en_val, "基材", zh_val)
            break

    # --- equipment / specialty category taken from the title
    for pattern, en_key, en_val, zh_key, zh_val in NAME_RULES:
        if re.search(pattern, name_en, re.I):
            add(en_key, en_val, zh_key, zh_val)
            break

    # --- surface / process features mentioned in the text
    for en_key, zh_key, pattern, en_val, zh_val in FEATURE_RULES:
        if re.search(pattern, low, re.I):
            add(en_key, en_val, zh_key, zh_val)

    # --- standards quoted in the source text
    standards = []
    for code in STANDARD_RE.findall(text):
        code = re.sub(r"\s+", " ", code).strip().upper().replace("–", "-")
        code = re.sub(r"^GB\s*/\s*T", "GB/T", code)
        code = re.sub(r"^GB\s*/\s*T\s+", "GB/T ", code)
        code = re.sub(r"^QB\s*/\s*T\s+", "QB/T ", code)
        if code not in standards:
            standards.append(code)
    if standards:
        add("Standard", ", ".join(standards[:6]), "执行标准", "、".join(standards[:6]))

    return rows_en, rows_zh
