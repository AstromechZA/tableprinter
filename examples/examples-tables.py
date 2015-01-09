from random import randint
from collections import Counter
import tableprinter
from tableprinter.table import Table
from itertools import combinations

data = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print Table(data, title='A longer title with words.')
print ''
print Table(data, title='compact', compact=True)
print ''
print Table(data, title='reversed', sort_reverse=True)

data = [
    ['John', 'Smith', '34', '7 Example Road, Suburb'],
    ['Joe', 'Soap', '16', '123 Another Example Street, City']
]

print ''
print Table(data, title='Table A: People', column_names=['Name', 'Surname', 'Age', 'Address'])

print ''
print Table([1, 2], title='Mini', compact=True)

print ''
print Table(list(combinations([1,2,3], 2)), title='Combinations')

print ''
print Table(
    dict(Counter([randint(1,6) for i in xrange(100000)])),
    title=['Distribution of', '100000 random dice rolls'],
    sort_key=lambda r:r[1],
    sort_reverse=True,
    column_names=['Dice number', 'Occurence', 'Unknown']
)
