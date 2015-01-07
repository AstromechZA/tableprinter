from pytabular.col_adjuster import adjust_columns, downscale

def test_demo():
    assert adjust_columns([10,10,5], 22) == 13