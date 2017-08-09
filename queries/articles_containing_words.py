'''
This module counts the number of articles that per year that contain
a given word. The input is a file containing a list of words to search for
and each words counts are given seperately.
'''

from operator import add


def do_query(issues, interesting_words_file):
    '''
    Get the count of specific words of interest by year
    '''
    # Get the list of words to search for
    interesting_words = [word.strip() for word in
                         list(open(interesting_words_file))]
    # Map each article in each issue to a year of publication
    articles = issues.flatMap(lambda issue: [(issue.date.year, article) for
                                             article in issue.articles])
    # Add 1 record for each word that appears in each article in each year
    interest = articles.flatMap(lambda (year, article):
                                [((year, word), 1) for word in
                                 interesting_words if
                                 article.words_string.contains(word)])
    # Now add sum the year-word counts, and change the format for output
    interesting_by_year = interest \
        .reduceByKey(add) \
        .map(lambda (year, word, count): (year, (word, count))) \
        .groupByKey() \
        .map(lambda (year, data): (year, list(data))) \
        .collect()
    return interesting_by_year
