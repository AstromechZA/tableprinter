
def _pad_ellipse(content, width):
    if len(content) <= width:
        return "{}{}".format(content, ' ' * (width - len(content)))
    else:
        return "{}..".format(content[:width-2])


def _header_line(column_widths, hchar='-'):
    return '+' + '+'.join([hchar * (w+2) for w in column_widths]) + '+'


def _content_line(items, column_widths):
    c = []
    for li in xrange(len(column_widths)):
        if li >= len(items):
            c.append(' ' * column_widths[li])
        else:
            c.append(_pad_ellipse(repr(items[li]), column_widths[li]))
    return '| ' + ' | '.join(c) + ' |'


def _tabulize2d_cols(o, column_widths, sort=False):
    print _header_line(column_widths, hchar='=')
    p = len(o) - 1
    if sort:
        o = sorted(o)
    for row in o:
        print _content_line(row, column_widths)
        if p > 0:
            p -= 1
            print _header_line(column_widths)
    print _header_line(column_widths, hchar='=')


def _tabulize2d(o, max_col_width, title, sort=False):
    column_widths = []
    for row in o:
        if len(column_widths) < len(row):
            column_widths = column_widths + [0] * (len(row) - len(column_widths))
        ith = 0
        for cell in row:
            l = len(repr(cell))
            if l > column_widths[ith]:
                column_widths[ith] = l
                if max_col_width is not None and l > max_col_width:
                    column_widths[ith] = max_col_width
            ith += 1

    if title is not None:
        tbl_width = sum(column_widths) + (len(column_widths) - 1) * 3

        title_len = len(title)
        if title_len < tbl_width:
            title_len = tbl_width
        else:
            if title_len > max_col_width:
                title_len = max_col_width
            column_widths[0] = column_widths[0] + (title_len - tbl_width)
        title = _pad_ellipse(title, title_len)

        print _header_line(column_widths, hchar='=')
        print "| {} |".format(title)

    _tabulize2d_cols(o, column_widths, sort)


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


def tabulize(data, max_col_width=50, title=None, sort=False):
    return _tabulize2d(_gridify(data), max_col_width=max_col_width, title=title, sort=sort)
