import html, re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
OLD = os.path.join(HERE, '..', 'source'); OUT = os.path.join(HERE, '..')
STORE = "https://apps.apple.com/app/apple-store/id6819672437?pt=129569890&amp;ct=website&amp;mt=8"

def shell(title, desc, path, head, body):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · Idealize</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://idealizepalace.com/{path}">
<meta name="theme-color" content="#C9DFF3" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#16304D" media="(prefers-color-scheme: dark)">
<link rel="icon" type="image/png" href="/assets/img/favicon.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<header class="nav">
  <div class="wrap">
    <a class="brand" href="/"><img src="/assets/img/icon.png" alt="">Idealize</a>
    <nav>
      <a href="/#how">How it works</a>
      <a href="/#free">Free &amp; Pro</a>
      <a href="/support/">Support</a>
      <a class="btn small" href="{STORE}">Get the app</a>
    </nav>
  </div>
</header>
<main>
  <section class="sky page-head">
    <canvas class="stars" aria-hidden="true"></canvas>
    <div class="cloud" style="top:20%;width:460px;height:140px;animation-duration:130s;animation-delay:-60s"></div>
    <div class="wrap">{head}</div>
  </section>
  <article class="doc">
{body}
  </article>
</main>
<footer>
  <div class="wrap">
    <div>
      <a class="brand" href="/"><img src="/assets/img/icon.png" alt="">Idealize</a>
      <p class="small">Get it out of your head. Idealize is made for busy, scattered, ADHD brains. It isn't a medical app and doesn't diagnose or treat anything.</p>
    </div>
    <div class="links">
      <a href="/privacy/">Privacy Policy</a>
      <a href="/terms/">Terms of Use</a>
      <a href="/support/">Support</a>
      <a href="mailto:support@idealizepalace.com">support@idealizepalace.com</a>
    </div>
  </div>
</footer>
<script src="/assets/site.js"></script>
</body>
</html>
'''

def linkify(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'support@idealizepalace\.com', '<a href="mailto:support@idealizepalace.com">support@idealizepalace.com</a>', t)
    t = re.sub(r'(?<![/@\w.])(https://)?idealizepalace\.com(?![\w/])', '<a href="https://idealizepalace.com">idealizepalace.com</a>', t)
    return t

def legal(name, path, desc):
    rows = [l.rstrip('\n').split('\t', 1) for l in open(f'{OLD}/{name}.txt') if '\t' in l]
    start = next(i for i, (t, x) in enumerate(rows) if t == 'h2')
    end = max(i for i, (t, x) in enumerate(rows) if t == 'h2' and x == 'Idealize')
    title = rows[start][1]
    rest = rows[start + 1:end]
    updated = ''
    if rest and rest[0][1].startswith('Last updated'):
        updated = rest.pop(0)[1]
    out, in_list = [], False
    for t, x in rest:
        if t == 'li' and not in_list:
            out.append('    <ul>'); in_list = True
        if t != 'li' and in_list:
            out.append('    </ul>'); in_list = False
        out.append(f'    <{t}>{linkify(x)}</{t}>')
    if in_list: out.append('    </ul>')
    body = '\n'.join(out)
    head = f'<h1>{html.escape(title)}</h1><p class="muted">{html.escape(updated)}</p>'
    open(f'{OUT}/{path}/index.html', 'w').write(shell(title, desc, path + '/', head, body))
    return len(rest)

print('privacy', legal('privacy', 'privacy', 'How Idealize collects, uses, stores and protects your information.'))
print('terms', legal('terms', 'terms', 'The terms for using the Idealize app, website and related services.'))

faq = [l.strip().split('|', 1) for l in open(f'{OLD}/support-faq.txt') if '|' in l]
items = '\n'.join(f'      <details><summary>{html.escape(q)}</summary><p>{linkify(a)}</p></details>' for q, a in faq)
body = f'''    <div class="card">
      <h2 style="margin-top:0">Contact support</h2>
      <p>For help with Idealize, email <a href="mailto:support@idealizepalace.com">support@idealizepalace.com</a>. We aim to answer as soon as we can.</p>
      <p>Please include the email address on your Idealize account and a short description of the problem. Never send us your password or other sign-in details.</p>
      <p style="margin-top:18px"><a class="btn" href="mailto:support@idealizepalace.com">Email support</a></p>
    </div>
    <h2>Frequently asked questions</h2>
    <div class="faq" style="margin-top:20px">
{items}
    </div>
    <h2>Privacy &amp; legal</h2>
    <p>To learn how Idealize handles your information, read our <a href="/privacy/">Privacy Policy</a> and <a href="/terms/">Terms of Use</a>.</p>'''
head = '<h1>How can we help?</h1><p class="lead">Trouble with Idealize, your account or your subscription? The answers to common questions are below, or you can write to us.</p>'
open(f'{OUT}/support/index.html', 'w').write(shell('Support', 'Get help with Idealize, your account or your subscription.', 'support/', head, body))
print('support', len(faq))
