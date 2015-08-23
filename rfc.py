import pydoc
import sys

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


def get_rfc(rfc):
    url = "http://www.ietf.org/rfc/rfc{0}.txt".format(rfc)
    f = urlopen(url)
    data = f.read()
    if isinstance(data, bytes):
        data = data.decode('utf-8')

    return data


def render_rfc(rfc):
    pydoc.pager(get_rfc(rfc))


if __name__ == "__main__":
    render_rfc(sys.argv[1])
