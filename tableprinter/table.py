from tableprinter import utils
from tableprinter.col_adjuster import adjust_columns
from tableprinter.data_extractor import extract2d, get_column_widths


class Table(object):

    def __init__(self, data=None, title=None, compact=False,
                 sort=False, sort_reverse=False, sort_key=None,
                 column_names=None):
        self.shape = (None, None)
        self.column_names = None
        self.compact = compact
        self.set_data(data)
        self.set_title(title)
        self.set_column_names(column_names)

        # apply the sort function on the data if data was provided
        if self.data is not None and (sort or sort_reverse or sort_key is not None):
            self.sort_data(key=sort_key, reverse=sort_reverse)

    def set_title(self, title):
        """Set the title displayed above the Table.

        Set it to None in order to remove the title.
        """
        self.title = title

    def set_data(self, data):
        """Set the data displayed by the table"""
        self.data, self.shape = extract2d(data)

    def set_column_names(self, column_names):
        """Set an array of column names for the Table, or remove column names by providing None.

        Columns will be added in order to match the number of column names provided.
        """
        self.column_names = column_names

    def set_compact(self, b):
        """Set the compact flag on the Table.

        If compact is True, borders will not be drawn between rows.
        """
        self.compact = b

    def sort_data(self, key=None, reverse=False):
        """Apply a sort to the data contained by the table.

        :param key: a function to apply to each row before rows are sorted
        :param reverse: reverse the order
        """
        if self.data is None:
            raise RuntimeError('No data to sort.')
        else:
            self.data.sort(key=key, reverse=reverse)

    def __repr__(self):
        """Returns a simple representation of the Table object.

        String contains Table title, shape, column names, sort. Other fields are ignored since
        they are too long.
        """
        return "%s(title=%r, shape=%r, column_names=%r)" % (
            self.__class__.__name__,
            self.title,
            self.shape,
            self.column_names)

    def __str__(self):
        """Return the 2d Table representation.

        Use this for printing the table. (eg: print Table())
        """
        lines = []
        max_table_width = utils.get_terminal_width()

        if self.column_names is not None:
            column_widths = get_column_widths(self.data + [self.column_names])
        else:
            column_widths = get_column_widths(self.data)

        current_table_width = sum(column_widths) + 4 + 3 * (len(column_widths) - 1)
        if current_table_width > max_table_width:
            column_widths = adjust_columns(column_widths, max_table_width)
        elif self.title is not None and len(self.title) > (current_table_width - 4):
            column_widths = adjust_columns(column_widths, min(len(self.title) + 4, max_table_width))

        if self.title is not None:
            l = sum(column_widths) + (len(column_widths) - 1) * 3
            lines.append('+=' + '=' * l + '=+')
            lines.append("| {} |".format(utils.pad_ellipse(self.title, l, align='^')))

        table_hborder = '+' + '+'.join(['=' * (w+2) for w in column_widths]) + '+'
        row_hborder = '+' + '+'.join(['-' * (w+2) for w in column_widths]) + '+'

        lines.append(table_hborder)

        if self.column_names is not None:
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
