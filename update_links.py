#!/usr/bin/env python3
# Refresh the "cost by state" links block on every page. Discovers states from directories.
import os, re
services = sorted(d for d in os.listdir('.') if os.path.isdir(d) and os.path.exists(f'{d}/index.html') and not d.startswith('.'))
states = []
for svc in services:
    for sub in sorted(os.listdir(svc)):
        if os.path.exists(f'{svc}/{sub}/index.html'):
            nm = sub.replace('-', ' ').title()
            if (sub, nm) not in states:
                states.append((sub, nm))
def block(svc, current):
    name = svc.replace('-', ' ').title()
    links = [] if current == '' else ['<a href="/%s/">National</a>' % svc]
    links += ['<a href="/%s/%s/">%s</a>' % (svc, slug, nm) for slug, nm in states if slug != current]
    return ('<section><h2>%s cost by state</h2><p class="sub">Compare %s prices: %s</p></section>'
            % (name, name.lower(), ' &middot; '.join(links)))
count = 0
for svc in services:
    for rel, cur in [('index.html', '')] + [(f'{s}/index.html', s) for s, _ in states]:
        p = f'{svc}/{rel}'
        if not os.path.exists(p): continue
        html = open(p).read()
        new = block(svc, cur)
        if 'cost by state' in html:
            html2 = re.sub(r'<section><h2>[^<]* cost by state</h2><p class="sub">.*?</p></section>', new, html, count=1, flags=re.S)
        else:
            html2 = html.replace('<section class="srcs">', new + '<section class="srcs">', 1)
        if html2 != html:
            open(p, 'w').write(html2); count += 1
print('updated:', count, '| states:', len(states))
