import pytest
from pytabular.data_extractor import extract2d, get_column_widths

def test_data_extractor():

    # check 1 dimensional list types
    for dt in [list, tuple, set]:
        assert extract2d(dt([1,2,3,4])) == ([[1],[2],[3],[4]], (4, 1))

    # check 2 dimension list types
    for dt in [list, tuple]:
        for dt2 in [list, tuple, set]:
            assert extract2d(dt([dt2([1,2]),dt2([3,4])])) == ([[1,2],[3,4]], (2,2))

    # check dictionary types
    r, s = extract2d({
        'john': 'charles',
        1: 'bob',
        'hello': 'world'
    })

    assert sorted(r) == sorted([['john', 'charles'],[1, 'bob'],['hello', 'world']])
    assert s == (3, 2)

def test_data_extractor_bad_type():
    with pytest.raises(RuntimeError):
        extract2d(1337)

def test_get_column_widths():
    assert get_column_widths([[1,2]]) == [1, 1]

    assert get_column_widths([
        ['hello',2],
        ['something']
    ]) == [11, 1]