from unittest import TestCase
from lxml import etree

from ...model.article import Article
from ...model.issue import Issue

class test_page(TestCase):
    def setUp(self):
        issue=Issue('cDdKH1qVCk87-TC6tGIb1oq6HN2sGC5q7k2DMb_B')
        issue.load()
        self.article=issue[0]
    def test_content(self):
        assert("LOVE THE AVENGER" in self.article.content)
