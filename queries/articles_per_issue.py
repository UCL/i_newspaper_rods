'''
A module to query article counts. This returns
the number of articles per issue.
'''


def print_datetime(datetime):
    '''
    Format a datetime. Cannot use strftime because the dates can be before 1900
    '''
    return "%02d-%02d-%04d" % (datetime.day, datetime.month, datetime.year)


def do_query(issues, _):
    '''
    Get the count of words by articles by issue
    '''
    # For each issue map the date, the number of articles as a key,
    # and the value is each articles length
    articles = issues.flatMap(lambda issue: [(print_datetime(issue.date),
                                              len(issue.articles))]) \
        .collect()
    return articles
