'''
Tests for Issue
'''

from unittest import TestCase
import os

from ..issue import Issue


class TestIssue(TestCase):
    '''
    Test for the Issue class
    '''

    def setUp(self):
        '''
        Load in the test file
        '''
        with open(os.path.join(os.path.dirname(__file__),
                               'fixtures', '2000_04_24.xml')) as fixture:
            self.issue = Issue(fixture)

    def test_date(self):
        '''
        Test that the date is correct
        '''
        assert self.issue.date.year == 2000
        assert self.issue.date.month == 4
        assert self.issue.date.day == 24

    def test_page_count(self):
        '''
        Test that the page count is correct
        '''
        assert self.issue.page_count == 88

    def test_day_of_week(self):
        '''
        Test that the day of the week is correct
        '''
        assert self.issue.day_of_week == 'Monday'

    def test_articles_per_issue(self):
        '''
        Test that the articles per issue is correct
        '''
        assert len(self.issue.articles) == 580
