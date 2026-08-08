#!/usr/bin/env python3
"""Build the animated Roam Prints social landing page."""

import json
from datetime import date
from html import escape
from pathlib import Path


OUT = Path(__file__).resolve().parent
SITE_NAME = "Roam Prints Studio"
SITE_URL = "https://www.roamprints.studio"
EMAIL = "roamcollectivetsudio@gmail.com"
OG_IMAGE = f"{SITE_URL}/assets/og-follow-the-brand.png"

SOCIALS = [
    {
        "index": "01",
        "name": "Instagram",
        "handle": "@roamprintsstudio",
        "url": "https://www.instagram.com/roamprintsstudio",
        "mark": "IG",
        "icon": "assets/social-icons/instagram.json",
        "description": "Updates and moments from Roam Prints.",
    },
    {
        "index": "02",
        "name": "Art by Roam",
        "handle": "@artbyroam",
        "url": "https://www.instagram.com/artbyroam",
        "mark": "IG",
        "icon": "assets/social-icons/instagram.json",
        "description": "Custom art from Art by Roam.",
    },
    {
        "index": "03",
        "name": "TikTok",
        "handle": "@roamprints",
        "url": "https://www.tiktok.com/@roamprints",
        "mark": "TT",
        "icon": "assets/social-icons/tiktok.json",
        "description": "Short-form videos and the latest from Roam Prints.",
    },
    {
        "index": "04",
        "name": "YouTube",
        "handle": "@roamprints",
        "url": "https://www.youtube.com/@roamprints",
        "mark": "YT",
        "icon": "assets/social-icons/youtube.json",
        "description": "Watch more from Roam Prints.",
    },
    {
        "index": "05",
        "name": "Facebook",
        "handle": "Roam Prints Studio",
        "url": "https://www.facebook.com/Roamprintsstudio/",
        "mark": "FB",
        "icon": "assets/social-icons/facebook.json",
        "description": "Follow Roam Prints on Facebook.",
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
  --black: #080808;
  --black-soft: #11110f;
  --white: #f7f4ee;
  --white-dim: #c6c1b8;
  --orange: #ff5a1e;
  --orange-hot: #ff7a47;
  --line: rgba(247, 244, 238, .18);
  --ink-line: rgba(8, 8, 8, .16);
  --display: "Bebas Neue", Impact, sans-serif;
  --body: "Manrope", ui-sans-serif, system-ui, sans-serif;
  --mono: "DM Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  --mx: 50vw; --my: 30vh;
  margin: 0; overflow-x: hidden; background: var(--black); color: var(--white);
  font-family: var(--body); -webkit-font-smoothing: antialiased;
}
body::before {
  content: ""; position: fixed; inset: 0; z-index: 4; pointer-events: none; opacity: .34;
  background: radial-gradient(380px circle at var(--mx) var(--my), rgba(255, 90, 30, .12), transparent 68%);
  mix-blend-mode: screen;
}
a { color: inherit; text-decoration: none; }
button { font: inherit; }
img { display: block; max-width: 100%; }
::selection { background: var(--orange); color: var(--black); }
.skip-link { position: absolute; left: 18px; top: -60px; z-index: 100; padding: 11px 15px; background: var(--white); color: var(--black); font-weight: 900; }
.skip-link:focus { top: 18px; }
.shell { width: min(1240px, calc(100% - 52px)); margin: 0 auto; }
.mono, .eyebrow { font-family: var(--mono); letter-spacing: .12em; text-transform: uppercase; }
.eyebrow { display: inline-flex; align-items: center; gap: 9px; color: var(--orange-hot); font-size: 10px; font-weight: 500; }
.eyebrow::before { content: ""; width: 20px; height: 1px; background: currentColor; }
#scroll-progress { position: fixed; top: 0; left: 0; z-index: 80; width: 0; height: 3px; background: var(--orange); box-shadow: 0 0 16px var(--orange); }

/* Hero */
.hero { position: relative; min-height: 100svh; isolation: isolate; overflow: clip; }
#filament-field { position: absolute; inset: 0; z-index: -2; width: 100%; height: 100%; opacity: .82; }
.hero::after { content: ""; position: absolute; z-index: -1; right: -15vw; top: 8vh; width: min(58vw, 720px); aspect-ratio: 1; border-radius: 50%; background: var(--orange); filter: blur(150px); opacity: .12; }
.nav { display: flex; align-items: center; justify-content: space-between; gap: 20px; min-height: 86px; border-bottom: 1px solid var(--line); }
.brand { display: inline-flex; align-items: center; gap: 11px; color: var(--white); font: 500 13px/1 var(--mono); letter-spacing: -.05em; }
.brand img { width: 31px; height: 31px; object-fit: contain; }
.nav-links { display: flex; align-items: center; gap: 25px; }
.nav-links a { color: var(--white-dim); font: 700 11px/1 var(--mono); letter-spacing: .08em; text-transform: uppercase; transition: color .2s ease; }
.nav-links a:hover { color: var(--orange-hot); }
.nav-pill { border: 1px solid var(--line); padding: 10px 13px; color: var(--white) !important; }
.nav-pill:hover { border-color: var(--orange); background: var(--orange); color: var(--black) !important; }
.hero-main { display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(350px, .95fr); gap: 64px; align-items: center; min-height: calc(100svh - 86px); padding: 72px 0 66px; }
.hero-copy { position: relative; z-index: 2; }
h1, h2, h3, p { margin: 0; }
h1 { max-width: 710px; margin-top: 24px; font: 400 clamp(84px, 12.4vw, 180px)/.75 var(--display); letter-spacing: -.035em; text-transform: uppercase; }
.hero-word { display: block; overflow: hidden; }
.hero-word > span { display: block; transform: translateY(110%); animation: word-in .85s cubic-bezier(.16, 1, .3, 1) forwards; }
.hero-word:nth-child(2) > span { animation-delay: .11s; color: var(--orange); }
.hero-word:nth-child(3) > span { animation-delay: .22s; }
@keyframes word-in { to { transform: translateY(0); } }
.hero-lede { max-width: 490px; margin-top: 35px; color: var(--white-dim); font-size: clamp(15px, 1.35vw, 18px); line-height: 1.68; opacity: 0; transform: translateY(16px); animation: fade-up .65s .42s ease forwards; }
.hero-actions { display: flex; align-items: center; gap: 21px; flex-wrap: wrap; margin-top: 31px; opacity: 0; transform: translateY(16px); animation: fade-up .65s .54s ease forwards; }
@keyframes fade-up { to { opacity: 1; transform: translateY(0); } }
.button { display: inline-flex; align-items: center; gap: 12px; padding: 15px 18px; background: var(--orange); color: var(--black); font-size: 12px; font-weight: 900; letter-spacing: -.02em; transition: transform .22s ease, background .22s ease; }
.button:hover { background: var(--orange-hot); }
.text-link { position: relative; padding-bottom: 5px; color: var(--white); font-size: 12px; font-weight: 800; }
.text-link::after { content: ""; position: absolute; right: 0; bottom: 0; left: 0; height: 1px; background: var(--white-dim); transition: background .2s ease, transform .2s ease; transform-origin: left; }
.text-link:hover { color: var(--orange-hot); }
.text-link:hover::after { background: var(--orange); transform: scaleX(.45); }
.hero-stage { position: relative; min-height: 550px; display: grid; place-items: center; perspective: 1000px; }
.orbit { position: relative; width: min(37vw, 490px); aspect-ratio: 1; transform-style: preserve-3d; animation: float 7s ease-in-out infinite; }
@keyframes float { 50% { transform: translateY(-18px) rotateX(3deg) rotateY(-4deg); } }
.orbit::before, .orbit::after { content: ""; position: absolute; border-radius: 50%; pointer-events: none; }
.orbit::before { inset: 10%; border: 1px solid rgba(255, 90, 30, .7); box-shadow: inset 0 0 36px rgba(255, 90, 30, .08), 0 0 48px rgba(255, 90, 30, .12); animation: spin 13s linear infinite; }
.orbit::after { inset: 21%; border: 1px solid rgba(247, 244, 238, .26); transform: rotateX(66deg) rotateZ(-16deg); animation: spin-reverse 11s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes spin-reverse { to { transform: rotateX(66deg) rotateZ(344deg); } }
.thread { position: absolute; left: 5%; width: 90%; height: 25%; border: 2px solid var(--orange); border-radius: 50%; opacity: .9; filter: drop-shadow(0 0 9px rgba(255, 90, 30, .35)); }
.thread:nth-child(1) { top: 25%; transform: rotate(14deg) skewX(-17deg); }
.thread:nth-child(2) { top: 30%; transform: rotate(31deg) skewX(-17deg); opacity: .62; }
.thread:nth-child(3) { top: 35%; transform: rotate(48deg) skewX(-17deg); opacity: .38; }
.thread:nth-child(4) { top: 40%; transform: rotate(65deg) skewX(-17deg); opacity: .2; }
.logo-core { position: absolute; inset: 13%; overflow: hidden; border-radius: 50%; background: var(--black); box-shadow: 0 26px 60px rgba(0, 0, 0, .76), 0 0 0 1px rgba(255, 90, 30, .4), 0 0 42px rgba(255, 90, 30, .16); transform: rotate(-4deg); }
.logo-core img { width: 100%; height: 100%; object-fit: cover; }

/* Social hub */
.social-section { position: relative; padding: clamp(60px, 6vw, 82px) 0; background: var(--black); overflow: hidden; }
.social-section::before { content: ""; position: absolute; inset: 0; pointer-events: none; background: radial-gradient(700px circle at 100% 0, rgba(255, 90, 30, .1), transparent 66%); }
.section-top { position: relative; display: flex; align-items: end; justify-content: space-between; gap: 30px; max-width: 900px; margin: 0 auto 31px; }
.section-top h2 { margin-top: 17px; font: 400 clamp(56px, 8vw, 105px)/.8 var(--display); letter-spacing: -.025em; text-transform: uppercase; }
.section-top p { max-width: 265px; color: var(--white-dim); font-size: 14px; line-height: 1.55; }
.social-grid { position: relative; display: grid; gap: 12px; max-width: 900px; margin: 0 auto; }
.social-card { --rx: 0deg; --ry: 0deg; position: relative; min-height: 104px; display: flex; align-items: center; gap: 18px; overflow: hidden; padding: 16px 20px; border: 1px solid var(--line); background: rgba(255, 255, 255, .025); transform: perspective(900px) rotateX(var(--rx)) rotateY(var(--ry)); transform-style: preserve-3d; transition: background .28s ease, border-color .28s ease, transform .13s ease; }
.social-card::before { content: ""; position: absolute; right: -28px; width: 160px; aspect-ratio: 1; border: 1px solid rgba(255, 90, 30, .55); border-radius: 50%; opacity: 0; transform: scale(.7); transition: opacity .3s ease, transform .45s cubic-bezier(.2, .8, .2, 1); }
.social-card::after { content: ""; position: absolute; bottom: 0; left: 0; height: 3px; width: 100%; background: var(--orange); transform: scaleX(0); transform-origin: left; transition: transform .3s ease; }
.social-card:hover, .social-card:focus-visible { background: #151310; border-color: rgba(255, 90, 30, .75); outline: none; }
.social-card:hover::before, .social-card:focus-visible::before { opacity: 1; transform: scale(1); }
.social-card:hover::after, .social-card:focus-visible::after { transform: scaleX(1); }
.card-top, .card-body, .card-bottom { position: relative; z-index: 1; }
.card-top { display: flex; align-items: center; }
.card-index { display: none; }
.service-mark { position: relative; display: grid; width: 58px; height: 58px; place-items: center; overflow: hidden; border: 1px solid rgba(247, 244, 238, .6); color: var(--white); font: 500 13px/1 var(--mono); letter-spacing: -.08em; transition: background .25s ease, color .25s ease, border-color .25s ease; }
.service-mark svg { width: 100% !important; height: 100% !important; }
.mark-fallback { position: absolute; inset: 0; display: grid; place-items: center; transition: opacity .15s ease; }
.service-mark.lottie-ready .mark-fallback { opacity: 0; }
.social-card:hover .service-mark, .social-card:focus-visible .service-mark { border-color: var(--orange); background: rgba(255, 90, 30, .12); color: var(--orange-hot); }
.card-body { display: grid; gap: 6px; }
.social-name { display: block; font: 400 clamp(31px, 4vw, 48px)/.8 var(--display); letter-spacing: -.015em; text-transform: uppercase; }
.social-handle { display: block; color: var(--white-dim); font: 500 11px/1.2 var(--mono); letter-spacing: .02em; }
.card-description { display: none; }
.card-bottom { display: flex; align-items: center; margin-left: auto; color: var(--white); }
.card-arrow { color: var(--orange-hot); font: 400 36px/.5 var(--display); transition: transform .25s ease; }
.social-card:hover .card-arrow, .social-card:focus-visible .card-arrow { transform: translate(5px, -5px); }

/* Contact */
.contact { position: relative; overflow: hidden; padding: 70px 0 0; background: var(--orange); color: var(--black); }
.contact::before { content: ""; position: absolute; right: -8vw; top: -23vw; width: min(43vw, 530px); aspect-ratio: 1; border-radius: 50%; border: clamp(28px, 4vw, 62px) solid rgba(247, 244, 238, .28); }
.contact .eyebrow { color: var(--black); }
.contact-grid { position: relative; display: flex; align-items: end; justify-content: space-between; gap: 32px; padding-bottom: 72px; }
.contact h2 { margin-top: 14px; font: 400 clamp(54px, 8.4vw, 100px)/.78 var(--display); letter-spacing: -.025em; text-transform: uppercase; }
.contact-copy { position: relative; z-index: 1; text-align: right; }
.contact-copy p { color: #3c190d; font: 700 11px/1.4 var(--mono); letter-spacing: .08em; text-transform: uppercase; }
.email-link { display: inline-flex; align-items: center; gap: 12px; margin-top: 18px; padding: 15px 18px; background: var(--black); color: var(--white); font: 800 12px/1 var(--body); letter-spacing: -.01em; transition: background .2s ease, color .2s ease, transform .2s ease; }
.email-link:hover { background: var(--white); color: var(--black); transform: translateY(-3px); }
.contact-foot { position: relative; z-index: 1; border-top: 1px solid rgba(8, 8, 8, .22); padding: 22px 0 25px; }
.contact-foot-inner { display: flex; justify-content: space-between; gap: 20px; color: #4b2112; font: 500 10px/1.45 var(--mono); letter-spacing: .1em; text-transform: uppercase; }
.contact-foot a:hover { color: var(--white); }

/* Entrance and responsive detail */
[data-reveal] { opacity: 0; transform: translateY(34px); transition: opacity .7s ease, transform .7s cubic-bezier(.2, .8, .2, 1); }
[data-reveal].visible { opacity: 1; transform: translateY(0); }
@media (max-width: 800px) {
  .shell { width: min(100% - 36px, 650px); }
  .nav { min-height: 70px; }
  .nav-links { gap: 14px; }
  .nav-links a:not(.nav-pill) { display: none; }
  .hero { min-height: auto; }
  .hero-main { grid-template-columns: 1fr; gap: 24px; min-height: auto; padding: 48px 0 60px; }
  h1 { font-size: clamp(78px, 24vw, 130px); }
  .hero-lede { margin-top: 26px; line-height: 1.58; }
  .hero-actions { gap: 16px; margin-top: 26px; }
  .button, .text-link { min-height: 48px; }
  .text-link { display: inline-flex; align-items: center; }
  .hero-stage { min-height: clamp(320px, 84vw, 410px); margin-top: -4px; }
  .orbit { width: min(84vw, 420px); }
  .social-section { padding: 58px 0; }
  .section-top { display: block; }
  .section-top p { margin-top: 20px; }
  .social-card { min-height: 88px; padding: 14px 16px; }
  .card-body { min-width: 0; }
  .social-handle { max-width: 48vw; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .card-arrow { font-size: 32px; }
  .contact { padding-top: 50px; }
  .contact-grid { display: block; }
  .contact-grid { padding-bottom: 52px; }
  .contact-copy { margin-top: 26px; text-align: left; }
  .email-link { min-height: 52px; }
  .contact-foot { padding: 18px 0 22px; }
  .contact-foot-inner { flex-direction: column; }
}
@media (max-width: 430px) {
  .shell { width: min(100% - 32px, 650px); }
  .nav { min-height: 64px; gap: 10px; }
  .brand { font-size: 11px; }
  .brand img { width: 27px; height: 27px; }
  .nav-pill { display: inline-flex; align-items: center; min-height: 40px; padding: 9px 10px; }
  .hero-main { padding: 40px 0 54px; }
  h1 { font-size: clamp(70px, 22.5vw, 98px); }
  .hero-stage { min-height: 294px; }
  .social-card { gap: 14px; padding: 14px; }
  .service-mark { width: 50px; height: 50px; }
  .social-name { font-size: clamp(30px, 10vw, 40px); }
  .contact h2 { font-size: clamp(58px, 16vw, 74px); }
  .email-link { width: 100%; justify-content: space-between; }
}
@media (max-width: 360px) {
  .brand { gap: 7px; font-size: 9px; }
  .brand img { width: 24px; height: 24px; }
  .nav-pill { font-size: 9px !important; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; transition-duration: .01ms !important; }
}
"""


SCRIPT = r"""
<script>
(() => {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const progress = document.querySelector("#scroll-progress");
  const updateProgress = () => {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.width = `${max > 0 ? (window.scrollY / max) * 100 : 0}%`;
  };
  window.addEventListener("scroll", updateProgress, { passive: true });
  updateProgress();

  window.addEventListener("pointermove", (event) => {
    document.body.style.setProperty("--mx", `${event.clientX}px`);
    document.body.style.setProperty("--my", `${event.clientY}px`);
  }, { passive: true });

  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) entry.target.classList.add("visible");
    });
  }, { threshold: .14 });
  document.querySelectorAll("[data-reveal]").forEach((element) => revealObserver.observe(element));

  document.querySelectorAll("[data-tilt]").forEach((card) => {
    card.addEventListener("pointermove", (event) => {
      if (reduce) return;
      const rect = card.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width - .5;
      const y = (event.clientY - rect.top) / rect.height - .5;
      card.style.setProperty("--rx", `${-y * 5}deg`);
      card.style.setProperty("--ry", `${x * 5}deg`);
    });
    card.addEventListener("pointerleave", () => {
      card.style.setProperty("--rx", "0deg");
      card.style.setProperty("--ry", "0deg");
    });
  });

  document.querySelectorAll("[data-magnetic]").forEach((element) => {
    element.addEventListener("pointermove", (event) => {
      if (reduce) return;
      const rect = element.getBoundingClientRect();
      const x = (event.clientX - rect.left - rect.width / 2) * .16;
      const y = (event.clientY - rect.top - rect.height / 2) * .16;
      element.style.transform = `translate(${x}px, ${y}px)`;
    });
    element.addEventListener("pointerleave", () => { element.style.transform = "translate(0, 0)"; });
  });

  const activateSocialIcons = () => {
    if (!window.lottie) return;
    document.querySelectorAll("[data-lottie]").forEach((holder) => {
      const animation = window.lottie.loadAnimation({
        container: holder,
        renderer: "svg",
        loop: false,
        autoplay: false,
        path: holder.dataset.lottie,
      });
      holder.classList.add("lottie-ready");
      const play = () => animation.goToAndPlay(0, true);
      const card = holder.closest(".social-card");
      card.addEventListener("pointerenter", play);
      card.addEventListener("focus", play);
    });
  };
  if (window.lottie) activateSocialIcons();
  else window.addEventListener("load", activateSocialIcons, { once: true });

  const canvas = document.querySelector("#filament-field");
  const context = canvas.getContext("2d");
  const mouse = { x: .6, y: .46 };
  const strands = Array.from({ length: 14 }, (_, index) => ({
    offset: index / 14,
    speed: .00013 + (index % 4) * .000045,
    width: 1 + (index % 3) * .55,
  }));
  const resize = () => {
    const pixelRatio = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = window.innerWidth * pixelRatio;
    canvas.height = window.innerHeight * pixelRatio;
    context.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
  };
  const trackMouse = (event) => {
    mouse.x = event.clientX / window.innerWidth;
    mouse.y = event.clientY / window.innerHeight;
  };
  window.addEventListener("resize", resize);
  window.addEventListener("pointermove", trackMouse, { passive: true });
  resize();

  const draw = (time) => {
    const width = window.innerWidth;
    const height = window.innerHeight;
    context.clearRect(0, 0, width, height);
    strands.forEach((strand, index) => {
      const travel = (time * strand.speed + strand.offset) % 1;
      const startY = height * (.11 + index * .055);
      const bend = (mouse.y - .5) * 220 + Math.sin(time * .00055 + index) * 28;
      const centerX = width * (.48 + (mouse.x - .5) * .15);
      context.beginPath();
      context.moveTo(-60, startY);
      context.bezierCurveTo(width * .22, startY - bend, centerX, height * (.53 + Math.sin(index) * .1), width + 80, height * (.18 + (1 - travel) * .68));
      context.strokeStyle = index % 4 === 0 ? "rgba(247,244,238,.19)" : `rgba(255,90,30,${.08 + (index % 5) * .042})`;
      context.lineWidth = strand.width;
      context.stroke();
    });
    if (!reduce) window.requestAnimationFrame(draw);
  };
  if (reduce) draw(0); else window.requestAnimationFrame(draw);
})();
</script>
"""


def social_card(social):
    return f"""
      <a class="social-card" data-tilt href="{social['url']}" target="_blank" rel="noopener noreferrer" aria-label="Open Roam Prints Studio on {social['name']} (opens in a new tab)">
        <span class="card-top"><span class="service-mark" data-lottie="{social['icon']}" aria-hidden="true"><span class="mark-fallback">{social['mark']}</span></span></span>
        <span class="card-body"><span class="social-name">{social['name']}</span><span class="social-handle">{social['handle']}</span></span>
        <span class="card-bottom"><span class="card-arrow" aria-hidden="true">↗</span></span>
      </a>"""


def document(title, description, body):
    schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SITE_NAME,
        "url": SITE_URL,
        "email": EMAIL,
        "sameAs": [social["url"] for social in SOCIALS],
    }
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(description, quote=True)}">
  <link rel="canonical" href="{SITE_URL}/">
  <link rel="icon" href="/assets/favicon.png" type="image/png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js" defer></script>
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Roam Prints Studio">
  <meta property="og:title" content="{escape(title, quote=True)}">
  <meta property="og:description" content="{escape(description, quote=True)}">
  <meta property="og:url" content="{SITE_URL}/">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Roam Prints — Follow the brand">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(title, quote=True)}">
  <meta name="twitter:description" content="{escape(description, quote=True)}">
  <meta name="twitter:image" content="{OG_IMAGE}">
  <script type="application/ld+json">{json.dumps(schema)}</script>
  <title>{escape(title)}</title>
  <style>{CSS}</style>
</head>
{body}
</html>"""


def build_home():
    cards = "".join(social_card(social) for social in SOCIALS)
    body = f"""<body>
  <div id="scroll-progress" aria-hidden="true"></div>
  <a class="skip-link" href="#socials">Skip to social links</a>
  <header class="hero">
    <canvas id="filament-field" aria-hidden="true"></canvas>
    <nav class="shell nav" aria-label="Main navigation">
      <a class="brand" href="/" aria-label="Roam Prints Studio home"><img src="assets/rp-mark-light.png" alt="">ROAM PRINTS / STUDIO</a>
      <div class="nav-links"><a class="nav-pill" href="#contact">Contact ↗</a></div>
    </nav>
    <div class="shell hero-main">
      <div class="hero-copy">
        <span class="eyebrow">Roam Prints Studio</span>
        <h1 aria-label="Follow Roam Prints"><span class="hero-word"><span>Follow</span></span><span class="hero-word"><span>Roam Prints.</span></span></h1>
        <p class="hero-lede">Follow Roam Prints across our social channels.</p>
        <div class="hero-actions"><a class="button" data-magnetic href="#socials">Choose a platform <span aria-hidden="true">↓</span></a><a class="text-link" href="mailto:{EMAIL}">Partnerships</a></div>
      </div>
      <div class="hero-stage" aria-hidden="true">
        <div class="orbit"><span class="thread"></span><span class="thread"></span><span class="thread"></span><span class="thread"></span><div class="logo-core"><img src="assets/hero-logo.png" alt=""></div></div>
      </div>
    </div>
  </header>
  <main>
    <section class="social-section" id="socials"><div class="shell">
      <div class="section-top" data-reveal><div><span class="eyebrow">Find us online</span><h2>Follow<br>along.</h2></div><p>Follow us on all platforms.</p></div>
      <div class="social-grid">{cards}</div>
    </div></section>
    <section class="contact" id="contact"><div class="shell contact-grid" data-reveal>
      <div><span class="eyebrow">Partnerships + brand work</span><h2>Let’s talk.</h2></div>
      <div class="contact-copy"><p>For collaborations and brand partnerships</p><a class="email-link" href="mailto:{EMAIL}" aria-label="Email Roam Prints Studio to work together">Email us to work together <span aria-hidden="true">↗</span></a></div>
    </div><footer class="contact-foot"><div class="shell contact-foot-inner"><span>© {date.today().year} Roam Prints Studio</span><a href="#socials">Back to the feeds ↑</a></div></footer></section>
  </main>
{SCRIPT}
</body>"""
    return document(
        "Roam Prints Studio — Follow Roam Prints",
        "Follow Roam Prints Studio on Instagram, TikTok, YouTube, and Facebook. For partnerships, get in touch.",
        body,
    )


def build_redirect():
    return """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex,follow"><meta http-equiv="refresh" content="0; url=/"><link rel="canonical" href="https://www.roamprints.studio/"><title>Roam Prints Studio</title></head><body><p>This page has moved. <a href="/">Go to Roam Prints Studio.</a></p></body></html>"""


def build_sitemap():
    today = date.today().isoformat()
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{SITE_URL}/</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>
</urlset>
"""


def write_file(filename, contents):
    (OUT / filename).write_text(contents, encoding="utf-8")


write_file("index.html", build_home())
for filename in LEGACY_PAGES:
    write_file(filename, build_redirect())
write_file("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
write_file("sitemap.xml", build_sitemap())
print("Built animated Roam Prints landing page.")
