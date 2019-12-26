#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert an Enpass export file so it can be imported to a KeePass database using KeePassXC

Documentation & Issues: https://github.com/jsphpl/enpass-to-keepass

License: Public Domain
Author: Joseph Paul <joseph@sehrgute.software>

Updated by: deltreey 2019-12-26
"""

import argparse
import csv
import json

ALLOWED_FIELDS = ['url', 'username', 'password']
HEADERS = ['title', 'url', 'username', 'password', 'group', 'notes']

extra_keys = set([])

def main(args):
    results = []
    with open('export.json') as json_file:
        data = json.load(json_file)
        folders = data['folders']
        items = data['items']

        for item in items:
            results.append(processItem(item, folders))

    if (len(results) == 0):
        print('No rows to write (empty input file?)')
        return

    print('%d rows processed' % len(results))
    print('Writing to %s' % args.output_file.name)
    if (len(extra_keys) > 0):
        print('Found extra keys: ' + ', '.join(extra_keys))

    writer = csv.DictWriter(args.output_file, HEADERS)
    writer.writeheader()
    writer.writerows(results)


def processItem(item, folders):
    print('Reading item: ' + item['title'])
    result = {
        'title': item['title'],
        'notes': item['subtitle'] + '\n\n\n'
    }

    if item.get('folders'):
        for folder in folders:
            if folder['uuid'] == item['folders'][0]:
                result['group'] = folder['title']
                break

    for field in item.get('fields', []):
        if field['label'] in result or field['label'].lower() not in ALLOWED_FIELDS:
            result['notes'] += "%s\n%s\n\n" % (field['label'], field['value'])
            extra_keys.add(field['label'])
        else:
            result[field['label'].lower()] = field['value']

    result['notes'] += "NOTES\n\n" + item['note']

    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('input_file', type=argparse.FileType('r'),
                        help='Path to Enpass csv export file')
    parser.add_argument('output_file', type=argparse.FileType('w'),
                        help='Path to output file (csv)')
    main(parser.parse_args())
