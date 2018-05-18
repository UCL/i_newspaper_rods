"""
A module to query files to find every word used in the TDA and its frequency
"""

from operator import add


def do_query(issues, _in, _log):
    """
    Count each word that occurs in the archive
    """
    # Break out each article from each issue
    articles = issues.flatMap(lambda issue: [article for
                                             article in issue.articles])
    # Break out each word from each article
    words = articles.flatMap(lambda article: [(str(word), 1) for
                                              word in article.words])

    # Now add sum the word counts
    word_counts = words.reduceByKey(add).collect()
    return word_counts
