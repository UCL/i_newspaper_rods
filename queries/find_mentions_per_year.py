def mapper(issue, match):
    matches = 0
    for article in issue.articles:
        for word in article.words:
            lword = word.lower().replace('.','').replace(':','').replace(',','').replace(';','')
            if lword == match:
                matches += 1
    return {issue.date.year: matches}

reducer = merge_under(sum)
