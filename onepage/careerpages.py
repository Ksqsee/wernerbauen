"""Career page in German plus PL/RU/UK/TR, and the header of every German page with the language menu.
Writes out-lang/<page>/<n>-<comp>.json and out-lang/headers/<pagekey>.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pages  # noqa
from gen import header, hero, career, footer, img, alt, localize  # noqa
from i18n import T, career_tr  # noqa

FORM = '0739696d-3160-42d8-8269-ee2db280093c'
HERO_IMG = img(pages.F + 'fassadensanierung-hamburg-experten-2.jpg')
ACTIVE = {'start': '/', 'fassadensanierung': '/fassadensanierung', 'wohnung': '/wohnungs-gebaeudesanierung',
          'oeffentlich': '/oeffentliche-einrichtungen', 'ueber-uns': '/ueber-uns', 'kontakt': '/kontakt',
          'impressum': '/impressum', 'datenschutz': '/datenschutz', 'karriere': '/karriere'}


def career_page(lang):
    if lang == 'de':
        return [('header', header('/karriere')), ('hero', hero(HERO_IMG, alt('fassadensanierung-hamburg-experten-2.jpg'))),
                ('career', career(FORM)), ('footer', footer())]
    t = T[lang]
    slug = '/karriere-' + lang
    h = localize(header(slug, lang, '/karriere'), dict(t['header'], applyHref=slug + '#bewerben'))
    h['onepage']['control']['navItems']['default'] = [dict(n, href=slug) if n['href'] == '/karriere' else n
                                                      for n in h['onepage']['control']['navItems']['default']]
    return [('header', h), ('hero', hero(HERO_IMG, t['hero_alt'])), ('career', localize(career(FORM, lang), career_tr(lang))), ('footer', footer())]


if __name__ == '__main__':
    for lang in ['de', 'en', 'pl', 'ru', 'uk', 'tr']:
        d = 'out-lang/karriere-' + lang
        os.makedirs(d, exist_ok=True)
        for i, (c, p) in enumerate(career_page(lang), 1):
            json.dump(p, open('%s/%d-%s.json' % (d, i, c), 'w'), indent=2, ensure_ascii=False)
    os.makedirs('out-lang/headers', exist_ok=True)
    for key, active in ACTIVE.items():
        json.dump(header(active), open('out-lang/headers/%s.json' % key, 'w'), indent=2, ensure_ascii=False)
    print('ok')
