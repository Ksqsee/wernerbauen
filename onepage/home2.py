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
        S.append({'image': ph['image'], 'alt': alt_text, 'caption': cap})
    ctl = {
        'eyebrow': c('Überzeile', 'text', 'Werner Bau · Hamburg', 'content', 'copy'),
        'headline': c('Überschrift', 'text', 'Was Hamburg schön macht,', 'content', 'copy'),
        'accent': c('Überschrift zweite Zeile (hell)', 'text', 'machen wir wieder schön.', 'content', 'copy'),
        'sub': c('Text', 'text', 'Fassaden, Denkmäler, Wohnungen und Schulen – saniert von einem Hamburger Familienunternehmen mit fast 100 Jahren Erfahrung.', 'content', 'copy'),
        'trust': c('Vertrauenszeile (eine Zeile pro Punkt)', 'text', 'Familienunternehmen seit fast 100 Jahren\nPräqualifiziert für öffentliche Aufträge\nEin Unternehmen der GRUPPENWERK', 'content', 'copy'),
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
        items.append({'image': ph['image'], 'alt': ph['alt'], 'title': t, 'text': x, 'href': h})
    ctl = {
        'eyebrow': c('Überzeile', 'text', 'Leistungen', 'content', 'root'),
        'title': c('Überschrift', 'text', 'Drei Leistungen. Ein Anspruch: Qualität, die bleibt.', 'content', 'root'),
        'items': c('Kacheln', 'array', items, 'content', 'root', items={
            'image': {'title': 'Foto', 'type': 'media'}, 'alt': {'title': 'Alt-Text', 'type': 'text'}, 'title': {'title': 'Titel', 'type': 'text'},
            'text': {'title': 'Ein Satz', 'type': 'text'}, 'href': {'title': 'Link', 'type': 'text'}}),
        'moreLabel': c('Link Text', 'text', 'Mehr erfahren', 'content', 'root'),
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
    keep = {'Villa – Fassade', 'Altbauzimmer', 'Badezimmer', 'Küche'}
    ctl['pairs']['default'] = [x for x in ctl['pairs']['default'] if x['title'] in keep]
    return p


if __name__ == '__main__':
    out = os.path.join(D, 'out-home2'); os.makedirs(out, exist_ok=True)
    for n, p in {'hero2.json': hero2(), 'tiles.json': tiles(), 'compare.json': compare()}.items():
        json.dump(p, open(os.path.join(out, n), 'w'), indent=2, ensure_ascii=False)
    print(sorted(os.listdir(out)))
