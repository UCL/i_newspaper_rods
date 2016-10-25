def mapper(issue):
    word_count = 0
    for article in issue.articles:
        word_count += len(article.words)
    return {issue.date.year: [1, word_count]}

reducer=merge_under(double_sum)
