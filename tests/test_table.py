import pytest
from mock import patch
from tableprinter.table import Table

def test_construct():
    t = Table([['hello', 'world']])

def test_construct_with_sort():
    t = Table([['hello', 'world'], ['aaa', 'bbb']], sort=True)
    assert t.data == [['aaa', 'bbb'], ['hello', 'world']]

def test_construct_with_column_names():
    t = Table([['hello', 'world']], column_names=['One', 'Two'])
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

def test__balance_columns_normal():
    t = Table([['hello', 8], ['this is a thing', 10]])
    assert t._balance_columns(False) == [17, 2]

def test__balance_columns_with_colnames():
    t = Table([['hello', 8], ['this is a thing', 10]], column_names=['words', 'numbers'])
    assert t._balance_columns(False) == [17, 7]

def test__balance_columns_with_title():
    t = Table([['hello', 8], ['this is a thing', 10]], title='A fairly long title. Longer than content.')
    assert t._balance_columns(False) == [34, 4]

def test__balance_columns_with_multiline_title():
    t = Table([['hello', 8], ['this is a thing', 10]], title=['A fairly' , 'long title. Longer than content.'])
    assert t._balance_columns(False) == [25, 4]

def test__title_lines():
    t = Table([[]], title='Some title')
    assert list(t._title_lines(20, False)) == [
        '+==================+',
        '|    Some title    |',
    ]

def test__title_lines_bold():
    t = Table([[]], title='Some title')
    assert list(t._title_lines(20, True)) == [
        '+==================+',
        '| \033[1m   Some title   \033[22m |',
    ]

def test__title_lines_multi():
    t = Table([[]], title=['Some title', 'sub-title'])
    assert list(t._title_lines(20, False)) == [
        '+==================+',
        '|    Some title    |',
        '|    sub-title     |'
    ]

def test__column_name_lines():
    t = Table([[]], column_names=['Column 1', 'Column 2', 'Column 3'])

    assert list(t._column_name_lines([10, 8, 7, 5])) == [
        '| Column 1   | Column 2 | Colum.. |       |'
    ]

def test__cell_row_lines():
    t = Table([[]])

    assert list(t._cell_row_lines([10, 5, 5], ['thing', 'thing'])) == [
        "| 'thing'    : 'th.. :       |"
    ]

def test_lines():
    t = Table([[1,2]])

    assert list(t.lines()) == [
        '+===+===+',
        '| 1 : 2 |',
        '+===+===+',
    ]

def test_lines_2():
    t = Table([[1,2], [3]])

    assert list(t.lines()) == [
        '+===+===+',
        '| 1 : 2 |',
        '+---+---+',
        '| 3 :   |',
        '+===+===+',
    ]

def test_lines_with_colnames():
    t = Table([[1,2]], column_names=['Number'])
    assert list(t.lines()) == [
        '+========+===+',
        '| Number |   |',
        '+========+===+',
        '| 1      : 2 |',
        '+========+===+'
    ]

def test_lines_with_title():
    t = Table([[1,2]], title='Numbers')
    assert list(t.lines()) == [
        '+=========+',
        '| \x1b[1mNumbers\x1b[22m |',
        '+====+====+',
        '| 1  : 2  |',
        '+====+====+'
    ]

def test___str__():
    t = Table([[1,2]])
    assert str(t) == '+===+===+\n| 1 : 2 |\n+===+===+'
