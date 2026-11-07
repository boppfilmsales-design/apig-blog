# -*- coding: utf-8 -*-
"""Shared content model for the bilingual APIG blog site (EN + ZH)."""

# ---------------------------------------------------------------- company ---
COMPANY = {
    "en": {
        "legal_name": "Asia Pacific Industry Group Co., Limited",
        "short_name": "Asia Pacific Industry Group",
        "tagline": "Precision-engineered BOPP, BOPET &amp; CPP films for global packaging.",
        "address_label": "Add.",
        "address": "No.3399 Luzhou Ave., Baohe Industrial District, 230051, Hefei city, Anhui Province, P.R. China",
        "tel_label": "Tel",
        "tel": "+0086-551-64687285 / 18919654871",
        "fax_label": "Fax",
        "fax": "+0086-551-64683490",
        "web_label": "Website",
        "websites": ["www.apigcl.com", "https://www.boppfilmsales.com"],
        "email_label": "Email",
        "emails": ["sales@boppfilmsales.com", "admin@apigcl.com"],
        "im_label": "On-line contact message",
        "im": [("Skype", "asiapacificsale"), ("QQ", "840715367")],
        "mobile_label": "Mobile/WeChat/Whatsapp",
        "mobile": ["0086-18919654871", "18919659471"],
        "copyright": "&copy; 2026 Asia Pacific Industry Group Co., Limited. All rights reserved.",
    },
    "zh": {
        "legal_name": "亚太工业集团有限公司",
        "legal_name_en": "Asia Pacific Industry Group Co., Limited",
        "short_name": "亚太工业集团",
        "tagline": "面向全球包装行业的精密级 BOPP、BOPET 与 CPP 薄膜。",
        "address_label": "地址",
        "address": "中国安徽省合肥市包河工业区庐州大道 3399 号，邮编 230051",
        "tel_label": "电话",
        "tel": "+0086-551-64687285 / 18919654871",
        "fax_label": "传真",
        "fax": "+0086-551-64683490",
        "web_label": "网址",
        "websites": ["www.apigcl.com", "https://www.boppfilmsales.com"],
        "email_label": "邮箱",
        "emails": ["sales@boppfilmsales.com", "admin@apigcl.com"],
        "im_label": "在线联系",
        "im": [("Skype", "asiapacificsale"), ("QQ", "840715367")],
        "mobile_label": "手机/微信/WhatsApp",
        "mobile": ["0086-18919654871", "18919659471"],
        "copyright": "&copy; 2026 亚太工业集团有限公司 版权所有",
    },
}

# -------------------------------------------------------------- categories ---
# key = legacy SortID on aenmgroup.com
CATEGORIES = {
    1:  {"slug": "bopp-film",        "en": "BOPP Film",              "zh": "BOPP 薄膜"},
    3:  {"slug": "tape-jumbo",       "en": "Adhesive Tape Jumbo Rolls", "zh": "胶粘带大卷"},
    4:  {"slug": "tape-finished",    "en": "Adhesive Tape Finished Rolls", "zh": "胶粘带成品卷"},
    5:  {"slug": "bopet-film",       "en": "BOPET Film",             "zh": "BOPET 薄膜"},
    13: {"slug": "bopa-bops-cpp",    "en": "BOPA, BOPS & CPP Film",  "zh": "BOPA / BOPS / CPP 薄膜"},
    17: {"slug": "ttr-labels",       "en": "Thermal Transfer Ribbon, Labels & Barcode Printers", "zh": "热转印膜、标签与条码打印机"},
    18: {"slug": "pof-pvc-pe",       "en": "POF, PVC & PE Film and Bags", "zh": "POF、PVC、PE 薄膜与包装袋"},
    20: {"slug": "paper-inkjet",     "en": "LWC, Copy, Photo Paper & Inkjet Supplies", "zh": "轻涂纸、复印纸、相纸与墨盒耗材"},
    22: {"slug": "tear-tape-alu",    "en": "Tear Tape, Clips, Belt & Aluminium Foil", "zh": "易撕胶带、烟盒夹、腰带与铝箔"},
    23: {"slug": "bopp-products",    "en": "BOPP Products",          "zh": "BOPP 制品"},
    24: {"slug": "coating-film",     "en": "Coating Film",           "zh": "涂布膜"},
    25: {"slug": "bestsellers",      "en": "Best-sellers",          "zh": "热销产品"},
    26: {"slug": "electronic",       "en": "Electronic Products",    "zh": "电子产品"},
    27: {"slug": "equipment",        "en": "Machine Equipment & Parts", "zh": "机械设备与零部件"},
    29: {"slug": "deep-processing",  "en": "Deep-processing Packaging Film", "zh": "深加工包装膜"},
    31: {"slug": "bopet-45",         "en": "4.5 µm BOPET Film",      "zh": "4.5 微米 BOPET 薄膜"},
    36: {"slug": "tire-wheel",       "en": "Tire & Wheel",           "zh": "轮胎与车轮"},
    37: {"slug": "new-development",  "en": "New Development Products", "zh": "新品开发"},
}

# --------------------------------------------- name translation (EN -> ZH) ---
# multi-word phrases first, then single tokens
ZH_PHRASES = [
    ("THERMAL TRANSFER RIBBONS", "热转印膜"),
    ("THERMAL TRANSFER RIBBON", "热转印膜"),
    ("THERMAL LAMINATING FILM", "热复合膜"),
    ("THERMAL LAMINATION FILM", "热复合膜"),
    ("ADHESIVE TAPE JUMBO ROLLS", "胶粘带大卷"),
    ("ADHESIVE TAPE FINISHED ROLLS", "胶粘带成品卷"),
    ("ADHESIVE TAPE", "胶粘带"),
    ("TAPE GRADE FILM", "胶带级薄膜"),
    ("TAPE GRADE", "胶带级"),
    ("TEAR TAPE", "易撕胶带"),
    ("FLOWER WRAPPING FILM", "花束包装膜"),
    ("PVDC COATING FILM", "PVDC 涂布膜"),
    ("ANTI STATIC FILM", "防静电膜"),
    ("CAPACITOR FILM", "电容器膜"),
    ("SHOPPING BAG", "购物袋"),
    ("GROCERY BAG", "购物袋"),
    ("BASE FILM", "基膜"),
    ("LABEL FILM", "标签膜"),
    ("BARCODE", "条码"),
    ("CLEAR FILM", "透明膜"),
    ("PRINTING FILM", "印刷膜"),
    ("WRAPPING FILM", "包装膜"),
    ("PACKING TAPE", "包装胶带"),
    ("DOUBLE SIDES", "双面"),
    ("TWO SIDES", "双面"),
    ("ONE SIDE", "单面"),
    ("HEAT SEALABLE", "可热封"),
    ("TIE TAPE", "捆扎带"),
    ("MACHINE PARTS", "设备零件"),
    ("MACHINE", "设备"),
    ("EQUIPMENT", "设备"),
    ("SHRINKAGE FILM", "收缩膜"),
    ("SHRINK FILM", "收缩膜"),
    ("WINDOW FILM", "窗膜"),
    ("METALLIZED", "镀铝"),
    ("VACUUM METALLIZED", "真空镀铝"),
    ("4.5 MIC BOPET FILM", "4.5 微米 BOPET 薄膜"),
    ("4.5 MIC BOPET", "4.5 微米 BOPET"),
    ("MICRONS", "微米"),
    ("MIC", "微米"),
    ("FILM", "薄膜"),
    ("TAPE", "胶带"),
    ("ROLL", "卷"),
]

ZH_TOKENS = {
    "BOPP": "BOPP", "BOPET": "BOPET", "CPP": "CPP", "BOPA": "BOPA", "BOPS": "BOPS",
    "TTR": "TTR", "PVC": "PVC", "PE": "PE", "PP": "PP", "PET": "PET", "PVA": "PVA",
    "EVOH": "EVOH", "PVDC": "PVDC", "MOPP": "MOPP", "TPU": "TPU", "PS": "PS",
    "EPS": "EPS", "ABS": "ABS", "HDPE": "HDPE", "LDPE": "LDPE", "LLDPE": "LLDPE",
    "PA": "PA", "PU": "PU", "PI": "PI", "UM": "微米", "GSM": "克重",
    "CLEAR": "透明", "TRANSPARENT": "透明", "WHITE": "白色", "BLACK": "黑色",
    "SILVER": "银色", "GOLD": "金色", "GOLDEN": "金色", "COLOR": "彩色",
    "COLOUR": "彩色", "PRINTED": "印刷型", "PRINT": "印刷", "PRINTING": "印刷",
    "HOT": "热熔", "SELF": "自粘", "ADHESIVE": "胶粘", "ULTRA": "超",
    "THIN": "超薄", "HIGH": "高", "STRENGTH": "强度", "QUALITY": "高品质",
    "SUPER": "超", "THERMAL": "热", "LAMINATING": "复合", "LAMINATION": "复合",
    "TRANSFER": "转印", "RIBBON": "色带", "RIBBONS": "色带", "LABEL": "标签",
    "LABELS": "标签", "PRINTABLE": "可打印", "FOOD": "食品", "PACKAGING": "包装",
    "PACKING": "包装", "WRAPPING": "包裹", "FLOWER": "花束", "TAPE": "胶带",
    "TEAR": "易撕", "JUMBO": "大卷", "MINI": "迷你", "ROLL": "卷", "ROLLS": "卷",
    "CIGARETTE": "烟用", "CIGARETTES": "烟用", "TIE": "捆扎", "BAND": "束带",
    "CLIP": "烟盒夹", "BELT": "腰带", "ALUMINIUM": "铝", "ALUMINUM": "铝",
    "FOIL": "箔", "VACUUM": "真空", "METALLIZED": "镀铝", "ANTI": "抗",
    "FOG": "雾", "HEAT": "热", "SEAL": "封", "SEALABLE": "可热封",
    "COPOLYMER": "共聚", "HOMOPOLYMER": "均聚", "COATING": "涂布",
    "COATED": "涂布", "DOUBLE": "双面", "SINGLE": "单面", "SOFT": "软",
    "TOUCH": "触感", "VELVET": "绒感", "MATTE": "哑光", "GLOSS": "高光",
    "WINDOW": "窗", "FLOOR": "地板", "TIRE": "轮胎", "WHEEL": "车轮",
    "BAG": "袋", "BAGS": "袋", "CUP": "杯", "BOTTLE": "瓶", "PHOTO": "相纸",
    "PAPER": "纸张", "COPY": "复印", "LWC": "轻涂", "INKJET": "喷墨",
    "PRINTER": "打印机", "MACHINE": "设备", "PART": "零件", "PARTS": "零件",
    "EQUIPMENT": "设备", "DEEP": "深加工", "PROCESSING": "加工",
    "WATER": "水溶性", "SOLUBLE": "可溶", "SEMI": "半", "FINISHED": "成品",
    "SERIES": "系列", "BASIC": "基础", "USED": "适用于", "FOR": "用于",
    "IN": "在", "ON": "用", "TO": "用于", "AND": "与", "OR": "或", "WITH": "含",
    "FROM": "来自", "THE": "", "OF": "", "A": "", "AN": "", "IS": "为",
    "NEW": "新", "PRODUCT": "产品", "ALL": "全", "SIZE": "规格",
    "SIZES": "规格", "ROLLING": "卷材", "SEALING": "封口", "POLYPROPYLENE": "聚丙烯",
    "POLYESTER": "聚酯", "POLYSTYRENE": "聚苯乙烯", "CAPACITOR": "电容器",
    "CAPACITORS": "电容器", "SAFETY": "安全", "TWIST": "扭结", "STRAP": "捆扎带",
    "CUT": "分切", "CUTTED": "分切", "SLITTING": "分切", "LINE": "产线",
    "LINES": "产线", "CAN": "可", "MAKE": "制造", "MADE": "制造",
    "CAPACITY": "产能", "PREMIX": "预混", "COMPOUND": "复合", "BLEND": "混配",
    "MASTERBATCH": "母粒", "RESIN": "树脂", "FLEXIBLE": "柔性", "RIGID": "硬质",
    "HARD": "硬质", "STRETCH": "拉伸", "CAST": "流延", "ORIENTED": "拉伸",
    "Biaxially": "双向", "TWO": "双", "ONE": "单", "SHADE": "色", "GRADE": "牌号",
    "THICKNESS": "厚度", "WIDTH": "宽度", "LENGTH": "长度", "COLOUR": "颜色",
}

# hand-checked names for the products the site already featured
ZH_NAME_OVERRIDE = {
    "504": "BOPET 易撕胶带",
    "505": "CPP 薄膜",
    "506": "BOPP 胶粘带（机械线）",
    "507": "烟用易撕胶带",
    "508": "烟用胶粘易撕胶带",
    "509": "BOPP 胶带级半成品（水性透明）",
    "511": "BOPP 透明胶带大卷",
    "512": "绒感软触膜（EVA 胶粘涂层）",
    "513": "BOPP 热复合膜",
    "515": "BOPP 花束包装膜（迷你卷）",
    "516": "BOPP 花束包装膜（透明与印刷型）",
    "517": "BOPP 胶带级薄膜",
    "519": "聚丙烯薄膜",
    "521": "BOPP 透明薄膜（双向拉伸）",
    "522": "4.5 微米 BOPET 热转印膜（基础型）",
}

# --------------------------------------------------------------- features ----
# per-category highlights + typical applications, used to enrich sparse pages
CATEGORY_CONTENT = {
    "bopp-film": {
        "en": {
            "highlights": [
                "Consistent thickness across the web for uninterrupted converting",
                "Excellent heat-seal strength and broad sealing window",
                "High optical clarity with low haze for premium shelf appeal",
                "Stable corona treatment for reliable printing and lamination",
            ],
            "applications": ["Flexible packaging", "Labels &amp; wrap-around labels", "Food and snack bags",
                             "Shrink and overwrap film", "Book and magazine covers"],
        },
        "zh": {
            "highlights": [
                "全幅厚度一致，装机过程稳定不中断",
                "热封强度优异，密封窗口宽",
                "高透明度、低雾度，货架陈列效果佳",
                "电晕处理稳定，印刷与复合可靠",
            ],
            "applications": ["软包装", "标签与缠绕标签", "食品与零食袋",
                             "收缩膜与缠绕膜", "书刊封面"],
        },
    },
    "bopet-film": {
        "en": {
            "highlights": [
                "High tensile strength and dimensional stability in both directions",
                "Excellent thermal stability for heat-lamination and metallising",
                "Superior print sharpness for fine typography and barcodes",
                "Low haze and high gloss for premium flexible packaging",
            ],
            "applications": ["Thermal transfer ribbon base film", "Label &amp; face film",
                             "Metallised and vacuum-deposited structures", "Lamination for flexible packs",
                             "Electrical and industrial insulation films"],
        },
        "zh": {
            "highlights": [
                "纵横双向高抗拉强度，尺寸稳定性优异",
                "热稳定性出色，适合热复合与镀铝工艺",
                "印刷套色清晰，细小字体与条码均可精确呈现",
                "低雾度高光泽，满足高端软包装需求",
            ],
            "applications": ["热转印膜基材", "标签与面材",
                             "镀铝与真空镀膜结构", "软包装复合",
                             "电子与工业绝缘膜"],
        },
    },
    "bopa-bops-cpp": {
        "en": {
            "highlights": [
                "CPP offers built-in heat-sealability without added coatings",
                "Excellent moisture and aroma barrier for dry-food packaging",
                "Good printability on both sides for pouch designs",
                "Available in clear, metallised and coated grades",
            ],
            "applications": ["Stand-up pouches", "Snack and confectionery packs",
                             "Retort and boil-in-bag pouches", "Paper and film laminations"],
        },
        "zh": {
            "highlights": [
                "CPP 自带热封性，无需额外涂布",
                "阻隔水汽与香气性能优异，适合干燥食品包装",
                "双面可印刷，便于软袋结构设计",
                "提供透明、镀铝与涂布多种规格",
            ],
            "applications": ["自立袋", "零食与糖果包装",
                             "蒸煮与水煮袋", "纸张与薄膜复合"],
        },
    },
    "tape-jumbo": {
        "en": {
            "highlights": [
                "Consistent caliper across the jumbo roll for high-speed slitting",
                "Low defect rate for automatic tape-making lines",
                "Controlled release force for clean, repeatable unwinding",
                "Tailored core sizes for existing converting equipment",
            ],
            "applications": ["BOPP tape jumbo rolls", "Masking and double-sided tape",
                             "Automotive and electrical insulation tape"],
        },
        "zh": {
            "highlights": [
                "大卷全幅厚度均匀，适合高速分切",
                "缺陷率低，适配全自动胶带生产线",
                "离型力稳定，卷材放卷顺畅可重复",
                "纸芯尺寸可按现有设备定制",
            ],
            "applications": ["BOPP 胶粘带大卷", "美纹纸与双面胶带",
                             "汽车与电气绝缘胶带"],
        },
    },
    "tape-finished": {
        "en": {
            "highlights": [
                "Ready-to-use slit rolls sized for hand and machine application",
                "Clean adhesive edges with no edge shedding",
                "Consistent colour and thickness between production lots",
                "Printed and unprinted versions available",
            ],
            "applications": ["Carton sealing tape", "Cigarette pack sealing",
                             "Office and packaging tape retail packs"],
        },
        "zh": {
            "highlights": [
                "分切成品卷，可直接用于手工与机器作业",
                "胶边洁净无毛边",
                "不同批次之间颜色与厚度一致",
                "可提供印刷与非印刷版本",
            ],
            "applications": ["纸箱封箱胶带", "烟盒封口",
                             "办公与包装胶带零售装"],
        },
    },
    "ttr-labels": {
        "en": {
            "highlights": [
                "Ultra-thin base films down to 4.5 µm for high-speed ribbon winding",
                "Consistent release layer for clean, sharp transfer",
                "Excellent thermal transfer density and dark image retention",
                "Low defect rate protects thermal print heads",
            ],
            "applications": ["Thermal transfer ribbon film", "Variable barcode labels",
                             "Logistics and retail labelling", "Industrial barcode printing"],
        },
        "zh": {
            "highlights": [
                "基材薄至 4.5 微米，适配高速色带卷绕",
                "离型层稳定，转印干净锐利",
                "热转印密度高，条码深黑持久",
                "缺陷率低，保护热敏打印头",
            ],
            "applications": ["热转印色带膜", "可变条码标签",
                             "物流与零售标签", "工业条码打印"],
        },
    },
    "coating-film": {
        "en": {
            "highlights": [
                "Functional coating chemistry tuned for specific end use",
                "Adhesion, printability and sealability balanced for lamination",
                "Corona-treated for consistent ink and adhesive wetting",
                "Tailored surface tension for fast converting",
            ],
            "applications": ["Corona-treated base film", "Print receptive film",
                             "Anti-fog and anti-static coatings", "Adhesive lamination film"],
        },
        "zh": {
            "highlights": [
                "功能涂层化学配方针对终端用途定制",
                "粘附力、印刷适性与热封性平衡，适合复合",
                "电晕处理均匀，油墨与胶粘剂润湿良好",
                "表面张力可调，适配高速分切复合",
            ],
            "applications": ["电晕处理基膜", "油墨接受层薄膜",
                             "防雾与防静电涂层", "胶粘复合薄膜"],
        },
    },
    "tear-tape-alu": {
        "en": {
            "highlights": [
                "Precise tear initiation for a clean, controlled opening",
                "Adhesive performance tuned for paperboard and film substrates",
                "Metallised and laser-holographic versions for premium packs",
                "Consistent unwind tension for high-speed cartoning",
            ],
            "applications": ["Cigarette pack tear tape", "Carton opening strips",
                             "Gift and luxury packaging", "Tobacco and food cartons"],
        },
        "zh": {
            "highlights": [
                "精确的撕口起点，开启干净可控",
                "针对纸板与薄膜基材优化粘附性能",
                "提供镀铝与激光全息版本，满足高端包装",
                "放卷张力稳定，适配高速装盒",
            ],
            "applications": ["烟盒易撕胶带", "纸箱开封条",
                             "礼品与奢侈包装", "烟草与食品纸盒"],
        },
    },
    "deep-processing": {
        "en": {
            "highlights": [
                "Multi-layer structures engineered for demanding barriers",
                "Precise metallisation with uniform deposition across the web",
                "Slit-and-fold grades for tube and bag making",
                "Validated reels for high-speed, low-waste running",
            ],
            "applications": ["Multi-layer flexible packaging", "Metallised film structures",
                             "Tube film and bag making", "Retort and stand-up pouch lamination"],
        },
        "zh": {
            "highlights": [
                "多层结构设计，满足高阻隔需求",
                "镀层均匀，全幅沉积一致",
                "分切折卷级膜料，适配吹膜与制袋",
                "卷料经校验，高速低损耗运行",
            ],
            "applications": ["多层软包装", "镀铝膜结构",
                             "吹膜与制袋", "蒸煮袋与自立袋复合"],
        },
    },
    "bopp-products": {
        "en": {
            "highlights": [
                "Converted-ready formats for faster line set-up",
                "Consistent quality across jumbo, slit and finished rolls",
                "Tailored widths and core sizes",
                "Batch-to-batch traceability",
            ],
            "applications": ["Converted film supply", "Packaging converters", "Print and laminate suppliers"],
        },
        "zh": {
            "highlights": [
                "可直接转换的规格，加快产线调试",
                "大卷、分切卷、成品卷质量一致",
                "宽度与纸芯尺寸可定制",
                "批次可追溯",
            ],
            "applications": ["转换膜料供应", "包装加工企业", "印刷与复合供应商"],
        },
    },
    "pof-pvc-pe": {
        "en": {
            "highlights": [
                "Printable grades for shrink sleeves and wrap films",
                "Good forming and neck-in behaviour on shrinking equipment",
                "Clear and printed options",
                "Consistent shrinkage across the roll",
            ],
            "applications": ["Shrink sleeves", "Shrink wrap film", "Printed wrap films", "Protective covers"],
        },
        "zh": {
            "highlights": [
                "适合收缩标签与缠绕膜的印刷级产品",
                "成型与收缩颈缩表现良好",
                "提供透明与印刷版本",
                "整卷收缩率一致",
            ],
            "applications": ["收缩标签", "收缩缠绕膜", "印刷缠绕膜", "防护覆盖膜"],
        },
    },
    "paper-inkjet": {
        "en": {
            "highlights": [
                "Consistent whiteness and smoothness for clean print images",
                "Optimised coating for inkjet and laser print engines",
                "Reliable feeding for high-volume office devices",
                "Available in A4/A3 and jumbo formats",
            ],
            "applications": ["Thermal transfer ribbon", "Label printing", "Office printing", "Photo printing"],
        },
        "zh": {
            "highlights": [
                "白度与平滑度稳定，print 图像清晰",
                "涂层针对喷墨与激光打印引擎优化",
                "高速办公设备走纸可靠",
                "提供 A4/A3 及大卷规格",
            ],
            "applications": ["热转印", "标签打印", "办公打印", "照片打印"],
        },
    },
    "equipment": {
        "en": {
            "highlights": [
                "Machinery and spare parts matched to our film portfolio",
                "Support from an experienced production team",
                "Spares availability for continuous running",
                "Practical guidance on installation and setup",
            ],
            "applications": ["Film making lines", "Slitting and rewinding", "Tape making lines", "Converting equipment"],
        },
        "zh": {
            "highlights": [
                "设备与备件与自有膜料品类配套",
                "由资深生产团队提供支持",
                "备件供应有保障，保障连续生产",
                "就安装与调试提供实用指导",
            ],
            "applications": ["制膜生产线", "分切复卷", "胶带生产线", "转换设备"],
        },
    },
    "electronic": {
        "en": {
            "highlights": [
                "Reliable components for converting and packing lines",
                "Tested for continuous-duty operation",
                "Documentation and wiring guidance included",
                "Spare units available for line criticality",
            ],
            "applications": ["Converting line electronics", "Printing and coding", "Packaging machinery", "Factory automation"],
        },
        "zh": {
            "highlights": [
                "转换与包装线用可靠电子元件",
                "经连续运行测试验证",
                "随机提供接线图与技术说明",
                "关键产线可另购备机",
            ],
            "applications": ["转换线电子部件", "打印与打码", "包装机械", "工厂自动化"],
        },
    },
    "new-development": {
        "en": {
            "highlights": [
                "New developments developed with customer feedback",
                "Pilot and trial quantities available before volume runs",
                "Specification support from our technical team",
                "Room for custom development requests",
            ],
            "applications": ["New packaging concepts", "Trial and pilot projects", "Custom film development"],
        },
        "zh": {
            "highlights": [
                "结合客户反馈持续开发的新品",
                "批量生产前可提供试产与样品数量",
                "技术团队提供规格支持",
                "可承接定制开发需求",
            ],
            "applications": ["新包装概念", "试产与试点项目", "定制薄膜开发"],
        },
    },
    "bestsellers": {
        "en": {
            "highlights": [
                "Proven demand across repeat OEM and converter orders",
                "Stable supply and consistent quality",
                "Ready stock on core grades",
                "Competitive lead times",
            ],
            "applications": ["High-volume flexible packaging", "Tape and label converters", "Export trading partners"],
        },
        "zh": {
            "highlights": [
                "经 OEM 与转换商重复订单验证",
                "供应稳定、品质一致",
                "常规规格常备库存",
                "交期有竞争力",
            ],
            "applications": ["大批量软包装", "胶带与标签转换商", "外贸合作伙伴"],
        },
    },
    "bopet-45": {
        "en": {
            "highlights": [
                "4.5 µm base film for ultra-thin thermal transfer ribbon",
                "High tensile and modulus for winding stability at high speed",
                "Excellent dimensional consistency for tight tolerance printing",
                "Low gel and low defect rate",
            ],
            "applications": ["Thermal transfer ribbon film", "Super-thin label stock", "Security and marking films"],
        },
        "zh": {
            "highlights": [
                "4.5 微米基材，用于超薄热转印色带",
                "高强度高模量，高速卷绕稳定",
                "尺寸一致性优异，适应高精度印刷",
                "凝胶与缺陷率低",
            ],
            "applications": ["热转印色带膜", "超薄标签材料", "防伪与标记膜"],
        },
    },
    "tire-wheel": {
        "en": {
            "highlights": [
                "High-strength film for tyre labelling and wrapping",
                "Resistant to heat, oil and mechanical wear",
                "Accurate printing for size and batch identification",
                "Stable supply for continuous production",
            ],
            "applications": ["Tyre label film", "Tyre wrap and protection film", "Component identification"],
        },
        "zh": {
            "highlights": [
                "高强度薄膜用于轮胎标识与包覆",
                "耐热、耐油、耐机械磨损",
                "规格与批次标识印刷精确",
                "供应稳定，保障连续生产",
            ],
            "applications": ["轮胎标签膜", "轮胎包覆与防护膜", "零部件标识"],
        },
    },
}

# ---------------------------------------------------------- site furniture ---
NAV = {
    "en": [("home", "Home", "index.html"), ("products", "Products", "products.html"),
           ("blog", "Blog", "blog.html"), ("about", "About", "about.html"),
           ("contact", "Contact", "contact.html")],
    "zh": [("home", "首页", "index.html"), ("products", "产品中心", "products.html"),
           ("blog", "技术博客", "blog.html"), ("about", "关于我们", "about.html"),
           ("contact", "联系我们", "contact.html")],
}

STATS = {
    "en": [("20+", "Years in flexible-film manufacturing"),
           ("150+", "Product references in the catalogue"),
           ("80+", "Countries served by export sales"),
           ("ISO", "Certified quality management")],
    "zh": [("20+", "深耕柔性薄膜制造二十余年"),
           ("150+", "产品型号覆盖目录"),
           ("80+", "出口销售覆盖国家和地区"),
           ("ISO", "质量管理体系认证")],
}

PILLARS = {
    "en": [
        ("Stable process", "Every roll is produced on audited lines with in-line gauge and defect control, so specification holds from the first reel to the millionth."),
        ("Engineering support", "Our technicians help match grade, thickness and surface treatment to your converting equipment and end use."),
        ("Global logistics", "Hefei port and regional warehouses keep lead times short for customers in Europe, North America, South America, Africa and Asia."),
    ],
    "zh": [
        ("稳定的生产工艺", "全部产线均通过审核，配备在线测厚与缺陷检测，从第一卷到百万卷，规格始终如一。"),
        ("工程技术支持", "技术团队协助客户匹配牌号、厚度与表面处理方式，适配其转换设备与终端用途。"),
        ("全球物流体系", "依托合肥港口与区域仓储，为欧洲、北美、南美、非洲与亚洲客户保持较短交期。"),
    ],
}


# ---------------------------------------------------------------------------
# Additional product-name vocabulary.  The legacy catalogue names products with
# a very mixed vocabulary ("BI-AXIALLY ORIENTED", "SHRINKAGE FILM",
# "RC PAPER" ...); these entries close the remaining gaps.
# ---------------------------------------------------------------------------
ZH_TOKENS_EXTRA = {
    "BASE": "基材", "WAX": "蜡", "ELECTRONIC": "电子", "CLING": "缠绕",
    "CRYSTAL": "晶体", "CLEAR/TRANSPARENT": "透明", "WAX/RESIN": "蜡/树脂",
    "B": "B", "STOCK": "库存", "UNCOATING": "不涂布", "PLAIN": "平膜",
    "BI-AXIALLY": "双向", "METALIZED": "镀铝", "GLOSSY": "光面",
    "MATTER": "亚光", "PRODUCTION": "生产", "SEMI-FINISHED": "半成品",
    "ACRYLIC": "丙烯酸", "MASKING": "遮蔽", "LASER": "镭射",
    "SHEETS": "片材", "FLAT": "平膜", "ZIPPER": "拉链", "ZIPPERS": "拉链",
    "PLASTIC": "塑料", "POF": "POF", "SHRINKAGE": "收缩",
    "PERFORATED": "打孔", "MACHINES": "设备", "LETTER": "打字",
    "LEGAL": "法律", "RC": "RC", "WEIGHT": "克重", "SLEEVE": "套管",
    "EVA": "EVA", "MINI-ROLLS": "小卷", "TREATED": "处理",
    "OTHER": "其他", "SIDE": "面", "SLIVER": "细条",
    "BIAXIAL-ORIENTED": "双向拉伸", "GARADE": "牌号",
    "PEARLIZED": "珠光", "OPAQUE": "不透明", "RUBBER": "橡胶",
    "BASED": "基", "GLUE": "胶", "MELT": "熔融", "SOLVENT": "溶剂",
    "OPP": "OPP", "CLEAR/TAN": "透明/本色", "ADHASIVE": "胶粘",
    "CUTTER": "切刀", "CUTTING": "分切", "TYPE": "类型",
    "THERNAL": "热", "WINDOWS": "窗", "ENVELOPE": "信封",
    "VMCPP": "VMCPP", "GENERAL": "通用", "ECONOMICAL": "经济型",
    "STANDARD": "标准", "PLUS-WAX": "加蜡", "ENHANCE": "增强",
    "HEAD": "头部", "WAX&RESIN": "蜡&树脂", "NORMAL": "常规",
    "WASH": "清洗", "CARE": "保养", "CODING": "喷码", "INK": "油墨",
    "ROLLER": "导辊", "SLITTER": "分切机", "DATES": "日期",
    "AGRICULTURE": "农业", "CARDS": "卡片", "GARBAGE": "垃圾",
    "&": "&", "PALLETS": "托盘", "SHRINK": "收缩", "FLUEY": "短纤",
    "SURFACE/CANVAS": "表面/画布", "RESIN,WATERPROOF": "树脂，防水",
    "GLOSSY/MATTE": "光面/哑光", "LOWER": "下限", "LIGHT": "透光",
    "PRODUCTS": "产品", "WOODFREE": "木浆", "CIAGRETTE": "烟用",
    "HAIR": "毛发", "STRIP": "条", "CLIPS": "夹子", "CORE,PAPER": "纸芯",
    "STRAW": "吸管", "DECORATIVE": "装饰", "RIBBONS,ARTIFICIAL": "人造丝带",
    "FLOWER,CREPE": "花束，皱纹", "PAPER,DECORATIVE": "装饰纸",
    "MESH": "网", "HOLOGRAPHIC": "全息", "BOPP/CPP": "BOPP/CPP",
    "MACRO": "粗孔", "MICRO": "微孔", "ANTI-FOG": "防雾", "ZN-AL": "锌铝",
    "ROUGH": "粗糙", "SOFT-TOUCH": "软触感", "SMALLER": "小规格",
    "K": "K", "CRYLIC": "丙烯酸", "ACID": "酸",
    "BOPP/BOPET/BOPA": "BOPP/BOPET/BOPA", "OFFICE": "办公",
    "PHOTOCOPY": "复印", "CBB": "CBB", "HC": "HC", "SMD": "SMD",
    "RELAY": "继电器", "FLANGES": "法兰", "SEIRES": "系列",
    "USING": "使用", "WERE": "曾", "PLUS": "加", "PP": "PP",
    "PS": "PS", "PE": "PE", "PET": "PET", "PVC": "PVC",
    "BOPP": "BOPP", "BOPET": "BOPET", "BOPA": "BOPA", "BOPS": "BOPS",
    "CPP": "CPP", "TTR": "TTR", "PVA": "PVA", "EVOH": "EVOH",
    "PVDC": "PVDC", "MOPP": "MOPP", "TPU": "TPU", "EPS": "EPS",
    "ABS": "ABS", "HDPE": "HDPE", "LDPE": "LDPE", "LLDPE": "LLDPE",
}

ZH_TOKENS.update(ZH_TOKENS_EXTRA)

ZH_TOKENS.update({
    "FILM": "薄膜", "PACKAGE": "包装", "SIDES": "双面", "MICRONS": "微米",
    "UM": "微米", "LWC": "轻涂", "TAPE": "胶带", "GLOSSY": "光面",
    "MATTER": "亚光", "LINES": "产线", "PRODUCTION": "生产",
    "PLASTIC": "塑料", "ZIPPER": "拉链", "ZIPPERS": "拉链",
})
