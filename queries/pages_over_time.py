#sample query: return count of articles that mention Disraeli

def mapper(issue):
    return {issue.date.year: [1, issue.page_count]}

reducer = merge_under(double_sum)
