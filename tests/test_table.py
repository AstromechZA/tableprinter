import pytest
from pytabular.table import Table

def test_construct():
    t = Table([['hello', 'world']])

def test_construct_with_sort():
    t = Table([['hello', 'world'], ['aaa', 'bbb']], sort=True)
    assert t.data == [['aaa', 'bbb'], ['hello', 'world']]

def test_construct_with_column_names():
    t = Table([['hello', 'world']], column_names=['One', 'Two'])
    assert t.has_column_names
    assert t.column_names == ['One', 'Two']

def test_change_compact():
    t = Table([['hello', 'world']])
    t.set_compact(True)
    assert t.compact
    t.set_compact(False)
    assert not t.compact

def test_sort_no_data():
    t = Table([['hello', 'world']])
    with pytest.raises(RuntimeError):
        t.data = None
        t.sort_data()

def test_repr():
    t = Table([['hello', 'world']], title='Test Table')
    assert repr(t) == "Table(title='Test Table', shape=(1, 2), column_names=None)"
