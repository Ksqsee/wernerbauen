"""Page "Für Hausverwaltungen" (damage reporting) and the project request CTA. Writes out-hv/*.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import header_lux, pagehero, steps_section, wizard, footer_lux, photo  # noqa

D = os.path.dirname(os.path.abspath(__file__))
TEAM = {p['name']: p for p in json.load(open(os.path.join(D, 'out-about/4-people.json')))['onepage']['control']['people']['default']}
def person(name): p = TEAM[name]; return {'photo': p['photo'], 'name': p['name'], 'role': p['role']}

HV_LEFT = {
    'eyebrow': 'Für Hausverwaltungen, Hausmeister & Vermieter',
    'title': 'Schaden melden. Wir kümmern uns.',
    'text': 'Adresse, Wohnung und gern ein paar Fotos – mehr brauchen wir nicht. Den Rest klären wir direkt mit Ihren Mietern.',
    'checks': ['Adresse und Bereich genügen', 'Mehrere Wohnungen in einem Formular', 'Rückruf am selben Werktag'],
}
PROJECT_LEFT = {
    'eyebrow': 'Projekt anfragen',
    'title': 'Erzählen Sie uns von Ihrem Projekt.',
    'text': 'Ein paar Klicks genügen. Schicken Sie gern Fotos mit – den Rest besprechen wir persönlich mit Ihnen.',
    'timeline': [
        {'big': 'Heute', 'label': 'Anfrage per Formular, Telefon oder E-Mail', 'sub': 'Das Formular ist rund um die Uhr erreichbar'},
        {'big': 'Noch heute', 'label': 'Rückruf aus unserem Haus', 'sub': 'Am selben Werktag, direkt von der Projektleitung'},
        {'big': 'Vor Ort', 'label': 'Besichtigung und Angebot', 'sub': 'Termin nach Ihren Wünschen'},
    ],
}

STEPS = steps_section(
    'So läuft’s', 'Vier Schritte. Drei davon übernehmen wir.',
    'Sie melden uns den Schaden. Um Termine mit den Mietern, die Arbeit vor Ort und die Rückmeldung kümmern wir uns.',
    [
        {'who': 'Sie', 'title': 'Schaden melden', 'text': 'Adresse, Wohnung und – wenn vorhanden – Fotos ins Formular. Mehrere Wohnungen auf einmal sind kein Problem.'},
        {'who': 'Wir', 'title': 'Termin mit den Mietern', 'text': 'Wir stimmen den Termin direkt mit Ihren Mietern ab und sehen uns den Schaden vor Ort an.'},
        {'who': 'Wir', 'title': 'Instandsetzung aus einer Hand', 'text': 'Maurer-, Putz- und Malerarbeiten, Sanitär, Elektro, Böden und Fliesen – koordiniert von einem Ansprechpartner.'},
        {'who': 'Wir', 'title': 'Rückmeldung an Sie', 'text': 'Sie erfahren, was gemacht wurde. Die Rechnung geht an Sie oder Ihre Hausverwaltung.'},
    ],
    [
        {'title': 'Ein Ansprechpartner', 'text': 'Für alle Gewerke und alle Objekte. Sie müssen nichts selbst koordinieren.'},
        {'title': 'Rahmenverträge möglich', 'text': 'Mit der Hamburger Wohnungswirtschaft arbeiten wir seit vielen Jahren partnerschaftlich zusammen.'},
        {'title': 'Termingerecht', 'text': 'Leerstand kostet. Wir planen so, dass Wohnungen schnell wieder bewohnt werden können.'},
    ])

hero_img = photo('fassade-sanierung-balkon-5.jpg')
OUT = {
    'hv-1-header.json': header_lux('/hausverwaltungen'),
    'hv-2-hero.json': pagehero(hero_img['image'], hero_img['alt'], 'Für Hausverwaltungen, Hausmeister & Vermieter', 'Sie melden den Schaden. Wir erledigen den Rest.', 'lg'),
    'hv-3-steps.json': STEPS,
    'hv-4-wizard.json': wizard('damage', 'd45ddd4b-26db-45c8-8198-4bc1e78ec413', HV_LEFT, person('Christoph Kapust')),
    'hv-5-footer.json': footer_lux(),
    'project-wizard.json': wizard('project', 'd0866296-4379-4bce-9327-0da2d5a726cf', PROJECT_LEFT, person('Meik Thie')),
}
if __name__ == '__main__':
    os.makedirs(os.path.join(D, 'out-hv'), exist_ok=True)
    for n, p in OUT.items():
        json.dump(p, open(os.path.join(D, 'out-hv', n), 'w'), indent=2, ensure_ascii=False)
    print(sorted(OUT))


def process_section():
    from gen import pkg, c
    st = STEPS['onepage']['control']
    steps = [dict(x) for x in st['steps']['default']]
    ph = lambda n: photo(n)['image']
    extra = [
        {'panelTitle': 'Neue Schadensmeldung', 'status': 'Eingegangen',
         'panelRows': 'Objekt | Beispielstraße 12, Hamburg\nWohnung | 1. OG links\nSchaden | Feuchtigkeit im Bad\nDringlichkeit | Zeitnah',
         'photo1': ph('Wohnungssanierung-Badezimmer-1a-vorher.jpg'), 'photo2': ph('Wohnungssanierung-Flur-1a-vorher.jpg'), 'photo3': ph('Wohnungssanierung-Kueche-1a-vorher.jpg'),
         'footer': 'Meldung bestätigt – Rückruf am selben Werktag'},
        {'panelTitle': 'Termin mit den Mietern', 'status': 'Abgestimmt',
         'panelDays': 'Mo | 12\nDi | 13\nMi | 14 | 10:00 Besichtigung\nDo | 15\nFr | 16',
         'panelRows': 'Mieter | informiert\nZugang | über den Mieter',
         'footer': 'Termin direkt mit den Mietern vereinbart'},
        {'panelTitle': 'Instandsetzung', 'status': 'In Arbeit',
         'panelBars': 'Maurerarbeiten | 100\nPutz | 100\nSanitär | 80\nMalerarbeiten | 45\nBöden | 0',
         'footer': 'Ein Ansprechpartner koordiniert alle Gewerke'},
        {'panelTitle': 'Rückmeldung an Sie', 'status': 'Abgeschlossen',
         'panelRows': 'Arbeiten | abgeschlossen\nRückmeldung | was gemacht wurde\nRechnung | an Sie oder Ihre Hausverwaltung',
         'photo1': ph('Wohnungssanierung-Badezimmer-1c-nachher.jpg'), 'photo2': ph('Wohnungssanierung-Badezimmer-1d-nachher.jpg'),
         'footer': 'Abschluss an die Hausverwaltung gemeldet'},
    ]
    keys = ['panelTitle', 'status', 'panelRows', 'panelDays', 'panelBars', 'photo1', 'photo2', 'photo3', 'photo1Label', 'photo2Label', 'photo3Label', 'footer']
    for s, e in zip(steps, extra):
        for k in keys:
            s[k] = e.get(k, '' if 'photo' not in k or 'Label' in k else None)
        for k in ('photo1', 'photo2', 'photo3'):
            if s[k] is None:
                s[k] = {'src': '', 'name': '', 'width': 0, 'height': 0}
    T = lambda t, ty='text': {'title': t, 'type': ty}
    items = {'who': T('Wer (Sie/Wir)'), 'title': T('Titel'), 'text': T('Text'),
             'panelTitle': T('Fenster: Titel'), 'status': T('Fenster: Status'),
             'panelRows': T('Fenster: Zeilen (Bezeichnung | Wert)'), 'panelDays': T('Fenster: Kalender (Tag | Datum | Termin)'),
             'panelBars': T('Fenster: Balken (Gewerk | Prozent)'),
             'photo1': T('Foto 1', 'media'), 'photo2': T('Foto 2', 'media'), 'photo3': T('Foto 3', 'media'),
             'photo1Label': T('Foto 1 Beschriftung'), 'photo2Label': T('Foto 2 Beschriftung'), 'photo3Label': T('Foto 3 Beschriftung'),
             'footer': T('Fenster: Fußzeile')}
    ctl = {
        'eyebrow': c('Überzeile', 'text', st['eyebrow']['default'], 'content', 'head'),
        'title': c('Überschrift', 'text', st['title']['default'], 'content', 'head'),
        'intro': c('Text', 'text', st['intro']['default'], 'content', 'head'),
        'panelLabel': c('Fenster: Bezeichnung oben', 'text', 'Werner Bau · Auftrag', 'content', 'head'),
        'exampleLabel': c('Fenster: Hinweis „Beispiel“', 'text', 'Beispiel', 'content', 'head'),
        'seconds': c('Sekunden pro Schritt', 'number', 6, 'content', 'head'),
        'steps': c('Schritte', 'array', steps, 'content', 'steps', items=items),
        'benefits': c('Vorteile', 'array', st['benefits']['default'], 'content', 'benefits', items={'title': T('Titel'), 'text': T('Text')}),
    }
    return pkg('process', ctl, {'head': {'title': 'Überschrift & Fenster'}, 'steps': {'title': 'Schritte'}, 'benefits': {'title': 'Vorteile'}})


if __name__ == '__main__':
    json.dump(process_section(), open(os.path.join(D, 'out-hv', 'hv-3-process.json'), 'w'), indent=2, ensure_ascii=False)
    print('process ok')
