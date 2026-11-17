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


LANGS = [('de', 'DE', 'Deutsch'), ('en', 'EN', 'English'), ('pl', 'PL', 'Polski'), ('ru', 'RU', 'Русский'), ('uk', 'UK', 'Українська'), ('tr', 'TR', 'Türkçe')]


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
        'emailLabel': c('E-Mail Button Text', 'text', 'E-Mail', 'content', 'meta'),
        'mailSubject': c('Betreff', 'text', 'Anfrage über die Website', 'content', 'mail'),
        'mailApps': c('Mail-Programme', 'array', [
            {'label': 'Mail-App', 'url': 'mailto:{to}?subject={subject}', 'copy': False},
            {'label': 'Gmail', 'url': 'https://mail.google.com/mail/?view=cm&fs=1&to={to}&su={subject}', 'copy': False},
            {'label': 'Outlook', 'url': 'https://outlook.live.com/mail/0/deeplink/compose?to={to}&subject={subject}', 'copy': False},
            {'label': 'GMX', 'url': 'https://www.gmx.net/', 'copy': True},
            {'label': 'WEB.DE', 'url': 'https://web.de/', 'copy': True}], 'content', 'mail', items={
            'label': {'title': 'Name', 'type': 'text'}, 'url': {'title': 'Link ({to} = Adresse, {subject} = Betreff)', 'type': 'text'},
            'copy': {'title': 'Adresse vorher kopieren', 'type': 'checkbox'}}),
        'mailCopyLabel': c('Kopieren Text', 'text', 'Adresse kopieren', 'content', 'mail'),
        'mailCopiedLabel': c('Kopiert Text', 'text', 'Kopiert', 'content', 'mail'),
        'mailCopyHint': c('Hinweis bei Kopieren', 'text', 'Adresse wird kopiert', 'content', 'mail'),
        'mailNoApp': c('Hinweis ohne Mailprogramm', 'text', 'Auf diesem Gerät ist kein Mailprogramm eingerichtet. Die Adresse wurde kopiert – fügen Sie sie einfach in Ihrem E-Mail-Postfach ein.', 'content', 'mail'),
        'phone': c('Telefon', 'text', PHONE, 'content', 'meta'),
        'phoneHref': c('Telefon Link', 'text', PHONE_HREF, 'content', 'meta'),
        'contactLabel': c('Anfrage Button Text', 'text', 'Anfrage senden', 'content', 'meta'),
        'contactHref': c('Kontakt Link', 'text', '/kontakt', 'content', 'meta'),
        'applyLabel': c('Bewerben Button Text', 'text', 'Jetzt bewerben', 'content', 'meta'),
        'applyHref': c('Bewerben Button Link', 'text', '/karriere#bewerben', 'content', 'meta'),
        'navItems': c('Menüpunkte (stehen hinter „Leistungen“; ein Link zur Startseite steht davor)', 'array', [{'label': 'Referenzen', 'href': '/referenzen'}, {'label': 'Für Hausverwaltungen', 'href': '/hausverwaltungen'}, {'label': 'Über uns', 'href': '/ueber-uns'}, {'label': 'Karriere', 'href': '/karriere'}], 'content', 'nav', items=LINK_ITEMS),
        'servicesLabel': c('Leistungen Menüpunkt', 'text', 'Leistungen', 'content', 'nav'),
        'serviceItems': c('Leistungen Untermenü', 'array', [n for n in NAV_MAIN if n['href'] not in ('/', '/ueber-uns', '/karriere')], 'content', 'nav', items=LINK_ITEMS),
        'activeHref': c('Aktive Seite (Link)', 'text', active, 'content', 'nav'),
        'menuLabel': c('Menü öffnen Label', 'text', 'Menü öffnen', 'content', 'nav'),
        'closeLabel': c('Menü schließen Label', 'text', 'Menü schließen', 'content', 'nav'),
        'languages': c('Sprachen', 'array', lang_links(lang, de_href or active), 'content', 'lang', items={
            'label': {'title': 'Name', 'type': 'text'}, 'short': {'title': 'Kürzel', 'type': 'text'},
            'code': {'title': 'Sprachcode', 'type': 'text'}, 'href': {'title': 'Link', 'type': 'text'},
            'current': {'title': 'Aktuelle Sprache', 'type': 'checkbox'}}),
        'langLabel': c('Sprachauswahl (Screenreader)', 'text', 'Sprache wählen', 'content', 'lang'),
        'navLang': c('Sprache der Menüpunkte (Code)', 'text', 'de', 'content', 'nav'),
        'whatsappNumber': c('WhatsApp-Nummer (international ohne +, z. B. 4915112345678)', 'text', '', 'content', 'whatsapp'),
        'whatsappText': c('WhatsApp Begrüßungstext', 'text', 'Hallo Werner Bau, ich habe eine Anfrage:', 'content', 'whatsapp'),
        'whatsappButton': c('WhatsApp Button Text', 'text', 'WhatsApp', 'content', 'whatsapp'),
        'whatsappLabel': c('WhatsApp Button (Screenreader)', 'text', 'Per WhatsApp schreiben', 'content', 'whatsapp'),
        'whatsappFallback': c('Link solange keine Nummer eingetragen ist', 'text', '/kontakt', 'content', 'whatsapp'),
    }
    return pkg('header', ctl, {'brand': {'title': 'Logo'}, 'meta': {'title': 'Kontaktzeile'}, 'nav': {'title': 'Navigation'}, 'lang': {'title': 'Sprachauswahl'}, 'whatsapp': {'title': 'WhatsApp'}, 'mail': {'title': 'E-Mail-Menü'}})

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


VOICE_DE = {
    'voiceLabel': 'Lieber erzählen statt schreiben?', 'voiceHint': 'Nehmen Sie eine Sprachnachricht auf (bis 3 Minuten). Sie wird mit dem Formular an uns gesendet.',
    'voiceRecord': 'Sprachnachricht aufnehmen', 'voiceStop': 'Aufnahme beenden', 'voiceRecording': 'Aufnahme läuft', 'voiceDelete': 'Löschen',
    'voiceDenied': 'Kein Zugriff auf das Mikrofon. Bitte erlauben Sie den Zugriff in Ihrem Browser oder schreiben Sie uns einfach.',
    'voiceFileHint': 'Auf dem Handy öffnet sich die Sprachaufnahme oder Ihre Sprachmemos, am Computer wählen Sie eine Audiodatei aus. Sie wird mit dem Formular an uns gesendet.',
}


def voice_controls(defaults=None, group='voice'):
    d = dict(VOICE_DE, **(defaults or {}))
    t = {'voiceLabel': 'Überschrift', 'voiceHint': 'Hinweis', 'voiceRecord': 'Button Aufnehmen', 'voiceStop': 'Button Stopp',
         'voiceRecording': 'Text während der Aufnahme', 'voiceDelete': 'Button Löschen', 'voiceDenied': 'Meldung ohne Mikrofon-Zugriff', 'voiceFileHint': 'Hinweis, wenn als Datei aufgenommen wird'}
    return {k: c(t[k], 'text', d[k], 'content', group) for k in t}


JOB_DE = {
    'jobEyebrow': 'Aktuell gesucht',
    'jobTitle': 'Projektassistenz Bau (m/w/d)',
    'jobMeta': 'Hamburg · Büro und Baustelle',
    'jobHook': 'Sie denken mit. Sie packen an. Sie wollen etwas bewegen.',
    'jobIntro': 'Sie haben bereits erste Erfahrungen im Berufsleben gesammelt, interessieren sich für das Baugewerbe und möchten mehr als nur Aufgaben abarbeiten? Dann sollten wir uns kennenlernen.\n\nBei uns arbeiten Sie eng mit einem erfahrenen Kollegen zusammen, der sowohl im Büro als auch auf unseren Baustellen unterwegs ist. Sie unterstützen ihn bei der Organisation und Abwicklung unserer Bauprojekte, behalten Termine und Abläufe im Blick und übernehmen Schritt für Schritt eigene Verantwortung. Dabei wünschen wir uns jemanden, der nicht nur mitarbeitet, sondern mitdenkt: der Fragen stellt, Zusammenhänge erkennt und eigene Ideen einbringt.',
    'jobMoreLabel': 'Stellenbeschreibung anzeigen',
    'jobLessLabel': 'Stellenbeschreibung ausblenden',
    'jobTasksTitle': 'Was Sie bei uns erwartet',
    'jobTasks': 'Sie unterstützen die Projektleitung bei der Organisation und Koordination unserer Bauprojekte.\nSie sind eine wichtige Verbindung zwischen Büro, Baustelle und unseren Projektbeteiligten.\nSie erstellen Bautagesberichte, Protokolle und den projektbezogenen Schriftverkehr.\nSie unterstützen bei der Vorbereitung von Angeboten, Aufträgen und Abrechnungen.\nSie behalten Termine, Unterlagen und organisatorische Abläufe im Blick.\nSie begleiten bei Bedarf auch Termine auf unseren Baustellen.\nSie bringen eigene Ideen ein, wie wir Abläufe einfacher, digitaler und effizienter gestalten können.',
    'jobProfileTitle': 'Was Sie mitbringen sollten',
    'jobProfile': 'Eine abgeschlossene kaufmännische oder bautechnische Ausbildung, idealerweise mit Bezug zum Baugewerbe\nErste Berufserfahrung in einem Bau- oder Handwerksunternehmen wäre wünschenswert\nEin gutes organisatorisches Verständnis und Freude daran, unterschiedliche Aufgaben miteinander zu verbinden\nSicheres Deutsch in Wort und Schrift sowie einen routinierten Umgang mit digitalen Anwendungen\nEine selbstständige, strukturierte und zuverlässige Arbeitsweise\nNeugier, Eigeninitiative und die Bereitschaft, Verantwortung zu übernehmen',
    'jobOfferTitle': 'Was wir Ihnen bieten',
    'jobOffer': 'Einen erfahrenen Kollegen an Ihrer Seite, der sein Wissen gerne weitergibt\nEine gründliche Einarbeitung und die Möglichkeit, sich fachlich und persönlich weiterzuentwickeln\nAbwechslungsreiche Aufgaben zwischen Büro und Baustelle\nKurze Entscheidungswege und ein Umfeld, in dem Ihre Meinung zählt\nDie Möglichkeit, eigene Ideen einzubringen und Veränderungen aktiv mitzugestalten\nEin kollegiales Team, das sich gegenseitig unterstützt',
    'jobNote': 'Sie müssen nicht alles können. Aber Sie sollten Lust haben, dazuzulernen und Ihr Wissen einzubringen.',
    'jobContactTitle': 'Ihre Ansprechpartnerin',
    'jobContactName': 'Susan Khallaf',
    'jobContactPhone': '0178 35 70 021',
    'jobContactPhoneHref': 'tel:+4917835700' + '21',
    'jobContactEmail': 's.khallaf@gruppenwerk.de',
    'jobApplyLabel': 'Auf diese Stelle bewerben',
}
JOB_GROUP = {k: g for g, ks in {
    'job': ['jobEyebrow', 'jobTitle', 'jobMeta', 'jobHook', 'jobIntro', 'jobMoreLabel', 'jobLessLabel'],
    'jobDetails': ['jobTasksTitle', 'jobTasks', 'jobProfileTitle', 'jobProfile', 'jobOfferTitle', 'jobOffer', 'jobNote'],
    'jobContact': ['jobContactTitle', 'jobContactName', 'jobContactPhone', 'jobContactPhoneHref', 'jobContactEmail', 'jobApplyLabel']}.items() for k in ks}
JOB_TITLES = {'jobTitle': 'Stellentitel (leer = keine Stelle anzeigen)', 'jobTasks': 'Aufgaben (eine Zeile pro Punkt)', 'jobProfile': 'Profil (eine Zeile pro Punkt)', 'jobOffer': 'Angebot (eine Zeile pro Punkt)', 'jobIntro': 'Text (Absätze mit Leerzeile trennen)'}



def career(form_id='', lang='de'):
    benefits = [{'text': t} for t in [
        'Ein traditionsreiches Hamburger Familienunternehmen mit fast 100 Jahren Erfahrung',
        'Ein fester, qualifizierter Mitarbeiterstamm und ein kollegiales Miteinander',
        'Abwechslungsreiche Projekte – vom denkmalgeschützten Altbau bis zur Hamburger Schule',
        'Regelmäßige Schulungen zu neuen Produkten und Techniken',
    ]]
    ctl = {
        'title': c('Überschrift', 'text', 'Karriere', 'content', 'intro'),
        'intro': c('Einleitung (Absätze mit Leerzeile trennen)', 'text', 'Bei uns werden Erfahrungen seit jeher von Generation zu Generation weitergegeben. Damit das so bleibt, suchen wir Menschen, die ihr Handwerk lieben und unsere Projekte mit Sorgfalt und Verlässlichkeit umsetzen.\n\nOb Fassadensanierung, Denkmalschutz oder Wohnungssanierung: Bei Werner Bau arbeiten Sie an Gebäuden, die das Stadtbild Hamburgs prägen – in einem Team, das sich aufeinander verlassen kann.', 'content', 'intro'),
        'applyLabel': c('Bewerben Button', 'text', 'Jetzt bewerben', 'content', 'intro'),
        'benefitsTitle': c('Vorteile Überschrift', 'text', 'Was Sie bei uns erwartet', 'content', 'benefits'),
        'benefits': c('Vorteile', 'array', benefits, 'content', 'benefits', items={'text': {'title': 'Text', 'type': 'text'}}),
        'initiativeTitle': c('Initiativbewerbung Überschrift', 'text', 'Initiativbewerbungen erwünscht', 'content', 'jobs'),
        'initiativeText': c('Initiativbewerbung Text (Absätze mit Leerzeile trennen)', 'text', 'Darüber hinaus schreiben wir keine festen Stellen aus. Ob Handwerk, Bauleitung oder Quereinstieg: Uns interessiert, was Sie können und wer Sie sind – nicht, ob Sie in eine Stellenbezeichnung passen.\n\nSie denken, Sie gehören dazu? Dann sind Sie bei uns an Bord. Schreiben Sie uns einfach.', 'content', 'jobs'),
        **{k: c(JOB_TITLES.get(k, k.replace('job', 'Stelle: ')), 'text', v, 'content', JOB_GROUP[k]) for k, v in JOB_DE.items()},
        'formAnchor': c('Anker-ID Formular', 'text', 'bewerben', 'settings', 'form'),
        'formTitle': c('Formular Überschrift', 'text', 'Jetzt bewerben', 'content', 'form'),
        'formIntro': c('Formular Text', 'text', 'Senden Sie uns Ihre Initiativbewerbung bequem über das Formular – Lebenslauf und Zeugnisse können Sie direkt anhängen. Wir melden uns zeitnah bei Ihnen.', 'content', 'form'),
        'firstNameLabel': c('Vorname', 'text', 'Vorname', 'content', 'fields'),
        'lastNameLabel': c('Nachname', 'text', 'Nachname', 'content', 'fields'),
        'emailLabel': c('E-Mail', 'text', 'E-Mail Adresse', 'content', 'fields'),
        'phoneLabel': c('Telefon', 'text', 'Rufnummer', 'content', 'fields'),
        'positionLabel': c('Beruf / Erfahrung', 'text', 'Ihr Beruf / Ihre Erfahrung', 'content', 'fields'),
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
        'langTitle': c('Sprachen Hinweis', 'text', 'Auch verfügbar auf:', 'content', 'lang'),
        'formLangLabel': c('Sprachwahl am Formular', 'text', 'Formular in Ihrer Sprache', 'content', 'lang'),
        'langLinks': c('Sprachen', 'array', lang_links(lang, '/karriere'), 'content', 'lang', items={
            'label': {'title': 'Name', 'type': 'text'}, 'code': {'title': 'Sprachcode', 'type': 'text'},
            'href': {'title': 'Link', 'type': 'text'}, 'current': {'title': 'Aktuelle Sprache', 'type': 'checkbox'}}),
    }
    return pkg('career', ctl, {'lang': {'title': 'Sprachen'}, 'intro': {'title': 'Einleitung'}, 'benefits': {'title': 'Vorteile'}, 'jobs': {'title': 'Initiativbewerbung'}, 'job': {'title': 'Stelle'}, 'jobDetails': {'title': 'Stelle: Details'}, 'jobContact': {'title': 'Stelle: Kontakt'}, 'form': {'title': 'Formular'}, 'fields': {'title': 'Formularfelder'}, 'attach': {'title': 'Dateianhang'}, 'notes': {'title': 'Hinweise'}, 'messages': {'title': 'Meldungen'}})


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
        ph['cover'] = n in cover if isinstance(cover, (list, tuple)) else n == cover
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
            {'value': 'h1first', 'label': 'Seitentitel (H1) mit Einleitung'}, {'value': 'lead', 'label': 'Einleitung ohne Überschrift (Titel steht im Banner)'}, {'value': 'h2', 'label': 'Normale Überschrift (H2)'}]),
        'projectsEyebrow': c('Überzeile', 'text', 'Referenzen', 'content', 'projects'),
        'projectsTitle': c('Überschrift', 'text', 'Projekte & Einblicke', 'content', 'projects'),
        'allLabel': c('Link zu allen Referenzen (Text)', 'text', 'Alle Referenzen ansehen', 'content', 'projects'),
        'allHref': c('Link zu allen Referenzen', 'text', '/referenzen', 'content', 'projects'),
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


def header_lux(active, lang='de', de_href=None):
    p = header(active, lang, de_href)
    ctl = p['onepage']['control']
    for k in [k for k in ctl if k.startswith('whatsapp')]:
        del ctl[k]
    del p['onepage']['group']['whatsapp']
    return p


def hook(slides, links):
    S = []
    for name, caption in slides:
        ph = photo(name)
        S.append({'image': ph['image'], 'alt': ph['alt'], 'caption': caption})
    ctl = {
        'eyebrow': c('Überzeile', 'text', 'Werner Bau · Hamburg · seit fast 100 Jahren', 'content', 'copy'),
        'headline': c('Überschrift', 'text', 'Wir erhalten,', 'content', 'copy'),
        'accent': c('Überschrift zweite Zeile (grau)', 'text', 'was Hamburg ausmacht.', 'content', 'copy'),
        'sub': c('Text', 'text', 'Fassaden, Denkmäler und Wohnräume – saniert mit der Erfahrung aus fast 100 Jahren Hamburger Baugeschichte.', 'content', 'copy'),
        'primaryLabel': c('Button Text', 'text', 'Projekt anfragen', 'content', 'buttons'),
        'primaryHref': c('Button Link', 'text', '/kontakt', 'content', 'buttons'),
        'secondaryLabel': c('Zweiter Button Text', 'text', 'Referenzen ansehen', 'content', 'buttons'),
        'secondaryHref': c('Zweiter Button Link', 'text', '/referenzen', 'content', 'buttons'),
        'slides': c('Fotos (wechseln automatisch)', 'array', S, 'content', 'slides', items={
            'image': {'title': 'Foto', 'type': 'media'}, 'alt': {'title': 'Alt-Text', 'type': 'text'},
            'caption': {'title': 'Bildunterschrift', 'type': 'text'}}),
        'interval': c('Sekunden pro Foto', 'number', 6, 'content', 'slides'),
        'links': c('Leistungen unten', 'array', links, 'content', 'links', items=LINK_ITEMS),
    }
    return pkg('hook', ctl, {'copy': {'title': 'Text'}, 'buttons': {'title': 'Buttons'}, 'slides': {'title': 'Fotos'}, 'links': {'title': 'Leistungen'}})


def pagehero(image, alt, eyebrow, title, height='md'):
    ctl = {
        'image': c('Bild', 'media', image, 'content', 'root'),
        'imageAlt': c('Bild Alt-Text', 'text', alt, 'content', 'root'),
        'eyebrow': c('Überzeile', 'text', eyebrow, 'content', 'root'),
        'title': c('Seitentitel', 'text', title, 'content', 'root'),
        'height': c('Höhe', 'select', height, 'content', 'root', options=[{'value': 'lg', 'label': 'Groß'}, {'value': 'md', 'label': 'Mittel'}, {'value': 'sm', 'label': 'Klein'}]),
    }
    return pkg('pagehero', ctl, {})


def footer_lux():
    ctl = {
        'logo': c('Logo', 'media', {'src': 'https://onecdn.io/media/7d0e1be6-3b43-400d-bec2-fb30c4090b17/full', 'name': 'logo-wernerbau-negative.svg', 'width': 1000, 'height': 667}, 'content', 'brand'),
        'logoAlt': c('Logo Alt-Text', 'text', 'WERNER GMBH Bauunternehmung', 'content', 'brand'),
        'claim': c('Satz neben dem Logo', 'text', 'Wir erhalten, was Hamburg ausmacht.', 'content', 'brand'),
        'ctaLabel': c('Button Text', 'text', 'Projekt anfragen', 'content', 'brand'),
        'ctaHref': c('Button Link', 'text', '/kontakt', 'content', 'brand'),
        'contactTitle': c('Überschrift', 'text', 'Kontakt', 'content', 'contact'),
        'company': c('Firma', 'text', 'WERNER GMBH Bauunternehmung', 'content', 'contact'),
        'address': c('Anschrift (eine Zeile pro Umbruch)', 'text', 'Heselstücken 10\n22453 Hamburg', 'content', 'contact'),
        'phone': c('Telefon', 'text', '(040) 357 032-74', 'content', 'contact'),
        'phoneHref': c('Telefon Link', 'text', PHONE_HREF, 'content', 'contact'),
        'email': c('E-Mail', 'text', EMAIL, 'content', 'contact'),
        'servicesTitle': c('Überschrift', 'text', 'Leistungen', 'content', 'services'),
        'serviceItems': c('Links', 'array', [n for n in NAV_MAIN if n['href'] not in ('/', '/ueber-uns', '/karriere')], 'content', 'services', items=LINK_ITEMS),
        'companyTitle': c('Überschrift', 'text', 'Unternehmen', 'content', 'company'),
        'companyItems': c('Links', 'array', [{'label': 'Über uns', 'href': '/ueber-uns'}, {'label': 'Referenzen', 'href': '/referenzen'}, {'label': 'Für Hausverwaltungen', 'href': '/hausverwaltungen'}, {'label': 'Karriere', 'href': '/karriere'}, {'label': 'Kontakt', 'href': '/kontakt'}], 'content', 'company', items=LINK_ITEMS),
        'groupTitle': c('Gruppe Überschrift', 'text', 'Ein Unternehmen der', 'content', 'group'),
        'groupLogo': c('Gruppe Logo', 'media', {'src': 'https://onecdn.io/media/3077348b-2423-4dca-a394-955347bc2d58/full', 'name': 'gruppenwerk-logo-weiss.svg', 'width': 439, 'height': 72}, 'content', 'group'),
        'showGroup': c('GRUPPENWERK anzeigen', 'checkbox', False, 'content', 'group'),
        'groupAlt': c('Gruppe Alt-Text', 'text', 'Zur Gruppenwerk Website', 'content', 'group'),
        'groupHref': c('Gruppe Link', 'text', 'https://www.gruppenwerk.de', 'content', 'group'),
        'legalItems': c('Rechtliche Links', 'array', [{'label': 'Impressum', 'href': '/impressum'}, {'label': 'Datenschutz', 'href': '/datenschutz'}], 'content', 'legal', items=LINK_ITEMS),
        'copyright': c('Copyright Name', 'text', 'WERNER GMBH Bauunternehmung', 'content', 'legal'),
    }
    return pkg('footer', ctl, {'brand': {'title': 'Logo & Button'}, 'contact': {'title': 'Kontakt'}, 'services': {'title': 'Leistungen'}, 'company': {'title': 'Unternehmen'}, 'group': {'title': 'Gruppenwerk'}, 'legal': {'title': 'Rechtliches'}})


def certs_lux(base):
    p = json.loads(json.dumps(base))
    ctl = {'eyebrow': c('Überzeile', 'text', 'Qualifikationen', 'content', 'root'),
           'title': c('Überschrift', 'text', 'Fachkunde, die wir nachweisen.', 'content', 'root')}
    ctl.update(p['onepage']['control'])
    p['onepage']['control'] = ctl
    return p


def steps_section(eyebrow, title, intro, steps, benefits):
    ctl = {
        'eyebrow': c('Überzeile', 'text', eyebrow, 'content', 'root'),
        'title': c('Überschrift', 'text', title, 'content', 'root'),
        'intro': c('Einleitung', 'text', intro, 'content', 'root'),
        'steps': c('Schritte', 'array', steps, 'content', 'steps', items={
            'who': {'title': 'Wer (z. B. SIE / WIR)', 'type': 'text'}, 'title': {'title': 'Titel', 'type': 'text'}, 'text': {'title': 'Text', 'type': 'text'}}),
        'benefits': c('Vorteile', 'array', benefits, 'content', 'benefits', items={
            'title': {'title': 'Titel', 'type': 'text'}, 'text': {'title': 'Text', 'type': 'text'}}),
    }
    return pkg('steps', ctl, {'steps': {'title': 'Schritte'}, 'benefits': {'title': 'Vorteile'}})


def _o(*labels):
    return [{'label': l} for l in labels]


def wizard(mode, form_id, left, person):
    """mode 'project' (Projektanfrage) or 'damage' (Schaden melden)."""
    damage = mode == 'damage'
    O = {'label': {'title': 'Text', 'type': 'text'}}
    T = {'big': {'title': 'Groß', 'type': 'text'}, 'label': {'title': 'Titel', 'type': 'text'}, 'sub': {'title': 'Zusatz', 'type': 'text'}}
    ctl = {

        'mode': c('Variante', 'select', mode, 'settings', 'form', options=[{'value': 'project', 'label': 'Projektanfrage'}, {'value': 'damage', 'label': 'Schaden melden (Hausverwaltung)'}]),
        'formId': c('CRM Formular-ID', 'text', form_id, 'settings', 'form'),
        'eyebrow': c('Überzeile', 'text', left['eyebrow'], 'content', 'left'),
        'title': c('Überschrift', 'text', left['title'], 'content', 'left'),
        'text': c('Text', 'text', left['text'], 'content', 'left'),
        'timeline': c('Ablauf (links)', 'array', left.get('timeline', []), 'content', 'left', items=T),
        'checks': c('Haken-Liste (links)', 'array', _o(*left.get('checks', [])), 'content', 'left', items=O),
        'personPhoto': c('Ansprechpartner Foto', 'media', person['photo'], 'content', 'person'),
        'personName': c('Ansprechpartner Name', 'text', person['name'], 'content', 'person'),
        'personRole': c('Ansprechpartner Funktion', 'text', person['role'], 'content', 'person'),
        'personLabel': c('Ansprechpartner Überzeile', 'text', 'Ihr Ansprechpartner', 'content', 'person'),
        'phone': c('Telefon', 'text', '(040) 357 032-74', 'content', 'person'),
        'phoneHref': c('Telefon Link', 'text', PHONE_HREF, 'content', 'person'),
        'email': c('E-Mail', 'text', EMAIL, 'content', 'person'),
        'tabQuickTitle': c('Reiter 1 Titel', 'text', 'Rückruf anfordern' if damage else 'Schnell-Anfrage', 'content', 'tabs'),
        'tabQuickSub': c('Reiter 1 Zusatz', 'text', 'Wenige Klicks, Rückruf am selben Werktag', 'content', 'tabs'),
        'tabFullTitle': c('Reiter 2 Titel', 'text', 'Schaden melden' if damage else 'Ausführlich', 'content', 'tabs'),
        'tabFullSub': c('Reiter 2 Zusatz', 'text', 'Adresse, Wohnungen, Fotos' if damage else 'Alle Details, mit Fotos', 'content', 'tabs'),
        'stepOf': c('Schritt-Trenner', 'text', '/', 'content', 'tabs'),
        'qWho': c('Frage: Wer meldet', 'text', 'Wer meldet?', 'content', 'reporter'),
        'whoOptions': c('Auswahl Wer meldet', 'array', _o('Hausverwaltung', 'Hausmeister', 'Vermieter / Eigentümer', 'Mieter'), 'content', 'reporter', items=O),
        'qScope': c('Frage: Was ist betroffen', 'text', 'Was ist betroffen?', 'content', 'reporter'),
        'scopeOptions': c('Auswahl Was ist betroffen', 'array', _o('Eine Wohnung', 'Mehrere Wohnungen', 'Treppenhaus & Gemeinschaftsflächen', 'Keller', 'Fassade & Dach', 'Außenanlagen'), 'content', 'reporter', items=O),
        'qCount': c('Frage: Anzahl Wohnungen', 'text', 'Wie viele Wohnungen?', 'content', 'questions'),
        'qCountUnit': c('Einheit Wohnungen', 'text', 'Wohnungen', 'content', 'questions'),
        'qCountHint': c('Hinweis Anzahl', 'text', 'Schätzung reicht', 'content', 'questions'),
        'qUrgency': c('Frage: Dringlichkeit', 'text', 'Wie dringend ist es?', 'content', 'questions'),
        'qServices': c('Frage: Leistung', 'text', 'Worum geht es?', 'content', 'questions2'),
        'qTime': c('Frage: Zeitraum', 'text', 'Wann soll es losgehen?', 'content', 'questions2'),
        'qObject': c('Frage: Projekt', 'text', 'Ihr Projekt', 'content', 'questions2'),
        'qPlace': c('Frage: Objekt', 'text', 'Objekt & Details', 'content', 'questions2'),
        'qUnits': c('Frage: Objekt & Wohnungen', 'text', 'Objekt & Wohnungen', 'content', 'questions'),
        'qDamage': c('Frage: Schaden', 'text', 'Was ist passiert?', 'content', 'questions'),
        'qContact': c('Frage: Kontakt', 'text', 'Ihre Kontaktdaten', 'content', 'questions2'),
        'serviceOptions': c('Auswahl Leistungen', 'array', _o('Fassadensanierung', 'Denkmalschutz', 'Balkonsanierung', 'Wohnungssanierung', 'Gebäudesanierung', 'Schule / öffentliches Gebäude'), 'content', 'options', items=O),
        'timeOptions': c('Auswahl Zeitraum', 'array', _o('So bald wie möglich', 'In 1–3 Monaten', 'In diesem Jahr', 'Noch offen'), 'content', 'options', items=O),
        'objectOptions': c('Auswahl Objektart', 'array', _o('Mehrfamilienhaus', 'Ein- oder Zweifamilienhaus', 'Gewerbeimmobilie', 'Öffentliches Gebäude'), 'content', 'options', items=O),
        'urgencyOptions': c('Auswahl Dringlichkeit', 'array', _o('Dringend', 'In den nächsten Wochen', 'Planbar', 'Leerwohnung vor Neuvermietung'), 'content', 'options', items=O),
        'damageOptions': c('Auswahl Schadensart', 'array', _o('Wasserschaden', 'Feuchtigkeit & Schimmel', 'Putz & Fassade', 'Balkon', 'Fenster & Türen', 'Sanitär', 'Elektro', 'Sonstiges'), 'content', 'options', items=O),
        'lCompany': c('Feld Firma', 'text', 'Hausverwaltung / Firma' if damage else 'Firma (optional)', 'content', 'fields'),
        'lName': c('Feld Name', 'text', 'Ihr Name', 'content', 'fields'),
        'lPhone': c('Feld Telefon', 'text', 'Telefon', 'content', 'fields'),
        'lEmail': c('Feld E-Mail', 'text', 'E-Mail', 'content', 'fields'),
        'lAddress': c('Feld Adresse', 'text', 'Adresse des Objekts', 'content', 'object'),
        'lAddressPh': c('Platzhalter Adresse', 'text', 'Straße, Hausnummer, Stadtteil', 'content', 'object'),
        'lPlace': c('Feld Ort', 'text', 'Ort / Stadtteil', 'content', 'fields'),
        'lPlacePh': c('Platzhalter Ort', 'text', 'z. B. Hamburg-Eppendorf', 'content', 'fields'),
        'lDescription': c('Feld Beschreibung', 'text', 'Kurze Beschreibung', 'content', 'fields'),
        'lDescriptionPh': c('Platzhalter Beschreibung', 'text', 'Was ist zu tun? Je genauer, desto besser.', 'content', 'fields'),
        'lUnit': c('Wohnung Titel', 'text', 'Wohnung / Bereich', 'content', 'units'),
        'lUnitLocation': c('Feld Lage', 'text', 'Lage (optional)', 'content', 'units'),
        'lUnitLocationPh': c('Platzhalter Lage', 'text', 'z. B. 2. OG links oder Treppenhaus', 'content', 'units'),
        'lTenantName': c('Feld Mieter', 'text', 'Mieter (optional)', 'content', 'units'),
        'lTenantContact': c('Feld Mieter-Kontakt', 'text', 'Telefon oder E-Mail des Mieters (optional)', 'content', 'units'),
        'lAddUnit': c('Weitere Wohnung', 'text', 'Weitere Wohnung hinzufügen', 'content', 'units'),
        'lRemoveUnit': c('Entfernen', 'text', 'Entfernen', 'content', 'units'),
        'lTenantConsent': c('Hinweis Mieter', 'text', 'Die Mieter wissen Bescheid und sind einverstanden, dass Werner Bau sie zur Terminabsprache kontaktiert.', 'content', 'units'),
        'lPhotos': c('Feld Fotos', 'text', 'Fotos (optional)', 'content', 'upload'),
        'lPhotosButton': c('Fotos Button', 'text', 'Fotos auswählen', 'content', 'upload'),
        'lPhotosHint': c('Fotos Hinweis', 'text', 'Bilder oder PDF, bis zu 8 Dateien', 'content', 'upload'),
        'contactHint': c('Hinweis Rückruf', 'text', 'Wir rufen Sie noch am selben Werktag zurück und klären alles Weitere persönlich.', 'content', 'legal'),
        'consentPre': c('Datenschutz vor Link', 'text', 'Mit dem Absenden nehmen Sie unsere', 'content', 'legal'),
        'privacyLabel': c('Datenschutz Link Text', 'text', 'Datenschutzerklärung', 'content', 'legal'),
        'privacyHref': c('Datenschutz Link', 'text', '/datenschutz', 'content', 'legal'),
        'consentPost': c('Datenschutz nach Link', 'text', 'zur Kenntnis.', 'content', 'legal'),
        'nextLabel': c('Weiter', 'text', 'Weiter', 'content', 'buttons'),
        'backLabel': c('Zurück', 'text', 'Zurück', 'content', 'buttons'),
        'submitLabel': c('Absenden', 'text', 'Schaden melden' if damage else 'Anfrage senden', 'content', 'buttons'),
        'sendingLabel': c('Wird gesendet', 'text', 'Wird gesendet …', 'content', 'buttons'),
        'successTitle': c('Erfolg Titel', 'text', 'Vielen Dank!', 'content', 'messages'),
        'successText': c('Erfolg Text', 'text', 'Ihre Meldung ist bei uns angekommen. Wir melden uns noch am selben Werktag bei Ihnen.' if damage else 'Ihre Anfrage ist bei uns angekommen. Wir melden uns noch am selben Werktag bei Ihnen.', 'content', 'messages'),
        'errorText': c('Fehler Text', 'text', 'Das hat leider nicht geklappt. Bitte versuchen Sie es erneut oder rufen Sie uns an.', 'content', 'messages'),
        'requiredError': c('Pflichtfeld Hinweis', 'text', 'Bitte füllen Sie die markierten Pflichtfelder aus.', 'content', 'messages'),
        'emailError': c('E-Mail Hinweis', 'text', 'Bitte geben Sie eine gültige E-Mail-Adresse ein.', 'content', 'messages'),
    }
    groups = {k: {'title': t} for k, t in [('form', 'Formular'), ('left', 'Linke Seite'), ('person', 'Ansprechpartner'), ('tabs', 'Reiter'), ('reporter', 'Wer & Was'), ('questions', 'Fragen Hausverwaltung'), ('questions2', 'Fragen Projekt'), ('object', 'Objekt'),
                                           ('options', 'Auswahlmöglichkeiten'), ('fields', 'Felder'), ('units', 'Wohnungen'), ('upload', 'Fotos'), ('legal', 'Hinweise'),
                                           ('buttons', 'Buttons'), ('messages', 'Meldungen')]}
    return pkg('wizard', ctl, groups)
