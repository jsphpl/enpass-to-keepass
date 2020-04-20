# enpass-to-keepass
Convert an Enpass csv export so it can be imported to a KeePass database using KeePassXC

## Updates
This now imports from a JSON export from enpass, and includes folders from enpass as groups.  Since enpass now uses folders as "labels" and can have multiple, this chooses the first item in the list as the group

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
