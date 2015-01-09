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

    def _balance_columns(self, ignore_terminal_width=False):
        terminal_width = utils.get_terminal_width() - 1

        column_widths = get_column_widths(self.data)

        if self.column_names is not None:
            for i, w in enumerate(column_widths):
                if i < len(self.column_names):
                    column_widths[i] = max(len(self.column_names[i]), w)

        inner_margins = (len(column_widths) - 1) * 3
        outer_margins = 2 * 2
        total_margins = inner_margins + outer_margins

        current_table_width = sum(column_widths) + total_margins

        if self.title is not None:
            current_table_width = max(len(self.title) + outer_margins, current_table_width)

        if not ignore_terminal_width:
            current_table_width = min(current_table_width, terminal_width)

        return adjust_columns(column_widths, current_table_width - total_margins)

    def lines(self):
        """
        Generate the 2d Table representation as a list of lines.
        """
        column_widths = self._balance_columns()

        if self.title is not None:
            l = sum(column_widths) + (len(column_widths) - 1) * 3
            yield '+=' + '=' * l + '=+'
            yield "| \033[1m{}\033[22m |".format(utils.pad_ellipse(self.title, l, align='^'))

        table_hborder = '+' + '+'.join(['=' * (w+2) for w in column_widths]) + '+'
        row_hborder = '+' + '+'.join(['-' * (w+2) for w in column_widths]) + '+'

        yield table_hborder

        if self.column_names is not None:
            c = []
            for i, width in enumerate(column_widths):
                if i >= len(self.column_names):
                    c.append(' ' * width)
                else:
                    c.append(utils.pad_ellipse(self.column_names[i], width))
            yield '| ' + ' | '.join(c) + ' |'
            yield table_hborder

        for i, row in enumerate(self.data):
            if i > 0 and not self.compact:
                yield row_hborder
            c = []
            for i, width in enumerate(column_widths):
                if i >= len(row):
                    c.append(' ' * width)
                else:
                    c.append(utils.pad_ellipse(repr(row[i]), width))
            yield '| ' + ' : '.join(c) + ' |'

        yield table_hborder


    def __str__(self):
        return '\n'.join(self.lines())
