'''
This module finds which words are contained together in articles.
'''

from operator import concat
import re


def print_datetime(datetime):
    '''
    Format a datetime. Cannot use strftime because the dates can be before 1900
    '''
    return "%02d-%02d-%04d" % (datetime.day, datetime.month, datetime.year)


def do_query(issues, interesting_words_file):
    '''
    Get the words which appear together in articles.
    '''
    # Get the list of words to search for
    interesting_words = [re.compile(r'\b' + word.strip() + r'\b', re.I | re.U)
                         for word in list(open(interesting_words_file))]
    # Map each article in each issue to a year of publication
    articles = issues.flatMap(lambda issue: [(print_datetime(issue.date),
                                              issue.date.year,
                                              idx, article) for
                                             idx, article in
                                             enumerate(issue.articles)])
    # Add word that appears in each article
    interest = articles.flatMap(lambda (date, year, idx, article):
                                [((date, year, idx), [regex.pattern]) for
                                 regex in interesting_words if
                                 regex.findall(article.words_string)])
    # Now add sum the year-word counts, and change the format for output
    interesting_by_year = interest \
        .reduceByKey(concat) \
        .map(lambda (date_idx, patterns): (date_idx[1],
                                           [[pat.replace(r'\b', '') for pat in
                                             patterns]])) \
        .reduceByKey(concat) \
        .collect()
    return interesting_by_year
