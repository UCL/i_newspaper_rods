from unittest import TestCase

from ...model.corpus import Corpus

from tempfile import mkdtemp
import os

class test_corpus(TestCase):
    def setUp(self):
        self.source='/rdZone/live/rd009s/2TB-Drive-Transfer-06-07-q2016/TDA_GDA_1785-2009'
        self.corpus=Corpus(self.source)
    def test_count(self):
        assert(len(self.corpus)==75503)
    def test_get_oid(self):
        assert 'cDdKH1qVCk87-TC6tGIb1oq6HN2sGC5q7k2DMb_B' in self.corpus.oids()
    def test_save_load_corpus(self):
        td = mkdtemp()
        tf = os.path.join(td,'corpus.yml')
        self.corpus.save(tf)
        c2 = Corpus(tf,True)
        assert 'cDdKH1qVCk87-TC6tGIb1oq6HN2sGC5q7k2DMb_B' in self.corpus.oids()
