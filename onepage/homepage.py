"""Start page in the calm split style: banner, the three services as 50/50 rows (text verbatim from
PAGES['start']), the WERNER BAU block and the footer. Writes out-home/<n>-<comp>.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pages  # noqa
from gen import split, hero, img, BANNER_ALT  # noqa

PHOTOS = {'/fassadensanierung': 'fassade-oberfinanzdirektion-9.jpg',
          '/wohnungs-gebaeudesanierung': 'Wohnungssanierung-1-Flur.jpg',
          '/oeffentliche-einrichtungen': 'c_0006_1000px.jpg'}

comp = {c: p for c, _t, p in pages.PAGES['start']}
items = comp['services']['onepage']['control']['items']['default']
rows = [{'title': it['title'], 'text': it['text'], 'linkLabel': it['linkLabel'], 'linkHref': it['linkHref'], 'photo': PHOTOS[it['linkHref']]} for it in items]
home = split(rows, [], heading='h2')
home['onepage']['control']['photos']['default'] = []

OUT = [('header', comp['header']), ('hero', hero(img(pages.BAN + 'banner-1.jpg'), BANNER_ALT['banner-1.jpg'], 'lg')),
       ('split', home), ('about', comp['about']), ('footer', comp['footer'])]
if __name__ == '__main__':
    os.makedirs('out-home', exist_ok=True)
    for i, (c, p) in enumerate(OUT, 1):
        json.dump(p, open('out-home/%d-%s.json' % (i, c), 'w'), indent=2, ensure_ascii=False)
        print(i, c)
