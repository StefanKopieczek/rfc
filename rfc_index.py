try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

from xml.etree import ElementTree


class Index(object):
    URL = 'http://www.rfc-editor.org/in-notes/rfc-index.xml'
    NAMESPACE = '{http://www.rfc-editor.org/rfc-index}'
    RFC_TAG_NAME = NAMESPACE + 'rfc-entry'

    def __init__(self):
        self.rfcs = []

    def load(self):
        index_data = urlopen(Index.URL)
        index_tree = ElementTree.parse(index_data)
        root = index_tree.getroot()
        rfc_elements = root.findall(Index.RFC_TAG_NAME)
        self.rfcs = [Entry(element) for element in rfc_elements]

    def __str__(self):
        return '\n'.join(str(rfc) for rfc in self.rfcs)


class Entry(object):
    AUTHOR_TAG_NAME = Index.NAMESPACE + 'author'
    DOC_ID_TAG_NAME = Index.NAMESPACE + 'doc-id'
    AUTHOR_NAME_TAG_NAME = Index.NAMESPACE + 'name'
    SUMMARY_TAG_NAME = Index.NAMESPACE + 'title'

    def __init__(self, xml):
        self.author = xml.find(
            Entry.AUTHOR_TAG_NAME).find(
            Entry.AUTHOR_NAME_TAG_NAME).text
        self.doc_id = int(xml.find(Entry.DOC_ID_TAG_NAME).text[3:])
        self.summary = xml.find(Entry.SUMMARY_TAG_NAME).text

    def __str__(self):
        return 'RFC{0} - {1}, by {2}'.format(
            self.doc_id, self.summary, self.author)


if __name__ == "__main__":
    index = Index()
    index.load()
    print(str(index))
