"""Generate package.json files (controls + page-specific defaults) for every section instance."""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from alts import alt, BANNER_ALT  # noqa: E402

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
    return [{'image': {'src': u['url'], 'name': u['name'], 'width': u.get('width') or 1000, 'height': u.get('height') or 667}, 'alt': alt(u['name'])}
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
    {'label': 'Karriere', 'href': '/karriere'},
    {'label': 'Kontakt', 'href': '/kontakt'},
]
LINK_ITEMS = {'label': {'title': 'Label', 'type': 'text'}, 'href': {'title': 'Link', 'type': 'text'}}


NAV_MAIN = [n for n in NAV if n['href'] != '/kontakt']


LANGS = [('de', 'DE', 'Deutsch'), ('pl', 'PL', 'Polski'), ('ru', 'RU', 'Русский'), ('uk', 'UK', 'Українська'), ('tr', 'TR', 'Türkçe')]


def lang_links(current, de_href):
    # Only the career page is translated; on German pages the other languages lead to the translated career page.
    return [{'code': code, 'short': short, 'label': label, 'href': de_href if code == 'de' else '/karriere-' + code, 'current': code == current}
            for code, short, label in LANGS]


def localize(p, tr):
    for k, v in (tr or {}).items():
        p['onepage']['control'][k]['default'] = v
    return p


def header(active, lang='de', de_href=None):
    ctl = {
        'logo': c('Logo', 'media', img('_themes/lightwhite/logo-wernerbau.svg'), 'content', 'brand'),
        'logoAlt': c('Logo Alt-Text', 'text', 'WERNER GMBH Bauunternehmung', 'content', 'brand'),
        'logoHref': c('Logo Link', 'text', '/', 'content', 'brand'),
        'email': c('E-Mail', 'text', EMAIL, 'content', 'meta'),
        'phone': c('Telefon', 'text', PHONE, 'content', 'meta'),
        'phoneHref': c('Telefon Link', 'text', PHONE_HREF, 'content', 'meta'),
        'contactLabel': c('Kontakt Text', 'text', 'Kontakt', 'content', 'meta'),
        'contactHref': c('Kontakt Link', 'text', '/kontakt', 'content', 'meta'),
        'applyLabel': c('Bewerben Button Text', 'text', 'Jetzt bewerben', 'content', 'meta'),
        'applyHref': c('Bewerben Button Link', 'text', '/karriere#bewerben', 'content', 'meta'),
        'navItems': c('Menüpunkte', 'array', NAV_MAIN, 'content', 'nav', items=LINK_ITEMS),
        'activeHref': c('Aktive Seite (Link)', 'text', active, 'content', 'nav'),
        'menuLabel': c('Menü öffnen Label', 'text', 'Menü öffnen', 'content', 'nav'),
        'closeLabel': c('Menü schließen Label', 'text', 'Menü schließen', 'content', 'nav'),
        'languages': c('Sprachen', 'array', lang_links(lang, de_href or active), 'content', 'lang', items={
            'label': {'title': 'Name', 'type': 'text'}, 'short': {'title': 'Kürzel', 'type': 'text'},
            'code': {'title': 'Sprachcode', 'type': 'text'}, 'href': {'title': 'Link', 'type': 'text'},
            'current': {'title': 'Aktuelle Sprache', 'type': 'checkbox'}}),
        'langLabel': c('Sprachauswahl (Screenreader)', 'text', 'Sprache wählen', 'content', 'lang'),
    }
    return pkg('header', ctl, {'brand': {'title': 'Logo'}, 'meta': {'title': 'Kontaktzeile'}, 'nav': {'title': 'Navigation'}, 'lang': {'title': 'Sprachauswahl'}})

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
        'bannerAlt': c('Banner Alt-Text', 'text', BANNER_ALT['banner-1.jpg'], 'content', 'root'),
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
        'attachLabel': c('Anhang Label', 'text', 'Dateien anhängen', 'content', 'attach'),
        'attachHint': c('Anhang Hinweis', 'text', 'z. B. Fotos, Pläne oder PDF – bis zu 5 Dateien, max. 10 MB je Datei', 'content', 'attach'),
        'attachButton': c('Anhang Button', 'text', 'Dateien auswählen', 'content', 'attach'),
        'attachRemove': c('Anhang entfernen (Screenreader)', 'text', 'Datei entfernen', 'content', 'attach'),
        'attachTooLarge': c('Datei zu groß', 'text', 'Mindestens eine Datei war größer als 10 MB und wurde nicht hinzugefügt.', 'content', 'attach'),
        'attachAccept': c('Erlaubte Dateitypen', 'text', 'image/*,.pdf,.doc,.docx,.xls,.xlsx,.dwg,.zip', 'settings', 'attach'),
        'attachMaxFiles': c('Max. Anzahl Dateien', 'number', 5, 'settings', 'attach'),
        'attachMaxMb': c('Max. MB je Datei', 'number', 10, 'settings', 'attach'),
        'formId': c('CRM Formular-ID', 'text', form_id, 'settings', 'messages'),
    }
    return pkg('contact', ctl, {'info': {'title': 'Kontaktdaten'}, 'fields': {'title': 'Formularfelder'}, 'notes': {'title': 'Hinweise'}, 'messages': {'title': 'Meldungen & CRM'}, 'attach': {'title': 'Dateianhang'}})


FOOTER_BG = {'src': 'https://onecdn.io/media/fb608040-1adc-425e-8524-af41b2d94094/full', 'name': 'footer.jpg', 'width': 2000, 'height': 500}


def footer():
    ctl = {
        'background': c('Hintergrundbild', 'media', FOOTER_BG, 'content', 'brand'),
        'logo': c('Logo (hell)', 'media', img('_themes/lightwhite/logo-wernerbau-negative.svg'), 'content', 'brand'),
        'logoAlt': c('Logo Alt-Text', 'text', 'WERNER GMBH Bauunternehmung', 'content', 'brand'),
        'groupTitle': c('Gruppe Text', 'text', '', 'content', 'group'),
        'groupLogo': c('Gruppenwerk Logo', 'media', img('Gruppenwerk_Unternehmen_weiss.png'), 'content', 'group'),
        'groupAlt': c('Gruppe Alt-Text', 'text', 'Zur Gruppenwerk Website', 'content', 'group'),
        'groupHref': c('Gruppe Link', 'text', 'https://www.gruppenwerk.de', 'content', 'group'),
        'legalItems': c('Links', 'array', [{'label': 'Impressum', 'href': '/impressum'}, {'label': 'Datenschutz', 'href': '/datenschutz'}, {'label': 'Kontakt', 'href': '/kontakt'}], 'content', 'group', items=LINK_ITEMS),
    }
    return pkg('footer', ctl, {'brand': {'title': 'Hintergrund & Logo'}, 'group': {'title': 'Gruppenwerk & Links'}})


def career(form_id='', lang='de'):
    jobs = [
        {'title': 'Maurer (m/w/d)', 'meta': 'Vollzeit · Hamburg', 'text': 'Mauerwerks-, Putz- und Fassadenarbeiten an Alt- und Denkmalbauten sowie in der Wohnungssanierung.'},
        {'title': 'Maler und Lackierer (m/w/d)', 'meta': 'Vollzeit · Hamburg', 'text': 'Maler- und Stuckarbeiten in Wohnungen, Gebäuden und öffentlichen Einrichtungen.'},
        {'title': 'Projekt-/Bauleiter (m/w/d)', 'meta': 'Vollzeit · Hamburg', 'text': 'Planung, Steuerung und Abnahme unserer Sanierungsprojekte – von der Fassade bis zur bezugsfertigen Wohneinheit.'},
    ]
    benefits = [{'text': t} for t in [
        'Ein traditionsreiches Hamburger Familienunternehmen mit fast 100 Jahren Erfahrung',
        'Ein fester, qualifizierter Mitarbeiterstamm und ein kollegiales Miteinander',
        'Abwechslungsreiche Projekte – vom denkmalgeschützten Altbau bis zur Hamburger Schule',
        'Regelmäßige Schulungen zu neuen Produkten und Techniken',
        'Teil der Unternehmensgruppe GRUPPENWERK',
    ]]
    ctl = {
        'title': c('Überschrift', 'text', 'Karriere', 'content', 'intro'),
        'intro': c('Einleitung (Absätze mit Leerzeile trennen)', 'text', 'Bei uns werden Erfahrungen seit jeher von Generation zu Generation weitergegeben. Damit das so bleibt, suchen wir Menschen, die ihr Handwerk lieben und unsere Projekte mit Sorgfalt und Verlässlichkeit umsetzen.\n\nOb Fassadensanierung, Denkmalschutz oder Wohnungssanierung: Bei Werner Bau arbeiten Sie an Gebäuden, die das Stadtbild Hamburgs prägen – in einem Team, das sich aufeinander verlassen kann.', 'content', 'intro'),
        'applyLabel': c('Bewerben Button', 'text', 'Jetzt bewerben', 'content', 'intro'),
        'benefitsTitle': c('Vorteile Überschrift', 'text', 'Was Sie bei uns erwartet', 'content', 'benefits'),
        'benefits': c('Vorteile', 'array', benefits, 'content', 'benefits', items={'text': {'title': 'Text', 'type': 'text'}}),
        'jobsTitle': c('Stellen Überschrift', 'text', 'Offene Stellen', 'content', 'jobs'),
        'jobs': c('Stellen', 'array', jobs, 'content', 'jobs', items={'title': {'title': 'Titel', 'type': 'text'}, 'meta': {'title': 'Art · Ort', 'type': 'text'}, 'text': {'title': 'Kurzbeschreibung', 'type': 'text'}}),
        'initiativeLabel': c('Initiativbewerbung Text', 'text', 'Initiativbewerbung', 'content', 'jobs'),
        'formAnchor': c('Anker-ID Formular', 'text', 'bewerben', 'settings', 'form'),
        'formTitle': c('Formular Überschrift', 'text', 'Jetzt bewerben', 'content', 'form'),
        'formIntro': c('Formular Text', 'text', 'Senden Sie uns Ihre Bewerbung bequem über das Formular – Lebenslauf und Zeugnisse können Sie direkt anhängen. Wir melden uns zeitnah bei Ihnen.', 'content', 'form'),
        'firstNameLabel': c('Vorname', 'text', 'Vorname', 'content', 'fields'),
        'lastNameLabel': c('Nachname', 'text', 'Nachname', 'content', 'fields'),
        'emailLabel': c('E-Mail', 'text', 'E-Mail Adresse', 'content', 'fields'),
        'phoneLabel': c('Telefon', 'text', 'Rufnummer', 'content', 'fields'),
        'positionLabel': c('Stelle', 'text', 'Gewünschte Stelle', 'content', 'fields'),
        'positionPlaceholder': c('Stelle Platzhalter', 'text', 'Bitte auswählen', 'content', 'fields'),
        'messageLabel': c('Nachricht', 'text', 'Ihre Nachricht an uns', 'content', 'fields'),
        'submitLabel': c('Absenden Button', 'text', 'Bewerbung senden', 'content', 'fields'),
        'attachLabel': c('Anhang Label', 'text', 'Lebenslauf & Zeugnisse', 'content', 'attach'),
        'attachHint': c('Anhang Hinweis', 'text', 'PDF, Word oder Bilder – bis zu 5 Dateien, max. 10 MB je Datei', 'content', 'attach'),
        'attachButton': c('Anhang Button', 'text', 'Dateien auswählen', 'content', 'attach'),
        'attachRemove': c('Anhang entfernen (Screenreader)', 'text', 'Datei entfernen', 'content', 'attach'),
        'attachTooLarge': c('Datei zu groß', 'text', 'Mindestens eine Datei war größer als 10 MB und wurde nicht hinzugefügt.', 'content', 'attach'),
        'attachAccept': c('Erlaubte Dateitypen', 'text', 'image/*,.pdf,.doc,.docx', 'settings', 'attach'),
        'attachMaxFiles': c('Max. Anzahl Dateien', 'number', 5, 'settings', 'attach'),
        'attachMaxMb': c('Max. MB je Datei', 'number', 10, 'settings', 'attach'),
        'consentPre': c('Datenschutz-Hinweis (vor Link)', 'text', 'Mit dem Absenden des Formulars nehmen Sie unserer', 'content', 'notes'),
        'privacyLabel': c('Datenschutz Link Text', 'text', 'Datenschutzerklärung', 'content', 'notes'),
        'privacyHref': c('Datenschutz Link', 'text', '/datenschutz', 'content', 'notes'),
        'consentPost': c('Datenschutz-Hinweis (nach Link)', 'text', 'zur Kenntnis und akzeptieren diese.', 'content', 'notes'),
        'requiredNote': c('Pflichtfeld-Hinweis', 'text', 'Felder, welche mit * markiert sind, sind Pflichtfelder und müssen vor dem Absenden ausgefüllt werden.', 'content', 'notes'),
        'sendingLabel': c('Senden läuft', 'text', 'Wird gesendet …', 'content', 'messages'),
        'successText': c('Erfolgsmeldung', 'text', 'Vielen Dank für Ihre Bewerbung. Wir melden uns schnellstmöglich bei Ihnen.', 'content', 'messages'),
        'errorText': c('Fehlermeldung', 'text', 'Die Bewerbung konnte nicht gesendet werden. Bitte versuchen Sie es erneut oder rufen Sie uns an.', 'content', 'messages'),
        'requiredError': c('Pflichtfeld-Fehler', 'text', 'Bitte füllen Sie dieses Pflichtfeld aus.', 'content', 'messages'),
        'emailError': c('E-Mail-Fehler', 'text', 'Bitte geben Sie eine gültige E-Mail-Adresse ein.', 'content', 'messages'),
        'formId': c('CRM Formular-ID', 'text', form_id, 'settings', 'form'),
        'langTitle': c('Sprachen Überschrift', 'text', 'Diese Seite in anderen Sprachen', 'content', 'lang'),
        'langLinks': c('Sprachen', 'array', lang_links(lang, '/karriere'), 'content', 'lang', items={
            'label': {'title': 'Name', 'type': 'text'}, 'code': {'title': 'Sprachcode', 'type': 'text'},
            'href': {'title': 'Link', 'type': 'text'}, 'current': {'title': 'Aktuelle Sprache', 'type': 'checkbox'}}),
    }
    return pkg('career', ctl, {'lang': {'title': 'Sprachen'}, 'intro': {'title': 'Einleitung'}, 'benefits': {'title': 'Vorteile'}, 'jobs': {'title': 'Stellen'}, 'form': {'title': 'Formular'}, 'fields': {'title': 'Formularfelder'}, 'attach': {'title': 'Dateianhang'}, 'notes': {'title': 'Hinweise'}, 'messages': {'title': 'Meldungen'}})


def photo(name, alt_text=None):
    u = next((x for x in UP if x['name'] == name and x.get('url')), None)
    if not u:
        raise SystemExit('missing photo: ' + name)
    return {'image': {'src': u['url'], 'name': u['name'], 'width': u.get('width') or 1000, 'height': u.get('height') or 667}, 'alt': alt_text or alt(name)}


def project(title, names, cover=None):
    out = []
    for n in names:
        ph = photo(n)
        ph['project'] = title
        ph['cover'] = n == cover
        out.append(ph)
    return out


def split(blocks, projects, heading='h1first'):
    rows = []
    for b in blocks:
        p = photo(b['photo'], b.get('imageAlt'))
        rows.append({'title': b.get('title', ''), 'text': b.get('text', ''), 'bullets': b.get('bullets', ''), 'textAfter': b.get('textAfter', ''),
                     'linkLabel': b.get('linkLabel', ''), 'linkHref': b.get('linkHref', ''),
                     'image': p['image'], 'imageAlt': b.get('imageAlt') or p['alt'], 'imageFit': b.get('imageFit', 'cover')})
    ctl = {
        'blocks': c('Text & Bild (abwechselnd links/rechts)', 'array', rows, 'content', 'blocks', items={
            'title': {'title': 'Überschrift', 'type': 'text'},
            'text': {'title': 'Text (Absätze mit Leerzeile trennen, **fett**)', 'type': 'text'},
            'bullets': {'title': 'Aufzählung (eine Zeile pro Punkt)', 'type': 'text'},
            'textAfter': {'title': 'Text nach Aufzählung', 'type': 'text'},
            'linkLabel': {'title': 'Link Text (optional)', 'type': 'text'},
            'linkHref': {'title': 'Link (optional)', 'type': 'text'},
            'image': {'title': 'Bild', 'type': 'media'},
            'imageAlt': {'title': 'Bild Alt-Text', 'type': 'text'},
            'imageFit': {'title': 'Bilddarstellung', 'type': 'select', 'options': [
                {'value': 'cover', 'label': 'Foto (füllend)'}, {'value': 'contain', 'label': 'Logo (eingepasst)'}]}}),
        'headingMode': c('Erste Überschrift', 'select', heading, 'settings', 'labels', options=[
            {'value': 'h1first', 'label': 'Seitentitel (H1) mit Einleitung'}, {'value': 'h2', 'label': 'Normale Überschrift (H2)'}]),
        'projectsEyebrow': c('Überzeile', 'text', 'Referenzen', 'content', 'projects'),
        'projectsTitle': c('Überschrift', 'text', 'Projekte & Einblicke', 'content', 'projects'),
        'photos': c('Fotos (gleicher Projektname = eine Karte)', 'array', [ph for grp in projects for ph in grp], 'content', 'photos', items={
            'image': {'title': 'Bild', 'type': 'media'},
            'alt': {'title': 'Alt-Text', 'type': 'text'},
            'project': {'title': 'Projekt', 'type': 'text'},
            'cover': {'title': 'Titelbild der Karte', 'type': 'checkbox'}}),
        'photosLabel': c('Wort hinter Fotoanzahl', 'text', 'Fotos', 'content', 'projects'),
        'openLabel': c('Öffnen (Screenreader)', 'text', 'Fotos ansehen', 'content', 'labels'),
        'closeLabel': c('Schließen (Screenreader)', 'text', 'Schließen', 'content', 'labels'),
        'prevLabel': c('Zurück (Screenreader)', 'text', 'Vorheriges Bild', 'content', 'labels'),
        'nextLabel': c('Weiter (Screenreader)', 'text', 'Nächstes Bild', 'content', 'labels'),
    }
    return pkg('split', ctl, {'blocks': {'title': 'Text & Bild'}, 'projects': {'title': 'Projektkarten'}, 'photos': {'title': 'Projektfotos'}, 'labels': {'title': 'Beschriftungen'}})


def people(persons, eyebrow, title):
    ctl = {
        'eyebrow': c('Überzeile', 'text', eyebrow, 'content', 'root'),
        'title': c('Überschrift', 'text', title, 'content', 'root'),
        'people': c('Personen', 'array', persons, 'content', 'people', items={
            'photo': {'title': 'Foto', 'type': 'media'},
            'photoAlt': {'title': 'Foto Alt-Text', 'type': 'text'},
            'name': {'title': 'Name', 'type': 'text'},
            'role': {'title': 'Funktion', 'type': 'text'},
            'phoneLabel': {'title': 'Telefon Bezeichnung', 'type': 'text'},
            'phone': {'title': 'Telefon', 'type': 'text'},
            'phoneHref': {'title': 'Telefon Link', 'type': 'text'},
            'emailLabel': {'title': 'E-Mail Bezeichnung', 'type': 'text'},
            'email': {'title': 'E-Mail', 'type': 'text'}}),
    }
    return pkg('people', ctl, {'people': {'title': 'Personen'}})
