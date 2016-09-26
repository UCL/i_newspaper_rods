#sample query: return count of articles per year

def mapper(issue):
    return {issue.date.year: [1, len(issue.articles)]}

reducer = merge_under(double_sum)
