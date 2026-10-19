"""Page specs: ordered (component, title, package.json) per page. Writes out/<page>/<n>-<comp>.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import *  # noqa

F = 'fassadensanierung/'
W = 'wohnungssanierung/'
O = 'oeffentliche-einrichtungen/'
BAN = '_themes/lightwhite/banner/'

PAGES = {}

PAGES['start'] = [
    ('header', 'Navigation', header('/')),
    ('hero', 'Hero', hero(img(BAN + 'banner-1.jpg'), 'WERNER BAU', eyebrow='WERNER GMBH Bauunternehmung',
                          text='Zuverlässig – Erfahren – Qualifiziert', primary=('Kontakt', '/kontakt'),
                          secondary=('Mehr Infos', '#leistungen'), height='lg', size='xxl', overlay=75)),
    ('services', 'Leistungen', services([
        {'image': img(F + 'fassadensanierung-hamburg-1.jpg'), 'imageAlt': 'Fassadensanierung', 'title': 'FASSADENSANIERUNG',
         'text': 'Die fachgerechte Erhaltung einer Fassade dient der Werterhaltung des gesamten Gebäudes. Sie ist die schützende Hülle eines jeden Bauwerks und bestimmt dessen optischen Gesamteindruck. Die Fassadensanierung bedarf Erfahrung und umfassende Fachkenntnisse - insbesondere, wenn es sich um Altbauobjekte oder unter Denkmalschutz stehende Gebäude handelt. Als traditionsreiches Unternehmen, welches bald 100 Jahre tätig ist, können wir auf einen umfangreichen Erfahrungsschatz zurückgreifen. Im Rahmen der Fassadensanierung führen wir auch bekämpfende Holzschutzmaßnahmen sowie die Sanierung von Balkonen durch.',
         'buttonLabel': 'Mehr Infos', 'buttonHref': '/fassadensanierung'},
        {'image': img(W + 'Wohnungssanierung-Kueche-1b-nacher.jpg'), 'imageAlt': 'Wohnungs- & Gebäudesanierung', 'title': 'WOHNUNGS- & GEBÄUDESANIERUNG',
         'text': 'Die Sanierung von Wohnraum und ganzer Gebäude erfordert neben qualitativ hochwertiger und fachgerechter Umsetzung vor allen Dingen eine termingerechte Fertigstellung. Denn jeder Leerstand von Wohn- oder Gewerbeflächen verursacht beim Eigentümer zusätzliche Kosten. Das Management aller Gewerke sowie die einwandfreie und terminierte Umsetzung hat daher bei uns höchste Priorität. Von Maurer-, Putz- und Malerarbeiten über den Einbau von Türen und Fenstern sowie Heizungs-, Elektro- und Sanitärtechnik bis hin zu Bodenbelags- & Fliesenarbeiten – bei uns erhalten Sie alle Leistungen aus einer Hand.',
         'buttonLabel': 'Mehr Infos', 'buttonHref': '/wohnungs-gebaeudesanierung'},
        {'image': img(O + 'c_0083_1000px.jpg'), 'imageAlt': 'Öffentliche Einrichtungen', 'title': 'ÖFFENTLICHE EINRICHTUNGEN',
         'text': 'Seit Jahrzehnten setzen wir umfangreiche Projekte im Bereich der Fassaden- sowie Innenraumsanierung für öffentliche Auftraggeber um. So sind wir bestens vertraut mit den Anforderungen öffentlicher Auftraggeber und haben ein umfangreiches Know-how – insbesondere im Bereich der historischen und denkmalgeschützten Gebäude, wie beispielsweise die zahlreichen Hamburger Schulen mit historischen Backsteinfassaden. Für öffentliche Vergabeverfahren sind wir natürlich präqualifiziert und weisen die Eignungsvoraussetzungen der VOB mit der PQ VOB nach.',
         'buttonLabel': 'Mehr Infos', 'buttonHref': '/oeffentliche-einrichtungen'},
    ])),
    ('about', 'Über uns', about(img(F + 'fassade-oberfinanzdirektion.jpg'), 'WERNER BAU', 'Zuverlässig – Erfahren – Qualifiziert',
        'Unser traditionsreiches, mittelständisches Unternehmen mit Sitz in Hamburg kann auf eine fast hundertjährige Geschichte zurückblicken. Seit jeher ist es unser Anspruch, für unsere Kunden die optimale Lösung zu finden und diese nach höchsten Qualitätsanforderungen umzusetzen. Dabei pflegen wir mit unseren Kunden eine partnerschaftliche Zusammenarbeit. Sie können sich auf unsere Absprachen verlassen und sicher sein, eine ehrliche und kompetente Beratung zu erhalten.\n\nErfahrungen wurden bei uns seit jeher von Generation zu Generation weitergegeben und werden fortlaufend durch Schulungsprogramme zu neuen, innovativen Produkten und Techniken ausgebaut.',
        ('Mehr Infos', '/ueber-uns'))),
    ('footer', 'Footer', footer()),
]

def sub(active, banner, h1, blocks, gal_cat=None, extra=None):
    secs = [('header', 'Navigation', header(active)),
            ('hero', 'Hero', hero(img(BAN + banner), h1, height='md', size='xl', overlay=65)),
            ('content', 'Inhalt', content(blocks))]
    if gal_cat:
        secs.append(('gallery', 'Galerie', gallery(cat(gal_cat), eyebrow=h1)))
    if extra:
        secs += extra
    secs.append(('certs', 'Qualifikationen', certs()))
    secs.append(('footer', 'Footer', footer()))
    return secs


PAGES['fassadensanierung'] = sub('/fassadensanierung', 'banner-1.jpg', 'Fassadensanierung', [
    {'lead': True, 'text': 'Die Fassade bestimmt stets den ersten Gesamteindruck eines Gebäudes. Sie nimmt Einfluss auf den Charakter ganzer Straßenzüge und Stadtteile. Teilweise sind Fassaden sogar Zeugen unserer Geschichte - insbesondere Altbauten und denkmalgeschützte Gebäude sind hier anzuführen. Entsprechend wichtig ist die fachgerechte Erhaltung der Fassade – nicht nur aus optischen Gesichtspunkten. Fassadensanierung dient der Werterhaltung des gesamten Gebäudes.'},
    {'title': 'Individuelle Sanierungskonzepte', 'layout': 'imageRight', 'image': img(F + 'fassadensanierung-hamburg-experten.jpg'), 'imageAlt': 'Individuelle Sanierungskonzepte',
     'text': 'Schäden an Fassaden können unterschiedlichsten Ursprungs sein: Umwelteinflüsse durch Abgase, Witterung aber auch chemische Prozesse wirken auf die Fassade. Ein universell einsetzbares Verfahren zur Erhaltung und Sanierung von Mauerwerk und Fassade gibt es nicht. Wir erarbeiten individuelle Sanierungskonzepte auf Basis der vorliegenden Schädigung und der eingesetzten Baustoffe.\n\nAuf Basis unserer langjährigen Erfahrung sowie umfassenden Fachkenntnissen über bauphysikalische Zusammenhänge sanieren wir Mauerwerk und Fassaden von Ein- und Mehrfamilienhäusern, Wohnhäusern sowie Öffentlichen Einrichtungen. Wir sind Experten für die fachgerechte Sanierung von',
     'bullets': 'Mauerwerk,\nPutzfassaden,\nBacksteinfassaden,\nNatursteinfassaden,\nVerblendfassaden sowie\nBetonoberflächen und Holzelementen.'},
    {'title': 'Denkmalschutz', 'layout': 'imageLeft', 'image': img(F + 'fassade-oberfinanzdirektion-1.jpg'), 'imageAlt': 'Denkmalschutz',
     'text': 'Insbesondere Altbauobjekte und unter Denkmalschutz stehende Gebäude machen den Charme Hamburgs aus und sorgen für ein Stück Geschichte in unseren Straßen. Umso wichtiger ist die fachgerechte Erhaltung dieser Gebäude. In aller Regel wurde viel Mühe zur Gestaltung der Fassaden historischer Gebäude aufgebracht. Ebenso viel Mühe sollte in den Erhalt dieser Werke gesteckt werden.\n\nWir haben uns auf die Sanierung denkmalgeschützter Gebäude spezialisiert. Neben handwerklichem Geschick erfordert dies vor allem umfangreiche Kenntnisse der Arbeitsmethoden, der Materialien und nicht zuletzt der Stilkunde. Den Charakter unserer Hansestadt auf diese Art und Weise zu erhalten, erfüllt uns mit Stolz.'},
    {'title': 'Balkonsanierung', 'layout': 'imageRight', 'image': img(F + 'fassade-sanierung-balkon-1.jpg'), 'imageAlt': 'Balkonsanierung',
     'text': 'Eine besondere Herausforderung im Rahmen der Balkonsanierung stellt hier die Abdichtung dar. Eindringen von Wasser in den Unterbau kann schwere Folgen wie die Korrosion der Bewehrung mit sich bringen. Jede Balkonsanierung beginnt bei uns mit einer Untersuchung der Bausubstanz auf Feuchtigkeit und bestehende Schäden. Anforderungen wie die Festigkeit des Estrichs, das Gefälle des Balkons und der Übergang zur Hauswand müssen gegeben sein, um mit der Reinigung und Beschichtung des Balkons fortfahren zu können. Die vollflächige und nahtlose Beschichtung mit elastischem Flüssigkunststoff stellt die Abdichtung sicher. Für den Belag des Balkons stehen zahlreiche Möglichkeiten zur Verfügung, die sich an der Gestaltung des Hauses orientieren sollten.'},
    {'title': 'Bekämpfende Holzschutzmaßnahmen', 'layout': 'imageLeft', 'image': img(F + 'fassadensanierung_villa_1b_nachher.jpg'), 'imageAlt': 'Bekämpfende Holzschutzmaßnahmen',
     'text': 'Holz zerstörende Pilze, welche durch Feuchtigkeit verursacht werden, und Insekten können Holzfassaden und -elemente elementar schädigen. Vorbeugende Maßnahmen sind sehr empfehlenswert. Wurde dies jedoch verpasst und ist der Befall von Pilzen oder Insekten bereits gegeben, sollten unverzüglich bekämpfende Holzschutzmaßnahmen eingeleitet werden. Die jeweiligen Sanierungsschritte werden nach einer genauen Analyse geplant und sind abhängig von der Art des Befalls sowie vom Beschädigungsgrad des Holzes.'},
], 'fassade')

PAGES['wohnung'] = sub('/wohnungs-gebaeudesanierung', 'banner-2.jpg', 'Wohnungssanierung & Gebäuderevitalisierung', [
    {'lead': True, 'text': 'Als Vermieter sind gepflegte Immobilien unerlässlich, um angemessene Mietrenditen und Wertsteigerungen zu erzielen. Doch Leerstand von Wohn- und Gewerbeflächen kostet. Eine termingerechte und fachmännische Sanierung ist erforderlich, um eine zügige Wiedervermietung sicherzustellen. Wir sind spezialisiert auf die umfassende und ganzheitliche Sanierung von Wohnungen im Bestand sowie die komplette Revitalisierung von Gebäuden. Durch gute Planung und Arbeitsvorbereitung stellen wir die qualitativ einwandfreie sowie terminierte Fertigstellung unserer Sanierungsprojekte sicher.'},
    {'title': 'Alle Arbeiten aus einer Hand', 'layout': 'imageRight', 'image': img(W + 'Wohnungssanierung-Badezimmer-1b-nachher.jpg'), 'imageAlt': 'Alle Arbeiten aus einer Hand',
     'text': 'Bei uns haben Sie einen Ansprechpartner, welcher mit Ihnen das Projekt bespricht und während der Projektzeit zur Seite steht. Wir liefern alle Leistungen bis zur bezugsfertigen Wohneinheit aus einer Hand. Sie müssen sich nicht mit unterschiedlichen Gewerken abstimmen. Arbeiten, die wir nicht selbst ausführen, werden ausschließlich durch verlässliche Spezialisten, mit denen wir schon viele Jahre zusammenarbeiten, durchgeführt. Gemeinsam mit unseren Partnern führen wir alle Sanierungs- und Revitalisierungsarbeiten nach höchsten Ansprüchen durch, dazu gehören',
     'bullets': 'Maurer- & Putzarbeiten,\nTrockenbauarbeiten,\nFenster- & Türenbau,\nMaler- & Stuckarbeiten,\nHeizungs-, Elektro- & Sanitärtechnik,\nBodenbelags- & Fliesenarbeiten,\nEinbau von Küchen,\nBalkon- & Fassadensanierung sowie\ndie Umsetzung von Anbauten.'},
    {'title': 'Rahmenverträge für die Wohnungswirtschaft', 'layout': 'imageLeft', 'image': img(W + 'Wohnungssanierung-Flur-1b-nachher.jpg'), 'imageAlt': 'Rahmenverträge für die Wohnungswirtschaft',
     'text': 'Mit unseren Kunden der Hamburger Wohnungswirtschaft pflegen wir lange und partnerschaftliche Zusammenarbeiten. Bei der Sanierung von Leerwohnungen aber auch gesamten Gebäuden arbeiten wir in der Regel über Rahmenverträge. Dies gibt Ihnen Kostensicherheit bei voller Flexibilität. Änderungen und besondere Wünsche können natürlich jederzeit mit Ihrem persönlichen Ansprechpartner bei uns im Hause besprochen und kalkuliert werden.'},
    {'title': 'Kellertrockenlegung', 'layout': 'text',
     'text': 'Bei feuchten Kellerwänden oder gar Schimmel an den Wänden empfiehlt sich zügiges Handeln. Feuchtigkeit als Ursache für viele Arten von Bauschäden beeinflusst die Lebensdauer eines Bauwerkes maßgeblich. Nicht nur zum Schutz der Bausubstanz sollte die Dichtigkeit des Kellers gegeben sein, Pilze oder Mikroorganismen können sich ansiedeln und die Gesundheit der Bewohner beeinträchtigen.\n\nJeder Kellertrockenlegung geht bei uns eine Analyse der Ursachen voraus, wie die Feuchtigkeit eindringen konnte. Auf Basis der Ergebnisse leiten wir individuelle Maßnahmen zur Sanierung und Trockenlegung der Kellerräume ab. In der Umsetzung arbeiten wir ausschließlich mit den hochwertigen und praxiserprobten Produktsystemen von Remmers. Wir vertrauen in die innovativen Produktsysteme des deutschen Herstellers und können Ihnen mit der Remmers-System-Garantie (RSG) eine 10-jährige Qualitätsgarantie geben.'},
], 'wohnung')

PAGES['oeffentlich'] = sub('/oeffentliche-einrichtungen', 'banner-4.jpg', 'Schulen & öffentliche Einrichtungen', [
    {'lead': True, 'text': 'Die Sanierung öffentlicher Einrichtungen erfordert spezielle Kenntnisse, insbesondere wenn es sich um Altbau oder gar denkmalgeschützte Bauwerke handelt. Beispielhaft sind hier die vielen Hamburger Schulen aus Backstein anzuführen. Durch unsere Spezialisierung auf die Fassadensanierung sowie die Innenraumsanierung decken wir das nötige Leistungsspektrum zur fachgerechten Umsetzung optimal ab. Aus diesem Grund arbeiten wir seit Jahrzehnten für öffentliche Auftraggeber und verfügen über einen entsprechend großen Erfahrungsschatz.'},
    {'title': 'Alle Arbeiten aus einer Hand', 'layout': 'imageRight', 'image': img(O + 'c_0125_1000px.jpg'), 'imageAlt': 'Alle Arbeiten aus einer Hand',
     'text': 'Von der Fassade über die Kantine bis hin zur Umsetzung von Anbauten - bieten wir Ihnen alle Leistungen, welche für die Sanierung oder Erweiterung von öffentlichen Einrichtungen notwendig sind. Arbeiten, die wir nicht selbst ausführen, werden ausschließlich durch verlässliche Spezialisten, mit denen wir schon viele Jahre zusammenarbeiten, durchgeführt. Sie als Auftraggeber müssen sich nicht mit verschiedenen Gewerken abstimmen, dies übernimmt Ihr Ansprechpartner aus unserem Hause. Gemeinsam mit unseren Partnern führen wir alle Arbeiten nach höchsten Ansprüchen an Qualität und fachgerechter Umsetzung durch, dazu gehören',
     'bullets': 'Maurer-, Fassaden- & Putzarbeiten,\nFenster- & Türenbau,\nMaler- & Stuckarbeiten,\nHeizungs-, Elektro- & Sanitärtechnik,\nBodenbelags- & Fliesenarbeiten,\nTischlerarbeiten,\nFassadensanierung sowie\ndie Umsetzung von Anbauten.'},
    {'title': 'Schulen & Bildungseinrichtungen', 'layout': 'imageLeft', 'image': img(O + 'b_9849_1000px.jpg'), 'imageAlt': 'Schulen & Bildungseinrichtungen',
     'text': 'Mit zahlreichen Hamburger Bildungseinrichtungen arbeiten wir bereits seit vielen Jahren partnerschaftlich zusammen. Oft laufen diese Zusammenarbeiten über Rahmenverträge. So beispielsweise auch im Bereich des Hochschulbaus mit der HAW (Hochschule für Angewandte Wissenschaften Hamburg).\n\nSie haben einen festen Ansprechpartner bei uns im Hause, der Ihre Immobilie ganz genau kennt. So können Sie sich immer sicher sein, beste Beratung für das jeweilige Bauwerk zu erhalten und eine zügige Umsetzung erwarten.'},
    {'title': 'Denkmalschutz', 'layout': 'imageRight', 'image': img(F + 'fassade-oberfinanzdirektion-2.jpg'), 'imageAlt': 'Oberfinanzdirektion am Rödingsmarkt',
     'text': 'Insbesondere denkmalgeschützte Bauwerke aber auch die vielen historischen Backstein-Fassaden, wie sie bei Hamburger Schulen zu finden sind, erfordern Know-how und Erfahrung bei Reparatur, Erweiterungs- oder Sanierungsarbeiten. Wir haben uns auf die Sanierung denkmalgeschützter Gebäude spezialisiert. Neben handwerklichem Geschick stellen wir durch umfangreiche Kenntnisse der Arbeitsmethoden, der Materialien und nicht zuletzt der Stilkunde die fachgerechte Umsetzung sicher.\n\nBeispielhaft kann die denkmalgeschützte Oberfinanzdirektion am Rödingsmarkt angeführt werden. Im Jahr 2006 haben wir die Fassade des 1907 im Stil des Neobarocks erbauten Bauwerks saniert. Die Geschichte Hamburgs auf diese Art und Weise zu pflegen, erfüllt uns mit Stolz.'},
    {'title': 'Präqualifiziert', 'layout': 'text',
     'text': 'Wir sind für öffentliche Vergabeverfahren präqualifiziert. Mit der PQ VOB weisen wir die Eignungsvoraussetzungen der VOB in Bezug auf unsere Fachkunde, Zuverlässigkeit und Leistungsfähigkeit nach.'},
], 'oeffentlich')

PAGES['ueber-uns'] = sub('/ueber-uns', 'banner-1.jpg', 'Über uns', [
    {'lead': True, 'text': 'Wir sind ein traditionsreiches Hamburger Bauunternehmen, das auf eine bald hundertjährige Firmengeschichte zurückblicken kann. Erfahrungen werden bei uns seit jeher von Generation zu Generation weitergegeben. Spezialisiert auf Sanierungsarbeiten – sowohl für Wohn- und Gewerbeimmobilien als auch öffentliche Einrichtungen – konnten wir das Stadtbild Hamburgs im Laufe unserer Geschichte schon ein wenig mitgestalten und blicken immer wieder gern auf unsere umgesetzten Projekte.'},
    {'title': 'Erfahrung & Know-How', 'layout': 'imageRight', 'image': img(F + 'fassadensanierung-hamburg-experten-2.jpg'), 'imageAlt': 'Erfahrung & Know-How',
     'text': 'Wir sind seit fast 100 Jahren am Markt. Erfahrungen wurden bei uns seit jeher von Generation zu Generation übertragen. Wir setzen seit Jahren auf einen bestehenden festen und qualifizierten Mitarbeiterstamm. Durch Weiterbildungsmaßnahmen aber auch den internen Austausch stellen wir die stetige Weiterentwicklung sicher. Dank Schulungen zu innovativen Produkten und Techniken beherrschen wir auch diese und können Ihnen stets das optimale Verfahren für die Umsetzung Ihres Projektes empfehlen.'},
    {'title': 'Wofür wir stehen', 'layout': 'text',
     'text': 'Wir sind zuverlässig. Auf unsere Absprachen können Sie zählen. Vereinbarte Termine und Ausführungen werden bei uns so abgeliefert wie besprochen.\n\nWir liefern Qualität. Wir blicken mit Stolz auf unsere umgesetzten Projekte. Das können wir, weil wir ein jedes Projekt mit unserem hohen Anspruch an Qualität umsetzen. Deshalb arbeiten wir auch nur mit Spezialisten anderer Gewerke zusammen, welche den gleichen Anspruch an fachgerechte und qualitativ hochwertige Umsetzung haben wie wir.\n\nWir finden die optimale Lösung für Sie. Wir führen kein Projekt nach Schema F durch. Grundlage einer jeden Sanierung ist eine Untersuchung der Ursachen. Anhand der Ergebnisse entwickeln wir das optimale Konzept zur Umsetzung Ihres Vorhabens. Ehrliche Beratung wird bei uns groß geschrieben.'},
    {'title': 'Teil einer starken Gruppe', 'layout': 'text',
     'text': 'Die Werner GmbH Bauunternehmung ist Teil der Unternehmensgruppe GRUPPENWERK, der mittelständische Betriebe der norddeutschen Handwerks und Immobilienwirtschaft angehören. Alle Unternehmen der Gruppe vereinigt ein gemeinsamer Qualitätsanspruch und der Antrieb unsere Kunden zu begeistern. Unsere Vision: Gemeinsam erreichen wir den größten Mehrwert für jedes einzelne Unternehmen, unsere Kunden und Mitarbeiter.'},
], None, extra=[('team', 'Team', team())])

PAGES['kontakt'] = [
    ('header', 'Navigation', header('/kontakt')),
    ('hero', 'Hero', hero(img(BAN + 'banner-3.jpg'), 'Kontakt', height='sm', size='xl', overlay=65)),
    ('contact', 'Kontakt', contact()),
    ('certs', 'Qualifikationen', certs()),
    ('footer', 'Footer', footer()),
]

PAGES['impressum'] = [
    ('header', 'Navigation', header('/impressum')),
    ('content', 'Impressum', content([
        {'title': 'Impressum', 'h1': True, 'layout': 'text',
         'text': 'WERNER GMBH\nBauunternehmung\nHeselstücken 10\n22453 Hamburg\n\nTelefon: (040) 357 032-74\nTelefax: (040) 357 032-680\nE-Mail: info@werner-bau.eu\n\nUSt-ID: DE 118 694 510\nHandelsregister: HR Hamburg, Nr.B 38869\nGeschäftsführer: Meik Thie, Axel Seehafer\n\nVerantwortlich für den Inhalt:\nAxel Seehafer'},
        {'title': 'Urheberrechte', 'layout': 'text',
         'text': 'Werner GmbH\nAlle Rechte vorbehalten.\n\nInhalte der Website unterliegen dem Schutz des Urheberrechts und anderer Schutzgesetze. Die Vervielfältigung von Informationen oder Daten, insbesondere die Verwendung von Texten, Textteilen oder Bildmaterial, bedarf der vorherigen Zustimmung der Werner GmbH.\n\nAls öffentlich gekennzeichnete Dokumente (wie Pressemitteilungen) dürfen in öffentlichen Mitteilungen verwenden werden.'},
        {'title': 'Haftungsbeschränkung', 'layout': 'text',
         'text': 'Diese Website wurde mit größtmöglicher Sorgfalt zusammengestellt und wird regelmäßig aktualisiert. Trotzdem kann keine Gewähr für die Fehlerfreiheit und Genauigkeit der enthaltenen Informationen übernommen werden. Jegliche Haftung für Schäden, die direkt oder indirekt aus der Benutzung dieser Website entstehen, wird ausgeschlossen, soweit diese nicht auf Vorsatz oder grober Fahrlässigkeit beruhen.\n\nSofern von dieser Website auf Internetseiten verwiesen wird, die von Dritten betrieben werden, haftet die Werner GmbH nicht für deren Inhalte.\n\nDie Werner GmbH behält sich das Recht vor, Änderungen oder Ergänzungen der an bereitgestellten Informationen jederzeit vorzunehmen.'},
    ], compact=True)),
    ('footer', 'Footer', footer()),
]

GA_OPT = 'Sie können die Erfassung Ihrer Daten durch Google Analytics verhindern, indem Sie auf folgenden Link klicken. Es wird ein Opt-Out-Cookie gesetzt, der die Erfassung Ihrer Daten bei zukünftigen Besuchen dieser Website verhindert: Google Analytics deaktivieren'
PAGES['datenschutz'] = [
    ('header', 'Navigation', header('/datenschutz')),
    ('content', 'Datenschutz', content([
        {'title': 'Datenschutz', 'h1': True, 'layout': 'text',
         'text': 'Die Betreiber dieser Seiten nehmen den Schutz Ihrer persönlichen Daten sehr ernst. Wir behandeln Ihre personenbezogenen Daten vertraulich und entsprechend der gesetzlichen Datenschutzvorschriften sowie dieser Datenschutzerklärung.\n\nDie Nutzung unserer Webseite ist in der Regel ohne Angabe personenbezogener Daten möglich. Soweit auf unseren Seiten personenbezogene Daten (beispielsweise Name, Anschrift oder E-Mail-Adressen) erhoben werden, erfolgt dies, soweit möglich, stets auf freiwilliger Basis. Diese Daten werden ohne Ihre ausdrückliche Zustimmung nicht an Dritte weitergegeben.\n\nWir weisen darauf hin, dass die Datenübertragung im Internet (z.B. bei der Kommunikation per E-Mail) Sicherheitslücken aufweisen kann. Ein lückenloser Schutz der Daten vor dem Zugriff durch Dritte ist nicht möglich.'},
        {'title': 'Cookies', 'layout': 'text',
         'text': 'Die Internetseiten verwenden teilweise so genannte Cookies. Cookies richten auf Ihrem Rechner keinen Schaden an und enthalten keine Viren. Cookies dienen dazu, unser Angebot nutzerfreundlicher, effektiver und sicherer zu machen. Cookies sind kleine Textdateien, die auf Ihrem Rechner abgelegt werden und die Ihr Browser speichert.\n\nDie meisten der von uns verwendeten Cookies sind so genannte „Session-Cookies“. Sie werden nach Ende Ihres Besuchs automatisch gelöscht. Andere Cookies bleiben auf Ihrem Endgerät gespeichert, bis Sie diese löschen. Diese Cookies ermöglichen es uns, Ihren Browser beim nächsten Besuch wiederzuerkennen.\n\nSie können Ihren Browser so einstellen, dass Sie über das Setzen von Cookies informiert werden und Cookies nur im Einzelfall erlauben, die Annahme von Cookies für bestimmte Fälle oder generell ausschließen sowie das automatische Löschen der Cookies beim Schließen des Browser aktivieren. Bei der Deaktivierung von Cookies kann die Funktionalität dieser Website eingeschränkt sein.'},
        {'title': 'Kontaktformular', 'layout': 'text',
         'text': 'Wenn Sie uns per Kontaktformular Anfragen zukommen lassen, werden Ihre Angaben aus dem Anfrageformular inklusive der von Ihnen dort angegebenen Kontaktdaten zwecks Bearbeitung der Anfrage und für den Fall von Anschlussfragen bei uns gespeichert. Diese Daten geben wir nicht ohne Ihre Einwilligung weiter.'},
        {'title': 'Datenschutzerklärung für die Nutzung von Google Analytics', 'layout': 'text',
         'text': 'Diese Website nutzt Funktionen des Webanalysedienstes Google Analytics. Anbieter ist die Google Inc., 1600 Amphitheatre Parkway Mountain View, CA 94043, USA.\n\nGoogle Analytics verwendet so genannte "Cookies". Das sind Textdateien, die auf Ihrem Computer gespeichert werden und die eine Analyse der Benutzung der Website durch Sie ermöglichen. Die durch den Cookie erzeugten Informationen über Ihre Benutzung dieser Website werden in der Regel an einen Server von Google in den USA übertragen und dort gespeichert.\n\n' + GA_OPT + '.\n\nMehr Informationen zum Umgang mit Nutzerdaten bei Google Analytics finden Sie in der Datenschutzerklärung von Google: https://support.google.com/analytics/answer/6004245?hl=de'},
        {'title': 'Browser Plugin', 'layout': 'text',
         'text': 'Sie können die Speicherung der Cookies durch eine entsprechende Einstellung Ihrer Browser-Software verhindern; wir weisen Sie jedoch darauf hin, dass Sie in diesem Fall gegebenenfalls nicht sämtliche Funktionen dieser Website vollumfänglich werden nutzen können. Sie können darüber hinaus die Erfassung der durch den Cookie erzeugten und auf Ihre Nutzung der Website bezogenen Daten (inkl. Ihrer IP-Adresse) an Google sowie die Verarbeitung dieser Daten durch Google verhindern, indem Sie das unter dem folgenden Link verfügbare Browser-Plugin herunterladen und installieren: https://tools.google.com/dlpage/gaoptout?hl=de'},
        {'title': 'Widerspruch gegen Datenerfassung', 'layout': 'text', 'text': GA_OPT},
        {'title': 'Auftragsdatenverarbeitung', 'layout': 'text',
         'text': 'Wir haben mit Google einen Vertrag zur Auftragsdatenverarbeitung abgeschlossen und setzen die strengen Vorgaben der deutschen Datenschutzbehörden bei der Nutzung von Google Analytics vollständig um.\n\nQuellverweis: https://www.e-recht24.de'},
    ], compact=True)),
    ('footer', 'Footer', footer()),
]

if __name__ == '__main__':
    page = sys.argv[1]
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', page)
    os.makedirs(out, exist_ok=True)
    for i, (comp, title, p) in enumerate(PAGES[page]):
        fn = os.path.join(out, f'{i + 1}-{comp}.json')
        json.dump(p, open(fn, 'w'), indent=2, ensure_ascii=False)
        print(fn, os.path.getsize(fn), title)
