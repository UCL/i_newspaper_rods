
from ..fixtures import sample_query

from ...harness.query import query, clparser


# def test_query():
#     result = query(sample_query.mapper, sample_query.reducer,
#         '/rdZone/live/rd009s/2TB-Drive-Transfer-06-07-q2016/TDA_GDA_1785-2009',
#         2048)
#     assert result == 36

def test_parser_simple():
    space = clparser(['abc','def'])
    assert space.corpus_path == 'def'
    assert space.query_path == 'abc'
    assert space.downsample == 1
    assert space.search_for == None

def test_parser_downsample():
    space = clparser(['abc','def','--downsample','4'])
    assert space.corpus_path == 'def'
    assert space.query_path == 'abc'
    assert space.downsample == 4

def test_parser_search_for():
    space = clparser(['abc', 'def','--search_for','hello' ])
    assert space.corpus_path == 'def'
    assert space.query_path == 'abc'
    assert space.search_for == 'hello'
