"""Page "Für Hausverwaltungen" (damage reporting) and the project request CTA. Writes out-hv/*.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import header_lux, pagehero, steps_section, wizard, footer_lux, photo  # noqa

D = os.path.dirname(os.path.abspath(__file__))
TEAM = {p['name']: p for p in json.load(open(os.path.join(D, 'out-about/4-people.json')))['onepage']['control']['people']['default']}
def person(name): p = TEAM[name]; return {'photo': p['photo'], 'name': p['name'], 'role': p['role']}

HV_LEFT = {
    'eyebrow': 'Für Hausverwaltungen & Vermieter',
    'title': 'Schaden melden. Wir kümmern uns.',
    'text': 'Adresse, Wohnung und gern ein paar Fotos – mehr brauchen wir nicht. Den Rest klären wir direkt mit Ihren Mietern.',
    'checks': ['Adresse und Wohnung genügen', 'Mehrere Wohnungen in einem Formular', 'Rückruf am selben Werktag'],
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
    'hv-2-hero.json': pagehero(hero_img['image'], hero_img['alt'], 'Für Hausverwaltungen & Vermieter', 'Sie melden den Schaden. Wir erledigen den Rest.', 'lg'),
    'hv-3-steps.json': STEPS,
    'hv-4-wizard.json': wizard('damage', 'd45ddd4b-26db-45c8-8198-4bc1e78ec413', HV_LEFT, person('Christoph Kapust')),
    'hv-5-footer.json': footer_lux(),
    'project-wizard.json': wizard('project', '', PROJECT_LEFT, person('Meik Thie')),
}
if __name__ == '__main__':
    os.makedirs(os.path.join(D, 'out-hv'), exist_ok=True)
    for n, p in OUT.items():
        json.dump(p, open(os.path.join(D, 'out-hv', n), 'w'), indent=2, ensure_ascii=False)
    print(sorted(OUT))
