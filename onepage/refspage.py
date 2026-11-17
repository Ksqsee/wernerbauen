"""Page "Referenzen": interactive gallery of all projects + before/after slider. Writes out-refs/*.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import header_lux, pagehero, footer_lux, photo, pkg, c, LINK_ITEMS  # noqa
from splitpages import PROJECTS  # noqa

D = os.path.dirname(os.path.abspath(__file__))
CATS = [{'key': 'fassade', 'label': 'Fassadensanierung'}, {'key': 'wohnung', 'label': 'Wohnungssanierung'}, {'key': 'oeffentlich', 'label': 'Schulen & öffentliche Einrichtungen'}]
CATKEY = {'fassadensanierung': 'fassade', 'wohnung': 'wohnung', 'oeffentlich': 'oeffentlich'}
PAIRS = [
    ('Villa – Fassade', 'fassadensanierung_villa_2a_vorher.jpg', 'fassadensanierung_villa_2b_nachher.jpg'),
    ('Villa – Giebel', 'fassadensanierung_villa_1a_vorher.jpg', 'fassadensanierung_villa_1b_nachher.jpg'),
    ('Altbauzimmer', 'Wohnungssanierung-1a-vorher.jpg', 'Wohnungssanierung-1b-nachher.jpg'),
    ('Badezimmer', 'Wohnungssanierung-Badezimmer-1a-vorher.jpg', 'Wohnungssanierung-Badezimmer-1b-nachher.jpg'),
    ('Küche', 'Wohnungssanierung-Kueche-1a-vorher.jpg', 'Wohnungssanierung-Kueche-1b-nacher.jpg'),
    ('Schlafzimmer', 'Wohnungssanierung-Schlafzimmer-1a-vorher.jpg', 'Wohnungssanierung-Schlafzimmer-1b-nachher.jpg'),
    ('Flur', 'Wohnungssanierung-Flur-1a-vorher.jpg', 'Wohnungssanierung-Flur-1b-nachher.jpg'),
]


def refs():
    photos = []
    for key, groups in PROJECTS.items():
        for g in groups:
            covers = [ph for ph in g if ph['cover']]
            after = [ph for ph in covers if 'nach' in ph['image']['name'].lower()]
            pick = (after or covers or g)[0]
            for ph in g:
                photos.append({'image': ph['image'], 'alt': ph['alt'], 'project': ph['project'], 'category': CATKEY[key], 'cover': ph is pick})
    pairs = []
    for t, b, a in PAIRS:
        pb, pa = photo(b), photo(a)
        pairs.append({'title': t, 'before': pb['image'], 'beforeAlt': pb['alt'], 'after': pa['image'], 'afterAlt': pa['alt']})
    ctl = {
        'eyebrow': c('Überzeile', 'text', 'Ausgewählte Projekte', 'content', 'intro'),
        'title': c('Überschrift', 'text', 'Fast 100 Jahre Hamburger Baugeschichte – Projekt für Projekt.', 'content', 'intro'),
        'intro': c('Einleitung', 'text', 'Fassaden, Wohnungen, Schulen und Denkmäler: Ein Auszug aus unserer Arbeit in Hamburg. Wählen Sie eine Leistung und öffnen Sie ein Projekt, um alle Fotos zu sehen.', 'content', 'intro'),
        'allLabel': c('Filter „Alle“', 'text', 'Alle Projekte', 'content', 'filters'),
        'categories': c('Kategorien (Schlüssel wie bei den Fotos)', 'array', CATS, 'content', 'filters', items={'key': {'title': 'Schlüssel', 'type': 'text'}, 'label': {'title': 'Name', 'type': 'text'}}),
        'compareEyebrow': c('Überzeile', 'text', 'Vorher / Nachher', 'content', 'compare'),
        'compareTitle': c('Überschrift', 'text', 'Der Unterschied liegt im Detail.', 'content', 'compare'),
        'compareText': c('Text', 'text', 'Ziehen Sie den Regler, um den Zustand vor und nach unserer Arbeit zu vergleichen.', 'content', 'compare'),
        'compareLinkLabel': c('Link Text (optional)', 'text', '', 'content', 'compare'),
        'compareLinkHref': c('Link (optional)', 'text', '', 'content', 'compare'),
        'pairs': c('Vorher-Nachher-Paare', 'array', pairs, 'content', 'compare', items={
            'title': {'title': 'Titel', 'type': 'text'}, 'before': {'title': 'Vorher', 'type': 'media'}, 'beforeAlt': {'title': 'Vorher Alt-Text', 'type': 'text'},
            'after': {'title': 'Nachher', 'type': 'media'}, 'afterAlt': {'title': 'Nachher Alt-Text', 'type': 'text'}}),
        'beforeLabel': c('Beschriftung Vorher', 'text', 'Vorher', 'content', 'compare'),
        'afterLabel': c('Beschriftung Nachher', 'text', 'Nachher', 'content', 'compare'),
        'photos': c('Fotos (gleicher Projektname + Kategorie = ein Projekt)', 'array', photos, 'content', 'photos', items={
            'image': {'title': 'Bild', 'type': 'media'}, 'alt': {'title': 'Alt-Text', 'type': 'text'}, 'project': {'title': 'Projekt', 'type': 'text'},
            'category': {'title': 'Kategorie-Schlüssel', 'type': 'text'}, 'cover': {'title': 'Titelbild', 'type': 'checkbox'}}),
        'photosLabel': c('Wort hinter Fotoanzahl', 'text', 'Fotos', 'content', 'labels'),
        'openLabel': c('Öffnen (Screenreader)', 'text', 'Fotos ansehen', 'content', 'labels'),
        'closeLabel': c('Schließen (Screenreader)', 'text', 'Schließen', 'content', 'labels'),
        'prevLabel': c('Zurück (Screenreader)', 'text', 'Vorheriges Bild', 'content', 'labels'),
        'nextLabel': c('Weiter (Screenreader)', 'text', 'Nächstes Bild', 'content', 'labels'),
        'sliderLabel': c('Regler (Screenreader)', 'text', 'Vorher-Nachher-Vergleich', 'content', 'labels'),
    }
    return pkg('refs', ctl, {'intro': {'title': 'Einleitung'}, 'filters': {'title': 'Filter'}, 'compare': {'title': 'Vorher / Nachher'}, 'photos': {'title': 'Projektfotos'}, 'labels': {'title': 'Beschriftungen'}})


if __name__ == '__main__':
    out = os.path.join(D, 'out-refs'); os.makedirs(out, exist_ok=True)
    hero = photo('fassadensanierung-hamburg-20.jpg')
    OUT = {'1-header.json': header_lux('/referenzen'), '2-hero.json': pagehero(hero['image'], hero['alt'], 'Referenzen', 'Unsere Projekte in Hamburg', 'lg'),
           '3-refs.json': refs(), '4-footer.json': footer_lux()}
    for n, p in OUT.items():
        json.dump(p, open(os.path.join(out, n), 'w'), indent=2, ensure_ascii=False)
    r = OUT['3-refs.json']['onepage']['control']
    print(len(r['photos']['default']), 'photos', len(r['pairs']['default']), 'pairs')
