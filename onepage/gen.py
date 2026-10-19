"""Generate package.json files (controls + page-specific defaults) for every section instance."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
UP = json.load(open(os.path.join(HERE, 'uploaded.json')))
BY_SRC = {u['src']: u for u in UP}
B = 'https://www.werner-bau.eu/files/nk24_contao/images/'


def img(path):
    u = BY_SRC.get(B + path)
    if not u or not u.get('url'):
        raise SystemExit('missing upload: ' + path)
    return {'src': u['url'], 'name': u['name'], 'width': u.get('width') or 1000, 'height': u.get('height') or 667}


def cat(c):
    return [{'image': {'src': u['url'], 'name': u['name'], 'width': u.get('width') or 1000, 'height': u.get('height') or 667}, 'alt': ''}
            for u in UP if u['cat'] == c and u.get('url')]


def pkg(name, control, groups):
    return {'name': name, 'dependencies': {}, 'onepage': {'control': control, 'group': groups}}


def c(title, type_, default, tab, group, **kw):
    d = {'title': title, 'type': type_, 'default': default, 'tab': tab, 'group': group}
    d.update(kw)
    return d


FULL = {'fullHeight': c('Full height', 'checkbox', False, 'layout', 'root')}
TONE = [{'value': 'white', 'label': 'Weiß'}, {'value': 'light', 'label': 'Hell (Stein)'}, {'value': 'dark', 'label': 'Dunkel'}]

PHONE = '040 / 35 70 32 — 74'
PHONE_HREF = 'tel:+494035703274'
EMAIL = 'info@werner-bau.eu'
NAV = [
    {'label': 'Start', 'href': '/'},
    {'label': 'Fassadensanierung', 'href': '/fassadensanierung'},
    {'label': 'Wohnungs- & Gebäudesanierung', 'href': '/wohnungs-gebaeudesanierung'},
    {'label': 'Öffentliche Einrichtungen', 'href': '/oeffentliche-einrichtungen'},
    {'label': 'Über uns', 'href': '/ueber-uns'},
    {'label': 'Kontakt', 'href': '/kontakt'},
]
LINK_ITEMS = {'label': {'title': 'Label', 'type': 'text'}, 'href': {'title': 'Link', 'type': 'text'}}


NAV_MAIN = [n for n in NAV if n['href'] != '/kontakt']


def header(active):
    ctl = {
        'logo': c('Logo', 'media', img('_themes/lightwhite/logo-wernerbau.svg'), 'content', 'brand'),
        'logoAlt': c('Logo Alt-Text', 'text', 'WERNER GMBH Bauunternehmung', 'content', 'brand'),
        'logoHref': c('Logo Link', 'text', '/', 'content', 'brand'),
        'email': c('E-Mail', 'text', EMAIL, 'content', 'meta'),
        'phone': c('Telefon', 'text', PHONE, 'content', 'meta'),
        'phoneHref': c('Telefon Link', 'text', PHONE_HREF, 'content', 'meta'),
        'contactLabel': c('Kontakt Text', 'text', 'Kontakt', 'content', 'meta'),
        'contactHref': c('Kontakt Link', 'text', '/kontakt', 'content', 'meta'),
        'navItems': c('Menüpunkte', 'array', NAV_MAIN, 'content', 'nav', items=LINK_ITEMS),
        'activeHref': c('Aktive Seite (Link)', 'text', active, 'content', 'nav'),
        'menuLabel': c('Menü öffnen Label', 'text', 'Menü öffnen', 'content', 'nav'),
        'closeLabel': c('Menü schließen Label', 'text', 'Menü schließen', 'content', 'nav'),
    }
    return pkg('header', ctl, {'brand': {'title': 'Logo'}, 'meta': {'title': 'Kontaktzeile'}, 'nav': {'title': 'Navigation'}})

def hero(image, alt, height='md'):
    ctl = {
        'image': c('Bannerbild', 'media', image, 'content', 'root'),
        'imageAlt': c('Bild Alt-Text', 'text', alt, 'content', 'root'),
        'height': c('Höhe', 'select', height, 'content', 'root', options=[{'value': 'lg', 'label': 'Groß'}, {'value': 'md', 'label': 'Mittel'}, {'value': 'sm', 'label': 'Klein'}]),
    }
    return pkg('hero', ctl, {})

def services(banner, items):
    ctl = {
        'bannerImage': c('Bannerbild', 'media', banner, 'content', 'root'),
        'bannerAlt': c('Banner Alt-Text', 'text', 'WERNER GMBH Bauunternehmung', 'content', 'root'),
        'anchorId': c('Anker-ID', 'text', 'leistungen', 'content', 'root'),
        'items': c('Leistungen', 'array', items, 'content', 'items', items={
            'image': {'title': 'Bild', 'type': 'media'}, 'title': {'title': 'Titel', 'type': 'text'},
            'text': {'title': 'Text', 'type': 'text'}, 'imageAlt': {'title': 'Alt-Text', 'type': 'text'},
            'linkLabel': {'title': 'Link Text', 'type': 'text'}, 'linkHref': {'title': 'Link', 'type': 'text'}}),
    }
    return pkg('services', ctl, {'items': {'title': 'Leistungen'}})

def about(title, subtitle, left, right, btn):
    ctl = {
        'title': c('Überschrift', 'text', title, 'content', 'root'),
        'subtitle': c('Unterzeile', 'text', subtitle, 'content', 'root'),
        'textLeft': c('Text links', 'text', left, 'content', 'root'),
        'textRight': c('Text rechts', 'text', right, 'content', 'root'),
        'buttonLabel': c('Link Text', 'text', btn[0], 'content', 'root'),
        'buttonHref': c('Link', 'text', btn[1], 'content', 'root'),
    }
    return pkg('about', ctl, {})

def content(blocks, images=None):
    full = [{'title': b.get('title', ''), 'text': b.get('text', ''), 'bullets': b.get('bullets', ''), 'textAfter': b.get('textAfter', '')} for b in blocks]
    ctl = {
        'blocks': c('Textblöcke', 'array', full, 'content', 'blocks', items={
            'title': {'title': 'Überschrift', 'type': 'text'},
            'text': {'title': 'Text (Absätze mit Leerzeile trennen, **fett**)', 'type': 'text'},
            'bullets': {'title': 'Aufzählung (eine Zeile pro Punkt)', 'type': 'text'},
            'textAfter': {'title': 'Text nach Aufzählung', 'type': 'text'}}),
        'images': c('Bilder (rechte Spalte)', 'array', images or [], 'content', 'images', items={'image': {'title': 'Bild', 'type': 'media'}, 'alt': {'title': 'Alt-Text', 'type': 'text'}}),
        'openLabel': c('Bild öffnen (Screenreader)', 'text', 'Bild vergrößern', 'content', 'images'),
        'closeLabel': c('Schließen (Screenreader)', 'text', 'Schließen', 'content', 'images'),
        'prevLabel': c('Zurück (Screenreader)', 'text', 'Vorheriges Bild', 'content', 'images'),
        'nextLabel': c('Weiter (Screenreader)', 'text', 'Nächstes Bild', 'content', 'images'),
    }
    return pkg('content', ctl, {'blocks': {'title': 'Text'}, 'images': {'title': 'Bilder'}})

def gallery(images, eyebrow='', title='', tone='light', initial=9):
    ctl = {
        'tone': c('Hintergrund', 'select', tone, 'styles', 'root', options=TONE),
        'eyebrow': c('Überzeile', 'text', eyebrow, 'content', 'root'),
        'title': c('Überschrift', 'text', title, 'content', 'root'),
        'images': c('Bilder', 'array', images, 'content', 'images', items={'image': {'title': 'Bild', 'type': 'media'}, 'alt': {'title': 'Alt-Text', 'type': 'text'}}),
        'initialCount': c('Anfangs sichtbar', 'number', initial, 'settings', 'labels'),
        'stepCount': c('Pro Klick nachladen', 'number', 9, 'settings', 'labels'),
        'moreLabel': c('Mehr-Button Text', 'text', 'Weitere Bilder anzeigen', 'content', 'labels'),
        'openLabel': c('Bild öffnen (Screenreader)', 'text', 'Bild vergrößern', 'content', 'labels'),
        'closeLabel': c('Schließen (Screenreader)', 'text', 'Schließen', 'content', 'labels'),
        'prevLabel': c('Zurück (Screenreader)', 'text', 'Vorheriges Bild', 'content', 'labels'),
        'nextLabel': c('Weiter (Screenreader)', 'text', 'Nächstes Bild', 'content', 'labels'),
    }
    return pkg('gallery', ctl, {'images': {'title': 'Bilder'}, 'labels': {'title': 'Beschriftungen'}})


SIVV = 'Unsere Mitarbeiter besitzen den SIVV-Befähigungsnachweis. Damit stellen wir sicher, Aufträge im Bereich der Betoninstandsetzung fachgerecht durchzuführen. Eine erfolgreiche Betoninstandsetzung erfordert objektgerechte Planung, Nutzung geprüfter und geeigneter Materialien und Verfahren sowie Praxiserfahrung – dies stellen wir durch den Besuch der SIVV-Seminare sowie der Erlangung der SIVV-Scheine sicher.'
TRGS = 'Früher vielfältig als Baustoff eingesetzt, weiß man heute um die gesundheitsgefährdenden Eigenschaften von Asbest. Sanierungsarbeiten kontaminierter Gebäude bedürfen entsprechend Know-how und Sorgfalt. Aus diesem Grund setzen wir auf gut geschulte Mitarbeiter und weisen unsere Qualifikation in der Asbestsanierung durch die Sachkundeprüfung für Arbeiten mit Asbest TRGS 519 nach.'
PQ = 'Wir sind für öffentliche Vergabeverfahren präqualifiziert. Mit der Präqualifikation weisen wir die Eignungsvoraussetzungen der VOB in Bezug auf unsere Fachkunde, Zuverlässigkeit und Leistungsfähigkeit nach.'
NBV = 'Als Mitglied des Norddeutschen Baugewerbeverbands halten wir uns auch hier ständig auf dem Laufenden was Neuerungen, gesetzliche Bestimmungen aber auch mögliche Förderungen für Kundenprojekte angeht.'


def certs():
    items = [
        {'logo': img('logo-sivv.png'), 'logoAlt': 'SIVV', 'title': 'SIVV', 'text': SIVV, 'linkLabel': 'Mehr erfahren', 'linkHref': '/ueber-uns'},
        {'logo': img('logo-trgs.png'), 'logoAlt': 'TRGS', 'title': 'Asbestsanierung - TRGS', 'text': TRGS, 'linkLabel': '', 'linkHref': ''},
        {'logo': img('logo-pq-vob.png'), 'logoAlt': 'PQ VOB', 'title': 'PQ VOB', 'text': PQ, 'linkLabel': '', 'linkHref': ''},
        {'logo': img('logo-handwerk.png'), 'logoAlt': 'Norddeutscher Baugewerbeverband e.V.', 'title': 'Norddeutscher Baugewerbeverband e.V.', 'text': NBV, 'linkLabel': '', 'linkHref': ''},
    ]
    ctl = {
        'items': c('Qualifikationen', 'array', items, 'content', 'items', items={
            'logo': {'title': 'Logo', 'type': 'media'}, 'logoAlt': {'title': 'Logo Alt-Text', 'type': 'text'},
            'title': {'title': 'Titel', 'type': 'text'}, 'text': {'title': 'Text', 'type': 'text'},
            'linkLabel': {'title': 'Link Text', 'type': 'text'}, 'linkHref': {'title': 'Link', 'type': 'text'}}),
    }
    return pkg('certs', ctl, {'items': {'title': 'Qualifikationen'}})


def team(intro, values, group, group_logo):
    TB = {'title': {'title': 'Überschrift', 'type': 'text'}, 'text': {'title': 'Text (Absätze mit Leerzeile trennen, **fett**)', 'type': 'text'}, 'big': {'title': 'Große Überschrift', 'type': 'checkbox'}}
    p = lambda photo, name, role, mail: {'photo': img('team/' + photo), 'name': name, 'role': role, 'phoneLabel': 'Rufnummer:', 'phone': '(040) 357 032-74', 'phoneHref': PHONE_HREF, 'emailLabel': 'E-Mail:', 'email': mail}
    people = [
        p('AxelSeehafer-Showroom-Lifestyle-Fotograf-Kathrin-Stahl-46.jpg', 'Meik Thie', 'Geschäftsführer', 'm.thie@werner-bau.eu'),
        p('AxelSeehafer-Showroom-Lifestyle-Fotograf-Kathrin-Stahl-31.jpg', 'Basri Köse', 'Projekt-/Bauleiter', 'b.koese@werner-bau.eu'),
        p('Christoph%20Kapust.jpg', 'Christoph Kapust', 'Projekt-/Bauleiter', 'c.kapust@werner-bau.eu'),
    ]
    ctl = {
        'introBlocks': c('Spalte links oben', 'array', intro, 'content', 'texts', items=TB),
        'valuesBlocks': c('Spalte rechts oben', 'array', values, 'content', 'texts', items=TB),
        'groupBlocks': c('Gruppe', 'array', group, 'content', 'group', items=TB),
        'groupLogo': c('Gruppenwerk Logo', 'media', group_logo, 'content', 'group'),
        'groupLogoAlt': c('Logo Alt-Text', 'text', 'GRUPPENWERK', 'content', 'group'),
        'people': c('Ansprechpartner', 'array', people, 'content', 'people', items={
            'photo': {'title': 'Foto', 'type': 'media'}, 'name': {'title': 'Name', 'type': 'text'}, 'role': {'title': 'Funktion', 'type': 'text'},
            'phoneLabel': {'title': 'Telefon Label', 'type': 'text'}, 'phone': {'title': 'Telefon', 'type': 'text'}, 'phoneHref': {'title': 'Telefon Link', 'type': 'text'},
            'emailLabel': {'title': 'E-Mail Label', 'type': 'text'}, 'email': {'title': 'E-Mail', 'type': 'text'}}),
    }
    return pkg('team', ctl, {'texts': {'title': 'Texte'}, 'group': {'title': 'Gruppe'}, 'people': {'title': 'Ansprechpartner'}})

def contact(form_id=''):
    ctl = {
        'infoTitle': c('Überschrift', 'text', 'Kontaktdaten', 'content', 'info'),
        'companyLines': c('Adresse (eine Zeile pro Eintrag)', 'text', 'WERNER GMBH\nBauunternehmung\nHeselstücken 10\n22453 Hamburg', 'content', 'info'),
        'phoneLabel': c('Telefon Label', 'text', 'Telefon', 'content', 'info'),
        'phone': c('Telefon', 'text', '(040) 357 032-74', 'content', 'info'),
        'phoneHref': c('Telefon Link', 'text', PHONE_HREF, 'content', 'info'),
        'faxLabel': c('Telefax Label', 'text', 'Telefax', 'content', 'info'),
        'fax': c('Telefax', 'text', '(040) 357 032-680', 'content', 'info'),
        'emailLabel': c('E-Mail Label', 'text', 'E-Mail', 'content', 'info'),
        'email': c('E-Mail', 'text', EMAIL, 'content', 'info'),
        'formTitle': c('Formular Überschrift', 'text', 'Senden Sie uns eine Nachricht', 'content', 'fields'),
        'firstNameLabel': c('Vorname', 'text', 'Vorname', 'content', 'fields'),
        'lastNameLabel': c('Nachname', 'text', 'Nachname', 'content', 'fields'),
        'companyLabel': c('Unternehmen', 'text', 'Unternehmen', 'content', 'fields'),
        'phoneFieldLabel': c('Rufnummer', 'text', 'Rufnummer', 'content', 'fields'),
        'emailFieldLabel': c('E-Mail Adresse', 'text', 'E-Mail Adresse', 'content', 'fields'),
        'messageLabel': c('Nachricht', 'text', 'Nachricht', 'content', 'fields'),
        'submitLabel': c('Absenden Button', 'text', 'Nachricht senden', 'content', 'fields'),
        'consentPre': c('Datenschutz-Hinweis (vor Link)', 'text', 'Mit dem Absenden des Formulars nehmen Sie unserer', 'content', 'notes'),
        'privacyLabel': c('Datenschutz Link Text', 'text', 'Datenschutzerklärung', 'content', 'notes'),
        'consentPost': c('Datenschutz-Hinweis (nach Link)', 'text', 'zur Kenntnis und akzeptieren diese.', 'content', 'notes'),
        'privacyHref': c('Datenschutz Link', 'text', '/datenschutz', 'content', 'notes'),
        'requiredNote': c('Pflichtfeld-Hinweis', 'text', 'Felder, welche mit * markiert sind, sind Pflichtfelder und müssen vor dem Absenden ausgefüllt werden.', 'content', 'notes'),
        'sendingLabel': c('Senden läuft', 'text', 'Wird gesendet …', 'content', 'messages'),
        'successText': c('Erfolgsmeldung', 'text', 'Vielen Dank für Ihre Nachricht. Wir melden uns schnellstmöglich bei Ihnen.', 'content', 'messages'),
        'errorText': c('Fehlermeldung', 'text', 'Die Nachricht konnte nicht gesendet werden. Bitte versuchen Sie es erneut oder rufen Sie uns an.', 'content', 'messages'),
        'requiredError': c('Pflichtfeld-Fehler', 'text', 'Bitte füllen Sie dieses Pflichtfeld aus.', 'content', 'messages'),
        'emailError': c('E-Mail-Fehler', 'text', 'Bitte geben Sie eine gültige E-Mail-Adresse ein.', 'content', 'messages'),
        'formId': c('CRM Formular-ID', 'text', form_id, 'settings', 'messages'),
    }
    return pkg('contact', ctl, {'info': {'title': 'Kontaktdaten'}, 'fields': {'title': 'Formularfelder'}, 'notes': {'title': 'Hinweise'}, 'messages': {'title': 'Meldungen & CRM'}})


FOOTER_BG = {'src': 'https://onecdn.io/media/fb608040-1adc-425e-8524-af41b2d94094/full', 'name': 'footer.jpg', 'width': 2000, 'height': 500}


def footer():
    ctl = {
        'background': c('Hintergrundbild', 'media', FOOTER_BG, 'content', 'brand'),
        'logo': c('Logo (hell)', 'media', img('_themes/lightwhite/logo-wernerbau-negative.svg'), 'content', 'brand'),
        'logoAlt': c('Logo Alt-Text', 'text', 'WERNER GMBH Bauunternehmung', 'content', 'brand'),
        'groupTitle': c('Gruppe Text', 'text', 'Ein Unternehmen von Gruppenwerk', 'content', 'group'),
        'groupLogo': c('Gruppenwerk Logo', 'media', img('Gruppenwerk_Unternehmen_weiss.png'), 'content', 'group'),
        'groupAlt': c('Gruppe Alt-Text', 'text', 'Zur Gruppenwerk Website', 'content', 'group'),
        'groupHref': c('Gruppe Link', 'text', 'https://www.gruppenwerk.de', 'content', 'group'),
        'legalItems': c('Links', 'array', [{'label': 'Impressum', 'href': '/impressum'}, {'label': 'Datenschutz', 'href': '/datenschutz'}, {'label': 'Kontakt', 'href': '/kontakt'}], 'content', 'group', items=LINK_ITEMS),
    }
    return pkg('footer', ctl, {'brand': {'title': 'Hintergrund & Logo'}, 'group': {'title': 'Gruppenwerk & Links'}})