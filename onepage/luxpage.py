"""Draft of the new start page: luxurious header, full-screen hook, then the existing service rows, about and footer.
Writes out-lux/<n>-<comp>.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import homepage  # noqa
from gen import header_lux, hook  # noqa

SLIDES = [('fassade-oberfinanzdirektion-6.jpg', 'Oberfinanzdirektion Hamburg'),
          ('fassadensanierung-hamburg-3.jpg', 'Restaurierte Karyatiden am Hauseingang'),
          ('fassadensanierung-hamburg-13.jpg', 'Balustradenbalkon mit Stuckkonsolen'),
          ('fassade-sanierung-balkon-3.jpg', 'Instandgesetzter Altbaubalkon'),
          ('c_0006_1000px.jpg', 'Schulgebäude in Backstein, Hamburg')]
LINKS = [{'label': 'Fassadensanierung & Denkmalschutz', 'href': '/fassadensanierung'},
         {'label': 'Wohnungs- & Gebäudesanierung', 'href': '/wohnungs-gebaeudesanierung'},
         {'label': 'Schulen & öffentliche Einrichtungen', 'href': '/oeffentliche-einrichtungen'}]

comp = dict(homepage.OUT)
OUT = [('header', header_lux('/')), ('hook', hook(SLIDES, LINKS)), ('split', comp['split']), ('about', comp['about']), ('footer', comp['footer'])]
if __name__ == '__main__':
    os.makedirs('out-lux', exist_ok=True)
    for i, (c, p) in enumerate(OUT, 1):
        json.dump(p, open('out-lux/%d-%s.json' % (i, c), 'w'), indent=2, ensure_ascii=False)
        print(i, c, len(json.dumps(p)))
