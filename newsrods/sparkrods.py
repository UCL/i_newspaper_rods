"""
Module to load and read the files using spark
"""

from fs.sshfs import SSHFS

from newsrods.issue import Issue

DATA_STORE_HOST = 'live.rd.ucl.ac.uk'


def get_streams(context, username, source='oids.txt'):
    """
    Turn a list of oids in a file into a RDD of Issues
    """
    filenames = [oid.strip() for oid in list(open(source))]

    fs = SSHFS(host=DATA_STORE_HOST, user=username)

    rddoids = context.parallelize(filenames)
    issues = rddoids.map(lambda filename: fs.open(filename)) \
                    .map(lambda stream: Issue(stream))
    return issues
