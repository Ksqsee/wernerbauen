"""New homepage: cinematic full-screen hero, service tiles, before/after band. Writes out-home2/*.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import photo, pkg, c  # noqa
import refspage  # noqa

D = os.path.dirname(os.path.abspath(__file__))
SLIDES = [
    ('banner-1.jpg', 'Historisches Schulgebäude', 'Saniertes historisches Schulgebäude mit heller Fassade und Schulhof'),
    ('banner-2.jpg', 'Altbauwohnung', 'Sanierte Altbauwohnung mit Dielenboden und Stuckleisten'),
    ('banner-4.jpg', 'Backsteinschule', 'Hamburger Backsteinschule mit verglastem Treppenturm und Schulhof'),
]


def hero2():
    S = []
    for n, cap, alt_text in SLIDES:
        ph = photo(n, alt_text)
        ph['image'].update({'width': 2000, 'height': 720})
        S.append({'image': ph['image'], 'alt': alt_text, 'caption': ''})
    ctl = {
        'eyebrow': c('Überzeile', 'text', '', 'content', 'copy'),
        'headline': c('Überschrift', 'text', 'Hamburg bleibt schön.', 'content', 'copy'),
        'accent': c('Überschrift zweite Zeile (hell)', 'text', 'Dafür sorgen wir.', 'content', 'copy'),
        'sub': c('Text', 'text', '', 'content', 'copy'),
        'trust': c('Vertrauenszeile (eine Zeile pro Punkt)', 'text', '', 'content', 'copy'),
        'primaryLabel': c('Button Text', 'text', 'Projekt anfragen', 'content', 'buttons'),
        'primaryHref': c('Button Link', 'text', '#anfrage', 'content', 'buttons'),
        'secondaryLabel': c('Zweiter Button Text', 'text', 'Referenzen ansehen', 'content', 'buttons'),
        'secondaryHref': c('Zweiter Button Link', 'text', '/referenzen', 'content', 'buttons'),
        'slides': c('Fotos (wechseln automatisch)', 'array', S, 'content', 'slides', items={
            'image': {'title': 'Foto', 'type': 'media'}, 'alt': {'title': 'Alt-Text', 'type': 'text'}, 'caption': {'title': 'Beschriftung unten', 'type': 'text'}}),
        'interval': c('Sekunden pro Foto', 'number', 7, 'content', 'slides'),
    }
    return pkg('hero2', ctl, {'copy': {'title': 'Text'}, 'buttons': {'title': 'Buttons'}, 'slides': {'title': 'Fotos'}})


def tiles():
    T = [
        ('fassade-oberfinanzdirektion-1.jpg', 'Fassadensanierung & Denkmalschutz', 'Backstein, Sandstein, Stuck: Wir sanieren Fassaden und denkmalgeschützte Gebäude fachgerecht – bis ins Detail.', '/fassadensanierung'),
        ('Wohnungssanierung-1-Flur.jpg', 'Wohnungs- & Gebäudesanierung', 'Vom Leerstand zur bezugsfertigen Wohnung: alle Gewerke aus einer Hand, termingerecht umgesetzt.', '/wohnungs-gebaeudesanierung'),
        ('c_0302_1000px.jpg', 'Schulen & öffentliche Einrichtungen', 'Seit Jahrzehnten Partner öffentlicher Auftraggeber in Hamburg – präqualifiziert nach VOB.', '/oeffentliche-einrichtungen'),
    ]
    items = []
    for n, t, x, h in T:
        ph = photo(n)
        items.append({'image': ph['image'], 'alt': ph['alt'], 'title': t, 'text': '', 'href': h})
    ctl = {
        'eyebrow': c('Überzeile', 'text', '', 'content', 'root'),
        'title': c('Überschrift', 'text', 'Was wir machen.', 'content', 'root'),
        'items': c('Kacheln', 'array', items, 'content', 'root', items={
            'image': {'title': 'Foto', 'type': 'media'}, 'alt': {'title': 'Alt-Text', 'type': 'text'}, 'title': {'title': 'Titel', 'type': 'text'},
            'text': {'title': 'Ein Satz', 'type': 'text'}, 'href': {'title': 'Link', 'type': 'text'}}),
        'moreLabel': c('Link Text', 'text', '', 'content', 'root'),
    }
    return pkg('tiles', ctl, {})


def compare():
    p = refspage.refs()
    ctl = p['onepage']['control']
    for k in ('eyebrow', 'title', 'intro'):
        ctl[k]['default'] = ''
    ctl['photos']['default'] = []
    ctl['compareTitle']['default'] = 'Vorher. Nachher. Sehen Sie selbst.'
    ctl['compareLinkLabel']['default'] = 'Alle Referenzen ansehen'
    ctl['compareLinkHref']['default'] = '/referenzen'
    keep = {'Villa – Fassade'}
    ctl['compareEyebrow']['default'] = ''
    ctl['compareText']['default'] = ''
    ctl['pairs']['default'] = [x for x in ctl['pairs']['default'] if x['title'] in keep]
    return p



SHOW = [
    ('fassade-oberfinanzdirektion-5.jpg', 'Oberfinanzdirektion Hamburg', 'Fassade & Denkmalschutz', True),
    ('fassadensanierung-hamburg-1.jpg', 'Hauseingang mit Karyatiden', 'Fassade & Denkmalschutz', False),
    ('Wohnungssanierung-Fensterbank.jpg', 'Altbaudetails', 'Wohnungssanierung', False),
    ('b_9908_1000px.jpg', 'Schulgebäude mit heller Fassade', 'Öffentliche Einrichtungen', True),
    ('fassade-sanierung-balkon-1.jpg', 'Altbaubalkone', 'Fassadensanierung', False),
    ('Wohnungssanierung-Badezimmer-1c-nachher.jpg', 'Badezimmer', 'Wohnungssanierung', False),
    ('c_0006_1000px.jpg', 'Historische Backsteinschule', 'Öffentliche Einrichtungen', True),
    ('fassadensanierung-hamburg-experten.jpg', 'Stadtvilla', 'Fassadensanierung', False),
    ('c_0757_1000px.jpg', 'Schulmensa', 'Öffentliche Einrichtungen', False),
    ('fassadensanierung-hamburg-16.jpg', 'Altbaufassaden', 'Fassadensanierung', True),
]


def showcase():
    items = []
    for n, t, cat, wide in SHOW:
        ph = photo(n)
        items.append({'image': ph['image'], 'alt': ph['alt'], 'title': t, 'category': cat, 'href': '/referenzen', 'wide': wide})
    ctl = {
        'eyebrow': c('Überzeile', 'text', 'Referenzen', 'content', 'root'),
        'title': c('Überschrift', 'text', 'Unsere Arbeit.', 'content', 'root'),
        'linkLabel': c('Link Text', 'text', 'Alle Referenzen', 'content', 'root'),
        'linkHref': c('Link', 'text', '/referenzen', 'content', 'root'),
        'cursorLabel': c('Text im Maus-Cursor', 'text', 'Ansehen', 'content', 'root'),
        'items': c('Projekte', 'array', items, 'content', 'items', items={
            'image': {'title': 'Foto', 'type': 'media'}, 'alt': {'title': 'Alt-Text', 'type': 'text'}, 'title': {'title': 'Titel', 'type': 'text'},
            'category': {'title': 'Kategorie', 'type': 'text'}, 'href': {'title': 'Link', 'type': 'text'}, 'wide': {'title': 'Breites Bild', 'type': 'checkbox'}}),
    }
    return pkg('showcase', ctl, {'root': {'title': 'Text'}, 'items': {'title': 'Projekte'}})


if __name__ == '__main__':
    out = os.path.join(D, 'out-home2'); os.makedirs(out, exist_ok=True)
    for n, p in {'hero2.json': hero2(), 'tiles.json': tiles(), 'compare.json': compare(), 'showcase.json': showcase()}.items():
        json.dump(p, open(os.path.join(out, n), 'w'), indent=2, ensure_ascii=False)
    print(sorted(os.listdir(out)))
