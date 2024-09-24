import os

BOLD = '\033[1m'
RESET = '\033[0m'
ITALIC = '\033[3m'

CACHE_PATH = os.getenv('OUTPUT_PATH', os.path.expanduser('/var/tmp/rir'))

sources = [
    {
        'name': 'afrinic',
        'url': 'http://ftp.afrinic.net/dbase/afrinic.db.gz',
        'db_file': 'afrinic.db.gz'
    },
    {
        'name': 'apnic',
        'url': 'http://ftp.apnic.net/pub/apnic/whois/apnic.db.inetnum.gz',
        'db_file': 'apnic.db.inetnum.gz'
    },
    {
        'name': 'lacnic',
        'url': 'https://raw.githubusercontent.com/trustedsec/hardcidr/master/lacnicdb.txt',
        'db_file': 'lacnic.db.txt'
    },
    {
        'name': 'ripe',
        'url': 'http://ftp.ripe.net/ripe/dbase/ripe.db.gz',
        'db_file': 'ripe.gz'
    }
]
