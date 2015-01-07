from pytabular import utils
from pytabular.col_adjuster import adjust_columns
from pytabular.data_extractor import extract2d, get_column_widths


class Table(object):

    def __init__(self, data=None, title=None, compact=False,
                 sort=False, sort_reverse=False, sort_key=None,
                 column_names=None):
        self.size = (None, None)
        self.has_column_names = False
        self.compact = compact
        self.set_data(data)
        self.set_title(title)
        self.set_column_names(column_names)

        if sort or sort_reverse or sort_key is not None:
            self.sort_data(key=sort_key, reverse=sort_reverse)

    def set_title(self, title):
        self.title = title

    def set_data(self, data):
        self.data, self.size = extract2d(data)

    def set_column_names(self, column_names):
        if column_names is not None:
            self.column_names = column_names
            self.has_column_names = True
        else:
            self.has_column_names = False

    def set_column_name(self, column_index, column_name):
        raise NotImplemented()

    def set_compact(self, b):
        self.compact = b

    def sort_data(self, key=None, reverse=False):
        if self.data is None:
            raise RuntimeError('No data to sort.')
        else:
            self.data.sort(key=key, reverse=reverse)

    def __str__(self):
        lines = []
        max_table_width = utils.get_terminal_width()

        if self.has_column_names:
            column_widths = get_column_widths(self.data + [self.column_names])
        else:
            column_widths = get_column_widths(self.data)

        ttw = sum(column_widths) + 4 + 3 * (len(column_widths) - 1)
        if ttw > max_table_width:
            column_widths = adjust_columns(column_widths, max_table_width)
        elif self.title is not None and len(self.title) > (ttw - 4):
            column_widths = adjust_columns(column_widths, min(len(self.title) + 4, max_table_width))

        if self.title is not None:
            l = sum(column_widths) + (len(column_widths) - 1) * 3
            lines.append('+=' + '=' * l + '=+')
            lines.append("| {} |".format(utils.pad_ellipse(self.title, l, align='^')))

        table_hborder = '+' + '+'.join(['=' * (w+2) for w in column_widths]) + '+'
        row_hborder = '+' + '+'.join(['-' * (w+2) for w in column_widths]) + '+'

        lines.append(table_hborder)

        if self.has_column_names:
            c = []
            for i, width in enumerate(column_widths):
                if i >= len(self.column_names):
                    c.append(' ' * width)
                else:
                    c.append(utils.pad_ellipse(self.column_names[i], width))
            lines.append('| ' + ' : '.join(c) + ' |')
            lines.append(table_hborder)

        for i, row in enumerate(self.data):
            if i > 0 and not self.compact:
                lines.append(row_hborder)
            c = []
            for i, width in enumerate(column_widths):
                if i >= len(row):
                    c.append(' ' * width)
                else:
                    c.append(utils.pad_ellipse(repr(row[i]), width))
            lines.append('| ' + ' : '.join(c) + ' |')

        lines.append(table_hborder)

        return '\n'.join(lines)
