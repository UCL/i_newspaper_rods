from newsrods.model.corpus import Corpus, Issue
import imp
import sys
from datetime import datetime
from argparse import ArgumentParser
import logging
import yaml
from utils import *

def main():
    args = clparser(sys.argv[1:])

    if args.storeids:
        corpus = Corpus(args.corpus_path)
        corpus.get_all_object_IDs_and_store()
        corpus.save(args.storeids)
        return

    execfile(args.query_path, globals()) # must define a function 'q',
    # taking an rdd of Issues which need load() ing and an sc
    result = query(q, args.corpus_path,
                   args.downsample, args.fromfile)

    if result:
        if args.outpath:
            outpath=args.outpath+'.yml'
            with open(outpath,'w') as result_file:
                result_file.write(yaml.safe_dump(result))
        else:
            print result

def clparser(commandline):
    clparser=ArgumentParser(description="Analyse a corpus")
    clparser.add_argument('query_path',type=str, help='path to python file describing query')
    clparser.add_argument('corpus_path',type=str, help='path on iRods to corpus')
    clparser.add_argument('--downsample',type=int, metavar='N', default=1, help='optionally, use only every Nth zipfile')
    clparser.add_argument('--outpath', default=None, type=str, help = 'output path to yaml dump result')
    clparser.add_argument('--loglevel', default='info', type=str, help = 'log level (debug, info, warn, error)')
    clparser.add_argument('--fromfile', action='store_true', help='read OIDs from file rather than query irods' )
    clparser.add_argument('--storeids', default=None, type=str, help = 'dump OIDs to file and exit')
    args=clparser.parse_args(commandline)
    return args

def query(query, corpus_path, downsample=1, fromfile=False,
          shuffler=None, reporter=None):

    if 'sc' not in locals():
        # No pre-loaded spark context, we are running
        # via spark-submit rather than pyspark
        from pyspark import SparkContext
        sc = SparkContext(appName="NewsRods")

    log4jLogger = sc._jvm.org.apache.log4j
    perfLogger = log4jLogger.LogManager.getLogger("NewsRods")
    perfLogger.info("pyspark script logger initialized")

    corpus=Corpus(corpus_path, fromfile)
    perfLogger.info("Constructed")



    rddoids = sc.parallelize(corpus.oids())
    if downsample!=1:
        down=rddoids.sample(False, 1.0 / downsample )
    else:
        down = rddoids
    issues = down.map(Issue)
    perfLogger.info("Preparing to run query")
    result = query(issues, sc)

    perfLogger.info("Finished analysis")
    return result

if __name__ == "__main__":
    main()
