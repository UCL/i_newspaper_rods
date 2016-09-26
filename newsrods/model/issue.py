from lxml import etree

from article import Article

from collections import defaultdict
from datetime import datetime

import logging
import re
import requests

class Issue(object):
    def __init__(self, oid):
        self.path = 'http://arthur.rd.ucl.ac.uk/objects/'+oid
        self.logger=logging.getLogger('performance')
        self.code = oid

    def load(self):
        self.logger.debug("Loading issue")
        result= requests.get('http://arthur.rd.ucl.ac.uk/objects/'+self.code,
                stream=True)
        self.logger.debug("Building issue DOM")
        self.tree = etree.parse(result.raw)
        # DTD says there's only one issue element
        # Note there are two different DTDs:
        # GALENP: /GALENP/*/issue/page/article/text/*/p/wd
        # LTO: /issue/article/text/*/p/wd
        try:
            self.issue = self.tree.xpath('.//issue')[0]
        except IndexError:
            self.issue = self.tree.xpath('/issue')[0]
        self.articles = self.issue.xpath('.//article')
        raw_date = self.single_query('//pf/text()')
        self.date = datetime.strptime(raw_date,"%Y%m%d")
        self.page_count = int(self.single_query('//ip/text()'))
        self.day_of_week = self.single_query('//dw/text()')
        # for article in self.articles:
        #     Article(article)
        return #for now
        self.title=self.single_query('//mods:title/text()')
        self.logger.debug("Sorting pages")
        self.page_codes = sorted(self.corpus.issue_codes[self.code], key=Issue.sorter)
        self.pages = len(self.page_codes)
        self.logger.debug("Sorted pages")
        self.years=Issue.parse_year(self.single_query('//mods:dateIssued/text()'))
        self.publisher=self.single_query('//mods:publisher/text()')
        self.place=self.single_query('//mods:placeTerm/text()')
        # places often have a year in:
        self.years+=Issue.parse_year(self.place)
        self.years=sorted(self.years)
        if self.years:
            self.year=self.years[0]
        else:
            self.year=None

    @staticmethod
    def parse_year(text):
        try:
            long=re.compile("(1[6-9]\d\d)")
            short=re.compile("\d\d")
            results=[]
            chunks=iter(long.split(text)[1:])
            for year, rest in zip(chunks,chunks):
                results.append(int(year))
                century=year[0:2]
                years=short.findall(rest)
                for year in years:
                    results.append(int(century+year))
            return sorted(set(results))
        except TypeError:
            return []

    @staticmethod
    def sorter(page_code):
        codes=map(int,page_code.split('_'))

    def query(self, query):
        return self.tree.xpath(query)

    def article(self):
        return Article()

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


    def words(self):
        yield "Disraeli" #Stub for testing harness
        return #Stub for testing harness
        # Somehow iterate through all the words in all the articles

    def images(self):
        # Somehow iterate through all the pictures' metadata
        # (Size, caption...)
        for page, image in self.scan_images():
            yield image
