from ..model.corpus import Corpus
from mpi4py import MPI
import imp
import sys
from datetime import datetime
from argparse import ArgumentParser
import logging
import yaml
from utils import *

from mapreduce import MapReduce

shuffler=None
reporter=None

def main():
    args = clparser(sys.argv[1:])

    perfLogger=logging.getLogger('performance')
    communicator=MPI.COMM_WORLD
    perfLogger.setLevel(getattr(logging,args.loglevel.upper()))
    stdout=logging.StreamHandler()
    stdout.setFormatter(logging.Formatter(str(communicator.rank)+'/'+str(communicator.size)+
        ' %(levelname)s: %(asctime)s %(message)s'))
    perfLogger.addHandler(stdout)

    if args.storeids:
        corpus = Corpus(args.corpus_path)
        corpus.get_all_object_IDs_and_store()
        corpus.save(args.storeids)
        return

    execfile(args.query_path, globals()) # must define 'mapper' and 'reducer'
                                         # may define shuffler and reporter
    result = query(mapper, reducer, args.corpus_path,
                   args.downsample, args.fromfile,
                   shuffler=shuffler, reporter=reporter)

    if result:
        if args.outpath:
            outpath=args.outpath+'_'+str(MPI.COMM_WORLD.rank)+'.yml'
            with open(outpath,'w') as result_file:
                result_file.write(yaml.safe_dump(result))
                perfLogger.info("Written result")
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

def query(mapper, reducer, corpus_path, downsample=1, fromfile=False,
          shuffler=None, reporter=None):
    communicator=MPI.COMM_WORLD
    perfLogger=logging.getLogger('performance')
    corpus=Corpus(corpus_path,fromfile)
    perfLogger.info("Constructed")
    harness = MapReduce(corpus.loadingMap(mapper), reducer,
                communicator, downsample, shuffler=shuffler)
    result = harness.execute(corpus)

    perfLogger.info("Finished analysis")
    if (not shuffler) and communicator.rank !=0:
        result=None
    if reporter and result:
           result=reporter(result)
           perfLogger.info("Finished postprocessing")
    return result

if __name__ == "__main__":
    main()
