"""Über uns in the calm split style: banner, text sections as 50/50 rows (text verbatim from
PAGES['ueber-uns']), large team portraits, certificates, footer. Writes out-about/<n>-<comp>.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pages  # noqa
from gen import split, people  # noqa

comp = {c: p for c, _t, p in pages.PAGES['ueber-uns']}
team = {k: v['default'] for k, v in comp['team']['onepage']['control'].items()}
intro, erfahrung = team['introBlocks']
values = team['valuesBlocks'][0]
group = team['groupBlocks'][0]

rows = [
    {'title': intro['title'], 'text': intro['text'], 'photo': 'fassade-oberfinanzdirektion-5.jpg'},
    {'title': erfahrung['title'], 'text': erfahrung['text'], 'photo': 'fassadensanierung-hamburg-3.jpg'},
    {'title': values['title'], 'text': values['text'], 'photo': 'fassadensanierung-hamburg-13.jpg'},
    {'title': group['title'], 'text': group['text'], 'photo': 'Gruppenwerk_Logo_RGB-43e28d96.png',
     'imageAlt': team['groupLogoAlt'], 'imageFit': 'contain'},
]
body = split(rows, [])
body['onepage']['control']['photos']['default'] = []

persons = [dict(p, photoAlt='Porträt ' + p['name'] + ', ' + p['role']) for p in team['people']]

OUT = [('header', comp['header']), ('hero', comp['hero']), ('split', body),
       ('people', people(persons, 'Team', 'Ihre Ansprechpartner')), ('certs', comp['certs']), ('footer', comp['footer'])]
if __name__ == '__main__':
    os.makedirs('out-about', exist_ok=True)
    for i, (c, p) in enumerate(OUT, 1):
        json.dump(p, open('out-about/%d-%s.json' % (i, c), 'w'), indent=2, ensure_ascii=False)
        print(i, c)
