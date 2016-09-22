from unittest import TestCase
from lxml import etree

from ...model.issue import Issue

class test_issue(TestCase):
    def setUp(self):
        self.issue=Issue('cDdKH1qVCk87-TC6tGIb1oq6HN2sGC5q7k2DMb_B')
        self.issue.load()
    def test_title(self):
        assert "Love the Avenger" in self.issue.title
    def test_place(self):
        assert "London" in self.issue.place
    def test_code(self):
        assert self.issue.code == 'cDdKH1qVCk87-TC6tGIb1oq6HN2sGC5q7k2DMb_B'
    def test_page_codes(self):
        assert '03_000002' in self.issue.page_codes
    def test_pages(self):
        assert self.issue.pages==306
    def test_content(self):
        assert ("the great Avorld of Paris" in self.issue[25].content)
    def test_year(self):
        assert self.issue.years==[1823, 1869]
    def test_yearify(self):
        fixtures={
                "[1866]": [1866],
                "1885]":[1885],
                "1847 [1846, 47]":[1846, 1847],
                "1862, [1861]":[1861, 1862],
                "1873-80":[1873, 1880],
                "[ca. 1730]":[1730],
                "1725, 26":[1725, 1726],
        }
        for case, expected in fixtures.iteritems():
            assert Book.parse_year(case) == expected
