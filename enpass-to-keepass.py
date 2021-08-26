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

DIRECTLY_MAPPED_FIELDS = ["url", "username", "password", "totp"]
CSV_HEADERS = ["title", "url", "username", "password", "group", "updated_at", "notes", "totp"]
FIELD_ALIASES = {
    "website": "url",
    "e-mail": "email",
    "login": "username",
    "benutzername": "username",
    "kennwort": "password",
}

extra_keys = set([])


def process_item(item, folders):
    print(f"Reading item: {item['title']}")
    result = {
        "title": item["title"],
    }

    if folders and item.get("folders"):
        for folder in folders:
            if folder["uuid"] == item["folders"][0]:
                result["group"] = folder["title"]
                break

    email = None
    username = None
    updated_at = None
    extra_fields = {}

    for field in item.get("fields", []):
        field_name = field.get("label", "").lower()
        field_alias = FIELD_ALIASES.get(field_name, field_name)

        field_updated_at = None
        try:
            field_updated_at = int(field["updated_at"])
        except (TypeError, ValueError):
            pass
        if field_updated_at is not None and \
                (updated_at is None or field_updated_at > updated_at):
            updated_at = field_updated_at

        if field_alias in DIRECTLY_MAPPED_FIELDS:
            result[field_alias] = field["value"]
            if field_alias == "username":
                username = field["value"]
        else:
            if field_alias == "email":
                email = field["value"]
                continue

            if len(str(field["value"])) > 0:
                extra_fields[field["label"]] = field["value"]

            extra_keys.add(field["label"])

    if email:
        if username:
            extra_fields["E-mail"] = email
        else:
            result["username"] = email

    if updated_at is not None:
        result["updated_at"] = updated_at

    result["notes"] = "\n".join(
        [f"{key}: {value}" for key, value in extra_fields.items()]
    )

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

    writer = csv.DictWriter(output_file, CSV_HEADERS)
    writer.writeheader()
    writer.writerows(results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "input_file",
        type=argparse.FileType("r"),
        help="Path to Enpass JSON export file",
    )
    parser.add_argument(
        "output_file", type=argparse.FileType("w"), help="Path to output file (CSV)"
    )
    args = parser.parse_args()
    convert_enpass_to_keypass(args.input_file, args.output_file)
