#!/usr/bin/env python3
# Generate state pages for all services from the Texas template.
# Usage: python3 gen_state.py <state-name> <slug> <multiplier> <narrative-file>
# Maps national prices x mult, swaps narrative + CALC mult, updates sitemap/urls.
import re, os, sys

state, slug, mult = sys.argv[1], sys.argv[2], float(sys.argv[3])
NARR = open(sys.argv[4]).read().strip()
TPL_MULT = 0.94  # texas template multiplier

def fmt(v):
    return f"{v:.2f}" if v < 100 else f"{v:,.0f}"

services = [d for d in os.listdir('.') if os.path.isdir(d) and os.path.exists(f'{d}/texas/index.html')]
for svc in services:
    tx = open(f'{svc}/texas/index.html').read()
    nat = open(f'{svc}/index.html').read()
    nat_vals = []
    for m in re.finditer(r'\$([0-9][0-9,.]*)', nat):
        v = float(m.group(1).replace(',', ''))
        if v not in nat_vals:
            nat_vals.append(v)
    out = re.sub(r'<p>Texas labor.*?</p>', NARR, tx, flags=re.S)
    out = out.replace('Texas', state).replace('texas', slug)
    for v in nat_vals:
        s_tx = fmt(round(v * TPL_MULT, 2) if v < 100 else v * TPL_MULT)
        s_new = fmt(round(v * mult, 2) if v < 100 else v * mult)
        if s_tx != s_new:
            out = out.replace(f'${s_tx}', f'${s_new}')
    def fix(m):
        v = float(m.group(1).replace(',', ''))
        base = v / TPL_MULT
        if base >= 100 and abs(base - round(base, 2)) < 1e-9:
            return '$' + fmt(base * mult)
        return m.group(0)
    out = re.sub(r'\$([0-9][0-9,.]*)', fix, out)
    out = out.replace(f'"mult": {TPL_MULT}', f'"mult": {mult}')
    os.makedirs(f'{svc}/{slug}', exist_ok=True)
    open(f'{svc}/{slug}/index.html', 'w').write(out)

sm = open('sitemap.xml').read()
if f'/{slug}/' not in sm:
    add = ''.join(f'<url><loc>https://projectpricely.pages.dev/{s}/{slug}/</loc></url>\n' for s in services)
    sm = sm.replace('</urlset>', add + '</urlset>')
    open('sitemap.xml', 'w').write(sm)
    with open('urls.txt', 'a') as f:
        for s in services:
            f.write(f'https://projectpricely.pages.dev/{s}/{slug}/\n')
print(f'{state}: {len(services)} pages at {mult}x')
