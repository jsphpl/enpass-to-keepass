# enpass-to-keepass
Convert an Enpass csv export so it can be imported to a KeePass database using KeePassXC

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
  input_file   Path to Enpass csv export file
  output_file  Path to output file (csv)

optional arguments:
  -h, --help   show this help message and exit
```

## License
Public Domain
