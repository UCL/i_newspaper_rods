'''
This module finds which words are contained together in articles.
'''

from operator import concat
import re


def concat_snd(a, b):  # pylint: disable=C0103
    '''
    Concatenate two lists in the second place of a tuple
    '''
    return (a[0], a[1] + b[1])


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
                                              issue.tree.getpath(article.tree),
                                              article) for
                                             article in
                                             issue.articles])
    # Add word that appears in each article
    interest = articles.flatMap(lambda (date, xpath, article):
                                [((date, xpath),
                                  [regex.pattern.replace(r'\b', '').lower()])
                                 for regex in interesting_words if
                                 regex.findall(article.words_string)])
    # Concatenate the words for each article
    words_grouped = interest.reduceByKey(concat)

    # sort the words, then find all the xpaths that match that word list
    xpaths_grouped = words_grouped \
        .map(lambda (date_path, patterns): (date_path, sorted(patterns))) \
        .map(lambda (date_path, patterns):
             ((date_path[0], str(patterns)),
              (patterns, [date_path[1]]))) \
        .reduceByKey(concat_snd) \
        .map(lambda (date_pat, pat_paths):
             (date_pat[0], (pat_paths[0], pat_paths[1]))) \
        .collect()
    return xpaths_grouped
