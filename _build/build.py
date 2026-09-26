# -*- coding: utf-8 -*-
"""Static site generator for Pyramid Engineering Private Limited.
Run:  python3 build.py      (from this directory)
Output: ../site/
"""
import os, json, re, html
from site_data import (COMPANY as C, SERVICES, SECTORS, PROJECTS, SECTOR_LABELS, TESTIMONIALS,
                       CLIENTS, CONTRACTORS, PLANTS, CERTIFICATIONS, FAQS, PROCESS, WHY_US,
                       LEGAL_PAGES)
from shell import head, header, footer, cta_band, page_hero, picture, icon, rel, SERVICE_ICON

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")
YEARS = 2026 - C["founded"]


def write(path, content, depth):
    content = content.replace("{B}", rel(depth))
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


# =========================================================================== HOME
def build_home():
    d = 0
    svc_cards = ""
    for i, s in enumerate(SERVICES[:6]):
        svc_cards += """<article class="card reveal reveal-d{dl}">
  <div class="card__media"><span class="card__idx">{idx}</span>{img}</div>
  <div class="card__body">
    <h3>{t}</h3><p>{p}</p>
    <div class="card__foot"><a class="link-arrow" href="{{B}}services/{s}.html">Explore {t}<span class="visually-hidden"> service page</span></a></div>
  </div>
</article>""".format(dl=(i % 3) + 1, idx="%02d" % (i + 1), img=picture(s["img"], s["img_alt"]),
                     t=s["nav"], p=s["short"], s=s["slug"])

    why = "".join("""<article class="fcard reveal reveal-d{dl}">
  <div class="ico">{ic}</div><h3>{t}</h3><p>{p}</p>
</article>""".format(dl=(i % 3) + 1, ic=icon(ik), t=t, p=p) for i, (t, p, ik) in enumerate(WHY_US))

    steps = "".join("<div><h3>%s</h3><p>%s</p></div>" % (t, p) for t, p in PROCESS[:4])

    sectors_grid = "".join("""<a class="fcard reveal reveal-d{dl}" href="{{B}}sectors.html#{sl}" style="text-decoration:none;display:block">
  <div class="ico">{ic}</div><h3>{n}</h3><p>{s}</p>
</a>""".format(dl=(i % 4) + 1, sl=s["slug"], ic=icon("layers"), n=s["name"], s=s["short"])
        for i, s in enumerate(SECTORS))

    feat = [p for p in PROJECTS if p[0] in (
        "REC Solar revamp projects", "Maintenance support under GE-FieldCore &amp; Hitachi",
        "Pfizer plant project", "Evonik ME06 / Linde IGP-2",
        "Shell Eastern Petroleum — Pulau Bukom turnaround", "Murata Electronics Singapore")][:6]
    feat_cards = "".join("""<article class="proj reveal reveal-d{dl}">
  <p class="proj__sector">{sec}</p><h3>{n}</h3>
  <p class="proj__meta">{cl} &middot; {per}</p><p class="proj__scope">{sc}</p>
</article>""".format(dl=(i % 3) + 1, sec=SECTOR_LABELS[sk.split()[0]], n=n, cl=cl, per=per, sc=sc)
        for i, (n, cl, sk, per, sc) in enumerate(feat))

    quotes = "".join("""<figure class="quote reveal reveal-d{dl}">
  <p class="quote__tag">{tag}</p><blockquote>&ldquo;{q}&rdquo;</blockquote>
  <figcaption><strong>{n}</strong><span>{r}</span></figcaption>
</figure>""".format(dl=(i % 3) + 1, tag=tag, q=q, n=n, r=r)
        for i, (tag, q, n, r) in enumerate(TESTIMONIALS[:3]))

    faqs = "".join("<details%s><summary>%s</summary><div class=\"acc__body\"><p>%s</p></div></details>"
                   % (" open" if i == 0 else "", q, a) for i, (q, a) in enumerate(FAQS[:6]))

    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage",
                  "mainEntity": [{"@type": "Question", "name": strip_tags(q),
                                  "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
                                 for q, a in FAQS[:6]]}

    body = """
<section class="hero">
  <div class="hero__media">{heroimg}</div>
  <div class="wrap hero__inner">
    <div class="hero__grid">
      <div class="reveal">
        <p class="eyebrow">Singapore &middot; Established {founded}</p>
        <h1>Electrical, C&amp;I, Automation and Thermal Insulation for <em>process plants</em></h1>
        <p class="hero__sub">Delivering safe, reliable and cost-effective engineering services to Singapore's
          refineries, petrochemical complexes, power stations and industrial facilities &mdash; backed by
          {years} years of project execution and long-term maintenance expertise.</p>
        <div class="btn-row">
          <a class="btn btn--red" href="{{B}}contact.html">Request a Project Consultation</a>
          <a class="btn btn--on-dark" href="{{B}}assets/downloads/pyramid-engineering-capability-statement.pdf"
             download>Download Capability Statement</a>
        </div>
      </div>
      <aside class="hero__card reveal reveal-d2">
        <h2>Talk to an engineer, not a call centre</h2>
        <p>Send a scope, a drawing or a shutdown date. We will respond with clarifications and a proposal.</p>
        <ul>
          <li>Multi-discipline crews under one contractor</li>
          <li>Live-plant and permit-to-work experienced</li>
          <li>Turnaround, call-out and term maintenance</li>
        </ul>
        <div class="btn-row">
          <a class="btn btn--primary btn--sm" href="tel:{tel}">Call {phone}</a>
          <a class="btn btn--on-dark btn--sm" href="https://wa.me/{wa}" rel="noopener">WhatsApp</a>
        </div>
      </aside>
    </div>
    <dl class="hero__trust reveal reveal-d3">
      <div><dt>{founded}</dt><dd>Established in Singapore</dd></div>
      <div><dt>50+</dt><dd>Plant projects executed</dd></div>
      <div><dt>18+</dt><dd>Process plants served</dd></div>
      <div><dt>STAR</dt><dd>bizSAFE level attained</dd></div>
    </dl>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <p class="eyebrow" style="justify-content:center;display:flex">Trusted by process industry clients and main contractors</p>
    <div class="logo-band reveal">{clients}</div>
  </div>
</section>

<section class="section section--paper2">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">Who we are</p>
        <h2>An engineering contractor built around plant that cannot stop</h2>
        <p class="lead">Pyramid Engineering Private Limited was founded in {founded} by a small, dedicated team
          focused on the Oil &amp; Gas, refinery, petrochemical and power generation industries. We specialise in
          plant maintenance, small capital projects, shutdown maintenance and start-up support, with deep expertise
          in electrical and instrumentation works and thermal insulation.</p>
        <p>Most of what we do happens inside operating plant &mdash; under permit, around live systems, and to a
          shutdown window that does not move. That constraint shapes how we plan, staff and document every job.</p>
        <ul class="checklist">
          <li>Certified to ISO 9001:2015 and ISO 45001:2018, and assessed at bizSAFE STAR</li>
          <li>Corporate member of ASPRI and the Singapore Welding Society</li>
          <li>Long-term maintenance relationships measured in years, not job numbers</li>
        </ul>
        <div class="btn-row" style="margin-top:26px">
          <a class="btn btn--primary" href="{{B}}about.html">More about Pyramid</a>
          <a class="btn btn--ghost" href="{{B}}certifications.html">Our certifications</a>
        </div>
      </div>
      <div class="img-duo reveal reveal-d2">
        <figure class="figure">{ab1}<figcaption class="figure__tag">Refinery &amp; petrochemical</figcaption></figure>
        <figure class="figure">{ab2}<figcaption class="figure__tag">Insulation</figcaption></figure>
        <figure class="figure">{ab3}<figcaption class="figure__tag">Instrumentation</figcaption></figure>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">What we do</p>
      <h2>Priority services</h2>
      <p>Six core disciplines, delivered separately or as one integrated package &mdash; which is usually
         what removes cost and delay from a plant project.</p>
    </div>
    <div class="grid g-3">{svc}</div>
    <div class="btn-row" style="margin-top:38px;justify-content:center">
      <a class="btn btn--ghost" href="{{B}}services.html">All eight service lines</a>
    </div>
  </div>
</section>

<section class="section section--dark bp">
  <div class="wrap">
    <div class="sec-head sec-head--center reveal">
      <p class="eyebrow">Why clients choose PEPL</p>
      <h2>Reasons procurement teams shortlist us</h2>
    </div>
    <div class="grid g-3">{why}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">By the numbers</p>
      <h2>A track record you can verify</h2>
      <p>Every figure below is traceable to the project register and certificates published on this site.</p>
    </div>
    <dl class="stats reveal">
      <div><dt><span data-count="{years}">{years}</span></dt><dd>Years in operation</dd></div>
      <div><dt><span data-count="50" data-suffix="+">50+</span></dt><dd>Documented projects</dd></div>
      <div><dt><span data-count="18" data-suffix="+">18+</span></dt><dd>Process plants served</dd></div>
      <div><dt><span data-count="12" data-suffix="">12</span></dt><dd>Main contractor partners</dd></div>
    </dl>
  </div>
</section>

<section class="section section--paper2">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Sectors we serve</p>
      <h2>Where our crews spend their time</h2>
      <p>Procurement teams shortlist on sector relevance. Here is exactly where we have worked.</p>
    </div>
    <div class="grid g-4">{sectors}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">How we work</p>
      <h2>From enquiry to handover</h2>
      <p>A method that assumes your plant is running and your window is fixed.</p>
    </div>
    <div class="steps reveal">{steps}</div>
    <div class="btn-row" style="margin-top:30px"><a class="link-arrow" href="{{B}}about.html#process">See the full six-stage process</a></div>
  </div>
</section>

<section class="section section--paper2">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Selected work</p>
      <h2>Recent and ongoing projects</h2>
      <p>A sample from a register spanning refineries, power generation, solar, pharmaceutical and manufacturing.</p>
    </div>
    <div class="proj-grid">{feat}</div>
    <div class="btn-row" style="margin-top:38px;justify-content:center">
      <a class="btn btn--primary" href="{{B}}projects.html">View the full project portfolio</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Client references</p>
      <h2>What our clients say</h2>
    </div>
    <div class="grid g-3">{quotes}</div>
    <div class="btn-row" style="margin-top:34px"><a class="link-arrow" href="{{B}}about.html#testimonials">Read all client references</a></div>
  </div>
</section>

<section class="section section--paper2">
  <div class="wrap">
    <div class="sec-head sec-head--center reveal">
      <p class="eyebrow">Certifications &amp; memberships</p>
      <h2>Qualified for procurement</h2>
      <p>Current certificates, numbers and validity dates are published in full &mdash; not just claimed.</p>
    </div>
    <div class="logo-band reveal">{certband}</div>
    <div class="btn-row" style="margin-top:34px;justify-content:center">
      <a class="btn btn--ghost" href="{{B}}certifications.html">View certificates and validity dates</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap wrap-narrow">
    <div class="sec-head sec-head--center reveal">
      <p class="eyebrow">Frequently asked</p>
      <h2>Questions we get before a first job</h2>
    </div>
    <div class="acc reveal">{faqs}</div>
    <p style="text-align:center;margin-top:26px"><a class="link-arrow" href="{{B}}contact.html">Ask us something else</a></p>
  </div>
</section>
{cta}""".format(
        heroimg=picture("hero-plant", "Industrial process plant at dusk with pipework, structures and process equipment",
                        loading="eager", fetchpriority="high"),
        founded=C["founded"], years=YEARS, tel=C["phone_tel"], phone=C["phone_display"], wa=C["whatsapp"],
        clients="".join("<span>%s</span>" % c for c in CLIENTS + CONTRACTORS[:6]),
        ab1=picture("p-process-piping", "Process piping and supports installed in an operating plant"),
        ab2=picture("p-insulated-vessel", "Insulated and clad process vessels"),
        ab3=picture("p-calibration", "Field instrument calibration in progress"),
        svc=svc_cards, why=why, sectors=sectors_grid, steps=steps, feat=feat_cards, quotes=quotes,
        certband="".join("<span>%s</span>" % c for c in
                         ["ISO 9001:2015", "ISO 45001:2018", "bizSAFE STAR", "ASPRI Corporate Member",
                          "Singapore Welding Society", "BCA Registered"]),
        faqs=faqs, cta=cta_band(depth=0))

    doc = (head("Electrical, C&I &amp; Insulation Contractor Singapore | Pyramid",
                "Singapore engineering contractor since 2008 — electrical, C&amp;I, thermal insulation, "
                "refractory and plant maintenance for refineries, petrochemical and power plants.",
                "index.html", 0, extra_schema=faq_schema)
           + header("index.html", 0) + body + footer(0))
    return write("index.html", doc, 0)


# =========================================================================== ABOUT
def build_about():
    d = 0
    quotes = "".join("""<figure class="quote reveal reveal-d{dl}">
  <p class="quote__tag">{tag}</p><blockquote>&ldquo;{q}&rdquo;</blockquote>
  <figcaption><strong>{n}</strong><span>{r}</span></figcaption>
</figure>""".format(dl=(i % 2) + 1, tag=tag, q=q, n=n, r=r)
        for i, (tag, q, n, r) in enumerate(TESTIMONIALS))

    steps = "".join("<div><h3>%s</h3><p>%s</p></div>" % (t, p) for t, p in PROCESS)

    milestones = [
        ("2008", "Founded in Singapore", "A small, dedicated team begins delivering essential services to Oil &amp; Gas, refinery, petrochemical and power plant clients. First projects executed under Kurihara Kogyo."),
        ("2009 – 2012", "Refinery turnaround credentials", "Turnaround scopes at ExxonMobil Asia Pacific, Shell Eastern Petroleum Pulau Bukom, the Singapore Refinery Complex and Tuas Incinerator Plant establish the company in shutdown work."),
        ("2011", "Industry membership", "Admitted as a corporate member of ASPRI (Association of Process Industry) and the Singapore Welding Society on 1 June 2011."),
        ("2012 – 2019", "Long-term maintenance relationships", "Continuous maintenance positions begin at Murata Electronics (2012) and Ashahi Kokusai Keiso, alongside project work for Chevron Ornite, DuPont, Lanxess, Evonik and Vopak."),
        ("2021 – 2023", "Power generation and renewables", "Shutdown maintenance across Keppel Merlimau, Senoko, Sembcorp Cogen Banyan and Tuas under GE-FieldCore and Hitachi; REC Solar revamp projects begin."),
        ("2024", "Certified management systems", "ISO 9001:2015 and ISO 45001:2018 certification awarded in February 2024; bizSAFE STAR certificate issued in March 2024."),
        ("Today", "A maintenance and project solutions partner", "Ongoing project and maintenance work for Pfizer, Kim Hock, Global Foundries, Micron, Air Liquide, REC Solar and Murata across eight service disciplines."),
    ]
    tl = "".join("""<div class="reveal"><h3><span style="font-family:var(--font-mono);font-size:.78rem;letter-spacing:.12em;color:var(--red-300);display:block;margin-bottom:8px">{y}</span>{t}</h3><p>{b}</p></div>""".format(y=y, t=t, b=b) for y, t, b in milestones)

    body = page_hero("About Pyramid Engineering",
                     "Your trusted partner in plant excellence and reliability — an engineering contractor "
                     "built in Singapore, for Singapore's process industry.",
                     "power-station", 0,
                     [("Home", "index.html"), ("About", "about.html")],
                     "Power generation plant with cooling towers at sunrise") + """
<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">Company overview</p>
        <h2>Engineering that keeps process plant running</h2>
        <p class="lead">Pyramid Engineering Private Limited (PEPL) is a trusted engineering contractor specialising
          in Electrical, Control &amp; Instrumentation (EC&amp;I), Automation Systems and Thermal Insulation for
          process piping and industrial equipment. With a skilled workforce and a strong project portfolio, PEPL
          consistently delivers safe, reliable and cost-effective engineering solutions for industrial clients.</p>
        <p>The company was founded in {founded} by a small, dedicated team focused on delivering essential services
          to the Oil &amp; Gas, refinery, petrochemical and power plant industries. We specialise in plant
          maintenance, small capital projects, shutdown maintenance and start-up support &mdash; the work that
          happens inside a live facility rather than on an empty construction site.</p>
        <p>PEPL's proven track record across major industrial sectors positions the company as a preferred partner
          for project execution, commissioning and long-term maintenance services. Our project management
          philosophy is founded on the ACTIVE principle &mdash; Achieving Competitiveness Through Innovation and
          Value Enhancement.</p>
      </div>
      <figure class="figure figure--framed reveal reveal-d2">{img}
      </figure>
    </div>
  </div>
</section>

<section class="section section--paper2">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Leadership</p><h2>A message from our Director</h2></div>
    <div class="split split--wide-left" style="align-items:start">
      <div class="reveal">
        <p class="lead">&ldquo;In {founded}, we embarked on a mission to excel in providing essential services to key
          industries. Today, our commitment remains unwavering.&rdquo;</p>
        <p>We specialise in plant maintenance, small capital projects, shutdown support and more, with a focus on
          electrical, instrumentation, thermal insulation and refractory solutions.</p>
        <p>Our journey is a testament to our team's dedication and expertise. They have consistently delivered
          excellence, and I am proud of what we have achieved together. We are your trusted partners, your
          problem-solvers, and your champions of excellence. Thank you for joining us on this journey.</p>
        <p style="margin-top:26px"><strong style="font-family:var(--font-display);font-size:1.05rem">Mr Bala</strong><br>
          <span style="color:var(--ink-3);font-size:.92rem">Director, Pyramid Engineering Private Limited</span></p>
      </div>
      <figure class="figure figure--framed reveal reveal-d2">{dir}</figure>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Vision, mission &amp; values</p><h2>What we hold ourselves to</h2></div>
    <div class="grid g-3">
      <article class="fcard reveal">
        <div class="ico">{ic1}</div>
        <h3>Our Vision</h3>
        <p>To be the best partner in the fields of engineering &mdash; electrical, control &amp; instrumentation,
          automation systems and thermal insulation. Excellence in engineering, client-centric partnerships,
          and global reach with local impact.</p>
      </article>
      <article class="fcard reveal reveal-d1">
        <div class="ico">{ic2}</div>
        <h3>Our Mission</h3>
        <ul class="card__list" style="margin-top:12px">
          <li>Commit to taking part in the Safety Management System</li>
          <li>Set the standard for technical knowledge, engineering quality and project management</li>
          <li>Add value and improve customer operations</li>
          <li>Deliver quality projects safely, on schedule and within budget</li>
          <li>Develop world-class systems integration capabilities</li>
          <li>Keep a skilled and disciplined staff</li>
        </ul>
      </article>
      <article class="fcard reveal reveal-d2">
        <div class="ico">{ic3}</div>
        <h3>Core Values</h3>
        <ul class="card__list" style="margin-top:12px">
          <li>Safety first, without exception</li>
          <li>Technical excellence in every discipline</li>
          <li>Transparent communication with clients</li>
          <li>On-time delivery against fixed windows</li>
          <li>Long-term partnership over single transactions</li>
        </ul>
      </article>
    </div>
  </div>
</section>

<section class="section section--dark bp">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Company history</p><h2>Milestones since {founded}</h2>
      <p>{years} years of continuous work in Singapore's process industry.</p></div>
    <div class="grid g-3">{tl}</div>
  </div>
</section>

<section class="section" id="capabilities">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Infrastructure &amp; capability</p>
      <h2>How the company is put together</h2></div>
    <div class="grid g-2">
      <div class="reveal">
        <h3>Workforce and project management</h3>
        <ul class="checklist">
          <li>Experienced engineering professionals and discipline supervisors</li>
          <li>Onsite coordinators and skilled tradesmen across all disciplines</li>
          <li>Documented health and safety policy applied on every site</li>
          <li>Quality control regime aligned to ISO 9001:2015</li>
          <li>Integrated project teams formed with client engineering organisations</li>
        </ul>
        <h3 style="margin-top:34px">Equipment management</h3>
        <p>Our equipment management function supports performance-driven construction by ensuring the availability
          of appropriate tools and equipment, and that everything issued to site is reliable and maintained in a
          safe, working condition.</p>
      </div>
      <div class="reveal reveal-d1">
        <h3>Delivery model</h3>
        <p>PEPL designs, supplies, installs, commissions, packages and upgrades mechanical, electrical,
          instrumentation, process control, thermal insulation, scaffolding and refractory lining systems.
          Installation, commissioning and project training are all services we are prepared to offer.</p>
        <p>To consistently deliver projects as safely as possible and in accordance with schedule and budget,
          PEPL forms an integrated project team with clients in engineering organisations who are independent
          manufacturers or contractors.</p>
        <div class="note-box" style="margin-top:24px">
          <strong>Additional capabilities.</strong> Alongside the eight service lines, PEPL provides scaffolding
          erection, modification and dismantling; tank cleaning, desludging and hydrojetting; and manpower
          provision for general works &mdash; frequently packaged with maintenance and turnaround scopes.
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--paper2" id="process">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Our method</p><h2>The six-stage delivery process</h2>
      <p>Designed around live plant, fixed shutdown windows and client permit systems.</p></div>
    <div class="steps reveal" style="grid-template-columns:repeat(3,1fr)">{steps}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Who we work with</p><h2>Clients, main contractors and plants</h2></div>
    <div class="grid g-3">
      <div class="reveal">
        <h3 style="font-size:1.02rem">Direct clients</h3>
        <ul class="card__list">{cl}</ul>
      </div>
      <div class="reveal reveal-d1">
        <h3 style="font-size:1.02rem">Main contractors</h3>
        <ul class="card__list">{co}</ul>
      </div>
      <div class="reveal reveal-d2">
        <h3 style="font-size:1.02rem">Plants worked in</h3>
        <ul class="card__list">{pl}</ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--paper2" id="testimonials">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Client references</p><h2>In our clients' words</h2>
      <p>References supplied by project and site managers at the companies we work for.</p></div>
    <div class="grid g-2">{quotes}</div>
  </div>
</section>
{cta}""".format(
        founded=C["founded"], years=YEARS,
        img=picture("team", "The Pyramid Engineering team"),
        dir=picture("director", "Mr Bala, Director of Pyramid Engineering Private Limited", w=520, h=640),
        ic1=icon("check"), ic2=icon("shield"), ic3=icon("team"), tl=tl, steps=steps, quotes=quotes,
        cl="".join("<li>%s</li>" % x for x in CLIENTS),
        co="".join("<li>%s</li>" % x for x in CONTRACTORS),
        pl="".join("<li>%s</li>" % x for x in PLANTS),
        cta=cta_band("Looking for a contractor who already knows your plant?",
                     "Tell us the facility, the discipline and the window. There is a good chance our crews "
                     "have worked there before.", 0))

    doc = (head("About Us | Pyramid Engineering Pte Ltd, Singapore",
                "Founded 2008. Singapore engineering contractor to refineries, petrochemical plants and power "
                "stations — our history, vision, leadership and client references.",
                "about.html", 0, og_image="power-station")
           + header("about.html", 0) + body + footer(0))
    return write("about.html", doc, 0)


# =========================================================================== SERVICES HUB
def build_services_hub():
    cards = ""
    for i, s in enumerate(SERVICES):
        bullets = "".join("<li>%s</li>" % b for grp in s["capabilities"][:2] for b in grp[1][:2])
        cards += """<article class="card reveal reveal-d{dl}">
  <div class="card__media"><span class="card__idx">{idx}</span>{img}</div>
  <div class="card__body">
    <h3>{t}</h3><p>{p}</p>
    <ul class="card__list">{b}</ul>
    <div class="card__foot"><a class="link-arrow" href="{{B}}services/{s}.html">{t} in detail</a></div>
  </div>
</article>""".format(dl=(i % 3) + 1, idx="%02d" % (i + 1), img=picture(s["img"], s["img_alt"]),
                     t=s["nav"], p=s["short"], b=bullets, s=s["slug"])

    body = page_hero("Services",
                     "Eight engineering disciplines delivered separately or as a single integrated package — "
                     "from a replacement transmitter to a complete turnaround scope.",
                     "p-plant-structure", 0,
                     [("Home", "index.html"), ("Services", "services.html")],
                     "Process plant structure with access scaffolding during a project") + """
<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Capability overview</p>
      <h2>One contractor, eight disciplines</h2>
      <p class="lead">Most plant projects fail at the interfaces &mdash; the day the cable crew waits on the civil
        crew, or the insulation contractor cannot start because the piping punch list is open. Pyramid Engineering
        holds those disciplines in-house, which is why clients ask us to take the whole package.</p>
    </div>
    <div class="grid g-3">{cards}</div>
  </div>
</section>

<section class="section section--dark bp">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">Additional capabilities</p>
        <h2>Support scopes we bundle with the main work</h2>
        <p class="lead">These are rarely bought on their own &mdash; they are what a maintenance or turnaround
          package needs in order to proceed.</p>
        <ul class="checklist">
          <li><strong style="color:#fff">Scaffolding</strong> &mdash; erection, modification and dismantling with
            scaffold design for access and formwork, including manpower supply and material hire or sale, for
            process plant construction and maintenance, building and tunnelling works.</li>
          <li><strong style="color:#fff">Tank cleaning and hydrojetting</strong> &mdash; desludging, hydrojetting,
            full shell cleaning by manual or manless methods, and sludge disposal.</li>
          <li><strong style="color:#fff">Surface preparation and coating</strong> &mdash; blasting, painting,
            GRE wrapping, TFA and galvanising coordinated within project scopes.</li>
          <li><strong style="color:#fff">Non-destructive examination</strong> &mdash; NDE coordination alongside
            fabrication and installation work.</li>
          <li><strong style="color:#fff">Manpower provision</strong> &mdash; skilled personnel supplied to client
            supervision for general works.</li>
        </ul>
      </div>
      <div class="img-duo reveal reveal-d2">
        <figure class="figure">{i1}<figcaption class="figure__tag">Scaffold access</figcaption></figure>
        <figure class="figure">{i2}<figcaption class="figure__tag">Tank cleaning</figcaption></figure>
        <figure class="figure">{i3}<figcaption class="figure__tag">Tank shell works</figcaption></figure>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Procurement notes</p><h2>How our scopes are usually bought</h2></div>
    <div class="table-scroll reveal">
      <table class="data">
        <caption class="visually-hidden">Common contracting models used by Pyramid Engineering clients</caption>
        <thead><tr><th scope="col">Model</th><th scope="col">Typical use</th><th scope="col">What we provide</th></tr></thead>
        <tbody>
          <tr><td><strong>Lump sum project</strong></td><td>Defined scope with drawings and specifications</td>
              <td>Fixed price, method statement, programme, QA/QC documentation and handover pack</td></tr>
          <tr><td><strong>Turnaround / shutdown package</strong></td><td>Fixed window, multi-discipline scope</td>
              <td>Pre-fabrication, mobilised crews, insulation strip-out and reinstatement, punch-list close-out</td></tr>
          <tr><td><strong>Term maintenance contract</strong></td><td>Ongoing plant support over 1&ndash;5 years</td>
              <td>Embedded crews, planned and preventive maintenance, agreed rates and reporting</td></tr>
          <tr><td><strong>Call-out agreement</strong></td><td>Unplanned breakdowns</td>
              <td>Defined response commitment, fault diagnosis and rectification across disciplines</td></tr>
          <tr><td><strong>Manpower supply</strong></td><td>Client-supervised works</td>
              <td>Skilled tradesmen and technicians with the relevant plant and safety certification</td></tr>
          <tr><td><strong>Subcontract to main contractor</strong></td><td>Works packaged under an EPC or main contractor</td>
              <td>Discipline package delivered inside the main contractor's controls and reporting</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>
{cta}""".format(cards=cards,
                i1=picture("p-scaffold-tower", "Scaffold access tower erected against a process column"),
                i2=picture("p-tank-clean-1", "Operatives cleaning the interior of a storage tank"),
                i3=picture("p-tank-shell", "Storage tank shell prepared for cleaning works"),
                cta=cta_band(depth=0))

    doc = (head("Services | Electrical, C&I, Insulation &amp; Civil — Pyramid",
                "Eight engineering disciplines from Pyramid Engineering Singapore: electrical, C&amp;I, fire "
                "&amp; gas, mechanical, insulation, refractory, civil works and plant maintenance.",
                "services.html", 0, og_image="p-plant-structure")
           + header("services.html", 0) + body + footer(0))
    return write("services.html", doc, 0)


# =========================================================================== SERVICE DETAIL
def build_service(s, prev_s, next_s):
    d = 1
    caps = ""
    for i, (grp, items) in enumerate(s["capabilities"]):
        caps += """<article class="fcard reveal reveal-d{dl}">
  <div class="ico">{ic}</div><h3>{g}</h3>
  <ul class="card__list" style="margin-bottom:0;margin-top:14px">{li}</ul>
</article>""".format(dl=(i % 2) + 1, ic=icon(SERVICE_ICON.get(s["slug"], "check")), g=grp,
                     li="".join("<li>%s</li>" % x for x in items))

    gal = "".join('<figure class="figure reveal reveal-d{dl}">{img}<figcaption class="figure__tag">{c}</figcaption></figure>'
                  .format(dl=(i % 3) + 1, img=picture(n, c), c=c) for i, (n, c) in enumerate(s["gallery"]))

    outcomes = "".join("""<article class="fcard reveal reveal-d{dl}"><div class="ico">{ic}</div>
      <h3>{t}</h3><p>{p}</p></article>""".format(dl=(i % 3) + 1, ic=icon("check"), t=t, p=p)
                       for i, (t, p) in enumerate(s["outcomes"]))

    others = "".join('<li><a href="{B}services/%s.html">%s</a></li>' % (o["slug"], o["nav"])
                     for o in SERVICES if o["slug"] != s["slug"])

    schema = {"@context": "https://schema.org", "@type": "Service",
              "serviceType": s["title"], "name": s["title"] + " — Pyramid Engineering",
              "description": strip_tags(s["short"]),
              "provider": {"@id": C["website"] + "/#organisation"},
              "areaServed": {"@type": "Country", "name": "Singapore"},
              "hasOfferCatalog": {"@type": "OfferCatalog", "name": s["title"] + " capabilities",
                                  "itemListElement": [
                                      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": strip_tags(x)}}
                                      for grp in s["capabilities"] for x in grp[1]]}}

    body = page_hero(s["title"], strip_tags(s["short"]), s["img"], d,
                     [("Home", "index.html"), ("Services", "services.html"), (s["nav"], "")],
                     s["img_alt"]) + """
<section class="section">
  <div class="wrap">
    <div class="split split--wide-left" style="align-items:start">
      <div class="reveal">
        <p class="eyebrow">Overview</p>
        <h2>{nav} at Pyramid</h2>
        <p class="lead">{intro}</p>
        <h3 style="margin-top:34px">Where this scope is applied</h3>
        <ul class="checklist">{apps}</ul>
      </div>
      <aside class="reveal reveal-d2">
        <div class="fcard" style="border-color:var(--blue-300)">
          <p class="eyebrow">Enquire</p>
          <h3>Request a proposal for {nav}</h3>
          <p>Send drawings, a specification or a scope description and we will respond with clarifications
             and a costed proposal.</p>
          <div class="btn-row" style="margin-top:20px;flex-direction:column">
            <a class="btn btn--red" href="{{B}}contact.html?service={slug}" style="width:100%">Request a Quotation</a>
            <a class="btn btn--ghost" href="tel:{tel}" style="width:100%">Call {phone}</a>
            <a class="btn btn--ghost" href="https://wa.me/{wa}" rel="noopener" style="width:100%">WhatsApp us</a>
          </div>
        </div>
        <div class="fcard" style="margin-top:20px">
          <p class="eyebrow">Standards &amp; codes</p>
          <ul class="card__list" style="margin-bottom:0">{std}</ul>
        </div>
      </aside>
    </div>
  </div>
</section>

<section class="section section--paper2">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Scope of work</p><h2>What we deliver</h2></div>
    <div class="grid g-2">{caps}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">On site</p><h2>{nav} in the field</h2></div>
    <div class="grid g-3">{gal}</div>
  </div>
</section>

<section class="section section--dark bp">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Why it matters</p><h2>What you get from this scope</h2></div>
    <div class="grid g-3">{out}</div>
  </div>
</section>

<section class="section section--paper2">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">Related capability</p>
        <h2>Often packaged with</h2>
        <p>Clients rarely buy a single discipline. Combining scopes under one contractor removes the interface
          delays that cost most plant projects their schedule.</p>
        <ul class="card__list" style="columns:2;column-gap:30px">{others}</ul>
        <div class="btn-row" style="margin-top:24px">
          <a class="btn btn--ghost" href="{{B}}services.html">All services</a>
          <a class="btn btn--ghost" href="{{B}}projects.html">Project portfolio</a>
        </div>
      </div>
      <div class="reveal reveal-d2">
        <div class="acc">
          <details open><summary>Do you work in live, operating plant?</summary>
            <div class="acc__body"><p>Yes. The majority of our {nav} work is executed inside running facilities
            under client permit-to-work, isolation and hazardous-area procedures. We hold bizSAFE STAR and are
            certified to ISO 45001:2018.</p></div></details>
          <details><summary>Can you supply materials as well as install?</summary>
            <div class="acc__body"><p>We do, and clients frequently ask us to, so that supply and installation sit
            with a single accountable party rather than being split across two purchase orders.</p></div></details>
          <details><summary>Will we get documentation at handover?</summary>
            <div class="acc__body"><p>Test records, calibration or inspection certificates, as-built marking and
            punch-list close-out are produced as the work proceeds and issued as a handover pack.</p></div></details>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="btn-row" style="justify-content:space-between">
      <a class="link-arrow" href="{{B}}services/{prev_s}.html" style="flex-direction:row-reverse">Previous: {prev_t}</a>
      <a class="link-arrow" href="{{B}}services/{next_s}.html">Next: {next_t}</a>
    </div>
  </div>
</section>
{cta}""".format(t=s["title"], nav=s["nav"], intro=s["intro"], slug=s["slug"],
                apps="".join("<li>%s</li>" % x for x in s["applications"]),
                std="".join("<li>%s</li>" % x for x in s["standards"]),
                caps=caps, gal=gal, out=outcomes, others=others,
                tel=C["phone_tel"], phone=C["phone_display"], wa=C["whatsapp"],
                prev_s=prev_s["slug"], prev_t=prev_s["nav"], next_s=next_s["slug"], next_t=next_s["nav"],
                cta=cta_band("Need %s on your plant?" % s["nav"].lower(),
                             "Tell us the facility, the scope and the window. We will come back with "
                             "clarifications and a proposal.", d))

    doc = (head("%s Singapore | Pyramid Engineering" % s.get("seo_title", s["title"]), s["meta"],
                "services/%s.html" % s["slug"], d, extra_schema=schema, og_image=s["img"])
           + header("services.html", d) + body + footer(d))
    return write("services/%s.html" % s["slug"], doc, d)


# =========================================================================== SECTORS
def build_sectors():
    blocks = ""
    for i, s in enumerate(SECTORS):
        flip = (i % 2 == 1)
        media = '<figure class="figure figure--framed reveal reveal-d2">%s</figure>' % picture(
            s["img"], "%s work by Pyramid Engineering" % s["name"])
        text = """<div class="reveal">
  <p class="eyebrow">{n:02d} &nbsp;/&nbsp; Sector</p>
  <h2 style="font-size:clamp(1.5rem,1.15rem + 1.3vw,2.1rem)">{name}</h2>
  <p class="lead">{short}</p>
  <h3 style="font-size:1.02rem;margin-top:26px">Typical scope of work</h3>
  <ul class="checklist">{scope}</ul>
  <h3 style="font-size:1.02rem;margin-top:26px">Relevant standards &amp; codes</h3>
  <p style="margin-bottom:18px">{std}</p>
  <h3 style="font-size:1.02rem">Sample projects &amp; plants</h3>
  <ul class="card__list">{cl}</ul>
  <a class="link-arrow" href="{{B}}projects.html?sector={slug}">See {name} projects</a>
</div>""".format(n=i + 1, name=s["name"], short=s["short"], slug=s["slug"],
                 scope="".join("<li>%s</li>" % x for x in s["scope"]),
                 std="".join('<span class="chip" style="margin-right:6px">%s</span>' % x for x in s["standards"]),
                 cl="".join("<li>%s</li>" % x for x in s["clients"]))
        inner = (media + text) if flip else (text + media)
        blocks += """<section class="section{bg}" id="{slug}">
  <div class="wrap"><div class="split">{inner}</div></div>
</section>""".format(bg=" section--paper2" if i % 2 else "", slug=s["slug"], inner=inner)

    jump = "".join('<a class="btn btn--ghost btn--sm" href="#%s">%s</a>' % (s["slug"], s["name"]) for s in SECTORS)

    body = page_hero("Sectors We Serve",
                     "Procurement teams shortlist on sector relevance. Here is precisely where our crews work, "
                     "what we deliver there, and which plants we have already been inside.",
                     "refinery-wide", 0,
                     [("Home", "index.html"), ("Sectors", "sectors.html")],
                     "Industrial refinery skyline with stacks and process units") + """
<section class="section section--tight">
  <div class="wrap">
    <div class="btn-row reveal">{jump}</div>
  </div>
</section>
""".format(jump=jump) + blocks + """
<section class="section section--dark bp">
  <div class="wrap">
    <div class="sec-head sec-head--center reveal">
      <p class="eyebrow">Safety compliance framework</p>
      <h2>The same framework applies in every sector</h2>
      <p>Sector-specific standards sit on top of a common safety and quality baseline.</p>
    </div>
    <div class="grid g-4">
      <article class="fcard reveal"><div class="ico">{i1}</div><h3>ISO 45001:2018</h3>
        <p>Certified occupational health and safety management system covering process and industrial plant works.</p></article>
      <article class="fcard reveal reveal-d1"><div class="ico">{i2}</div><h3>bizSAFE STAR</h3>
        <p>The highest tier of Singapore's WSH Council bizSAFE programme, valid to February 2027.</p></article>
      <article class="fcard reveal reveal-d2"><div class="ico">{i3}</div><h3>Permit-to-work</h3>
        <p>Crews trained and experienced in client permit, isolation, lock-out and confined-space systems.</p></article>
      <article class="fcard reveal reveal-d3"><div class="ico">{i4}</div><h3>Risk management</h3>
        <p>Risk assessments, method statements and toolbox briefings completed before mobilisation.</p></article>
    </div>
  </div>
</section>
{cta}""".format(i1=icon("shield"), i2=icon("check"), i3=icon("file"), i4=icon("team"),
                cta=cta_band("Working in a sector we have not listed?",
                             "Our certified scope covers process and industrial plant consultancy, engineering, "
                             "construction and maintenance. Tell us about the facility.", 0))

    doc = (head("Sectors We Serve | Refinery, Petrochemical &amp; Power — Pyramid",
                "Refineries, petrochemical, power generation, solar, pharmaceutical, manufacturing and storage "
                "terminals — sector scope, standards and reference plants for each.",
                "sectors.html", 0, og_image="refinery-wide")
           + header("sectors.html", 0) + body + footer(0))
    return write("sectors.html", doc, 0)


# =========================================================================== PROJECTS
def build_projects():
    keys = []
    for _, _, sk, _, _ in PROJECTS:
        for k in sk.split():
            if k not in keys:
                keys.append(k)
    order = ["refineries", "petrochemical", "power", "renewables", "pharmaceutical", "manufacturing", "storage"]
    keys = [k for k in order if k in keys]

    fbtns = '<button type="button" data-filter="all" aria-pressed="true">All projects</button>'
    fbtns += "".join('<button type="button" data-filter="%s" aria-pressed="false">%s</button>'
                     % (k, SECTOR_LABELS[k]) for k in keys)

    cards = "".join("""<article class="proj reveal" data-sector="{sk}">
  <p class="proj__sector">{sec}</p>
  <h3>{n}</h3>
  <p class="proj__meta">{cl}</p>
  <p class="proj__scope">{sc}</p>
  <div class="proj__chips"><span class="chip">{per}</span></div>
</article>""".format(sk=sk, sec=" &middot; ".join(SECTOR_LABELS[k] for k in sk.split()),
                     n=n, cl=cl, sc=sc, per=per) for n, cl, sk, per, sc in PROJECTS)

    schema = {"@context": "https://schema.org", "@type": "ItemList",
              "name": "Pyramid Engineering project portfolio",
              "numberOfItems": len(PROJECTS),
              "itemListElement": [{"@type": "ListItem", "position": i + 1,
                                   "name": strip_tags(p[0]) + " — " + strip_tags(p[1])}
                                  for i, p in enumerate(PROJECTS)]}

    body = page_hero("Project Portfolio",
                     "%d documented projects across refineries, petrochemical plants, power stations, solar, "
                     "pharmaceutical and manufacturing facilities in Singapore since %d."
                     % (len(PROJECTS), C["founded"]),
                     "p-spools", 0,
                     [("Home", "index.html"), ("Projects", "projects.html")],
                     "Prefabricated pipe spools staged for site installation") + """
<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Filterable register</p>
      <h2>Every project, by sector</h2>
      <p>Filter by sector to see the work most relevant to your facility. Showing
        <strong data-result-count>{n}</strong> of {n} projects.</p>
    </div>
    <div class="filters reveal" data-filters role="group" aria-label="Filter projects by sector">{f}</div>
    <div class="proj-grid">{cards}</div>
    <p class="no-results" data-no-results hidden>No projects match that filter.</p>
  </div>
</section>

<section class="section section--paper2">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">What a project record contains</p>
      <h2>Detailed references available on request</h2>
      <p>For pre-qualification we can provide fuller records for any project listed above.</p>
    </div>
    <div class="grid g-3">
      <article class="fcard reveal"><div class="ico">{i1}</div><h3>Scope &amp; deliverables</h3>
        <p>Discipline breakdown, equipment and systems handled, and the deliverables issued &mdash; drawings,
          test reports and commissioning documents.</p></article>
      <article class="fcard reveal reveal-d1"><div class="ico">{i2}</div><h3>Schedule performance</h3>
        <p>Planned versus actual duration, mobilisation profile and how the work sat against the client's
          shutdown or project programme.</p></article>
      <article class="fcard reveal reveal-d2"><div class="ico">{i3}</div><h3>Safety &amp; standards</h3>
        <p>Safety performance on the job, the technical standards applied, and the client permit regime the
          work was executed under.</p></article>
    </div>
    <div class="btn-row" style="margin-top:34px">
      <a class="btn btn--primary" href="{{B}}contact.html">Request project references</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Plants worked in</p><h2>Facilities our crews have entered</h2></div>
    <div class="logo-band reveal">{plants}</div>
  </div>
</section>
{cta}""".format(n=len(PROJECTS), f=fbtns, cards=cards, i1=icon("file"), i2=icon("clock"), i3=icon("shield"),
                plants="".join("<span>%s</span>" % p for p in PLANTS),
                cta=cta_band("Want to be the next entry on this list?",
                             "Send us your scope and we will tell you honestly whether it is work we should "
                             "be bidding for.", 0))

    doc = (head("Project Portfolio | 52 Plant Projects — Pyramid Engineering",
                "52 documented projects since 2008 — Shell Pulau Bukom, ExxonMobil, Chevron Ornite, Senoko, "
                "Tuas, Keppel Merlimau, REC Solar, Pfizer and Murata. Filter by sector.",
                "projects.html", 0, extra_schema=schema, og_image="p-spools")
           + header("projects.html", 0) + body + footer(0))
    return write("projects.html", doc, 0)


# =========================================================================== CERTIFICATIONS
def build_certifications():
    cards = "".join("""<article class="cert-card reveal reveal-d{dl}">
  <div class="cert-card__img">{img}</div>
  <div class="cert-card__body"><h3>{t}</h3><p>{b}</p></div>
</article>""".format(dl=(i % 3) + 1, img=picture(c["img"], c["title"] + " certificate"), t=c["title"], b=c["body"])
        for i, c in enumerate(CERTIFICATIONS))

    body = page_hero("Certifications &amp; Compliance",
                     "Current certificate numbers, issue dates and validity — published so that pre-qualification "
                     "does not have to start with a request for documents.",
                     "p-commissioning", 0,
                     [("Home", "index.html"), ("Certifications", "certifications.html")],
                     "Engineers performing verification work in a process plant") + """
<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Management systems</p>
      <h2>Certified, current and independently audited</h2>
      <p class="lead">Our quality and occupational health and safety management systems are certified to a scope
        written specifically for our work: process and industrial plant consultancy, engineering, construction
        and maintenance works for chemical, refineries and petrochemical industries.</p>
    </div>
    <div class="grid g-3">{cards}</div>
    <div class="note-box reveal" style="margin-top:36px">
      <strong>Verifying these certificates.</strong> Certificate copies in PDF, the current BCA registration
      and any additional pre-qualification documents are available on request &mdash;
      email <a href="mailto:{mail}">{mail}</a> or use the enquiry form and we will send them the same working day.
    </div>
    <div class="btn-row reveal" style="margin-top:26px">
      <a class="btn btn--primary" href="{{B}}assets/downloads/pyramid-engineering-capability-statement.pdf" download>
        Download Capability Statement (PDF)</a>
      <a class="btn btn--ghost" href="{{B}}contact.html">Request certificate copies</a>
    </div>
  </div>
</section>

<section class="section section--paper2">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">At a glance</p><h2>Certification register</h2></div>
    <div class="table-scroll reveal">
      <table class="data">
        <caption class="visually-hidden">Pyramid Engineering certifications with numbers and validity dates</caption>
        <thead><tr><th scope="col">Certification</th><th scope="col">Reference</th>
          <th scope="col">Issued</th><th scope="col">Valid to</th><th scope="col">Issuing body</th></tr></thead>
        <tbody>
          <tr><td><strong>ISO 9001:2015</strong><br><span style="color:var(--ink-3);font-size:.86rem">Quality management</span></td>
              <td>24EQMV39</td><td>26 Feb 2024</td><td>25 Feb 2027</td><td>EGAC / IAF accredited</td></tr>
          <tr><td><strong>ISO 45001:2018</strong><br><span style="color:var(--ink-3);font-size:.86rem">OH&amp;S management</span></td>
              <td>24EOMV46</td><td>27 Feb 2024</td><td>26 Feb 2027</td><td>EGAC / IAF accredited</td></tr>
          <tr><td><strong>bizSAFE STAR</strong><br><span style="color:var(--ink-3);font-size:.86rem">Highest bizSAFE tier</span></td>
              <td>&mdash;</td><td>14 Mar 2024</td><td>26 Feb 2027</td><td>WSH Council, Singapore</td></tr>
          <tr><td><strong>ASPRI Corporate Member</strong><br><span style="color:var(--ink-3);font-size:.86rem">Association of Process Industry</span></td>
              <td>C0656/2011</td><td>1 Jun 2011</td><td>Current</td><td>ASPRI</td></tr>
          <tr><td><strong>Singapore Welding Society</strong><br><span style="color:var(--ink-3);font-size:.86rem">Corporate member</span></td>
              <td>&mdash;</td><td>1 Jun 2011</td><td>Current</td><td>Singapore Welding Society</td></tr>
          <tr><td><strong>BCA Registration</strong><br><span style="color:var(--ink-3);font-size:.86rem">Building &amp; Construction Authority</span></td>
              <td>On request</td><td>&mdash;</td><td>Current</td><td>BCA, Singapore</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <p class="eyebrow">Safety in practice</p>
        <h2>What certification means on your site</h2>
        <p class="lead">A certificate on a wall is not a safety record. These are the practices the certificates
          describe, applied on every job.</p>
        <ul class="checklist">
          <li>Risk assessment and method statement completed and approved before mobilisation</li>
          <li>Work executed under the client's permit-to-work and isolation procedures</li>
          <li>Toolbox briefings at the start of every shift, in the languages the crew speaks</li>
          <li>Hazardous-area and confined-space requirements applied as a matter of routine</li>
          <li>Equipment issued to site checked, certified and maintained in safe working condition</li>
          <li>Incident reporting and corrective action tracked through the management system</li>
        </ul>
      </div>
      <div class="reveal reveal-d2">
        <div class="fcard">
          <p class="eyebrow">Company particulars</p>
          <h3>For your vendor registration</h3>
          <ul class="card__list" style="margin-bottom:0">
            <li><strong>Registered name</strong><br>{cn}</li>
            <li><strong>Business registration (UEN)</strong><br>{uen}</li>
            <li><strong>Year established</strong><br>{founded}</li>
            <li><strong>Registered address</strong><br>{addr}</li>
            <li><strong>Telephone</strong><br>{phone}</li>
            <li><strong>Email</strong><br>{mail} &middot; {admin}</li>
            <li><strong>Website</strong><br>{domain}</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>
{cta}""".format(cards=cards, mail=C["email"], admin=C["email_admin"], cn=C["name"], uen=C["uen"],
                founded=C["founded"], addr=C["address_full"], phone=C["phone_display"], domain=C["domain"],
                cta=cta_band("Need our documents for pre-qualification?",
                             "Certificates, insurance details, safety records and reference letters can be "
                             "issued the same working day.", 0))

    doc = (head("Certifications | ISO 9001, ISO 45001, bizSAFE STAR — Pyramid",
                "Certificate numbers and validity dates: ISO 9001:2015, ISO 45001:2018, bizSAFE STAR, ASPRI "
                "and Singapore Welding Society corporate membership.",
                "certifications.html", 0, og_image="p-commissioning")
           + header("certifications.html", 0) + body + footer(0))
    return write("certifications.html", doc, 0)


# =========================================================================== CONTACT
def build_contact():
    svc_opts = "".join('<option value="%s">%s</option>' % (s["nav"], s["nav"]) for s in SERVICES)
    sec_opts = "".join('<option value="%s">%s</option>' % (s["name"], s["name"]) for s in SECTORS)
    hours = "".join('<li><span style="display:block;color:var(--ink-3);font-size:.82rem">%s</span>'
                    '<strong style="font-weight:600;color:var(--ink)">%s</strong></li>' % (a, b)
                    for a, b in C["hours"])

    schema = {"@context": "https://schema.org", "@type": "ContactPage",
              "name": "Contact Pyramid Engineering",
              "mainEntity": {"@id": C["website"] + "/#organisation"}}

    body = page_hero("Contact Us",
                     "Send a scope, a drawing or a shutdown date. We reply with clarifications and a proposal — "
                     "usually within one working day.",
                     "consult", 0,
                     [("Home", "index.html"), ("Contact", "contact.html")],
                     "Client consultation meeting about a plant engineering project") + """
<section class="section">
  <div class="wrap">
    <div class="split split--wide-left" style="align-items:start">
      <div class="reveal">
        <p class="eyebrow">Request for quotation</p>
        <h2>Tell us about the work</h2>
        <p class="lead">The more you tell us up front &mdash; plant, discipline, window, permit requirements
          &mdash; the more useful our first reply will be.</p>

        <form class="form" data-enquiry-form novalidate style="margin-top:30px">
          <div class="row2">
            <div class="field"><label for="name">Your name <span class="req" aria-hidden="true">*</span></label>
              <input type="text" id="name" name="name" autocomplete="name" required></div>
            <div class="field"><label for="company">Company <span class="req" aria-hidden="true">*</span></label>
              <input type="text" id="company" name="company" autocomplete="organization" required></div>
          </div>
          <div class="row2">
            <div class="field"><label for="email">Email <span class="req" aria-hidden="true">*</span></label>
              <input type="email" id="email" name="email" autocomplete="email" required></div>
            <div class="field"><label for="phone">Telephone</label>
              <input type="tel" id="phone" name="phone" autocomplete="tel"></div>
          </div>
          <div class="row2">
            <div class="field"><label for="service">Service required</label>
              <select id="service" name="service">
                <option value="">Select a service&hellip;</option>{svc}
                <option value="Multiple / not sure">Multiple disciplines or not sure</option>
              </select></div>
            <div class="field"><label for="sector">Sector</label>
              <select id="sector" name="sector">
                <option value="">Select a sector&hellip;</option>{sec}
                <option value="Other">Other</option>
              </select></div>
          </div>
          <div class="field"><label for="location">Plant or site location</label>
            <input type="text" id="location" name="location" placeholder="e.g. Jurong Island, Tuas, Pulau Bukom">
            <p class="hint">Helpful for assessing access, permits and mobilisation.</p></div>
          <div class="field"><label for="message">Scope of work <span class="req" aria-hidden="true">*</span></label>
            <textarea id="message" name="message" required
              placeholder="Describe the work, the equipment or systems involved, and your target window or shutdown dates."></textarea></div>
          <div class="field"><label for="drawings">Drawings or specifications (optional)</label>
            <input type="file" id="drawings" name="drawings" multiple
                   accept=".pdf,.dwg,.doc,.docx,.xls,.xlsx,.zip,.jpg,.png">
            <p class="hint">If your browser cannot attach files here, email them to
              <a href="mailto:{mail}">{mail}</a> quoting your company name.</p></div>
          <div class="hp" aria-hidden="true"><label for="website_url">Leave this field empty</label>
            <input type="text" id="website_url" name="website_url" tabindex="-1" autocomplete="off"></div>
          <label class="check"><input type="checkbox" name="consent" required>
            <span>I consent to Pyramid Engineering using the details above to respond to this enquiry, in
            accordance with the <a href="{{B}}privacy-policy.html">Privacy Policy</a>.
            <span class="req" aria-hidden="true">*</span></span></label>
          <div>
            <button class="btn btn--red" type="submit">Send Enquiry</button>
          </div>
          <p class="form-note" data-form-status role="status" hidden></p>
          <p class="form-note">Fields marked <span class="req">*</span> are required. We use your details only to
            respond to this enquiry and never share them with third parties.</p>
        </form>
      </div>

      <aside class="reveal reveal-d2">
        <div class="fcard">
          <p class="eyebrow">Direct contact</p>
          <dl class="contact-list" style="margin-top:8px">
            <li><span class="ico">{i_pin}</span><div><dt>Office</dt>
              <dd>{addr1}<br>{addr2}<br>{addr3}</dd></div></li>
            <li><span class="ico">{i_phone}</span><div><dt>Telephone</dt>
              <dd><a href="tel:{tel}">{phone}</a></dd></div></li>
            <li><span class="ico">{i_mail}</span><div><dt>Enquiries</dt>
              <dd><a href="mailto:{mail}">{mail}</a></dd></div></li>
            <li><span class="ico">{i_mail}</span><div><dt>Administration</dt>
              <dd><a href="mailto:{admin}">{admin}</a></dd></div></li>
          </dl>
          <div class="btn-row" style="margin-top:24px;flex-direction:column">
            <a class="btn btn--primary" href="https://wa.me/{wa}?text=Hello%20Pyramid%20Engineering%2C%20I%20would%20like%20to%20enquire%20about%20"
               rel="noopener" style="width:100%">Message us on WhatsApp</a>
            <a class="btn btn--ghost" href="tel:{tel}" style="width:100%">Tap to call</a>
          </div>
        </div>

        <div class="fcard" style="margin-top:20px">
          <p class="eyebrow">Business hours</p>
          <ul class="card__list" style="margin-bottom:0">{hours}</ul>
        </div>

        <div class="fcard" style="margin-top:20px">
          <p class="eyebrow">Company particulars</p>
          <ul class="card__list" style="margin-bottom:0">
            <li><strong>{cn}</strong></li>
            <li>UEN {uen}</li>
            <li>Established {founded}</li>
            <li>ISO 9001:2015 &middot; ISO 45001:2018 &middot; bizSAFE STAR</li>
          </ul>
        </div>
      </aside>
    </div>
  </div>
</section>

<section class="section section--tight section--paper2">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Find us</p><h2>10 Buroh Street, West Connect Building</h2>
      <p>Located in the Jurong industrial district, minutes from Jurong Island access and the western
        process plant cluster.</p></div>
    <div class="map-embed reveal">
      <iframe title="Map showing Pyramid Engineering at 10 Buroh Street, West Connect Building, Singapore"
        src="https://www.google.com/maps?q=10+Buroh+Street+West+Connect+Building+Singapore&output=embed"
        loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
    </div>
  </div>
</section>
{cta}""".format(svc=svc_opts, sec=sec_opts, hours=hours, mail=C["email"], admin=C["email_admin"],
                addr1=C["address_line1"], addr2=C["address_line2"], addr3=C["address_city"],
                tel=C["phone_tel"], phone=C["phone_display"], wa=C["whatsapp"], cn=C["name"],
                uen=C["uen"], founded=C["founded"],
                i_pin=icon("pin"), i_phone=icon("phone"), i_mail=icon("mail"),
                cta=cta_band("Urgent breakdown or shutdown support?",
                             "Call the office directly. For clients under a call-out or term maintenance "
                             "agreement, response commitments are defined in your contract.", 0))

    doc = (head("Contact Us | Request a Quotation — Pyramid Engineering",
                "10 Buroh Street, West Connect Building #07-34, Singapore. Tel +65 6259 9046 or "
                "enquiry@pyramid-groups.com. Send us your scope and we will reply with a proposal.",
                "contact.html", 0, extra_schema=schema, og_image="consult")
           + header("contact.html", 0) + body + footer(0))
    return write("contact.html", doc, 0)


# =========================================================================== LEGAL + 404
LEGAL_CONTENT = {
"privacy-policy": ("Privacy Policy",
 "How Pyramid Engineering Private Limited collects, uses, retains and protects personal data, in accordance with the Singapore Personal Data Protection Act 2012.",
 """
<h2>1. About this policy</h2>
<p>Pyramid Engineering Private Limited (UEN {uen}) (&ldquo;PEPL&rdquo;, &ldquo;we&rdquo;, &ldquo;us&rdquo;) is committed to
protecting the personal data of visitors to this website and of the individuals we deal with in the course of
business. This policy explains what we collect, why we collect it, and what rights you have. It is written to
comply with the Singapore Personal Data Protection Act 2012 (PDPA).</p>

<h2>2. What we collect</h2>
<ul>
  <li><strong>Enquiry details</strong> &mdash; the name, company, email address, telephone number, site location
      and scope description you submit through our enquiry form or by email.</li>
  <li><strong>Attachments</strong> &mdash; drawings, specifications and other documents you choose to send us.</li>
  <li><strong>Technical data</strong> &mdash; where analytics are enabled, aggregated information such as pages
      visited, approximate location, browser and device type. This is not used to identify you personally.</li>
</ul>
<p>We do not collect sensitive personal data through this website and ask that you do not send it to us.</p>

<h2>3. Why we use it</h2>
<ul>
  <li>To respond to your enquiry and prepare a quotation or proposal</li>
  <li>To carry out and administer contracted works, including site access and vendor registration</li>
  <li>To maintain business records as required by Singapore law</li>
  <li>To improve the content and performance of this website</li>
</ul>
<p>We do not use your details for unsolicited marketing, and we do not sell personal data to any third party.</p>

<h2>4. Disclosure</h2>
<p>Personal data may be disclosed to our employees and authorised representatives who need it to respond to you,
and to third parties where required to deliver a contracted service (for example a main contractor administering
site access) or where required by law, regulation or a competent authority.</p>

<h2>5. Retention</h2>
<p>We keep enquiry records for as long as necessary to respond and to satisfy legal, accounting and contractual
record-keeping requirements, after which they are securely deleted or anonymised.</p>

<h2>6. Security</h2>
<p>We apply reasonable administrative, physical and technical measures to protect personal data against
unauthorised access, use or disclosure. No transmission over the internet can be guaranteed to be completely
secure, and you send information to us at your own risk.</p>

<h2>7. Your rights</h2>
<p>Under the PDPA you may request access to the personal data we hold about you, request correction of
inaccurate data, and withdraw consent for its use. Requests should be sent to
<a href="mailto:{admin}">{admin}</a>. We will respond within a reasonable time. Withdrawing consent may prevent
us from continuing to provide a service to you.</p>

<h2>8. Third-party links</h2>
<p>This website may link to third-party websites and embeds a Google Maps frame on the contact page. We are not
responsible for the privacy practices of those third parties and encourage you to read their policies.</p>

<h2>9. Changes</h2>
<p>We may update this policy from time to time. The version published on this page is the current one.</p>

<h2>10. Contact</h2>
<p>Questions about this policy or about personal data held by PEPL should be addressed to our Data Protection
contact at <a href="mailto:{admin}">{admin}</a>, or by post to {addr}.</p>"""),

"terms-and-conditions": ("Terms and Conditions",
 "Terms and conditions governing use of the Pyramid Engineering Private Limited website, including intellectual property, quotations and limitation of liability.",
 """
<h2>1. Acceptance</h2>
<p>By accessing or using this website you agree to these terms. If you do not agree, please do not use the site.</p>

<h2>2. Use of the website</h2>
<p>This website is provided for general information about Pyramid Engineering Private Limited and its services.
You may view, download and print content for your own internal, non-commercial evaluation of our services. You
may not reproduce, republish or distribute content for commercial purposes without our written permission.</p>

<h2>3. Intellectual property</h2>
<p>All content on this website &mdash; text, photographs, graphics, logos, layout and code &mdash; is owned by or
licensed to Pyramid Engineering Private Limited and is protected by copyright and other intellectual property
laws. The Pyramid name and logo are our trade marks and may not be used without written consent.</p>

<h2>4. Enquiries and quotations</h2>
<p>Nothing on this website constitutes an offer capable of acceptance. Descriptions of services are indicative.
Any quotation issued by us is subject to our written terms of trade, the specific scope agreed, site conditions,
and any main contractor or client requirements applicable to the work.</p>

<h2>5. Accuracy of information</h2>
<p>We take care to ensure information on this site is accurate at the time of publication. Standards, codes,
certificate validity and project details change. Where a matter is material to a decision you are making, please
contact us to confirm the current position in writing.</p>

<h2>6. Limitation of liability</h2>
<p>To the fullest extent permitted by law, Pyramid Engineering Private Limited excludes liability for any loss or
damage arising from use of, or reliance on, this website, including indirect or consequential loss. Nothing in
these terms excludes liability that cannot lawfully be excluded.</p>

<h2>7. Third-party content</h2>
<p>Links and embedded content from third parties are provided for convenience. We do not endorse and are not
responsible for third-party content.</p>

<h2>8. Governing law</h2>
<p>These terms are governed by the laws of the Republic of Singapore, and the courts of Singapore have exclusive
jurisdiction over any dispute arising from them.</p>

<h2>9. Contact</h2>
<p>Questions about these terms may be sent to <a href="mailto:{admin}">{admin}</a> or by post to {addr}.</p>"""),

"cookie-policy": ("Cookie Policy",
 "How the Pyramid Engineering website uses cookies and similar technologies, what each type does, and how to manage or block them in your browser.",
 """
<h2>1. What cookies are</h2>
<p>Cookies are small text files placed on your device by a website. They are widely used to make websites work,
to remember preferences, and to provide information to site owners about how a site is used.</p>

<h2>2. Cookies on this website</h2>
<p>This website is built as a static site and does not set advertising or profiling cookies. The cookies and
similar technologies that may be present are:</p>
<div class="table-scroll" style="margin:20px 0">
  <table class="data">
    <thead><tr><th scope="col">Type</th><th scope="col">Purpose</th><th scope="col">Set by</th></tr></thead>
    <tbody>
      <tr><td><strong>Strictly necessary</strong></td><td>Enable core page functions and security</td><td>This website / your hosting provider</td></tr>
      <tr><td><strong>Analytics</strong></td><td>Aggregated statistics on pages viewed and traffic sources, where analytics is enabled</td><td>Google Analytics (if activated)</td></tr>
      <tr><td><strong>Map embed</strong></td><td>Displays the office location map on the contact page</td><td>Google Maps</td></tr>
    </tbody>
  </table>
</div>

<h2>3. Managing cookies</h2>
<p>You can control and delete cookies through your browser settings. Most browsers let you block all cookies,
block third-party cookies, or delete cookies when you close the browser. Blocking cookies may affect the map
embed on the contact page but will not prevent you from using the rest of the site.</p>

<h2>4. Third-party services</h2>
<p>Where Google Analytics or Google Maps are used, those services are governed by Google's own privacy and
cookie policies. We recommend reviewing them directly.</p>

<h2>5. Changes and contact</h2>
<p>We may update this policy as the site changes. Questions may be sent to
<a href="mailto:{admin}">{admin}</a>.</p>"""),

"disclaimer": ("Disclaimer",
 "Important notices on the information published by Pyramid Engineering — general information only, not engineering advice or a project-specific assessment.",
 """
<h2>1. General information only</h2>
<p>The content of this website is published for general information about Pyramid Engineering Private Limited and
its capabilities. It does not constitute engineering advice, a technical recommendation, or a professional opinion
on any specific installation, system or plant.</p>

<h2>2. No engineering advice</h2>
<p>Descriptions of standards, codes, methods and scopes of work are indicative and are not a substitute for a
project-specific engineering assessment. No design, installation, maintenance or safety decision should be taken
on the basis of this website alone. Engage us, or another suitably qualified party, to assess your specific
circumstances.</p>

<h2>3. Standards and codes</h2>
<p>References to standards and codes indicate the frameworks we commonly work to. The applicable revision and the
governing specification for any particular job are established contractually and may differ from those listed here.</p>

<h2>4. Project and client information</h2>
<p>Project entries, client names and testimonials are published to describe the type and scale of work undertaken.
They do not imply any endorsement by the named organisations beyond the references supplied to us, nor any current
contractual relationship unless stated.</p>

<h2>5. Certificates and validity</h2>
<p>Certificate numbers and validity dates are published as at the date of the most recent site update.
Certificates are subject to surveillance audit and renewal. Please request current copies for pre-qualification
rather than relying on this page.</p>

<h2>6. Images</h2>
<p>Photographs include images of works executed by Pyramid Engineering as well as representative industry imagery.
Images are illustrative of capability and do not depict any particular contract unless captioned as such.</p>

<h2>7. External links</h2>
<p>We are not responsible for the content, accuracy or availability of external websites linked from this site.</p>

<h2>8. Contact</h2>
<p>To confirm any information on this website in writing, contact <a href="mailto:{mail}">{mail}</a> or
call {phone}.</p>"""),
}


def build_legal():
    out = []
    for slug, (title, desc, content) in LEGAL_CONTENT.items():
        body = page_hero(title, desc, "p-plant-structure", 0,
                         [("Home", "index.html"), (title, "")], "Industrial plant structure") + """
<section class="section">
  <div class="wrap wrap-narrow prose reveal">
    <p style="font-family:var(--font-mono);font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3)">
      Last updated: August 2026</p>
    {c}
  </div>
</section>
""".format(c=content.format(uen=C["uen"], admin=C["email_admin"], mail=C["email"],
                            addr=C["address_full"], phone=C["phone_display"]))
        doc = (head("%s | %s" % (title, C["short"]), desc, "%s.html" % slug, 0)
               + header("", 0) + body + footer(0))
        out.append(write("%s.html" % slug, doc, 0))
    return out


def build_404():
    body = """
<section class="section" style="padding:clamp(70px,9vw,140px) 0;text-align:center">
  <div class="wrap wrap-narrow">
    <p class="eyebrow" style="justify-content:center;display:flex">Error 404</p>
    <h1>That page is not on site</h1>
    <p class="lead">The page you asked for has been moved, renamed, or never existed. The links below cover
      everything on this website.</p>
    <div class="btn-row" style="justify-content:center;margin-top:32px">
      <a class="btn btn--primary" href="{B}index.html">Back to home</a>
      <a class="btn btn--ghost" href="{B}services.html">Browse services</a>
      <a class="btn btn--ghost" href="{B}contact.html">Contact us</a>
    </div>
  </div>
</section>
"""
    doc = (head("Page not found | %s" % C["short"],
                "The page you requested could not be found. Browse our services, projects and "
                "certifications, or contact Pyramid Engineering in Singapore directly.",
                "404.html", 0) + header("", 0) + body + footer(0))
    return write("404.html", doc, 0)


# =========================================================================== ASSETS
def build_static():
    favicon = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
<rect width="200" height="200" rx="34" fill="#07131F"/>
<polygon points="100,36 100,164 26,164" fill="#E8262E"/>
<polygon points="100,36 174,164 100,164" fill="#A8161C"/>
<g stroke="#7E0E13" stroke-opacity=".4" stroke-width="2" fill="none">
<path d="M84 64H116"/><path d="M70 90H130"/><path d="M56 116H144"/><path d="M42 142H158"/></g>
</svg>"""
    write("assets/img/favicon.svg", favicon, 0)

    pages = ["index.html", "about.html", "services.html", "sectors.html", "projects.html",
             "certifications.html", "contact.html"] \
        + ["services/%s.html" % s["slug"] for s in SERVICES] \
        + ["%s.html" % p for p in LEGAL_PAGES]
    prio = {"index.html": "1.0", "services.html": "0.9", "contact.html": "0.9",
            "about.html": "0.8", "sectors.html": "0.8", "projects.html": "0.8",
            "certifications.html": "0.8"}
    urls = "".join(
        "  <url><loc>{s}/{p}</loc><lastmod>2026-08-31</lastmod>"
        "<changefreq>{cf}</changefreq><priority>{pr}</priority></url>\n".format(
            s=C["website"], p=p, cf="monthly" if not p.startswith(("privacy", "terms", "cookie", "disclaimer")) else "yearly",
            pr=prio.get(p, "0.4" if p.endswith(("policy.html", "conditions.html", "disclaimer.html")) else "0.7"))
        for p in pages)
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % urls, 0)

    write("robots.txt",
          "User-agent: *\nAllow: /\n\n"
          "# Block nothing — this is a public marketing site.\n\n"
          "Sitemap: %s/sitemap.xml\n" % C["website"], 0)

    write(".htaccess", """# Pyramid Engineering — Apache configuration
# Remove or adapt if your host uses Nginx / IIS.

ErrorDocument 404 /404.html

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/plain text/xml application/javascript application/json image/svg+xml
</IfModule>

<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/jpeg  "access plus 1 year"
  ExpiresByType image/webp  "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType text/css    "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType text/html   "access plus 1 hour"
</IfModule>

<IfModule mod_headers.c>
  Header always set X-Content-Type-Options "nosniff"
  Header always set X-Frame-Options "SAMEORIGIN"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set Permissions-Policy "geolocation=(), microphone=(), camera=()"
</IfModule>

# Force HTTPS and canonical host (uncomment once SSL is live)
# <IfModule mod_rewrite.c>
#   RewriteEngine On
#   RewriteCond %{HTTPS} off
#   RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
#   RewriteCond %{HTTP_HOST} !^www\\. [NC]
#   RewriteRule ^(.*)$ https://www.%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
# </IfModule>
""", 0)


# =========================================================================== MAIN
def main():
    made = []
    made.append(build_home())
    made.append(build_about())
    made.append(build_services_hub())
    n = len(SERVICES)
    for i, s in enumerate(SERVICES):
        made.append(build_service(s, SERVICES[(i - 1) % n], SERVICES[(i + 1) % n]))
    made.append(build_sectors())
    made.append(build_projects())
    made.append(build_certifications())
    made.append(build_contact())
    made += build_legal()
    made.append(build_404())
    build_static()
    print("Built %d pages:" % len(made))
    for m in made:
        print("  ", m)


if __name__ == "__main__":
    main()
