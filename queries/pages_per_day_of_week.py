def mapper(issue):
    return {issue.day_of_week: [1, issue.page_count]}


reducer = merge_under(double_sum)
