from pytabular import utils
from pytabular.col_adjuster import adjust_columns

CONSOLE_WIDTH = utils.get_terminal_width()


def _pad_ellipse(content, width):
    if len(content) > width:
        return "{}..".format(content[:width-2])
    return "%-{}s".format(width) % content


def _header_line(column_widths, hchar='-'):
    return '+' + '+'.join([hchar * (w+2) for w in column_widths]) + '+'


def _content_line(items, column_widths):
    c = []
    for i, width in enumerate(column_widths):
        if i >= len(items):
            c.append(' ' * width)
        else:
            c.append(_pad_ellipse(repr(items[i]), width))
    return '| ' + ' : '.join(c) + ' |'


def _tabulize2d_cols(data, column_widths):
    print _header_line(column_widths, hchar='=')
    for i, row in enumerate(data):
        if i > 0:
            print _header_line(column_widths)
        print _content_line(row, column_widths)
    print _header_line(column_widths, hchar='=')


def _tabulize2d(o, column_widths, title=None):
    if title is not None:
        title_len = sum(column_widths) + (len(column_widths) - 1) * 3
        title = _pad_ellipse(title, title_len)
        print _header_line(column_widths, hchar='=')
        print "| {} |".format(title)

    _tabulize2d_cols(o, column_widths)


def _gridify(data):
    if isinstance(data, list) or isinstance(data, tuple) or isinstance(data, set):
        output = []
        for row in data:
            if isinstance(row, list) or isinstance(row, tuple) or isinstance(row, set):
                output.append(row)
            else:
                output.append([row])
        return output
    elif isinstance(data, dict):
        output = []
        for k, v in data.iteritems():
            output.append([k, v])
        return output
    else:
        raise RuntimeError('Cannot tabulize object of {}'.format(type(data)))

def _get_column_widths(data):
    column_widths = []
    for row in data:
        if len(column_widths) < len(row):
            column_widths = column_widths + [0] * (len(row) - len(column_widths))
        for i, cell in enumerate(row):
            l = len(repr(cell))
            if l > column_widths[i]:
                column_widths[i] = l
    return column_widths

def tabulize(data, title=None, sort=False):
    # extract data
    data = _gridify(data)

    # sort the data
    # TODO custom sort op
    if sort:
        data = sorted(data)

    column_widths = _get_column_widths(data)
    ttw = sum(column_widths) + 4 + 3 * (len(column_widths) - 1)
    max_table_width = utils.get_terminal_width()

    if ttw > max_table_width:
        column_widths = adjust_columns(column_widths, max_table_width)
    elif title is not None and len(title) > (ttw - 4):
        column_widths = adjust_columns(column_widths, min(len(title) + 4, max_table_width))

    return _tabulize2d(_gridify(data), column_widths, title=title)
