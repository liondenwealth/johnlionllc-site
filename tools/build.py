#!/usr/bin/env python3
"""Generate index.html and apps/<slug>/index.html from tools/apps.json."""
import html, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
apps = [a for a in json.load(open(os.path.join(ROOT, "tools", "apps.json"))) if not a.get("hidden")]
e = html.escape

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="/"><svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="16" fill="var(--accent)"/><text x="32" y="43" text-anchor="middle" font-family="Georgia, serif" font-size="30" font-weight="700" fill="#0b0d12">JL</text></svg><span>JOHN LION LLC</span></a>
  <nav class="nav">
    <a href="/#apps"{apps_cur}>Apps</a>
    <a href="/support.html">Support</a>
    <a href="/privacy.html">Privacy</a>
  </nav>
</div></header>
<main>
"""
FOOT = """</main>
<footer><div class="wrap">
  <span>&copy; 2026 John Lion LLC. All rights reserved.</span>
  <span><a href="/support.html">Support</a> &nbsp;·&nbsp; <a href="/privacy.html">Privacy Policy</a> &nbsp;·&nbsp; <a href="mailto:support@johnlionllc.com">support@johnlionllc.com</a></span>
</div></footer>
{script}</body>
</html>
"""


def badge(a):
    cls = "badge out" if a["status"] == "out" else "badge"
    return f'<span class="{cls}">{e(a["statusLabel"])}</span>'


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(text)


# ---------- home ----------
slides = "".join(
    f'''<a class="slide" href="{a["page"]}" style="--c:{a["accent"]}">
      <img src="/img/hero/{a["slug"]}.jpg" alt="" {"" if i == 0 else 'loading="lazy"'}>
      <div class="cap">{badge(a)}<h2>{e(a["name"])}</h2><p>{e(a["tagline"])}</p><span class="pill">Learn more</span></div>
    </a>'''
    for i, a in enumerate([x for x in apps if x.get("featured")])
)
nfeat = sum(1 for x in apps if x.get("featured"))
dots = "".join(f'<i{" class=on" if i == 0 else ""}></i>' for i in range(nfeat))
tiles = "".join(
    f'''<a class="tile" href="{a["page"]}" data-status="{a["status"]}" style="--c:{a["accent"]}">
      <div class="cover"><img src="/img/covers/{a["slug"]}.jpg" alt="{e(a["name"])} cover" loading="lazy" width="600" height="800">{badge(a)}</div>
      <h3>{e(a["name"])}</h3><p>{e(a["tagline"])}</p>
    </a>'''
    for a in apps
)
has_out = any(a["status"] == "out" for a in apps)
out_tab = '<button role="tab" aria-selected="false" data-f="out">Out now</button>' if has_out else ""

home_script = """<script>
(function(){
  var s=document.querySelector('.slides'),d=document.querySelectorAll('.dots i'),n=d.length,t;
  function idx(){return Math.round(s.scrollLeft/s.clientWidth)}
  function go(i){s.scrollTo({left:((i%n)+n)%n*s.clientWidth})}
  s.addEventListener('scroll',function(){var i=idx();d.forEach(function(x,k){x.classList.toggle('on',k===i)})});
  document.querySelector('.prev').onclick=function(){go(idx()-1)};
  document.querySelector('.next').onclick=function(){go(idx()+1)};
  function auto(){clearInterval(t);t=setInterval(function(){go(idx()+1)},6000)}
  if(!matchMedia('(prefers-reduced-motion: reduce)').matches){auto();s.addEventListener('pointerdown',function(){clearInterval(t)})}
  var tabs=document.querySelectorAll('.tabs button');
  tabs.forEach(function(b){b.onclick=function(){
    tabs.forEach(function(x){x.setAttribute('aria-selected',x===b)});
    document.querySelectorAll('.tile').forEach(function(el){el.hidden=b.dataset.f!=='all'&&el.dataset.status!==b.dataset.f});
  }});
})();
</script>
"""

home = HEAD.format(
    title="John Lion LLC", apps_cur=' aria-current="page"',
    desc="John Lion LLC makes thoughtful, private-by-default apps for iPhone.",
) + f"""<div class="lib-hero"><div class="wrap">
  <div class="carousel" aria-roledescription="carousel" aria-label="Featured apps">
    <div class="slides">{slides}</div>
    <button class="arrow prev" aria-label="Previous app">&#8249;</button>
    <button class="arrow next" aria-label="Next app">&#8250;</button>
    <div class="dots" aria-hidden="true">{dots}</div>
  </div>
</div></div>
<section id="apps" class="library"><div class="wrap">
  <h2>App library</h2>
  <p class="sub">Focused iPhone apps, made by one small studio.</p>
  <div class="tabs" role="tablist">
    <button role="tab" aria-selected="true" data-f="all">All</button>{out_tab}
    <button role="tab" aria-selected="false" data-f="soon">Coming soon</button>
  </div>
  <div class="tiles">{tiles}</div>
</div></section>
<section class="band"><div class="wrap">
  <h2>Useful apps, made with care.</h2>
  <p>John Lion LLC builds apps for creators, students and working people, designed to respect your time and keep your data on your device. Questions? <a href="mailto:support@johnlionllc.com">support@johnlionllc.com</a></p>
</div></section>
""" + FOOT.format(script=home_script)
write("index.html", home)

# ---------- app pages ----------
for a in apps:
    if a["page"].startswith("/timeflies"):
        continue  # keeps its hand-made page
    feats = "".join(
        f'<div class="feature"><div class="ic" aria-hidden="true">{ic}</div><h3>{e(h)}</h3><p>{e(p)}</p></div>'
        for ic, h, p in a.get("features", [])
    )
    shots = ""
    if a.get("shots"):
        figs = "".join(
            f'<figure><img src="/img/shots/{a["slug"]}/{s}.jpg" alt="{e(c)}" loading="lazy"><figcaption>{e(c)}</figcaption></figure>'
            for s, c in zip(a["shots"], a["shotCaptions"])
        )
        shots = f'<section><div class="wrap"><h2>A look inside</h2><div class="ap-shots">{figs}</div></div></section>'
    if a["status"] == "out":
        status = f'<div class="status-note">Available now on the App Store.</div>'
    else:
        status = f'<div class="status-note"><strong>{e(a["statusLabel"])}.</strong> Not on the App Store yet.</div>'
    note = f'<p class="status-note" style="margin-top:14px">{e(a["note"])}</p>' if a.get("note") else ""
    featsec = f'<section><div class="wrap"><h2>What it does</h2><div class="features">{feats}</div></div></section>' if feats else ""
    page = HEAD.format(
        title=f'{a["name"]} · John Lion LLC', apps_cur="", desc=a["blurb"],
    ) + f"""<div class="ap-hero" style="--c:{a["accent"]}">
  <img src="/img/hero/{a["slug"]}.jpg" alt="">
  <div class="wrap">
    <img class="ico" src="/img/icons/{a["slug"]}.png" alt="{e(a["name"])} app icon" width="120" height="120">
    <div><a class="crumb" href="/#apps">&larr; All apps</a><h1>{e(a["name"])}</h1><p class="tl">{e(a["tagline"])}</p></div>
  </div>
</div>
<div class="ap-body" style="--c:{a["accent"]}"><div class="wrap">
  <p class="lede">{e(a["blurb"])}</p>
  {status}{note}
</div></div>
{featsec}
{shots}
<section><div class="wrap">
  <h2>Questions?</h2>
  <p class="sub">See <a href="/support.html">Support</a> or read the <a href="/privacy.html">Privacy Policy</a>.</p>
</div></section>
""" + FOOT.format(script="")
    write(f'apps/{a["slug"]}/index.html', page)

print("built", len(apps), "apps")
