from query_rods import *
from itertools import islice

def test_rod_manager():
    rod_manager= TDAIRodsManager()
    assert(len(rod_manager)) == 75503
    top = str(rod_manager[52].next())
    print top
    assert "GALENP" in top
