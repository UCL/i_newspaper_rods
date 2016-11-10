from unittest import TestCase
import os

from ..issue import Issue

class test_page(TestCase):
    def setUp(self):
        with open(os.path.join(os.path.dirname(__file__),
                  'fixtures','2000_04_24.xml')) as fixture:
            issue = Issue(fixture)
        self.article = issue.articles[0]
    def test_words_in_article(self):
        assert len(self.article.words) == 18
