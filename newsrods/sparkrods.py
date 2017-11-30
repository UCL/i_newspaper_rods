'''
Module to load and read the files using spark
'''

from newsrods.issue import Issue
from newsrods.query import do_query  # noqa # pylint: disable=all

from pyspark import SparkContext  # pylint: disable=import-error
from pyspark.sql import SparkSession
from requests import get

import yaml

DATA_STORE_URL = "utilities.rd.ucl.ac.uk"


def run(iteration):
    '''
    Link the file loading with the query
    '''
    context = SparkContext(appName="iNewspaperRods")
    session = SparkSession(context)  # noqa
    issues = get_streams(context, source="oids." + iteration + ".txt")
    results = do_query(issues, 'input.1.data')

    with open('result.' + iteration + '.yml', 'w') as result_file:
        result_file.write(yaml.safe_dump(dict(results),
                          default_flow_style=False))


def get_streams(context, source="oids.txt"):
    '''
    Turn a list of oids in a file into a RDD of Issues
    '''
    oids = [oid.strip() for oid in list(open(source))]

    rddoids = context.parallelize(oids)
    issues = rddoids.map(lambda (oid): 'http://' + DATA_STORE_URL +
                         '/objects/' + oid) \
                    .map(lambda url: get(url, stream=True)) \
                    .map(lambda stream: Issue(stream.raw))
    return issues
