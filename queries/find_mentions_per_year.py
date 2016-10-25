def mapper(issue):
    prof_matches = 0
    professor_matches = 0
    for article in issue.articles:
        for word in article.words:
            lword = word.lower()
            if lword == "prof" or lword == "prof.":
                prof_matches += 1
            elif lword == "professor":
                professor_matches += 1
    return {issue.date.year: [prof_matches, professor_matches]}

reducer = merge_under(double_sum)
