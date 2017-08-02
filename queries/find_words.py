'''
A module to query files for counts of interesting words
'''


def do_query(issues, interesting_words_file):
    '''
    Get the count of specific words of interest by year
    '''
    interesting_words = [word.strip() for word in
                         list(open(interesting_words_file))]
    articles = issues.flatMap(lambda x: [(x.date.year, article) for article in
                                         x.articles])
    interest = articles.flatMap(lambda x: [((x[0], y), 1) for y in
                                           interesting_words if y in
                                           x[1].words])
    interesting_by_year = interest.reduceByKey(lambda x, y: x+y).map(
        lambda x: (x[0][0], (x[0][1], x[1]))).groupByKey().map(
            lambda x: (x[0], list(x[1]))).collect()
    return interesting_by_year
