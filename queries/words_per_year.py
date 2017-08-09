'''
A module to query files for counts of interesting words. This returns
the number of occurances of each of the target words for each year.
'''

from operator import add
import re


def do_query(issues, interesting_words_file):
    '''
    Get the count of specific words of interest by year
    '''
    interesting_words = [re.compile(r'\b' + word.strip() + r'\b', re.I | re.U)
                         for word in list(open(interesting_words_file))]
    # Map each article in each issue to a year of publication
    articles = issues.flatMap(lambda issue: [(issue.date.year, article) for
                                             article in issue.articles])
    # Add 1 record for each word that appears in each article in each year
    interest = articles.flatMap(lambda (year, article):
                                [((year, regex.pattern),
                                  len(regex.findall(article.words_string)))
                                 for regex in interesting_words])
    # Now add sum the year-word counts, and change the format for output
    interesting_by_year = interest \
        .reduceByKey(add) \
        .map(lambda (year_word, count): (year_word[0],
                                         (year_word[1].replace(r'\b', ''),
                                          count))) \
        .groupByKey() \
        .map(lambda (year, data): (year, list(data))) \
        .collect()
    return interesting_by_year
