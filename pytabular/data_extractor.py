import types


def extract2d(obj):
    num_rows = 0
    num_cols = 0
    output = []
    if isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
        num_rows = len(obj)
        for row in obj:
            if isinstance(row, list) or isinstance(row, tuple) or isinstance(row, set):
                output.append(row)
                num_cols = max(len(row), num_cols)
            else:
                num_cols = max(1, num_cols)
                output.append([row])
        return output, (num_rows, num_cols)
    elif isinstance(obj, dict) or isinstance(obj, types.DictProxyType):
        num_rows = len(obj)
        num_cols = 2
        for k in obj.keys():
            output.append([k, obj[k]])
        return output, (num_rows, num_cols)
    else:
        raise RuntimeError('Cannot tabulize object of {}'.format(type(obj)))


def get_column_widths(data2d):
    column_widths = []
    for row in data2d:
        if len(column_widths) < len(row):
            column_widths = column_widths + [0] * (len(row) - len(column_widths))
        for i, cell in enumerate(row):
            l = len(repr(cell))
            if l > column_widths[i]:
                column_widths[i] = l
    return column_widths
