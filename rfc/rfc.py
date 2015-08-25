from __future__ import print_function
import pydoc
import sys
import tabulate

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

from . import cache
from . import index
from . import output


USAGE = """
    rfc.py [view] RFC  - Display the specified RFC.
    rfc.py save   RFC  - Store the specified RFC so it can be viewed offline.
    rfc.py list        - Display all published RFCs in a table. Useful for grepping.
    rfc.py search TERM - List all RFCs with the given word or phrase in the summary text.
    rfc.py help        - Print this message.
"""


def get_rfc(rfc_number, use_cache=True):
    rfc = None

    if use_cache:
        rfc = cache.load_rfc(rfc_number)

    if rfc is None:
        url = "http://www.ietf.org/rfc/rfc{0}.txt".format(rfc_number)
        f = urlopen(url)
        rfc = f.read()
        if isinstance(rfc, bytes):
            rfc = rfc.decode('utf-8')

    return rfc


def get_rfc_index(use_cache=True):
    rfc_index = None
    if use_cache:
        rfc_index = cache.load_index()

    if rfc_index is None:
        if use_cache:
            output.say('No cached index found. '
                       'Downloading the RFC index; this may take a minute.')
        response = urlopen('http://www.rfc-editor.org/in-notes/rfc-index.xml')
        rfc_index = index.Index(response)
        cache.store_index(rfc_index)

    return rfc_index


def list_rfcs():
    pydoc.pager(tabulate.tabulate(iter(get_rfc_index()), tablefmt='plain'))


def search_rfcs(term):
    rfc_index = get_rfc_index()
    matches = (iter(rfc) for rfc in rfc_index if term.lower() in rfc.summary.lower())
    pydoc.pager(tabulate.tabulate(matches, tablefmt='plain'))


def show_rfc(rfc):
    pydoc.pager(rfc)


def main():
    output.INTERACTIVE_MODE = True

    cmd = sys.argv[1].lower()
    if cmd == 'save':
        rfc_num = int(sys.argv[2])
        output.say('Downloading RFC {0}...'.format(rfc_num))
        rfc = get_rfc(rfc_num, use_cache=False)
        output.say('Saving RFC {0}...'.format(rfc_num))
        cache.store_rfc(rfc_num, rfc)
        output.say('RFC saved.')
    elif cmd == 'list':
        list_rfcs()
    elif cmd == 'search':
        search_rfcs(sys.argv[2])
    elif cmd == 'help':
        print(USAGE)
    elif cmd == 'view':
        rfc = get_rfc(int(sys.argv[2]))
        show_rfc(rfc)
    else:
        rfc = get_rfc(int(sys.argv[1]))
        show_rfc(rfc)


if __name__ == '__main__':
    main()
