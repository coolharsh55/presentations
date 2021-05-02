#!/usr/bin/env python3
#author: Harshvardhan J. Pandit

# produce HTML output from `tree` command file listing
# takes JSON output and fills in a JINJA2 template

from jinja2 import FileSystemLoader, Environment
import json
import subprocess
subprocess.getoutput('tree -hr -H . -o tree.html -T "Presentations"')
output = json.loads(subprocess.getoutput('tree -hr -J'))
with open('tree.json', 'w+') as fd:
    fd.write(json.dumps(output, indent=2))

IGNORED_FILES = (
    'index.html',
    'index_template.html',
    'generate.py'
    )

data = list(filter(
    lambda x: x['type'] == 'directory', 
    output[0]['contents']))

DATA = []

for data_year in data:
    items = {}
    for contents in data_year['contents']:
        name = contents['name']
        size = contents['size']
        title, extension = name.split('.')
        if title in items:
            items[title]['formats'].append((extension, size))
            items[title]['formats'].sort()
        else:
            items[title] = {
                'href': title,
                'name': title.replace('_', ' ')[:-5],
                'formats': [(extension, size)],
            }
    items = sorted((
        tuple(x.values()) for x in items.values()),
        key=lambda x: x[0])
    DATA.append((data_year['name'], items))

template_loader = FileSystemLoader(searchpath='.')
template_env = Environment(
    loader=template_loader, 
    autoescape=True, trim_blocks=True, lstrip_blocks=True)
template = template_env.get_template('index_template.html')
with open('index.html', 'w+') as fd:
    fd.write(template.render(DATA=DATA))
