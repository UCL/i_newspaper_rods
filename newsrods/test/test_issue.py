from unittest import TestCase
import os

from ..issue import Issue

class test_issue(TestCase):
    def setUp(self):
        with open(os.path.join(os.path.dirname(__file__),
                  'fixtures','2000_04_24.xml')) as fixture:
            self.issue = Issue(fixture)
    def test_date(self):
        assert self.issue.date.year == 2000
        assert self.issue.date.month == 4
        assert self.issue.date.day == 24
    def test_page_count(self):
        assert self.issue.page_count == 88
    def test_day_of_week(self):
        assert self.issue.day_of_week == 'Monday'
    def test_articles_per_issue(self):
        assert len(self.issue.articles) == 580
    # def test_title(self):
    #     assert "Love the Avenger" in self.issue.title
    # def test_place(self):
    #     assert "London" in self.issue.place
    # def test_code(self):
    #     assert self.issue.code == 'cDdKH1qVCk87-TC6tGIb1oq6HN2sGC5q7k2DMb_B'
    # def test_page_codes(self):
    #     assert '03_000002' in self.issue.page_codes
    # def test_pages(self):
    #     assert self.issue.pages==306
    # def test_content(self):
    #     assert ("the great Avorld of Paris" in self.issue[25].content)
    # def test_year(self):
    #     assert self.issue.years==[1823, 1869]
    # def test_yearify(self):
    #     fixtures={
    #             "[1866]": [1866],
    #             "1885]":[1885],
    #             "1847 [1846, 47]":[1846, 1847],
    #             "1862, [1861]":[1861, 1862],
    #             "1873-80":[1873, 1880],
    #             "[ca. 1730]":[1730],
    #             "1725, 26":[1725, 1726],
    #     }
    #     for case, expected in fixtures.iteritems():
    #         assert Book.parse_year(case) == expected
