from newsrods.issue import Issue

import yaml
import pyspark

sc = pyspark.SparkContext(appName="sample_query")

oids = map(lambda x: x.strip(), list(open('oids.txt')))

rddoids = sc.parallelize(oids)
down = rddoids.sample(False, 1.0 / 1024 )

streams = down.map(lambda x:
                   requests.get('http://arthur.rd.ucl.ac.uk/objects/'+x,
                   stream=True))
                   
issues = streams.map(Issue)
articles = issues.flatMap(lambda x: x.articles)
disraelis = articles.filter(lambda x: "Disraeli" in x.words)

with open('result.yml','w') as result_file:
    result_file.write(str(articles.count()))
