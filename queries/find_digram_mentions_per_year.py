def mapper(issue):
    shesays_matches = 0
    hesays_matches = 0
    theysay_matches = 0
    for article in issue.articles:
        cword = None
        for word in article.words:
            lword = word.lower().replace('.','').replace(':','').replace(',','').replace(';','')
            if lword == "says":
                if cword == "she":
                    shesays_matches += 1
                elif cword == "he":
                    hesays_matches += 1
            if lword == "say":
                if cword == "they":
                    theysay_matches += 1
            cword = word
    return {issue.date.year: [shesays_matches, hesays_matches, theysay_matches]}

reducer = merge_under(triple_sum)
