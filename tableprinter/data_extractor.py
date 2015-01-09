import types


def extract2d(obj):
    """Extract a two dimensional array of data from the object provided.

    Currently supported are:
    - two dimensional list, tuple, or set
    - one dimensional list, tuple, or set
    - dict and dictproxy types (shown as key->value pairs)

    If your data object is not supported, create and intermediary step to parse it into a structure
    that this function does support.
    """
    # setup output object
    output = []
    num_rows = 0
    num_cols = 0

    # detect list types
    if isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
        num_rows = len(obj)
        # loop through inner items
        for row in obj:
            # nested lists count as columnar data
            if isinstance(row, list) or isinstance(row, tuple) or isinstance(row, set):
                output.append(list(row))
                num_cols = max(len(row), num_cols)
            else:
                output.append([row])
                num_cols = max(1, num_cols)
        # return data and dimension
        return output, (num_rows, num_cols)

    # detect dictionary types
    elif isinstance(obj, dict) or isinstance(obj, types.DictProxyType):
        num_cols, num_rows = 2, len(obj)
        for k in obj.keys():
            output.append([k, obj[k]])
        # return data and dimension
        return output, (num_rows, num_cols)
    else:
        raise RuntimeError('Cannot tabulize object of {}'.format(type(obj)))


def get_column_widths(data2d):
    """Determine the required column widths for the two dimentional data provided.

    Content width is based of the repr() function of each data element.
    """
    column_widths = []
    for row in data2d:
        # ensure the data structure has enough columns
        if len(column_widths) < len(row):
            column_widths = column_widths + [0] * (len(row) - len(column_widths))
        # loop through all the items in the row
        for i, cell in enumerate(row):
            # determine length of cell content
            l = len(repr(cell))
            # increase column width if required
            if l > column_widths[i]:
                column_widths[i] = l
    return column_widths
