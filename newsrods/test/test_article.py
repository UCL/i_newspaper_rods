"""
Tests for Article
"""

import os
from unittest import TestCase

from ..issue import Issue


class TestPage(TestCase):
    """
    Test class for Article
    """

    def setUp(self):
        """
        Load the standard test file
        """
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures', '2000_04_24.xml')) as fixture:
            issue = Issue(fixture)
        self.article = issue.articles[0]

    def test_words_in_article(self):
        """
        Check that the article length is correct
        """
        assert len(self.article.words) == 18

    def test_ocr_quality(self):
        """
        Make sure that the ocr quality is read
        """
        assert self.article.quality == 0
