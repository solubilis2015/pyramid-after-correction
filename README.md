# Pyramid Engineering Private Limited — Website

Deployment-ready static website. No server-side runtime, no build step, no database.
Upload the contents of this folder to any web host and it works.

---

## 1. What is here

```
index.html                  Home
about.html                  Company, history, vision/mission/values, leadership, testimonials
services.html               Services overview + contracting models
services/                   8 individual service pages
  electrical.html
  control-instrumentation.html
  fire-gas-security.html
  mechanical-piping.html
  thermal-insulation.html
  refractory-lining.html
  civil-works.html
  maintenance-shutdown.html
sectors.html                7 sectors with scope, standards and reference plants
projects.html               Filterable register of 52 documented projects
certifications.html         ISO 9001, ISO 45001, bizSAFE STAR, ASPRI, SWS + register
contact.html                Enquiry form, map, WhatsApp, business hours
privacy-policy.html         PDPA-aligned privacy policy
terms-and-conditions.html
cookie-policy.html
disclaimer.html
404.html                    Not-found page

assets/css/style.css        Complete design system (single file)
assets/js/main.js           Navigation, filters, reveals, form handling (no dependencies)
assets/fonts/               Self-hosted Archivo, Inter, IBM Plex Mono (WOFF2, 156 KB total)
assets/img/                 Optimised WebP + JPEG images, logo SVGs, favicon
assets/downloads/           Capability Statement PDF (4 pages, A4)

sitemap.xml                 All 19 indexable pages
robots.txt
.htaccess                   Apache: 404, compression, caching, security headers, HTTPS redirect
```

---

## 2. Before you go live — three things to check

1. **Postal code.** The address is published as **Singapore 627564** (from the PEPL company
   profile letterhead). The 2026 profile deck shows "627 9046", which appears to be a copy of
   the telephone number. Confirm the correct postcode and update it in the places listed in
   section 4 if it differs.
2. **Social links.** LinkedIn and Facebook URLs in the footer are placeholders (`#`). Add the
   real URLs or remove the icons.
3. **Enquiry form delivery.** See section 3 — the form currently opens the visitor's email
   client. Connect a form endpoint before launch.

---

## 3. Connecting the enquiry form

The form on `contact.html` has no `action` attribute. With no action set, `assets/js/main.js`
builds an email and opens the visitor's mail application addressed to
`enquiry@pyramid-groups.com`, so no enquiry is lost in the meantime.

To POST enquiries to a real endpoint instead, add an `action` to the form tag in
`contact.html`:

```html
<form class="form" data-enquiry-form novalidate
      action="https://your-form-endpoint" method="post"
      enctype="multipart/form-data">
```

The JavaScript then steps aside and the browser submits normally. Options that work with a
static site: Formspree, Web3Forms, Netlify Forms, or a small PHP/Node handler on your own
hosting. File attachments require `enctype="multipart/form-data"` and an endpoint that accepts
uploads.

**Spam protection already built in:** a hidden honeypot field (`website_url`) and a
three-second time trap. Both are handled client-side; validate them server-side too if your
endpoint supports it.

---

## 4. Where to edit content

Anything that appears on more than one page — company details, service lists, projects,
testimonials, certifications, FAQs — lives in the generator in the `_build/` folder supplied
alongside this site, in **`_build/site_data.py`**. Edit that file and run:

```bash
cd _build
python3 build.py        # regenerates every page into ../site/
```

This is the safest way to change the phone number, address, a service description or the
project register: one edit, all 20 pages updated consistently.

To edit a single page by hand instead, open the `.html` file directly — the markup is plain
and readable. Just remember that a hand edit to a shared element (header, footer, contact
details) will be overwritten the next time the generator runs.

**Company details appear in:** `_build/site_data.py` → `COMPANY` dictionary. Changing it
updates the header bar, footer, contact page, structured data and the certifications page.

---

## 5. Deployment

1. Upload everything in this folder to your web root (`public_html`, `www`, or equivalent).
2. Point `www.pyramid-groups.com` at the host and install an SSL certificate.
3. In `.htaccess`, uncomment the HTTPS and canonical-host redirect block once SSL is active.
4. If your host runs Nginx or IIS rather than Apache, `.htaccess` is ignored — ask your host
   to set the 404 page, gzip/Brotli compression and cache headers instead.

**Google Search Console:** submit `https://www.pyramid-groups.com/sitemap.xml`.

**Google Analytics:** paste your GA4 snippet immediately before `</head>`. In the generator,
add it to the `head()` function in `_build/shell.py` so every page gets it at once.

---

## 6. Technical notes

- **Fonts are self-hosted.** No Google Fonts request, no third-party tracking, faster first
  paint, and the site renders correctly on a network that blocks external CDNs.
- **Images** are served as WebP with a JPEG fallback via `<picture>`, lazy-loaded below the
  fold, with the hero image eagerly loaded and given fetch priority.
- **No JavaScript framework.** `main.js` is ~180 lines of vanilla JS. The site is fully
  readable and navigable with JavaScript disabled — only the project filter and the mobile
  drawer need it.
- **Accessibility:** skip link, single H1 per page, correct heading order, labelled form
  controls, visible focus states, keyboard-reachable menus with focus trapping in the mobile
  drawer, `prefers-reduced-motion` respected, and all text verified at WCAG AA contrast.
- **SEO:** unique title and meta description per page (within search-result length limits),
  canonical URLs, Open Graph and Twitter card tags, JSON-LD `GeneralContractor` on every page
  plus `Service`, `FAQPage`, `ItemList` and `ContactPage` where relevant, sitemap and robots.

---

## 7. Image credits

Photography is drawn from the Pyramid Engineering company profile documents — a mix of the
company's own site photography (switchgear, calibration, insulation, refractory, tank
cleaning, scaffolding, civil works) and licensed stock imagery already used in the 2026
company profile. Certificate images are reproductions of the company's own certificates.

If any image was licensed only for the printed profile, replace it before launch. The
company's own site photographs are the strongest images on the site and should be added to
over time — `assets/img/` is where they go, and the `picture()` helper in
`_build/shell.py` generates the WebP/JPEG markup.
