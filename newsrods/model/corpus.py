import glob
import os
import traceback

from issue import Issue
from functools import reduce

from dataset import DataSet

from ..harness.mapreduce import MapReduce
from ..harness.utils import merge
from ..harness.decomposer import Decomposer

import logging

class Corpus(DataSet):
    def __init__(self, path=None, communicator=None):
        if type(path)==str:
            path+='/*.zip'
        super(Corpus, self).__init__(Archive,path,communicator )

    def analyse(self, mapper, reducer, subsample=1, shuffler=None):
        harness = MapReduce(self.loadingMap(mapper), reducer, self.communicator, subsample, shuffler=shuffler)
        return harness.execute(self)

    def loadingMap(self, mapper):
        def _map(issue):
            self.logger.debug("Loading issue")
            try:
                issue.load()
            except Exception as exception:
                self.logger.warn("Problem loading " + issue.code + " in " + issue.path)
                self.logger.warn(traceback.format_exc())
                self.logger.warn(str(exception))
            self.logger.debug("Loaded issue")
            try:
                self.logger.debug("Considering issue")
                result= mapper(issue)
                self.logger.debug("Considered issue")
                return result
            except Exception as exception:
                self.logger.warn("Problem parsing " + issue.code + " in " + issue.path)
                self.logger.warn(traceback.format_exc())
                self.logger.warn(str(exception))
        return _map
