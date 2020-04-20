#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert an Enpass export file so it can be imported to a KeePass database using KeePassXC

Documentation & Issues: https://github.com/jsphpl/enpass-to-keepass

License: Public Domain
Author: Joseph Paul <joseph@sehrgute.software>
"""

import argparse
import csv
import json

ALLOWED_FIELDS = ['website', "username", 'password']
HEADERS = ["title", 'website', "username", 'password', "group", "notes"]

extra_keys = set([])


def process_item(item, folders):
    print(f"Reading item: {item['title']}")
    result = {
        "title": item["title"],
        "notes": item['subtitle'] + '\n\n\n'
    }

    if folders and item.get("folders"):
        for folder in folders:
            if folder["uuid"] == item["folders"][0]:
                result["group"] = folder["title"]
                break

    email = ""
    username = ""

    for field in item.get("fields", []):
        if field.get("label", "").lower() not in ALLOWED_FIELDS:
            if field["label"].lower() == 'e-mail':
                email = field["value"]
                continue

            result["notes"] += "%s\n%s\n\n" % (field["label"], field["value"])
            extra_keys.add(field["label"])
        else:
            result[field["label"].lower()] = field["value"]
            if field["label"].lower() == "username":
                username = field["value"]

    result["notes"] += "NOTES\n\n" + item["note"]
    if not username and email:
        result["username"] = email
    else:
        result["notes"] += "E-mail\n" + email

    return result


def convert_enpass_to_keypass(input_file, output_file):
    with input_file as json_file:
        data = json.load(json_file)

    if not data:
        print("No JSON data load from {args.input_file.name}")
        return

    folders = data.get("folders")
    items = data.get("items")

    results = [process_item(item, folders) for item in items]

    if not results:
        print("No rows to write (empty input file?)")
        return

    print(f"{len(results)} rows processed")
    print(f"Writing to {output_file.name}")
    if extra_keys:
        print(f"Found extra keys: {', '.join(extra_keys)}")

    writer = csv.DictWriter(output_file, HEADERS)
    writer.writeheader()
    writer.writerows(results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('input_file', type=argparse.FileType('r'),
                        help='Path to Enpass JSON export file')
    parser.add_argument('output_file', type=argparse.FileType('w'),
                        help='Path to output file (CSV)')
    args = parser.parse_args()
    convert_enpass_to_keypass(args.input_file, args.output_file)
