"""Split layout (50/50 text + photo rows, project cards) for the three service pages.
Text comes verbatim from the existing content blocks in pages.py; this file only pairs each block with a photo
and groups the gallery photos into project cards. Writes out-split/<page>.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pages  # noqa
from gen import split, project, UP  # noqa


def names(cat, test=lambda n: True):
    return [u['name'] for u in UP if u['cat'] == cat and test(u['name'])]


def num(n):
    return n.split('_')[1]


def blocks_of(key):
    for comp, _t, p in pages.PAGES[key]:
        if comp == 'content':
            return p['onepage']['control']['blocks']['default']


ROW_PHOTOS = {
    'fassadensanierung': ['fassade-oberfinanzdirektion-6.jpg', 'fassade-sanierung-hamburg.jpg', 'fassade-oberfinanzdirektion-1.jpg',
                          'fassade-sanierung-balkon-3.jpg', 'fassadensanierung-hamburg-18.jpg'],
    'wohnung': ['Wohnungssanierung-1-Flur.jpg', 'Wohnungssanierung-Badezimmer-1c-nachher.jpg', 'Wohnungssanierung-Fensterbank2.jpg',
                'Wohnungssanierung-Stuck.jpg'],
    'oeffentlich': ['c_0302_1000px.jpg', 'c_0757_1000px.jpg', 'b_9822_1000px.jpg', 'fassade-oberfinanzdirektion-2.jpg', 'c_0125_1000px.jpg'],
}

F_ALL = names('fassade')
W_ALL = names('wohnung')
MENSA = {'0750', '0757', '0764', '0771', '0778'}
INNEN = {'0069', '0071', '0083', '0086', '0192', '0612', '0622', '0779'}
DETAIL = {'0004', '0014', '0022', '0099', '0125', '0311', '0376', '0408', '0414', '0418', '0431', '0434', '0452', '0457', '0459', '0464', '0480', '0594'}
PAVILLON = {'0525', '0527', '0529', '0565', '0574', '0598', '0726', '0730', '0732', '0748'}
C = names('oeffentlich', lambda n: n.startswith('c_'))

PROJECTS = {
    'fassadensanierung': [
        project('Oberfinanzdirektion Hamburg', [n for n in F_ALL if 'oberfinanzdirektion' in n], 'fassade-oberfinanzdirektion-5.jpg'),
        project('Villa – vorher und nachher', [n for n in F_ALL if '_villa_' in n], 'fassadensanierung_villa_2b_nachher.jpg'),
        project('Altbaubalkone', [n for n in F_ALL if 'balkon' in n and 'experten' not in n], 'fassade-sanierung-balkon-3.jpg'),
        project('Stadtvillen und Eingänge', [n for n in F_ALL if 'experten' in n], 'fassadensanierung-hamburg-experten.jpg'),
        project('Altbaufassaden in Hamburg', [n for n in F_ALL if 'oberfinanz' not in n and 'balkon' not in n and 'experten' not in n and '_villa_' not in n],
                'fassadensanierung-hamburg-7.jpg'),
    ],
    'wohnung': [
        project('Altbauzimmer', [n for n in W_ALL if n.startswith('Wohnungssanierung-1a') or n.startswith('Wohnungssanierung-1b')], 'Wohnungssanierung-1b-nachher.jpg'),
        project('Badezimmer', [n for n in W_ALL if 'Badezimmer' in n], 'Wohnungssanierung-Badezimmer-1b-nachher.jpg'),
        project('Küche', [n for n in W_ALL if 'Kueche' in n], 'Wohnungssanierung-Kueche-1b-nacher.jpg'),
        project('Schlafzimmer', [n for n in W_ALL if 'Schlafzimmer' in n], 'Wohnungssanierung-Schlafzimmer-1b-nachher.jpg'),
        project('Flur', [n for n in W_ALL if 'Flur' in n], 'Wohnungssanierung-Flur-1b-nachher.jpg'),
        project('Details', [n for n in W_ALL if 'Fensterbank' in n or 'Stuck' in n], 'Wohnungssanierung-Fensterbank.jpg'),
    ],
    'oeffentlich': [
        project('Schulgebäude mit heller Fassade', names('oeffentlich', lambda n: n.startswith('b_')), 'b_9908_1000px.jpg'),
        project('Historische Schulfassaden', [n for n in C if num(n) not in MENSA | INNEN | DETAIL | PAVILLON], 'c_0006_1000px.jpg'),
        project('Eingänge und Bauschmuck', [n for n in C if num(n) in DETAIL], 'c_0014_1000px.jpg'),
        project('Pavillons und Erweiterungsbauten', [n for n in C if num(n) in PAVILLON], 'c_0730_1000px.jpg'),
        project('Mensen', [n for n in C if num(n) in MENSA], 'c_0764_1000px.jpg'),
        project('Treppenhäuser und Innenräume', [n for n in C if num(n) in INNEN], 'c_0083_1000px.jpg'),
    ],
}

if __name__ == '__main__':
    os.makedirs('out-split', exist_ok=True)
    for key, photos in ROW_PHOTOS.items():
        bl = blocks_of(key)
        assert len(bl) == len(photos), (key, len(bl))
        rows = [dict(b, photo=photos[i]) for i, b in enumerate(bl)]
        pk = split(rows, PROJECTS[key])
        total = sum(len(g) for g in PROJECTS[key])
        cat = {'fassadensanierung': 'fassade', 'wohnung': 'wohnung', 'oeffentlich': 'oeffentlich'}[key]
        assert total == len(names(cat)), (key, total, len(names(cat)))
        for g in PROJECTS[key]:
            assert sum(1 for p in g if p['cover']) == 1, (key, g[0]['project'])
        json.dump(pk, open('out-split/%s.json' % key, 'w'), indent=2, ensure_ascii=False)
        print(key, [(g[0]['project'], len(g)) for g in PROJECTS[key]])
