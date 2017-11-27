'''
A module to query files word and article counts. This returns
the word count per article for each issues (number of word counts
is the number of articles)
'''

from operator import concat


def print_datetime(datetime):
    '''
    Format a datetime. Cannot use strftime because the dates can be before 1900
    '''
    return "%02d-%02d-%04d" % (datetime.day, datetime.month, datetime.year)


def do_query(issues, _):
    '''
    Get the count of words by article by issue
    '''
    # For each issue map the date, the number of articles as a key,
    # and the value is each articles length
    articles = issues.flatMap(lambda issue: [(print_datetime(issue.date),
                                              [len(article.words)])
                                             for
                                             article in issue.articles])
    # Now add sum the issue-word counts, and change the format for output
    interesting_by_year = articles \
        .reduceByKey(concat) \
        .collect()
    return interesting_by_year
