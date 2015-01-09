# tableprinter - 1.0
This is a library for outputting a two-dimensional representation of a
dataset using ascii characters. 

For example:

    from tableprinter import Table
    print Table([[101, 'bob'], [(1,2), 5.412]], title='A sample table showing different data types', column_names=['Column 1', 'Column 2'])

Outputs:

    +=============================================+
    | A sample table showing different data types |
    +======================+======================+
    | Column 1             | Column 2             |
    +======================+======================+
    | 101                  : 'bob'                |
    +----------------------+----------------------+
    | (1, 2)               : 5.412                |
    +======================+======================+

## 1. General Usage
The general usage pattern is to construct a Table using the constructor, and then print it to the stdout stream. Arguments modifying the content and order of the table are given to the constructor, while arguments can be passed to the `__str__` function modify how the table is displayed.

Note: The `repr()` function is used to create the strings in the table cells, this allows the table to handle any type of object, but may have unintended consequences. Bare this in mind.

### 1.1 Constructor Arguments
- `data` This is the only required argument (since the table must contain some data). This should be either a one dimensional list, set, or tuple, which are displayed as single column tables; nested list, tuple, or set, which is displayed as a multicolumn-multirow table; or a dictionary structure which is displayed as two columns.
- `title (default None)` This should be provided as either a single string, or a list of strings. If the title is a list of strings it will be displayed on multiple lines.
- `column_names (default None)` This can be provided as a list of strings indicating column names. Columns are not added to the data in order to match the column names: extra column names are discarded, missing column names are shown as blank.
- `compact (default False)` If True, no lines are drawn between rows of the table.
- `sort (default False)` If True, the objects in the data set are sorted before being displayed.
- `sort_reverse (default False)` If True, the objects in the data set are sorted in reverse order.
- `sort_key (default None)` If a function is provided, the function is applied to objects before their sort order is determined. Ie: to sort on the second column use `lambda i: i[1]`.

### 1.2 `__str__` Arguments
Although `__str__` is usually called indirectly when you print the Table or use `str`, sometimes one might want to provide display arguments.
- `bold_title (default False)` If True, the title of the table is printed in bold output style. This should work in most terminals but is not completely universal.
- `table_width_override (default None)` Generally, the table shrinks to fit its contents, this can be overriden by providing an override value here. Note: this is still restricted by the terminal width unless `ignore_terminal_width` is True.
- `ignore_terminal_width (default False)` In normal operation the Table restricted to fit the width of the current terminal. By using this option, the table will never shrink in response to the terminal width.

### 1.3 The `.lines()` function
`lines()` is the function that does most of the work. It returns a generator which yields the lines representing the Table. The `__str__` function simply returns these lines joined with newline characters. The `lines()` function may be useful if you are printing the table into a log file which requires line-by-line printing for best results.

## 2. Examples
Table in compact mode:

    >>> print Table([[101, 'bob'], [(1,2), 5.412]], title='A sample table showing different data types', compact=True)
    +=============================================+
    | A sample table showing different data types |
    +======================+======================+
    | 101                  : 'bob'                |
    | (1, 2)               : 5.412                |
    +======================+======================+
  
Table showing a distribution of dice rolls. Arguments are used to sort the rows based on the count, and a multiline title is provided.

    >>> print Table(
        dict(Counter([randint(1,6) for i in xrange(100000)])),
        title=['Distribution of', '100000 random dice rolls'],
        sort_key=lambda r:r[1],
        sort_reverse=True,
        column_names=['Dice number', 'Occurence', 'Unknown']
    )
    +==========================+
    |     Distribution of      |
    | 100000 random dice rolls |
    +=============+============+
    | Dice number | Occurence  |
    +=============+============+
    | 5           : 16761      |
    +-------------+------------+
    | 2           : 16749      |
    +-------------+------------+
    | 1           : 16682      |
    +-------------+------------+
    | 6           : 16677      |
    +-------------+------------+
    | 4           : 16624      |
    +-------------+------------+
    | 3           : 16507      |
    +=============+============+

Example of using `table_width_override` to expand or shrink tables.

    >>> print t.__str__(table_width_override=90)
    +========================================================================================+
    |                                    Table A: People                                     |
    +===========+============+========+======================================================+
    | Name      | Surname    | Age    | Address                                              |
    +===========+============+========+======================================================+
    | 'John'    : 'Smith'    : '34'   : '7 Example Road, Suburb'                             |
    +-----------+------------+--------+------------------------------------------------------+
    | 'Joe'     : 'Soap'     : '16'   : '123 Another Example Street, City'                   |
    +===========+============+========+======================================================+
    >>> print t.__str__(table_width_override=50)
    +================================================+
    |                Table A: People                 |
    +========+=========+======+======================+
    | Name   | Surname | Age  | Address              |
    +========+=========+======+======================+
    | 'John' : 'Smith' : '34' : '7 Example Road, S.. |
    +--------+---------+------+----------------------+
    | 'Joe'  : 'Soap'  : '16' : '123 Another Examp.. |
    +========+=========+======+======================+
