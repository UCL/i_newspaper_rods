#sample query: return count of articles that mention Disraeli

def q(issues):
    articles = issues.flatMap(lambda x: x.articles)
    disraelis = articles.filter(lambda x: "Disraeli" in x.words)
    return disraelis.count()
