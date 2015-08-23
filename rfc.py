import argparse
import pydoc

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

import rfc_cache


def get_rfc(rfc_number, use_cache=True):
    rfc = None

    if use_cache:
        rfc = rfc_cache.get_from_cache(rfc_number)

    if rfc is None:
        url = "http://www.ietf.org/rfc/rfc{0}.txt".format(rfc_number)
        f = urlopen(url)
        rfc = f.read()
        if isinstance(rfc, bytes):
            rfc = rfc.decode('utf-8')

    return rfc


def render_rfc(rfc):
    pydoc.pager(rfc)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Download and browse RFCs, or save to read later')
    parser.add_argument('-d', '--download', action='store_true',
                        help='Save the RFC to read later')
    parser.add_argument('rfc', type=int)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.download:
        rfc_cache.add_to_cache(args.rfc, get_rfc(args.rfc, use_cache=False))
    else:
        render_rfc(get_rfc(args.rfc))
