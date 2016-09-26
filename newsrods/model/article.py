from lxml import etree

class Article(object):
    def __init__(self, source):
        self.tree = source
        # DTD says only one text element per article
        # Texts can have different children: preamble, title and cr. Each of those
        # is formed by pg (position guide) and p (paragraph) elements. Paras are
        # made of words (wd).
        self.title = self.tree.xpath('text/text.title/p/wd/text()')
        self.preamble = self.tree.xpath('text/text.preamble/p/wd/text()')
        self.cr = self.tree.xpath('text/text.cr/p/wd/text()')

    @property
    def words(self):
        return self.title + self.preamble + self.cr
