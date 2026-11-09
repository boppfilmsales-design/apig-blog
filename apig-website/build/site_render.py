# -*- coding: utf-8 -*-
"""HTML rendering helpers for the bilingual APIG site."""
import html
import os

from site_data import COMPANY, NAV, PILLARS, STATS

SITE_ROOT = "https://blog.boppfilmsales.com"

UI = {
    "en": {
        "menu": "Menu",
        "skip": "Skip to content",
        "products_cta": "View all products",
        "blog_cta": "Read the blog",
        "quote_cta": "Request a quote",
        "contact_cta": "Contact us",
        "learn_more": "Learn more",
        "specs": "Technical specifications",
        "specs_sub": "Key parameters taken from our production data sheet.",
        "features": "Product highlights",
        "applications": "Typical applications",
        "overview": "Overview",
        "related": "Related products",
        "related_sub": "More references in the same product family.",
        "article_cta": "Request samples or a quotation",
        "article_cta_sub": "Tell us the grade, thickness and quantity you need and our team will reply with a specification and lead time.",
        "inquiry": "Send an inquiry",
        "inquiry_sub": "We reply within one working day.",
        "name": "Your name",
        "company": "Company",
        "email": "Email",
        "country": "Country / region",
        "message": "Requirement",
        "message_ph": "Grade, thickness, width, coating, monthly quantity and destination port…",
        "submit": "Send inquiry",
        "form_note": "Or email us directly at sales@boppfilmsales.com — your message reaches the same export desk.",
        "latest_posts": "Latest from our blog",
        "latest_posts_sub": "Practical notes on film selection, converting, storage and packaging performance.",
        "featured": "Featured product lines",
        "featured_sub": "Core grades supplied to converters and brand owners worldwide.",
        "why": "Why converters work with us",
        "catalogue": "Product catalogue",
        "catalogue_sub": "Filter by family, or search by grade, model or application.",
        "results": "products",
        "no_results": "No product matches that filter yet — try another family or clear the search.",
        "search_ph": "Search grade, model or application…",
        "all": "All",
        "blog": "Blog",
        "blog_sub": "Technical articles on flexible film manufacturing, converting and end-of-line performance.",
        "read": "Read article",
        "minutes": "min read",
        "key_points": "Key points",
        "related_posts": "Keep reading",
        "back_blog": "Back to the blog",
        "home": "Home",
        "products": "Products",
        "about": "About",
        "contact": "Contact",
        "toc": "In this article",
        "our_story": "Who we are",
        "capability": "What we do",
        "quality": "Quality and compliance",
        "newsletter": "Talk to an engineer",
        "newsletter_sub": "Technical questions get a technical answer. Reach our export desk directly.",
        "copy": "Copy",
        "lang_name": "中文",
    },
    "zh": {
        "menu": "菜单",
        "skip": "跳到正文",
        "products_cta": "查看全部产品",
        "blog_cta": "进入技术博客",
        "quote_cta": "获取报价",
        "contact_cta": "联系我们",
        "learn_more": "了解更多",
        "specs": "技术参数",
        "specs_sub": "以下关键参数取自我们的产品规格书。",
        "features": "产品亮点",
        "applications": "典型应用",
        "overview": "产品概述",
        "related": "相关产品",
        "related_sub": "同一产品系列中的更多型号。",
        "article_cta": "索取样品或报价",
        "article_cta_sub": "告诉我们所需的牌号、厚度与数量，我们的团队会回复规格建议与交期。",
        "inquiry": "发送询盘",
        "inquiry_sub": "我们将在一个工作日内回复。",
        "name": "您的姓名",
        "company": "公司名称",
        "email": "电子邮箱",
        "country": "国家 / 地区",
        "message": "需求说明",
        "message_ph": "牌号、厚度、宽度、涂层、月度用量与目的港……",
        "submit": "发送询盘",
        "form_note": "您也可以直接发邮件至 sales@boppfilmsales.com，同样由外贸部门受理。",
        "latest_posts": "最新博客",
        "latest_posts_sub": "关于选型、转换加工、仓储与包装性能的实用经验。",
        "featured": "核心产品线",
        "featured_sub": "面向全球转换商与品牌商的常规供应牌号。",
        "why": "为何选择我们",
        "catalogue": "产品目录",
        "catalogue_sub": "可按产品族筛选，或按牌号、型号、应用检索。",
        "results": "个产品",
        "no_results": "没有符合条件的产品，请换一个产品族或清空搜索。",
        "search_ph": "搜索牌号、型号或应用……",
        "all": "全部",
        "blog": "技术博客",
        "blog_sub": "关于柔性薄膜制造、转换加工与终端应用性能的技术文章。",
        "read": "阅读文章",
        "minutes": "分钟阅读",
        "key_points": "要点速览",
        "related_posts": "继续阅读",
        "back_blog": "返回博客",
        "home": "首页",
        "products": "产品中心",
        "about": "关于我们",
        "contact": "联系我们",
        "toc": "本文目录",
        "our_story": "我们是谁",
        "capability": "我们做什么",
        "quality": "质量与合规",
        "newsletter": "与工程师直接对话",
        "newsletter_sub": "技术问题值得技术回答。直接联系我们的外贸部门。",
        "copy": "复制",
        "lang_name": "English",
    },
}

# label shown on the language toggle = the name of the *target* language
LANG_LABEL = {"en": "English", "zh": "中文"}


def esc(value):
    return html.escape(str(value or ""), quote=True)


def esc(value):
    return html.escape(str(value or ""), quote=True)


class Ctx:
    """Path helper.

    Every page lives inside its language folder (en/ or zh/), so links to
    sibling pages are relative to that folder while assets are relative to
    the site root.  ``depth`` is how many directories deep the page sits.
    """

    def __init__(self, lang, depth=0):
        self.lang = lang
        self.depth = depth
        self.up = "../" * depth
        self.t = UI[lang]
        self.current = ""

    def u(self, root_path):
        """Link to a path relative to the site root (no leading slash)."""
        return self.up + root_path

    def home(self):
        """Home page of the current language."""
        return self.up + "index.html"

    def page(self, name):
        """Another page of the current language, e.g. 'products.html'."""
        return self.up + name

    def asset(self, path):
        """Assets live at the site root, one level above the language folder."""
        return f"../{self.up}assets/{path}"

    def sibling(self, other_lang):
        """The same page in the other language."""
        if self.current:
            parts = self.current.split("/", 1)
            tail = parts[1] if len(parts) > 1 else "index.html"
            return f"../{self.up}{other_lang}/{tail}"
        return f"../{self.up}{other_lang}/index.html"

    def self_rel(self):
        """Relative URL of the current page itself."""
        if self.current:
            parts = self.current.split("/", 1)
            tail = parts[1] if len(parts) > 1 else "index.html"
            return self.up + tail
        return self.home()


def document(ctx, title, description, body, extra_head="", canonical=None, lang_attr=None):
    c = COMPANY[ctx.lang]
    full_title = f"{title} | {c['legal_name']}" if ctx.lang == "en" else f"{title} | {c['legal_name']}"
    lang_code = lang_attr or ctx.lang
    hreflang = "en" if ctx.lang == "en" else "zh-CN"
    alt_dir = "en" if ctx.lang == "en" else "zh"
    canon = canonical or (f"{SITE_ROOT}/{ctx.current}" if ctx.current else f"{SITE_ROOT}/{ctx.lang}/")
    return f"""<!DOCTYPE html>
<html lang="{lang_code}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{full_title}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canon)}">
<link rel="alternate" hreflang="{hreflang}" href="{esc(SITE_ROOT)}/{alt_dir}/">
<link rel="alternate" hreflang="x-default" href="{esc(SITE_ROOT)}/en/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(c['legal_name'])}">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(description)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{ctx.asset('css/site.css')}">
<meta name="theme-color" content="#064e3b">
{extra_head}
</head>
<body>
<a class="skip" href="#main" style="position:absolute;left:-9999px">{ctx.t['skip']}</a>
{header(ctx)}
<main id="main">
{body}
</main>
{footer(ctx)}
<script src="{ctx.asset('js/site.js')}" defer></script>
</body>
</html>
"""


def header(ctx):
    c = COMPANY[ctx.lang]
    other = "zh" if ctx.lang == "en" else "en"
    # Header text must match the live pages (brand mark "API", blog-website
    # name/sub). Do not "modernise" it here; the live header is the reference.
    brand_name = "ASIA PACIFIC INDUSTRY GROUP -BLOG WEBSITE" if ctx.lang == "en" else "亚太工业集团 - 博客网站"
    brand_sub = "BOPP .BOPET.BOPS FILMS. &amp; THERMAL FILM. ADHESIVE TAPE" if ctx.lang == "en" else "BOPP .BOPET.BOPS 薄膜 . 热封膜 . 胶粘带"
    items = []
    for key, label, href in NAV[ctx.lang]:
        items.append(f'<li><a href="{ctx.page(href)}">{esc(label)}</a></li>')
    return f"""<header class="site-header">
  <div class="shell bar">
    <a class="brand" href="{ctx.home()}">
      <span class="brand-mark">API</span>
      <span class="brand-text">
        <span class="brand-name">{brand_name}</span>
        <span class="brand-sub">{brand_sub}</span>
      </span>
    </a>
    <button class="nav-toggle" aria-label="{esc(ctx.t['menu'])}" aria-expanded="false">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
    <nav class="nav">
      <ul class="nav-list">{''.join(items)}</ul>
      <span class="lang-switch">
        <a href="{ctx.sibling(other)}" data-apig-lang="{other}">{LANG_LABEL[other]}</a>
        <a href="{ctx.self_rel()}" class="on">{LANG_LABEL[ctx.lang]}</a>
      </span>
    </nav>
  </div>
</header>"""


def footer(ctx):
    c = COMPANY[ctx.lang]
    t = ctx.t
    blog_links = "".join(
        f'<li><a href="{ctx.page("blog/" + a["slug"] + ".html")}">{esc(a["title"][ctx.lang])}</a></li>'
        for a in _articles()
    )
    nav_links = "".join(f'<li><a href="{ctx.page(href)}">{esc(label)}</a></li>' for _, label, href in NAV[ctx.lang])
    web_links = "".join(f'<li><a href="{esc(w)}" rel="noopener">{esc(w)}</a></li>' for w in c["websites"])
    mail_links = "".join(f'<li><a href="mailto:{esc(e)}">{esc(e)}</a></li>' for e in c["emails"])
    im_links = "".join(f'<li>{esc(k)}: {esc(v)}</li>' for k, v in c["im"])
    return f"""<footer class="site-footer">
  <div class="shell">
    <div class="footer-grid">
      <div class="footer-col footer-about">
        <span class="brand"><span class="brand-mark">API</span></span>
        <p>{esc(c['tagline'])}</p>
        <p style="font-size:13.5px">{esc(c['address'])}</p>
      </div>
      <div class="footer-col">
        <h4>{esc(t['products'])}</h4>
        <ul>{nav_links}</ul>
      </div>
      <div class="footer-col">
        <h4>{esc(t['blog'])}</h4>
        <ul>{blog_links}</ul>
      </div>
      <div class="footer-col">
        <h4>{esc(t['contact'])}</h4>
        <ul>
          <li>{esc(c['tel_label'])}: {esc(c['tel'])}</li>
          <li>{esc(c['fax_label'])}: {esc(c['fax'])}</li>
          {mail_links}
          {im_links}
          {web_links}
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>{c['copyright']}</span>
      <span>{esc(c['mobile_label'])}: {esc(c['mobile'][0])} / {esc(c['mobile'][1])}</span>
    </div>
  </div>
</footer>"""


_ARTICLES = None


def _articles():
    global _ARTICLES
    if _ARTICLES is None:
        from articles import ARTICLES
        _ARTICLES = ARTICLES
    return _ARTICLES


def page_head(ctx, crumbs, title, lede=""):
    trail = []
    for i, (label, url) in enumerate(crumbs):
        trail.append(f'<a href="{url}">{esc(label)}</a>' if url else f"<span>{esc(label)}</span>")
    return f"""<section class="page-head">
  <div class="shell">
    <div class="crumbs">{'<span>/</span>'.join(trail)}</div>
    <h1>{esc(title)}</h1>
    {f'<p class="lede">{esc(lede)}</p>' if lede else ''}
  </div>
</section>"""


def section_head(ctx, kicker, title, sub="", center=True):
    return f"""<div class="section-head{' center' if center else ''}">
  <span class="kicker">{esc(kicker)}</span>
  <h2 class="section-title">{title}</h2>
  {f'<p class="section-sub">{sub}</p>' if sub else ''}
</div>"""


def stat_block(ctx):
    cells = "".join(
        f'<div class="stat"><div class="n">{esc(n)}</div><div class="l">{esc(l)}</div></div>'
        for n, l in STATS[ctx.lang]
    )
    return f'<div class="stat-grid">{cells}</div>'


def pillar_block(ctx):
    out = []
    for i, (title, body) in enumerate(PILLARS[ctx.lang], 1):
        out.append(f"""<div class="pillar">
  <div class="ico">{i:02d}</div>
  <div><h4>{esc(title)}</h4><p>{esc(body)}</p></div>
</div>""")
    return "".join(out)


def contact_info_card(ctx):
    c = COMPANY[ctx.lang]
    rows = [
        (c["address_label"], esc(c["address"])),
        (c["tel_label"], esc(c["tel"])),
        (c["fax_label"], esc(c["fax"])),
        (c["web_label"], " ".join(f'<a href="{esc(w if w.startswith("http") else "https://" + w)}" rel="noopener">{esc(w)}</a>' for w in c["websites"])),
        (c["email_label"], " ".join(f'<a href="mailto:{esc(e)}">{esc(e)}</a>' for e in c["emails"])),
        (c["im_label"], " &nbsp; ".join(f"{esc(k)}: {esc(v)}" for k, v in c["im"])),
        (c["mobile_label"], esc(c["mobile"][0]) + " / " + esc(c["mobile"][1])),
    ]
    lis = "".join(f'<li><span class="k">{esc(k)}</span><span class="v">{v}</span></li>' for k, v in rows)
    return f"""<div class="info-card">
  <h3>{esc(c['legal_name'])}</h3>
  <ul class="info-list">{lis}</ul>
</div>"""


def inquiry_form(ctx, compact=False):
    t = ctx.t
    return f"""<div class="form-card">
  <h3>{esc(t['inquiry'])}</h3>
  <p style="font-size:13.5px;color:var(--muted)">{esc(t['inquiry_sub'])}</p>
  <form action="mailto:sales@boppfilmsales.com" method="post" enctype="text/plain">
    <div class="field"><label>{esc(t['name'])}</label><input type="text" name="name" required></div>
    <div class="field"><label>{esc(t['company'])}</label><input type="text" name="company"></div>
    <div class="field"><label>{esc(t['email'])}</label><input type="email" name="email" required></div>
    <div class="field"><label>{esc(t['country'])}</label><input type="text" name="country"></div>
    <div class="field"><label>{esc(t['message'])}</label><textarea name="message" placeholder="{esc(t['message_ph'])}"></textarea></div>
    <button class="btn btn-solid" style="width:100%" type="submit">{esc(t['submit'])}</button>
    <p class="form-note">{esc(t['form_note'])}</p>
  </form>
</div>"""


def cta_band(ctx, title=None, sub=None, label=None):
    t = ctx.t
    return f"""<div class="cta-band">
  <div>
    <h3>{esc(title or t['article_cta'])}</h3>
    <p>{esc(sub or t['article_cta_sub'])}</p>
  </div>
  <a class="btn btn-gold" href="{ctx.page('contact.html')}">{esc(label or t['quote_cta'])}</a>
</div>"""


def product_card(ctx, p):
    t = ctx.t
    en = ctx.lang == "en"
    name = p["name_en"] if en else p["name_zh"]
    summary = p["summary_en"] if en else p["summary_zh"]
    model = p["model_en"] if en else p["model_zh"]
    cat = p["cat_name"] if en else p["cat_name_zh"]
    img = p["image_main"] or ""
    alt = esc(name)
    no_label = "Product No." if en else "产品编号"
    return f"""<a class="card" href="{ctx.page('products/' + p['id'] + '.html')}" data-item data-cat="{esc(p['cat_slug'])}" data-search-text="{esc(p['search_text'])}">
  <div class="card-media">
    {f'<img src="{ctx.asset(img)}" alt="{alt}" loading="lazy">' if img else ''}
    <span class="card-badge">{esc(cat)}</span>
  </div>
  <div class="card-body">
    <h3 class="card-title">{esc(name)}</h3>
    <p class="card-desc">{esc(summary)}</p>
    <div class="card-foot"><span class="code">{esc(no_label)} {esc(p['id'])}</span><span>{esc(model or '')}</span></div>
  </div>
</a>"""


def post_card(ctx, article, featured=False):
    t = ctx.t
    title = article["title"][ctx.lang]
    return f"""<a class="post-card" href="{ctx.page('blog/' + article['slug'] + '.html')}">
  <div class="post-thumb"><span>{esc(article['category'][ctx.lang])}</span></div>
  <div class="post-body">
    <div class="post-meta">
      <span class="cat">{esc(article['category'][ctx.lang])}</span>
      <span>{esc(article['date'])}</span>
      <span>{article['minutes']} {esc(t['minutes'])}</span>
    </div>
    <h3 class="post-title">{esc(title)}</h3>
    <p class="post-excerpt">{esc(article['excerpt'][ctx.lang])}</p>
    <span class="post-more">{esc(t['read'])} &rarr;</span>
  </div>
</a>"""
