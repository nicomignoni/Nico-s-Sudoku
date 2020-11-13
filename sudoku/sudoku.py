import numpy as np
from copy import deepcopy
from itertools import product


class Sudoku:
    def __init__(self, table):
        self.table = table
        self.table_copy = deepcopy(self.table)
        self.minors = {
            0: {'indices': (slice(0, 3), slice(0, 3)), 'coordinates': ((0, 1, 2), (0, 1, 2))},
            1: {'indices': (slice(0, 3), slice(3, 6)), 'coordinates': ((0, 1, 2), (3, 4, 5))},
            2: {'indices': (slice(0, 3), slice(6, 9)), 'coordinates': ((0, 1, 2), (6, 7, 8))},
            3: {'indices': (slice(3, 6), slice(0, 3)), 'coordinates': ((3, 4, 5), (0, 1, 2))},
            4: {'indices': (slice(3, 6), slice(3, 6)), 'coordinates': ((3, 4, 5), (3, 4, 5))},
            5: {'indices': (slice(3, 6), slice(6, 9)), 'coordinates': ((3, 4, 5), (6, 7, 8))},
            6: {'indices': (slice(6, 9), slice(0, 3)), 'coordinates': ((6, 7, 8), (0, 1, 2))},
            7: {'indices': (slice(6, 9), slice(3, 6)), 'coordinates': ((6, 7, 8), (3, 4, 5))},
            8: {'indices': (slice(6, 9), slice(6, 9)), 'coordinates': ((6, 7, 8), (6, 7, 8))},
        }
        self.sheet = self.get_sheet()

    def extract(self, point, table=False, other_table=None):
        for key in self.minors:
            if point[0] in self.minors[key]['coordinates'][0] and point[1] in self.minors[key]['coordinates'][1]:
                if table:
                    return self.table[self.minors[key]['indices']]
                elif not table and other_table is None:
                    return self.sheet[self.minors[key]['indices']]
                elif other_table is not None:
                    return other_table[self.minors[key]['indices']]

    def issudoku(self):
        if 0 in self.table:
            return False
        for i in range(9):
            if (not np.array_equal(np.sort(self.table[i, :]), list(range(1, 10))) or
                    not np.array_equal(np.sort(self.table[:, i]).transpose(), list(range(1, 10))) or
                    not np.array_equal(np.sort(self.table[self.minors[i]['indices']], axis=None).flat, list(range(1, 10)))):
                return False
        return True

    def get_sheet(self):
        s = np.full((9, 9), set())
        zeros = tuple(zip(*np.where(self.table == 0)))
        for index in zeros:
            element_on_row = set(self.table[index[0], :])
            element_on_col = set(self.table[:, index[1]])
            element_on_extract = set(self.extract(point=index, table=True).flat)
            s[index] = set(range(1, 10)) - element_on_col - element_on_row - element_on_extract
        return s

    def ereaser(self, index, n):
        self.sheet[index] = set()
        for item in self.sheet[index[0], :]:
            item -= {n}
        for item in self.sheet[:, index[1]]:
            item -= {n}
        for item in self.extract(point=index):
            item -= {n}

    def deterministic_attempt(self):
        while set.union(*self.sheet.flat) != set():
            old_sheet = deepcopy(self.sheet)
            non_empties = tuple(zip(*np.where(self.sheet != set())))
            for index in non_empties:
                if len(self.sheet[index]) == 1:
                    addendum = self.sheet[index].pop()
                    self.table[index] = addendum
                    self.ereaser(index=index, n=addendum)
                else:
                    sheet_copy = deepcopy(self.sheet)
                    sheet_copy[index] = set()
                    for number in self.sheet[index]:
                        if (self.sheet[index] != set() and (number not in set.union(
                                *sheet_copy[index[0], :]) or number not in
                                set.union(*sheet_copy[:, index[1]]) or number not in set.union(
                                    *self.extract(point=index, other_table=sheet_copy).flat))):
                            self.table[index] = number
                            self.ereaser(index=index, n=number)
                row_col_and_extract = (self.sheet[index[0], :], self.sheet[:, index[1]], self.extract(point=index).flat)
                for vector in row_col_and_extract:
                    if np.count_nonzero(vector == self.sheet[index]) == len(self.sheet[index]):
                        for element in vector:
                            if element != self.sheet[index]:
                                element -= self.sheet[index]
            if np.array_equal(old_sheet, self.sheet):
                break

    def guessing_list(self):
        sizes = []
        for i in range(9):
            sizes.extend(list(map(lambda x: len(x), self.sheet[i, :])))
        unique_sizes = list(set(sizes))[1:]
        counted_sizes = list(map(lambda x: sizes.count(x), unique_sizes))
        power_sizes = np.array([unique_sizes[i] ** counted_sizes[i] for i in range(len(unique_sizes))])
        print(unique_sizes, counted_sizes, power_sizes)
        return [unique_sizes[i] for i in power_sizes.argsort()]

    def play(self):
        while not self.issudoku():
            self.deterministic_attempt()
            print(self.table)
            if self.issudoku():
                return
            else:
                n = 0
                table_bak = deepcopy(self.table)
                sheet_bak = deepcopy(self.sheet)
                table_sizes = np.array([list(map(lambda x: len(x), self.sheet[i, :])) for i in range(9)])
                for size in self.guessing_list():
                    I = tuple(zip(*np.where(table_sizes == size)))
                    sized_set_list = []
                    sized_set_list.extend(tuple(self.sheet[k]) for k in I)
                    for attempt in product(*sized_set_list, repeat=1):
                        if attempt == (2, 1, 9, 7, 4, 3, 1, 6, 7, 9, 1, 9, 2, 1, 2):
                            a = True
                        for i in range(len(attempt)):
                            self.table[I[i]] = attempt[i]
                        print('Attempt:', attempt, 'n.', n)
                        self.sheet = self.get_sheet()
                        self.deterministic_attempt()
                        if self.issudoku():
                            return
                        else:
                            self.table = deepcopy(table_bak)
                            self.sheet = deepcopy(sheet_bak)
                            n += 1


if __name__ == '__main__':
    test = Sudoku(table=np.array([[5, 0, 0, 0, 0, 2, 4, 0, 0],
                                  [0, 0, 0, 0, 3, 0, 2, 0, 0],
                                  [0, 4, 8, 1, 0, 0, 9, 0, 0],
                                  [1, 0, 7, 2, 0, 0, 0, 0, 3],
                                  [0, 3, 4, 0, 6, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 5, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 1, 9],
                                  [0, 6, 0, 0, 0, 3, 0, 0, 0],
                                  [0, 0, 0, 7, 1, 0, 0, 8, 0]], dtype=int))

    test.play()
    print(test.table)