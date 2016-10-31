from unittest import TestCase
from lxml import etree

from ...model.article import Article
from ...model.issue import Issue

class test_page(TestCase):
    def setUp(self):
        issue = Issue('qAr8caXjBSnUDlBpn1W-q4t9LC9AT4yC2lQfAFNA')
        self.article = issue.articles[0]
    def test_words_in_article(self):
        assert len(self.article.words) == 18
