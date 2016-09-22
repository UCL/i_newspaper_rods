#sample query: return count of articles that mention Disraeli

def mapper(article):
    if "Disraeli" in article.content:
        return 1
    else:
        return 0

def reducer(x, y):
    return x+y
