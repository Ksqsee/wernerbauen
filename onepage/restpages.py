"""Luxurious subpages: page hero with title, lead-only first split row, refined certificates, dark footer.
Writes out-rest/<page>/<comp>.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import pagehero, footer_lux, certs_lux  # noqa
from i18n import T  # noqa

D = os.path.dirname(os.path.abspath(__file__))
def load(p): return json.load(open(os.path.join(D, p)))
def heroimg(p): c = load(p)['onepage']['control']; return c['image']['default'], c['imageAlt']['default']

HERO = {  # page: (hero json for image, eyebrow, title, height)
    'fassadensanierung': ('out/fassadensanierung/2-hero.json', 'Leistungen', 'Fassadensanierung', 'lg'),
    'wohnung': ('out/wohnung/2-hero.json', 'Leistungen', 'Wohnungssanierung & Gebäuderevitalisierung', 'lg'),
    'oeffentlich': ('out/oeffentlich/2-hero.json', 'Leistungen', 'Schulen & öffentliche Einrichtungen', 'lg'),
    'ueber-uns': ('out/ueber-uns/2-hero.json', 'Unternehmen', 'Über uns', 'lg'),
    'kontakt': ('out/kontakt/2-hero.json', 'Werner Bau · Hamburg', 'Kontakt', 'md'),
    'impressum': ('out/impressum/2-hero.json', 'Rechtliches', 'Impressum', 'sm'),
    'datenschutz': ('out/datenschutz/2-hero.json', 'Rechtliches', 'Datenschutz', 'sm'),
    'karriere': ('out-lang/karriere-de/2-hero.json', 'Werner Bau · Hamburg', 'Karriere', 'md'),
}
for l in ['en', 'pl', 'ru', 'uk', 'tr']:
    HERO['karriere-' + l] = ('out-lang/karriere-%s/2-hero.json' % l, 'Werner Bau · Hamburg', T[l]['career']['title'], 'md')

SPLIT = {'fassadensanierung': 'out-split/fassadensanierung.json', 'wohnung': 'out-split/wohnung.json',
         'oeffentlich': 'out-split/oeffentlich.json', 'ueber-uns': 'out-about/3-split.json'}
CERTS = ['fassadensanierung', 'wohnung', 'oeffentlich', 'ueber-uns', 'kontakt']

if __name__ == '__main__':
    out = os.path.join(D, 'out-rest')
    for page, (src, eb, title, h) in HERO.items():
        os.makedirs(os.path.join(out, page), exist_ok=True)
        im, alt = heroimg(src)
        json.dump(pagehero(im, alt, eb, title, h), open(os.path.join(out, page, 'hero.json'), 'w'), indent=2, ensure_ascii=False)
    for page, src in SPLIT.items():
        p = load(src)
        p['onepage']['control']['headingMode']['default'] = 'lead'
        p['onepage']['control']['headingMode']['options'] = [{'value': 'h1first', 'label': 'Seitentitel (H1) mit Einleitung'}, {'value': 'lead', 'label': 'Einleitung ohne Überschrift (Titel steht im Banner)'}, {'value': 'h2', 'label': 'Normale Überschrift (H2)'}]
        p['onepage']['control']['blocks']['default'][0]['title'] = ''
        json.dump(p, open(os.path.join(out, page, 'split.json'), 'w'), indent=2, ensure_ascii=False)
    for page in CERTS:
        json.dump(certs_lux(load('out/%s/4-certs.json' % page)), open(os.path.join(out, page, 'certs.json'), 'w'), indent=2, ensure_ascii=False)
    os.makedirs(os.path.join(out, 'all'), exist_ok=True)
    json.dump(footer_lux(), open(os.path.join(out, 'all', 'footer.json'), 'w'), indent=2, ensure_ascii=False)
    for l in ['de', 'en', 'pl', 'ru', 'uk', 'tr']:
        p = load('out-lang/karriere-%s/3-career.json' % l)
        p['onepage']['control']['title']['default'] = ''
        json.dump(p, open(os.path.join(out, 'karriere' if l == 'de' else 'karriere-' + l, 'career.json'), 'w'), indent=2, ensure_ascii=False)
    print(sorted(os.listdir(out)))
