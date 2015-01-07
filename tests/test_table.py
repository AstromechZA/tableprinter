import pytest
from mock import patch
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

def test_tables():
    data = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    print Table(data, title='A longer title with words.')
    print Table(data, title='compact', compact=True)
    print Table(data, title='reversed', sort_reverse=True)

    data = [
        [1, 2, 3],
        [4, 5, 6],
        [7]
    ]

    print Table(data, column_names=['c1', 'c2', 'c3'])
    print Table(data, column_names=['c1', 'c2'])

    with patch('pytabular.utils.get_terminal_width') as tw_mock:
        tw_mock.return_value = 30

        data = [
            ['some fairly long string', 'another longish string']
        ]

        print Table(data, column_names=['c1', 'c2'])
