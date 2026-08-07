#!/usr/bin/env python3
"""Build the Roam Prints social hub and legacy route redirects."""

from datetime import date
from html import escape
from pathlib import Path


OUT = Path(__file__).resolve().parent
SITE_NAME = "Roam Prints Studio"
SITE_URL = "https://www.roamprints.studio"
EMAIL = "roamcollectivetsudio@gmail.com"
OG_IMAGE = f"{SITE_URL}/assets/og-social-hub.png"

SOCIALS = [
    {
        "name": "Instagram",
        "handle": "@roamprintsstudio",
        "url": "https://www.instagram.com/roamprintsstudio",
        "mark": "IG",
        "note": "Behind the scenes, fresh prints, and shop life.",
    },
    {
        "name": "TikTok",
        "handle": "@roamprints",
        "url": "https://www.tiktok.com/@roamprints",
        "mark": "TT",
        "note": "Printer jokes, experiments, and the good kind of chaos.",
    },
    {
        "name": "YouTube",
        "handle": "@roamprints",
        "url": "https://www.youtube.com/@roamprints",
        "mark": "YT",
        "note": "Longer builds, ideas in motion, and more from the studio.",
    },
    {
        "name": "Facebook",
        "handle": "Roam Prints Studio",
        "url": "https://www.facebook.com/Roamprintsstudio/",
        "mark": "FB",
        "note": "Follow along with what we are making and where it goes.",
    },
]

LEGACY_PAGES = [
    "shop.html",
    "function-organizers.html",
    "automotive.html",
    "decor.html",
    "keychains.html",
]


CSS = r"""
  :root {
    --ink: #11100e;
    --ink-2: #1b1915;
    --paper: #ece8df;
    --paper-deep: #d8d2c6;
    --orange: #ff5a1e;
    --orange-bright: #ff7948;
    --muted: #aaa397;
    --line: rgba(236, 232, 223, .18);
    --display: "DM Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
    --body: "Manrope", ui-sans-serif, system-ui, sans-serif;
  }
  * { box-sizing: border-box; }
  html { scroll-behavior: smooth; }
  body {
    margin: 0;
    overflow-x: hidden;
    background: var(--ink);
    color: var(--paper);
    font-family: var(--body);
    -webkit-font-smoothing: antialiased;
  }
  a { color: inherit; text-decoration: none; }
  img { display: block; max-width: 100%; }
  ::selection { background: var(--orange); color: var(--ink); }
  .skip-link {
    position: absolute; left: 18px; top: -56px; z-index: 20;
    padding: 10px 14px; background: var(--paper); color: var(--ink); font-weight: 800;
  }
  .skip-link:focus { top: 18px; }
  .shell { width: min(1180px, calc(100% - 48px)); margin: 0 auto; }
  .eyebrow {
    display: inline-flex; align-items: center; gap: 9px;
    color: var(--orange-bright); font: 500 11px/1 var(--display);
    letter-spacing: .16em; text-transform: uppercase;
  }
  .eyebrow::before { content: ""; width: 18px; height: 1px; background: currentColor; }

  .masthead { position: relative; min-height: 100svh; isolation: isolate; overflow: clip; }
  .masthead::after {
    content: ""; position: absolute; inset: auto -15vw -19vw auto; z-index: -1;
    width: min(57vw, 680px); aspect-ratio: 1; border-radius: 50%;
    background: var(--orange); filter: blur(105px); opacity: .17; pointer-events: none;
  }
  .nav {
    display: flex; align-items: center; justify-content: space-between; gap: 24px;
    min-height: 84px; border-bottom: 1px solid var(--line);
  }
  .brand { display: inline-flex; align-items: center; gap: 11px; font: 500 14px/1 var(--display); letter-spacing: -.04em; }
  .brand img { width: 31px; height: 31px; object-fit: contain; }
  .nav-link {
    color: var(--paper); font-size: 13px; font-weight: 800; letter-spacing: .01em;
    border-bottom: 1px solid var(--orange); padding: 6px 0; transition: color .2s ease;
  }
  .nav-link:hover { color: var(--orange-bright); }
  .hero {
    display: grid; grid-template-columns: minmax(0, 1.04fr) minmax(340px, .96fr); gap: 60px;
    align-items: center; min-height: calc(100svh - 84px); padding: 74px 0 86px;
  }
  h1, h2, p { margin: 0; }
  h1 {
    max-width: 720px; margin-top: 25px; font: 500 clamp(48px, 8.3vw, 114px)/.88 var(--display);
    letter-spacing: -.085em; text-wrap: balance;
  }
  h1 em { color: var(--orange); font-style: normal; }
  .hero-copy {
    max-width: 520px; margin-top: 31px; color: var(--muted); font-size: clamp(16px, 1.45vw, 19px); line-height: 1.65;
  }
  .hero-actions { display: flex; gap: 18px; align-items: center; flex-wrap: wrap; margin-top: 34px; }
  .button {
    display: inline-flex; align-items: center; justify-content: center; gap: 10px;
    padding: 14px 18px; background: var(--orange); color: var(--ink);
    font-size: 13px; font-weight: 900; letter-spacing: -.01em;
    transition: transform .2s ease, background .2s ease;
  }
  .button:hover { background: var(--orange-bright); transform: translateY(-3px); }
  .quiet-link { color: var(--paper); font-size: 13px; font-weight: 800; border-bottom: 1px solid var(--line); padding-bottom: 5px; }
  .quiet-link:hover { color: var(--orange-bright); border-color: var(--orange); }
  .art-card {
    position: relative; min-height: 490px; overflow: hidden; background: #050504;
    border: 1px solid rgba(236, 232, 223, .28); box-shadow: 22px 22px 0 rgba(255, 90, 30, .8);
    transform: rotate(2.25deg); transition: transform .5s cubic-bezier(.2,.8,.2,1), box-shadow .5s ease;
  }
  .art-card:hover { transform: rotate(0deg) translate(-4px, -4px); box-shadow: 30px 30px 0 rgba(255, 90, 30, .8); }
  .art-card img { width: 100%; height: 100%; min-height: 490px; object-fit: cover; }
  .art-card figcaption {
    position: absolute; right: 18px; bottom: 16px; left: 18px; display: flex; align-items: end; justify-content: space-between; gap: 18px;
    padding-top: 34px; border-top: 1px solid rgba(236, 232, 223, .4); color: var(--paper);
  }
  .art-card strong { font: 500 13px/1.25 var(--display); letter-spacing: -.045em; }
  .art-card span { color: #d0c9bd; font: 500 10px/1.25 var(--display); letter-spacing: .1em; text-align: right; text-transform: uppercase; }
  .marquee {
    overflow: hidden; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line);
    background: var(--orange); color: var(--ink); white-space: nowrap;
  }
  .marquee-track { display: inline-flex; gap: 31px; min-width: max-content; padding: 16px 0; animation: marquee 26s linear infinite; }
  .marquee-track span { font: 500 12px/1 var(--display); letter-spacing: .08em; text-transform: uppercase; }
  .marquee-track b { font-family: var(--display); font-size: 13px; }
  @keyframes marquee { to { transform: translateX(-50%); } }

  .social-section { padding: clamp(82px, 12vw, 156px) 0; background: var(--paper); color: var(--ink); }
  .section-heading { display: flex; align-items: end; justify-content: space-between; gap: 30px; margin-bottom: 44px; }
  .section-heading .eyebrow { color: #a8340d; }
  h2 { max-width: 740px; margin-top: 20px; font: 500 clamp(38px, 6.2vw, 78px)/.93 var(--display); letter-spacing: -.08em; text-wrap: balance; }
  .section-note { max-width: 290px; color: #5e574c; font-size: 14px; line-height: 1.55; }
  .social-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); border-top: 1px solid #aaa397; border-left: 1px solid #aaa397; }
  .social-card {
    position: relative; min-height: 270px; overflow: hidden; padding: 25px;
    border-right: 1px solid #aaa397; border-bottom: 1px solid #aaa397;
    background: var(--paper); transition: color .28s ease, background .28s ease, transform .28s ease;
  }
  .social-card::before { content: ""; position: absolute; width: 150px; height: 150px; right: -80px; top: -80px; border-radius: 50%; background: var(--orange); transform: scale(0); transition: transform .4s cubic-bezier(.2,.8,.2,1); }
  .social-card:hover, .social-card:focus-visible { color: var(--paper); background: var(--ink-2); transform: translateY(-6px); outline: none; }
  .social-card:hover::before, .social-card:focus-visible::before { transform: scale(1); }
  .service-mark, .social-content, .arrow { position: relative; z-index: 1; }
  .service-mark { display: grid; width: 45px; height: 45px; place-items: center; border: 1px solid currentColor; font: 500 13px/1 var(--display); letter-spacing: -.08em; }
  .social-card:hover .service-mark, .social-card:focus-visible .service-mark { border-color: var(--orange); color: var(--orange-bright); }
  .social-content { margin-top: 47px; }
  .social-name { display: block; font: 500 clamp(25px, 3vw, 36px)/1 var(--display); letter-spacing: -.07em; }
  .social-handle { display: block; margin-top: 9px; color: #746d62; font-size: 13px; font-weight: 800; }
  .social-card:hover .social-handle, .social-card:focus-visible .social-handle { color: #c9c1b4; }
  .social-note { max-width: 320px; margin-top: 17px; color: #6a6359; font-size: 13px; line-height: 1.5; }
  .social-card:hover .social-note, .social-card:focus-visible .social-note { color: #d4cdc1; }
  .arrow { position: absolute; right: 24px; bottom: 21px; font: 500 29px/1 var(--display); transition: transform .25s ease; }
  .social-card:hover .arrow, .social-card:focus-visible .arrow { color: var(--orange-bright); transform: translate(5px, -5px); }

  .contact-section { padding: 0; background: var(--ink); color: var(--paper); }
  .contact-card { display: grid; grid-template-columns: 1.08fr .92fr; gap: 40px; padding: clamp(70px, 10vw, 124px) 0; }
  .contact-card h2 { max-width: 680px; }
  .contact-copy { align-self: end; }
  .contact-copy p { max-width: 420px; color: #aaa397; font-size: 16px; line-height: 1.65; }
  .email-link {
    display: inline-flex; align-items: baseline; gap: 11px; margin-top: 26px; max-width: 100%;
    color: var(--orange-bright); border-bottom: 1px solid currentColor; overflow-wrap: anywhere;
    font: 500 clamp(16px, 2vw, 24px)/1.25 var(--display); letter-spacing: -.06em;
    transition: color .2s ease;
  }
  .email-link:hover { color: var(--paper); }
  .footer { border-top: 1px solid var(--line); padding: 25px 0 28px; }
  .footer-inner { display: flex; justify-content: space-between; gap: 18px; color: #8e877c; font: 500 10px/1.5 var(--display); letter-spacing: .07em; text-transform: uppercase; }
  .footer a:hover { color: var(--orange-bright); }

  @media (max-width: 780px) {
    .shell { width: min(100% - 36px, 650px); }
    .nav { min-height: 70px; }
    .nav-link { font-size: 12px; }
    .hero { grid-template-columns: 1fr; gap: 49px; padding: 63px 0 68px; }
    .art-card, .art-card img { min-height: 390px; }
    .art-card { width: calc(100% - 20px); margin-left: 2px; box-shadow: 16px 16px 0 var(--orange); }
    .section-heading, .contact-card { display: block; }
    .section-note { margin-top: 25px; }
    .social-grid { grid-template-columns: 1fr; }
    .social-card { min-height: 244px; }
    .contact-copy { margin-top: 42px; }
    .footer-inner { flex-direction: column; }
  }
  @media (max-width: 420px) {
    .brand { font-size: 12px; }
    .brand img { width: 27px; height: 27px; }
    h1 { font-size: 46px; }
    .hero-copy { font-size: 16px; }
    .art-card, .art-card img { min-height: 340px; }
  }
  @media (prefers-reduced-motion: reduce) {
    html { scroll-behavior: auto; }
    *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; transition-duration: .01ms !important; }
  }
"""


def document(title, description, body, *, robots="index,follow", canonical="/"):
    schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SITE_NAME,
        "url": SITE_URL,
        "email": EMAIL,
        "sameAs": [social["url"] for social in SOCIALS],
    }
    canonical_url = SITE_URL if canonical == "/" else f"{SITE_URL}/{canonical}"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(description, quote=True)}">
  <meta name="robots" content="{robots}">
  <link rel="canonical" href="{canonical_url}">
  <link rel="icon" href="/assets/favicon.png" type="image/png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;600;700;800&display=swap" rel="stylesheet">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{escape(title, quote=True)}">
  <meta property="og:description" content="{escape(description, quote=True)}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(title, quote=True)}">
  <meta name="twitter:description" content="{escape(description, quote=True)}">
  <meta name="twitter:image" content="{OG_IMAGE}">
  <script type="application/ld+json">{escape(__import__('json').dumps(schema), quote=False)}</script>
  <title>{escape(title)}</title>
  <style>{CSS}</style>
</head>
{body}
</html>"""


def social_card(social):
    return f"""
      <a class="social-card" href="{social['url']}" target="_blank" rel="noopener noreferrer" aria-label="Open Roam Prints Studio on {social['name']} (opens in a new tab)">
        <span class="service-mark" aria-hidden="true">{social['mark']}</span>
        <span class="social-content">
          <span class="social-name">{social['name']}</span>
          <span class="social-handle">{social['handle']}</span>
          <span class="social-note">{social['note']}</span>
        </span>
        <span class="arrow" aria-hidden="true">↗</span>
      </a>"""


def build_home():
    cards = "".join(social_card(social) for social in SOCIALS)
    body = f"""<body>
  <a class="skip-link" href="#socials">Skip to social links</a>
  <header class="masthead">
    <div class="shell nav">
      <a class="brand" href="/" aria-label="Roam Prints Studio home"><img src="assets/rp-mark-light.png" alt="">ROAM PRINTS STUDIO</a>
      <a class="nav-link" href="#contact">Partnerships ↘</a>
    </div>
    <div class="shell hero">
      <div>
        <span class="eyebrow">3D prints, in motion</span>
        <h1>FOLLOW<br>THE <em>BUILD.</em></h1>
        <p class="hero-copy">Experiments, printer chaos, and things we are genuinely excited to make. Find Roam Prints wherever you scroll.</p>
        <div class="hero-actions">
          <a class="button" href="#socials">Pick a platform <span aria-hidden="true">↓</span></a>
          <a class="quiet-link" href="mailto:{EMAIL}">Work with us</a>
        </div>
      </div>
      <figure class="art-card">
        <img src="assets/og-social-hub.png" alt="A sculptural 3D printed object surrounded by orange filament.">
        <figcaption><strong>Made layer by layer.</strong><span>Roam Prints<br>Studio</span></figcaption>
      </figure>
    </div>
  </header>
  <div class="marquee" aria-hidden="true"><div class="marquee-track">
    <span>Print</span><b>✦</b><span>Roam</span><b>✦</b><span>Repeat</span><b>✦</b><span>Print</span><b>✦</b><span>Roam</span><b>✦</b><span>Repeat</span><b>✦</b>
    <span>Print</span><b>✦</b><span>Roam</span><b>✦</b><span>Repeat</span><b>✦</b><span>Print</span><b>✦</b><span>Roam</span><b>✦</b><span>Repeat</span><b>✦</b>
  </div></div>
  <main>
    <section class="social-section" id="socials">
      <div class="shell">
        <div class="section-heading">
          <div><span class="eyebrow">Choose your feed</span><h2>Same studio.<br>Different corners.</h2></div>
          <p class="section-note">Four places to keep up with what is coming off the printer next.</p>
        </div>
        <div class="social-grid">{cards}
        </div>
      </div>
    </section>
    <section class="contact-section" id="contact">
      <div class="shell contact-card">
        <div><span class="eyebrow">Partnerships + brand work</span><h2>Got an idea worth making?</h2></div>
        <div class="contact-copy">
          <p>For collaborations, brand partnerships, and press, send us a note. We would love to hear what you are thinking.</p>
          <a class="email-link" href="mailto:{EMAIL}">{EMAIL}<span aria-hidden="true">↗</span></a>
        </div>
      </div>
    </section>
  </main>
  <footer class="footer"><div class="shell footer-inner"><span>© {date.today().year} Roam Prints Studio</span><a href="#socials">Find us online ↑</a></div></footer>
</body>"""
    return document(
        "Roam Prints Studio — Follow the Build",
        "Find Roam Prints Studio on Instagram, TikTok, YouTube, and Facebook. For partnerships and brand work, get in touch.",
        body,
    )


def build_redirect():
    body = """<body><main><p>This page has moved. <a href="/">Go to Roam Prints Studio.</a></p></main></body>"""
    page = document("Roam Prints Studio", "Find Roam Prints Studio online.", body, robots="noindex,follow")
    return page.replace("</head>", '  <meta http-equiv="refresh" content="0; url=/">\n</head>')


def build_sitemap():
    today = date.today().isoformat()
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{SITE_URL}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
"""


def write_file(filename, contents):
    (OUT / filename).write_text(contents, encoding="utf-8")


write_file("index.html", build_home())
for filename in LEGACY_PAGES:
    write_file(filename, build_redirect())
write_file("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
write_file("sitemap.xml", build_sitemap())
print("Built social hub and legacy redirects.")
