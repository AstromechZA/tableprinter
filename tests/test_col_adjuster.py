from tableprinter.col_adjuster import adjust_columns, downscale, upscale

def test_downscale():
    assert downscale([30], 40) == [30]
    assert downscale([30], 22) == [22]
    assert downscale([10,10,5], 22) == [10, 10, 5]
    assert downscale([20,30,40], 50) == [12, 19, 19]

def test_upscale():
    assert upscale([40], 100) == [100]
    assert upscale([10, 10], 40) == [20, 20]
    assert upscale([10, 10], 37) == [18, 19]


def test_adjust_columns():
    # exact match
    assert adjust_columns([10, 10], 20) == [10,10]

    # require upscale
    assert adjust_columns([10, 10], 60) == [30, 30]

    # require downscale
    assert adjust_columns([80, 80], 125) == [65, 60]