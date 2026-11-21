#!/usr/bin/env python3
"""Generates the Shopify theme files for the free planner pages into guides/shopify/theme/.

  python3 guides/shopify/build_shopify.py

Pages created in Shopify (both use their own template and a layout without the store header and footer):
  /pages/free-planner       landing page with the email sign-up (Shopify's own customer form)
  /pages/rhythm-planner     the interactive planner (opens for people who signed up)
"""
import io, re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
OUT = ROOT / "shopify" / "theme"
for d in ("assets", "layout", "sections", "templates"):
    (OUT / d).mkdir(parents=True, exist_ok=True)


def min_css(s: str) -> str:
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s*([{};,])\s*", r"\1", s)
    s = re.sub(r":\s+", ":", s)
    return s.strip()


def min_js(s: str) -> str:
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    lines = [ln.strip() for ln in s.splitlines()]
    return "\n".join(ln for ln in lines if ln and not ln.startswith("//"))


A = lambda name: "{{ '%s' | asset_url }}" % name

# ---------- images (kept small; they travel through the theme API) ----------
def small_png(src: str, out: str, width: int, colors: int):
    im = Image.open(SRC / "assets" / src).convert("RGBA")
    im = im.resize((width, round(width * im.height / im.width)), Image.LANCZOS)
    q = im.quantize(colors=colors, method=Image.Quantize.FASTOCTREE)
    q.save(OUT / "assets" / out, "PNG", optimize=True)

small_png("mark-gold.png", "ufd-mark-gold.png", 120, 4)  # tiny on purpose: files reach the theme through the API as text
small_png("word-ink.png", "ufd-word-ink.png", 320, 16)

# ---------- assets: css + js ----------
base = (SRC / "base.css").read_text()
(OUT / "assets" / "ufd-guide.css").write_text(min_css(base))
landing_css = min_css((SRC / "landing.css").read_text())
COVERMOCK_CSS = '.covermock{width:min(70%,330px);aspect-ratio:3/4.25;background:var(--aub);color:var(--cream);box-shadow:0 28px 50px -22px rgba(59,31,43,.6);transform:rotate(3deg);position:relative;padding:1.6rem 1.2rem;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;}.covermock::before{content:"";position:absolute;inset:9px;border:1px solid rgba(226,201,148,.5);}.cm-top,.cm-bot{position:absolute;left:0;right:0;font-size:.5rem;letter-spacing:.28em;text-transform:uppercase;color:var(--champ);}.cm-top{top:1.5rem;}.cm-bot{bottom:1.5rem;}.covermock .cm-mark{width:54px;margin:0 auto .9rem;}.cm-kick{font-size:.5rem;letter-spacing:.3em;text-transform:uppercase;color:var(--champ);margin:0 0 .7rem;}.cm-title{font-family:var(--serif);font-size:clamp(1.9rem,3.4vw,2.5rem);line-height:1;color:var(--cream);margin:0;}.cm-title i{color:var(--champ);}.cm-rule{display:block;width:34px;height:1px;background:var(--champ);margin:.9rem auto;}.cm-sub{font-family:var(--serif);font-style:italic;font-size:1rem;line-height:1.25;color:var(--cream);margin:0;max-width:16ch;}'
landing_css = re.sub(r"\.covers img\{width:min\(70%,340px\);[^}]*\}", lambda m: COVERMOCK_CSS, landing_css, count=1)
landing_css = landing_css.replace(".covers img{width:min(52%,220px);}", ".covermock{width:min(62%,250px);}")
(OUT / "assets" / "ufd-landing.css").write_text(landing_css)
common = (SRC / "common.js").read_text()
# the Shopify pages use Shopify's own customer form, so drop the browser-side sender and form handler
common = re.sub(r"  function send\(payload\).*?  function initCommon", """  function initGate() {
    var saved = store.get(KEY, null);
    if (saved) { unlock(saved.name); }
  }

  function initCommon""", common, flags=re.S)
(OUT / "assets" / "ufd-common.js").write_text(min_js(common))

planner = (SRC / "planner.html").read_text()
style = re.search(r"<style>\s*/\*@BASE_CSS\*/(.*?)</style>", planner, re.S).group(1)
(OUT / "assets" / "ufd-planner.css").write_text(min_css(style))
scripts = re.findall(r"<script>(.*?)</script>", planner, re.S)
app_js = [s for s in scripts if "PHASES" in s][0]
(OUT / "assets" / "ufd-planner.js").write_text(min_js(app_js))

# ---------- layout ----------
layout = """<!doctype html>
<html lang="{{ request.locale.iso_code }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{{ page_title }}{% if page_title != shop.name %} | {{ shop.name }}{% endif %}</title>
  {%- if page_description != blank -%}<meta name="description" content="{{ page_description | escape }}">{%- endif -%}
  <link rel="canonical" href="{{ canonical_url }}">
  {%- if settings.favicon != blank -%}<link rel="icon" type="image/png" href="{{ settings.favicon | image_url: width: 32, height: 32 }}">{%- endif -%}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,500;1,400;1,500&family=Poppins:wght@300;400;500&display=swap">
  <link rel="stylesheet" href="{{ 'ufd-guide.css' | asset_url }}">
  {{ content_for_header }}
</head>
<body>
  {{ content_for_layout }}
</body>
</html>
"""
(OUT / "layout" / "ufd-guide.liquid").write_text(layout)
(OUT / "templates" / "page.free-planner.liquid").write_text("{% layout 'ufd-guide' %}\n{% section 'ufd-free-planner' %}\n")
(OUT / "templates" / "page.rhythm-planner.liquid").write_text("{% layout 'ufd-guide' %}\n{% section 'ufd-rhythm-planner' %}\n")


def body_markup(html: str) -> str:
    m = re.search(r"<body>(.*)</body>", html, re.S).group(1)
    m = re.sub(r"<script>.*?</script>", "", m, flags=re.S)
    return m.strip()


def tokens(m: str) -> str:
    for t, a in (("@@MARK_LIGHT@@", "ufd-mark-gold.png"), ("@@MARK@@", "ufd-mark-gold.png"), ("@@WORD@@", "ufd-word-ink.png"), ("@@COVER_PLANNER@@", "ufd-cover-planner.jpg")):
        m = m.replace(t, A(a))
    return m


def compact_html(m: str) -> str:
    m = re.sub(r"<!--(?!\[).*?-->", "", m, flags=re.S)
    m = re.sub(r"\n\s+", "\n", m)
    return m.strip()


# ---------- landing section ----------
land = (SRC / "landing.html").read_text()
mk = body_markup(land)
GATE = """{%- form 'customer', id: 'ufd-form' -%}
  {%- if form.posted_successfully? -%}
    <script>try{localStorage.setItem('ufd:access',JSON.stringify({name:'',at:Date.now()}))}catch(e){}</script>
  {%- else -%}
  <div id="get" class="getanchor">
    <div class="formcard" id="gate-wrap">
      <h2>{{ section.settings.form_title }}</h2>
      <p class="small muted">{{ section.settings.form_intro }}</p>
      <input type="hidden" name="contact[tags]" value="free-planner,rhythm-of-the-body,newsletter">
      <div style="display:flex;flex-direction:column;gap:1rem;margin-top:1.1rem">
        <label class="field" for="g-name">First name
          <input id="g-name" name="contact[first_name]" type="text" autocomplete="given-name" placeholder="Your first name">
        </label>
        <label class="field" for="g-email">Email
          <input id="g-email" name="contact[email]" type="email" autocomplete="email" inputmode="email" placeholder="you@example.com" required>
        </label>
        <label class="check small" for="g-consent">
          <input id="g-consent" type="checkbox">
          <span>Yes, email me letters from Une Femme Divine. I can unsubscribe at any time.</span>
        </label>
        <p class="err" id="gate-err" role="alert">{%- if form.errors -%}{{ form.errors | default_errors }}{%- endif -%}</p>
        <button class="btn" type="submit">{{ section.settings.button_label }}</button>
      </div>
      <p class="fine">We send occasional letters, never spam, and we never share your email.</p>
    </div>
  </div>
  {%- endif -%}
{%- endform -%}
"""
THANKS = """<div class="thanks" id="thanks" data-locked hidden aria-live="polite">
  <p class="eyebrow">You are in</p>
  <p class="script" data-greet hidden style="color:var(--champ);margin:0 0 .3rem"></p>
  <h2>Your planner <i>is ready.</i></h2>
  <div class="row" style="margin-top:1.4rem"><a class="btn" href="{{ section.settings.planner_url }}">Open the planner</a><a class="btn ghost" href="{{ 'Rhythm-of-the-Body.pdf' | file_url }}" download>Download PDF</a></div>
  <p class="small">The online planner is interactive. The PDF can be printed or filled in on your screen. Save this page to find them again.</p>
  <p class="small">A link to your planner is also on its way to your inbox. If you do not see it, please check your spam folder.</p>
</div>
"""
mk = re.sub(r"<!--gate-->.*?<!--/gate-->", lambda m: GATE + THANKS, mk, flags=re.S)
mk = mk.replace('<h1>Rhythm of the Body, <i>your free planner.</i></h1>', '<h1>{{ section.settings.headline }}</h1>')
mk = mk.replace('<p class="eyebrow" style="margin-bottom:1.2rem">Free for you</p>', '<p class="eyebrow" style="margin-bottom:1.2rem">{{ section.settings.eyebrow }}</p>')
mk = re.sub(r'<p class="lead">A gentle cycle and self-care planner\..*?</p>', '<p class="lead">{{ section.settings.lead }}</p>', mk, count=1, flags=re.S)
mk = re.sub(r'<div class="covers" aria-hidden="true">.*?</div>', '<div class="covers" aria-hidden="true"><div class="covermock"><span class="cm-top">Une Femme Divine</span><img class="cm-mark" src="@@MARK@@" alt=""><p class="cm-kick">A gentle cycle planner</p><p class="cm-title">Rhythm of<br><i>the Body.</i></p><span class="cm-rule"></span><p class="cm-sub">See your month in four inner seasons.</p><span class="cm-bot">Made for women</span></div></div>', mk, count=1, flags=re.S)
mk = mk.replace('<a data-shop href="#" target="_blank" rel="noopener">Visit the shop</a>', '<a href="{{ routes.root_url }}">Visit the shop</a>')
mk = mk.replace('<a data-contact href="#">hello</a>', '<a href="mailto:help@unefemmedivine.com">help@unefemmedivine.com</a>')
mk = tokens(compact_html(mk))
cfg = ""
landing_js = """(function(){
var f=document.getElementById('ufd-form');
if(f){f.addEventListener('submit',function(e){
var em=f.querySelector('[name="contact[email]"]'),c=document.getElementById('g-consent'),err=document.getElementById('gate-err');
if(!em||!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{2,}$/.test(em.value.trim())){e.preventDefault();err.textContent='Please enter a valid email address.';return;}
if(!c.checked){e.preventDefault();err.textContent='Please tick the box so we can email you.';}
});}
document.addEventListener('ufd:unlocked',function(){var t=document.getElementById('top-cta');if(t){t.textContent='Your planner';}});
})();"""
(OUT / "assets" / "ufd-landing.js").write_text(landing_js)

section = f"""<link rel="stylesheet" href="{{{{ 'ufd-landing.css' | asset_url }}}}">
{mk}
<script>window.UFD_CONFIG={{guideId:'landing-free-planner',provider:'none',contactEmail:'help@unefemmedivine.com',shopUrl:'{{{{ routes.root_url }}}}'}};</script>
<script src="{{{{ 'ufd-common.js' | asset_url }}}}" defer></script>
<script src="{{{{ 'ufd-landing.js' | asset_url }}}}" defer></script>
{{% schema %}}
{{
  "name": "Free planner page",
  "settings": [
    {{ "type": "text", "id": "eyebrow", "label": "Small label", "default": "Free for you" }},
    {{ "type": "inline_richtext", "id": "headline", "label": "Headline", "default": "Rhythm of the Body, <em>your free planner.</em>" }},
    {{ "type": "textarea", "id": "lead", "label": "Intro text", "default": "A gentle cycle and self-care planner. See your month in four inner seasons, log how you feel, and add it all to your calendar. Join our email list to get it." }},
    {{ "type": "text", "id": "form_title", "label": "Form title", "default": "Get your free planner." }},
    {{ "type": "text", "id": "form_intro", "label": "Form intro", "default": "Tell us where to send your letters, and the planner is yours straight away." }},
    {{ "type": "text", "id": "button_label", "label": "Button label", "default": "Send me the planner" }},
    {{ "type": "text", "id": "planner_url", "label": "Planner page address", "default": "/pages/rhythm-planner" }}
  ],
  "presets": []
}}
{{% endschema %}}
"""
(OUT / "sections" / "ufd-free-planner.liquid").write_text(section)

# ---------- planner section ----------
pm = body_markup(planner)
pm = re.sub(r'<div class="gate-wrap" id="gate-wrap">.*?</ul>\s*</div>\s*</div>', """<div class="gate-wrap" id="gate-wrap">
<div class="card gate">
<h2>Open your <span class="it">planner.</span></h2>
<p class="small muted">The planner is free when you join our email list. It takes ten seconds.</p>
<p style="margin-top:1.2rem"><a class="btn" href="{{ routes.root_url }}pages/free-planner">Get the free planner</a></p>
</div>
</div>""", pm, count=1, flags=re.S)
pm = pm.replace('href="pdf/Rhythm-of-the-Body.pdf"', 'href="{{ \'Rhythm-of-the-Body.pdf\' | file_url }}"')
pm = pm.replace('<a data-shop href="#" target="_blank" rel="noopener">Visit the shop</a>', '<a href="{{ routes.root_url }}">Visit the shop</a>')
pm = tokens(compact_html(pm))
psec = f"""<link rel="stylesheet" href="{{{{ 'ufd-planner.css' | asset_url }}}}">
{pm}
<script>window.UFD_CONFIG={{guideId:'planner',provider:'none',contactEmail:'help@unefemmedivine.com',otherGuideUrl:'',shopUrl:'{{{{ routes.root_url }}}}'}};</script>
<script src="{{{{ 'ufd-common.js' | asset_url }}}}" defer></script>
<script src="{{{{ 'ufd-planner.js' | asset_url }}}}" defer></script>
{{% schema %}}
{{ "name": "Rhythm planner", "settings": [], "presets": [] }}
{{% endschema %}}
"""
(OUT / "sections" / "ufd-rhythm-planner.liquid").write_text(psec)

for p in sorted(OUT.rglob("*")):
    if p.is_file():
        print(f"{p.relative_to(OUT)}: {p.stat().st_size / 1024:.1f} KB")
