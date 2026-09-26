# -*- coding: utf-8 -*-
"""Shared page shell: <head>, header, mobile nav, footer, floating actions."""
import json
from site_data import COMPANY, NAV, SERVICES, LEGAL_PAGES

C = COMPANY


def rel(depth):
    return "../" * depth


ICONS = {
"chart": '<path d="M3 3v18h18"/><path d="M7 15l3.5-4 3 2.5L21 6"/>',
"layers": '<path d="M12 2 3 7l9 5 9-5-9-5Z"/><path d="m3 12 9 5 9-5"/><path d="m3 17 9 5 9-5"/>',
"team": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
"check": '<path d="M22 11.1V12a10 10 0 1 1-5.9-9.1"/><path d="m9 11 3 3L22 4"/>',
"clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 1.9"/>',
"shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/>',
"bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8Z"/>',
"gauge": '<path d="M12 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z"/><path d="M13.4 10.6 19 5"/><path d="M20.7 17A9 9 0 1 0 3.3 17"/>',
"flame": '<path d="M12 22c4 0 7-2.7 7-6.5 0-4.5-4-6-4-9.5 0 0-3 1.5-3 5 0 1.5-1 2-1.6 1.3C9 11 9 9.5 9 9.5 7 11 5 12.8 5 15.5 5 19.3 8 22 12 22Z"/>',
"wrench": '<path d="M14.7 6.3a4 4 0 0 0 5 5l-9.2 9.2a2.1 2.1 0 0 1-3-3l7.2-11.2Z"/><path d="M18 2.5 21.5 6"/>',
"snow": '<path d="M12 2v20M4.5 6.5l15 11M19.5 6.5l-15 11"/><path d="m9 4 3 2 3-2M9 20l3-2 3 2"/>',
"brick": '<path d="M2 6h20v5H2zM2 13h20v5H2z"/><path d="M8 6v5M16 6v5M5 13v5M12 13v5M19 13v5"/>',
"road": '<path d="M4 22 8 2M20 22 16 2"/><path d="M12 4v3M12 11v3M12 18v3"/>',
"tools": '<path d="M14.5 3.5a4.5 4.5 0 0 0 6 6L21 22H3l.5-12.5a4.5 4.5 0 0 0 6-6"/><path d="M9.5 3.5 12 9l2.5-5.5"/>',
"pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
"phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/>',
"mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/>',
"clock2": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
"file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6"/><path d="M9 15h6M9 11h3"/>',
}

SERVICE_ICON = {
    "electrical": "bolt", "control-instrumentation": "gauge", "fire-gas-security": "flame",
    "mechanical-piping": "wrench", "thermal-insulation": "snow", "refractory-lining": "brick",
    "civil-works": "road", "maintenance-shutdown": "tools",
}


def icon(name, cls=""):
    p = ICONS.get(name, ICONS["check"])
    return ('<svg viewBox="0 0 24 24" aria-hidden="true"%s>%s</svg>'
            % ((' class="%s"' % cls) if cls else "", p))


def picture(name, alt, cls="", sizes="", loading="lazy", w=None, h=None, fetchpriority=None):
    """<picture> with WebP + JPEG fallback."""
    attrs = ['alt="%s"' % alt, 'loading="%s"' % loading,
             'decoding="%s"' % ("sync" if loading == "eager" else "async")]
    if w: attrs.append('width="%d"' % w)
    if h: attrs.append('height="%d"' % h)
    if sizes: attrs.append('sizes="%s"' % sizes)
    if fetchpriority: attrs.append('fetchpriority="%s"' % fetchpriority)
    return ('<picture%s><source srcset="{B}assets/img/%s.webp" type="image/webp">'
            '<img src="{B}assets/img/%s.jpg" %s></picture>'
            % ((' class="%s"' % cls) if cls else "", name, name, " ".join(attrs)))


# --------------------------------------------------------------------------- head
def head(title, desc, canonical, depth, extra_schema=None, og_image="hero-plant"):
    B = rel(depth)
    org = {
        "@context": "https://schema.org",
        "@type": "GeneralContractor",
        "@id": C["website"] + "/#organisation",
        "name": C["name"],
        "alternateName": ["Pyramid Engineering", "PEPL", "Pyramid Engineering Pte Ltd"],
        "url": C["website"] + "/",
        "logo": C["website"] + "/assets/img/logo.svg",
        "image": C["website"] + "/assets/img/hero-plant.jpg",
        "description": "Singapore engineering contractor delivering electrical, control and instrumentation, "
                       "mechanical, thermal insulation, refractory and civil works for refineries, "
                       "petrochemical plants, power stations and industrial facilities.",
        "foundingDate": "2008",
        "telephone": C["phone_display"],
        "email": C["email"],
        "address": {"@type": "PostalAddress", "streetAddress": C["address_line1"] + ", " + C["address_line2"],
                    "addressLocality": "Singapore", "postalCode": "627564", "addressCountry": "SG"},
        "areaServed": {"@type": "Country", "name": "Singapore"},
        "knowsAbout": ["Electrical engineering", "Control and instrumentation", "Thermal insulation",
                       "Refractory lining", "Plant maintenance", "Turnaround and shutdown"],
        "hasCredential": ["ISO 9001:2015", "ISO 45001:2018", "bizSAFE STAR"],
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
             "opens": "08:30", "closes": "18:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "08:30", "closes": "13:00"},
        ],
    }
    blocks = ['<script type="application/ld+json">%s</script>' % json.dumps(org, ensure_ascii=False)]
    if extra_schema:
        blocks.append('<script type="application/ld+json">%s</script>'
                      % json.dumps(extra_schema, ensure_ascii=False))

    return """<!DOCTYPE html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{site}/{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#07131F">
<meta name="author" content="{cname}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{cname}">
<meta property="og:locale" content="en_SG">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{site}/{canonical}">
<meta property="og:image" content="{site}/assets/img/{og}.jpg">
<meta property="og:image:width" content="1920">
<meta property="og:image:height" content="760">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{site}/assets/img/{og}.jpg">
<link rel="icon" href="{B}assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{B}assets/img/apple-touch-icon.png">
<link rel="preload" href="{B}assets/fonts/archivo-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{B}assets/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{B}assets/css/style.css">
{schema}
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
""".format(title=title, desc=desc, site=C["website"], canonical=canonical, cname=C["name"],
           og=og_image, B=B, schema="\n".join(blocks))


# --------------------------------------------------------------------------- header
def header(active, depth):
    B = rel(depth)
    items = []
    for label, href, kind in NAV:
        cur = ' aria-current="page"' if active == href else ""
        if kind == "SERVICES":
            sub = "".join(
                '<li><a href="{B}services/{s}.html"><strong>{t}</strong><span>{n}</span></a></li>'.format(
                    B=B, s=s["slug"], t=s["nav"], n=s["menu_note"]) for s in SERVICES)
            items.append(
                '<li class="has-sub"><a href="{B}{h}"{c}>{l}</a>'
                '<ul class="submenu"><li><a href="{B}services.html"><strong>All services</strong>'
                '<span>Overview of every discipline we deliver</span></a></li>{sub}</ul></li>'.format(
                    B=B, h=href, c=cur, l=label, sub=sub))
        else:
            items.append('<li><a href="{B}{h}"{c}>{l}</a></li>'.format(B=B, h=href, c=cur, l=label))

    m_items = []
    for label, href, kind in NAV:
        if kind == "SERVICES":
            sub = "".join('<a href="{B}services/{s}.html">{t}</a>'.format(B=B, s=s["slug"], t=s["nav"])
                          for s in SERVICES)
            m_items.append('<li><a href="{B}{h}">{l}</a><div class="m-sub">{sub}</div></li>'.format(
                B=B, h=href, l=label, sub=sub))
        else:
            m_items.append('<li><a href="{B}{h}">{l}</a></li>'.format(B=B, h=href, l=label))

    brand = ('<a class="brand" href="{B}index.html" aria-label="{cn} — home">'
             '<img class="brand-logo" src="{B}assets/img/logo-pyramid.png" alt="" width="981" height="942">'
             '</a>').format(B=B, cn=C["name"])

    return """<header class="site-header">
  <div class="topbar">
    <div class="wrap">
      <div class="topbar-left">
        <a href="tel:{tel}">{phone_ico} {phone}</a>
        <a href="mailto:{mail}">{mail_ico} {mail}</a>
      </div>
      <div class="topbar-badges">
        <span class="topbar-logo"><img src="{B}assets/img/badge-iso9001.svg" alt="ISO 9001:2015 certified" width="186" height="64"></span>
        <span class="topbar-logo"><img src="{B}assets/img/badge-iso45001.svg" alt="ISO 45001:2018 certified" width="186" height="64"></span>
        <span class="topbar-logo"><img src="{B}assets/img/badge-bizsafe.png" alt="bizSAFE STAR" width="183" height="120"></span>
        <span class="topbar-logo"><img src="{B}assets/img/badge-aspri.png" alt="ASPRI Member" width="385" height="110"></span>
      </div>
    </div>
  </div>
  <div class="wrap">
    <nav class="nav" aria-label="Primary">
      {brand}
      <ul class="nav-menu">{items}</ul>
      <div class="nav-cta">
        <a class="btn btn--primary btn--sm" href="{B}contact.html">Request a Quote</a>
        <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false"
                aria-controls="mobile-nav" aria-label="Open navigation menu"><span></span></button>
      </div>
    </nav>
  </div>
</header>

<div class="mobile-nav" id="mobile-nav">
  <div class="wrap">
    <div class="mobile-nav-head">
      {brand}
      <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false"
              aria-label="Close navigation menu"><span></span></button>
    </div>
    <ul>{m_items}</ul>
    <a class="btn btn--primary" href="{B}contact.html">Request a Quote</a>
    <div class="m-contact">
      <a href="tel:{tel}">{phone}</a>
      <a href="mailto:{mail}">{mail}</a>
      <p style="margin:12px 0 0">{addr}</p>
    </div>
  </div>
</div>
<main id="main">
""".format(brand=brand, items="".join(items), m_items="".join(m_items), B=B,
           tel=C["phone_tel"], phone=C["phone_display"], mail=C["email"], addr=C["address_full"],
           phone_ico=icon("phone", "").replace('viewBox', 'width="13" height="13" fill="none" stroke="currentColor" stroke-width="1.8" viewBox'),
           mail_ico=icon("mail", "").replace('viewBox', 'width="13" height="13" fill="none" stroke="currentColor" stroke-width="1.8" viewBox'))


# --------------------------------------------------------------------------- CTA + footer
def cta_band(heading="Have a scope you need priced?",
             body="Send us drawings, a specification or a short description of the work. "
                  "We will come back with clarifications and a proposal — not a brochure.",
             depth=0):
    B = rel(depth)
    return """<section class="cta-band">
  <div class="wrap cta-band__inner">
    <div class="reveal"><h2>{h}</h2><p>{b}</p></div>
    <div class="btn-row reveal reveal-d1">
      <a class="btn btn--red" href="{B}contact.html">Request a Consultation</a>
      <a class="btn btn--on-dark" href="tel:{tel}">Call {phone}</a>
    </div>
  </div>
</section>
""".format(h=heading, b=body, B=B, tel=C["phone_tel"], phone=C["phone_display"])


def footer(depth):
    B = rel(depth)
    svc_links = ('<li><a href="{B}services/electrical.html">Electrical</a></li>'
                 '<li><a href="{B}services/control-instrumentation.html">Control & Instrumentation</a></li>\n'
                 '        <li><a href="{B}services/fire-gas-security.html">Fire & Gas and Security</a></li>\n'
                 '        <li><a href="{B}services/mechanical-piping.html">Mechanical & Piping</a></li>\n'
                 '        <li><a href="{B}services/thermal-insulation.html">Thermal Insulation</a></li>\n      ').format(B=B)
    legal = "".join('<li><a href="{B}{p}.html">{t}</a></li>'.format(
        B=B, p=p, t=p.replace("-", " ").replace("and", "&amp;").title().replace("&Amp;", "&amp;"))
        for p in LEGAL_PAGES)
    return """</main>
<footer class="site-footer">
  <h2 class="visually-hidden">Site footer</h2>
  <div class="wrap footer-main">
    <div class="footer-brand">
      <a class="brand" href="{B}index.html" aria-label="{cn} — home">
        <img class="brand-logo" src="{B}assets/img/logo-pyramid.png" alt="" width="981" height="942">
      </a>
      <p>Singapore engineering contractor delivering electrical, control &amp; instrumentation, mechanical,
         thermal insulation, refractory and civil works to process plants since 2008.</p>
      <div class="footer-badges">
        <span>ISO 9001:2015</span><span>ISO 45001:2018</span><span>bizSAFE STAR</span>
        <span>ASPRI</span><span>UEN {uen}</span>
      </div>
      <div class="socials">
        <a href="{li}" aria-label="Pyramid Engineering on LinkedIn"><svg viewBox="0 0 24 24"><path d="M4.98 3.5A2.5 2.5 0 1 1 0 3.5a2.5 2.5 0 0 1 4.98 0ZM.24 8.02h4.5V24H.24V8.02Zm7.86 0h4.31v2.18h.06c.6-1.14 2.07-2.34 4.26-2.34 4.56 0 5.4 3 5.4 6.9V24h-4.5v-7.34c0-1.75-.03-4-2.44-4-2.44 0-2.81 1.9-2.81 3.87V24H8.1V8.02Z"/></svg></a>
        <a href="mailto:{mail}" aria-label="Email Pyramid Engineering"><svg viewBox="0 0 24 24"><path d="M2 5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5Zm2.5.8L12 11.4l7.5-5.6H4.5Z"/></svg></a>
      </div>
    </div>
    <div>
      <h3>Services</h3>
      <ul>{svc}</ul>
    </div>
    <div>
      <h3>Company</h3>
      <ul>
        <li><a href="{B}about.html">About us</a></li>
        <li><a href="{B}sectors.html">Sectors we serve</a></li>
        <li><a href="{B}projects.html">Project portfolio</a></li>
        <li><a href="{B}certifications.html">Certifications</a></li>
        <li><a href="{B}contact.html">Contact</a></li>
        <li><a href="{B}assets/downloads/pyramid-engineering-capability-statement.pdf" download>Capability Statement (PDF)</a></li>
      </ul>
    </div>
    <div>
      <h3>Get in touch</h3>
      <ul>
        <li>{addr1}<br>{addr2}<br>{addr3}</li>
        <li><a href="tel:{tel}">{phone}</a></li>
        <li><a href="mailto:{mail}">{mail}</a></li>
        <li><a href="mailto:{admin}">{admin}</a></li>
        <li><a href="https://wa.me/{wa}" rel="noopener">WhatsApp us</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap">
    <div class="footer-bottom">
      <p style="margin:0">&copy; <span data-year>2026</span> {cn}. UEN {uen}. All rights reserved.</p>
      <ul>{legal}</ul>
    </div>
  </div>
</footer>

<div class="floaters">
  <a class="fl-wa" href="https://wa.me/{wa}?text=Hello%20Pyramid%20Engineering%2C%20I%20would%20like%20to%20enquire%20about%20"
     rel="noopener" aria-label="Chat with us on WhatsApp">
    <span class="tip">WhatsApp</span>
    <svg viewBox="0 0 24 24"><path d="M12.04 2C6.6 2 2.2 6.4 2.2 11.84c0 1.74.46 3.44 1.32 4.94L2.1 22l5.36-1.4a9.8 9.8 0 0 0 4.58 1.16h.01c5.43 0 9.84-4.4 9.84-9.84 0-2.63-1.02-5.1-2.88-6.96A9.78 9.78 0 0 0 12.04 2Zm0 17.96h-.01a8.2 8.2 0 0 1-4.16-1.14l-.3-.18-3.1.81.83-3.02-.2-.31a8.14 8.14 0 0 1-1.25-4.35c0-4.5 3.68-8.17 8.2-8.17a8.13 8.13 0 0 1 8.18 8.18c0 4.51-3.67 8.18-8.19 8.18Zm4.5-6.12c-.25-.13-1.46-.72-1.68-.8-.23-.09-.39-.13-.56.12-.16.25-.63.8-.78.96-.14.17-.29.19-.53.07-.25-.13-1.04-.39-1.98-1.23a7.4 7.4 0 0 1-1.37-1.7c-.14-.25-.01-.38.11-.5.11-.12.25-.29.37-.44.13-.15.17-.25.25-.42.09-.16.04-.31-.02-.44-.06-.12-.56-1.34-.76-1.84-.2-.48-.4-.42-.56-.42h-.47c-.16 0-.43.06-.65.31-.22.25-.85.84-.85 2.04s.87 2.37.99 2.53c.12.17 1.72 2.62 4.16 3.68.58.25 1.03.4 1.39.51.58.19 1.11.16 1.53.1.47-.07 1.46-.6 1.66-1.17.21-.58.21-1.07.15-1.17-.06-.11-.23-.17-.47-.29Z"/></svg>
  </a>
  <a class="fl-quote" href="{B}contact.html" aria-label="Request a quotation">
    <span class="tip">Request a quote</span>
    <svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6"/><path d="M9 15h6M9 11h3"/></svg>
  </a>
  <button class="fl-top" type="button" aria-label="Back to top">
    <svg viewBox="0 0 24 24"><path d="m6 15 6-6 6 6"/></svg>
  </button>
</div>

<script src="{B}assets/js/main.js" defer></script>
</body>
</html>
""".format(B=B, cn=C["name"], uen=C["uen"], svc=svc_links, legal=legal,
           addr1=C["address_line1"], addr2=C["address_line2"], addr3=C["address_city"],
           tel=C["phone_tel"], phone=C["phone_display"], mail=C["email"],
           admin=C["email_admin"], wa=C["whatsapp"], li=C["linkedin"])


def page_hero(title, sub, img, depth, crumbs, alt=""):
    B = rel(depth)
    mid = [c for c in crumbs[:-1] if c[1] != "index.html"]
    lis = "".join('<li><a href="%s%s">%s</a></li>' % (B, h, t) for t, h in mid)
    lis += '<li aria-current="page">%s</li>' % crumbs[-1][0]
    return """<section class="page-hero">
  <div class="page-hero__media">{img}</div>
  <div class="wrap page-hero__inner">
    <nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="{B}index.html">Home</a></li>{lis}</ol></nav>
    <h1>{t}</h1>
    <p>{s}</p>
  </div>
</section>
""".format(img=picture(img, alt or title, loading="eager", fetchpriority="high").replace("{B}", B),
           B=B, lis=lis, t=title, s=sub)
