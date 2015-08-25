import os
import logging
import sys
from zipfile import ZipFile

try:
    import cPickle as pickle
except ImportError:
    import pickle

from .rfc_exceptions import CriticalError


def store_rfc(rfc_id, rfc_text):
    with ZipFile(get_rfc_cache(), 'a') as cache:
        cache.writestr('rfc{0}.txt'.format(rfc_id), rfc_text)
    logging.debug('Cached RFC {0} to RFC cache file'.format(rfc_id))


def load_rfc(rfc_id):
    try:
        with ZipFile(get_rfc_cache(), 'r') as cache:
            with cache.open('rfc{0}.txt'.format(rfc_id), 'r') as rfc:
                data = rfc.read()
                if isinstance(data, bytes):
                    data = data.decode('utf-8')
                return data
    except KeyError:
        return None


def store_index(index):
    with ZipFile(get_rfc_cache(), 'a') as cache:
        cache.writestr('index.xml', pickle.dumps(index))
    logging.debug('Cached index to index.xml')


def load_index():
    try:
        with ZipFile(get_rfc_cache(), 'r') as cache:
            with cache.open('index.xml', 'r') as index_file:
                return pickle.load(index_file)
    except KeyError:
        return None


def get_appdata_folder():
    if sys.platform.startswith('linux'):
        return os.getenv('HOME')
    elif sys.platform in ['win32', 'cygwin']:
        return os.getenv('APPDATA')
    elif sys.platform == 'darwin':
        return os.path.expanduser('~/Library/Application Support')
    else:
        logging.warning('Unsupported platform {0}; '
                        'RFC storage may fail'.format(sys.platform))
        return os.getenv('HOME')


def get_rfc_cache():
    appdata_folder = get_appdata_folder()
    if not os.path.exists(appdata_folder):
        raise CriticalError('Unable to find appdata folder; '
                            '{0} does not exist'.format(appdata_folder))

    rfc_cache_folder = os.path.join(appdata_folder, '.rfccache')
    if not os.path.exists(rfc_cache_folder):
        os.mkdir(rfc_cache_folder)
        logging.debug('Created rfc cache folder at {0}'.format(
            rfc_cache_folder))
    elif not os.path.isdir(rfc_cache_folder):
        raise CriticalError('Unable to create rfc cache folder {0}; '
                            'a file already exists with that name'.format(
                                rfc_cache_folder))

    rfc_cache = os.path.join(rfc_cache_folder, 'rfcs.zip')
    if not os.path.exists(rfc_cache):
        # The RFC cache zip does not exist; create an empty zip.
        zf = ZipFile(rfc_cache, 'w')
        zf.close()
        logging.debug('Created rfc cache at {0}'.format(rfc_cache))

    return rfc_cache
