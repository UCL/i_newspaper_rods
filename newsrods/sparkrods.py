'''
Module to load and read the files using spark
'''

import pyspark
import requests


def get_streams(downsample=1, source="oids.txt", app="iRodsSpark"):
    '''
    Turn a list of oids in a file into a RDD of files
    '''

    context = pyspark.SparkContext(appName=app)

    oids = map(lambda x: x.strip(), list(open(source)))

    rddoids = context.parallelize(oids)
    down = rddoids.sample(False, 1.0 / downsample)

    streams = down.map(lambda x:
                       requests.get('http://arthur.rd.ucl.ac.uk/objects/'+x,
                                    stream=True).raw)
    return streams
