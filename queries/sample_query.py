from newsrods.issue import Issue
from newsrods.sparkrods import get_streams

import yaml

streams = get_streams(downsample = 1024)
issues = streams.map(Issue)
articles = issues.flatMap(lambda x: x.articles)
disraelis = articles.filter(lambda x: "Disraeli" in x.words)

with open('result.yml','w') as result_file:
    result_file.write(str(articles.count()))
