from lxml import etree

from article import Article

from collections import defaultdict
from datetime import datetime

import logging
import re
import requests

class Issue(object):
    def __init__(self, oid):
        self.path = 'http://arthur.rd.ucl.ac.uk/objects/' + oid
        self.logger = logging.getLogger('performance')
        self.code = oid

        self.logger.debug("Loading issue")
        result = requests.get('http://arthur.rd.ucl.ac.uk/objects/' + self.code,
                stream=True)
        self.logger.debug("Building issue DOM")
        # Try hard to parse the file, even if it looks like this:
        # <wd pos="1664,5777,2052,5799">Bart,OwnerndPetitioner.Take/wd>
        parser = etree.XMLParser(recover=True)
        try:
            self.tree = etree.parse(result.raw, parser)
        except etree.XMLSyntaxError as e:
            self.logger.error("Error when parsing %s: %s", self.code, e.msg)
            self.tree = None
            return
        # DTD says there's only one issue element
        # Note there are two different DTDs:
        # GALENP: /GALENP/*/issue/page/article/text/*/p/wd
        # LTO: /issue/article/text/*/p/wd
        try:
            self.issue = self.tree.xpath('.//issue')[0]
        except IndexError:
            self.issue = self.tree.xpath('/issue')[0]
        self.articles = [Article(article)
                         for article in self.issue.xpath('.//article')]
        raw_date = self.single_query('//pf/text()')
        self.date = datetime.strptime(raw_date,"%Y%m%d")
        self.page_count = int(self.single_query('//ip/text()'))
        self.day_of_week = self.single_query('//dw/text()')
        return #for now

    def query(self, query):
        if not self.tree:
            return []
        try:
            return self.tree.xpath(query)
        except AssertionError:
            return []

    def single_query(self, query):
        result=self.query(query)
        if not result:
            return None
        try:
            return str(result[0])
        except UnicodeEncodeError:
            return unicode(result[0])

    def __getitem__(self, index):
        return self.article(index)

    def __iter__(self):
        # Somehow iterate through all the articles
        pass

    def images(self):
        # Somehow iterate through all the pictures' metadata
        # (Size, caption...)
        for page, image in self.scan_images():
            yield image
