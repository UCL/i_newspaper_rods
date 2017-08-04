'''
Module to load and read the files using spark
'''

from newsrods.issue import Issue
from requests import get

DATA_STORE_URL = "utilities.rd.ucl.ac.uk"


def get_streams(context, downsample=1, source="oids.txt"):
    '''
    Turn a list of oids in a file into a RDD of Issues
    '''
    oids = [oid.strip() for oid in list(open(source))]

    rddoids = context.parallelize(oids)
    if downsample < 1:
        rddoids = rddoids.sample(False, 1.0 / downsample)

    issues = rddoids.map(lambda oid: 'http://' + DATA_STORE_URL +
                         '/objects/' + oid) \
                    .map(lambda url: get(url, stream=True)) \
                    .map(lambda stream: Issue(stream.raw))
    return issues
