# enpass-to-keepass
Convert an Enpass csv export so it can be imported to a KeePass database using KeePassXC

## Enpass Version
This version of the script converts an Enpass JSON export (Enpass version >=6). Since Enpass now uses folders as "labels" and can have multiple, the first item in the folder list is chosen as the Keepass "group".

**If you need to convert an older (Enpass < v6) CSV export, use the [`v1.0`](https://github.com/jsphpl/enpass-to-keepass/releases/tag/v1.0) tag of this git repository.**

## Background
Read this blog article for some background on this tool: [https://jsph.pl/migrating-from-enpass-to-keepass/](https://jsph.pl/migrating-from-enpass-to-keepass/)

## Usage
```
$ ./enpass-to-keepass.py --help
usage: enpass-to-keepass.py [-h] input_file output_file

Convert an Enpass export file so it can be imported to a KeePass database using KeePassXC

Documentation & Issues: https://github.com/jsphpl/enpass-to-keepass

License: Public Domain
Author: Joseph Paul <joseph@sehrgute.software>

positional arguments:
  input_file   Path to Enpass JSON export file
  output_file  Path to output file (CSV)

optional arguments:
  -h, --help   show this help message and exit
```

## License
Public Domain
