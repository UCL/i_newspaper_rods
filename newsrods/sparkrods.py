'''
Module to load and read the files using spark
'''

from itertools import cycle
from newsrods.issue import Issue
from requests import get

DATA_STORE_URL = "utilities.rd.ucl.ac.uk"
WOS_IP_BASE = '10.10.200.'
WOS_IP_RANGE = range(70, 82)


def get_streams(context, source="oids.txt"):
    '''
    Turn a list of oids in a file into a RDD of Issues
    '''
    oids = [oid.strip() for oid in list(open(source))]
    wos_ips = [WOS_IP_BASE + str(ip) for ip in WOS_IP_RANGE]
    url_parts = zip(cycle(wos_ips), oids)

    rddoids = context.parallelize(url_parts)
    issues = rddoids.map(lambda (ip, oid): 'http://' + ip +
                         '/objects/' + oid) \
                    .map(lambda url: get(url, stream=True)) \
                    .map(lambda stream: Issue(stream.raw))
    return issues
