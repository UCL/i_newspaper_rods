import glob
import os
import traceback
import requests
import subprocess
import logging
from StringIO import StringIO

from issue import Issue
from functools import reduce

from ..harness.mapreduce import MapReduce
from ..harness.utils import merge
from ..harness.decomposer import Decomposer

import logging
import yaml

class Corpus(object):
    def __init__(self, path, preloaded=False):
        self.path = path
        self.store = None
        self.logger = logging.getLogger('performance')
        if preloaded:
            with open(path) as fdata:
                self.store = yaml.load(fdata)
            self.logger.debug("Loaded "+str(len(self.store))+" object IDs from file "+path)

    def save(self, path):
        if not self.store:
            self.get_all_object_IDs_and_store()
        with open(path, 'w') as fdata:
            yaml.dump(self.store, fdata)

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

    def get_all_object_IDs_and_store(self):
        if self.store:
            return
        args = ["iquest","--no-page",'"%s"',
                '"SELECT DATA_PATH where COLL_NAME like '+
                "'"+self.path+"%' "+
                "and DATA_NAME like '%-%.xml' and DATA_RESC_HIER = 'wos;wosArchive'"+
                '"']
        results=subprocess.Popen(args, stdout=subprocess.PIPE)
        res = results.communicate()[0].split('\n')[:-1]
        self.store=map(lambda x:x[1:-1], res) # Remove initial and final quote

    def count(self):
        if not self.store:
            self.get_all_object_IDs_and_store()

        return len(self.store)

    def oid(self, index):
        if not self.store:
            self.get_all_object_IDs_and_store()
        return self.store[index]

    def oids(self):
        if not self.store:
            self.get_all_object_IDs_and_store()
        return self.store

    def __getitem__(self, index):
        return Issue(self.oid(index))

    def __len__(self):
        return self.count()
