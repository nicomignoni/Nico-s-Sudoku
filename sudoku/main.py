from tkinter import *
import sudoku as s
import numpy as np


def solve():
    if main_game.table.sum() == 0:
        return
    else:
        main_game.sheet = main_game.get_sheet()
        main_game.play()
        game_window.set_num_auto()


class Window:
    def __init__(self):
        self.master = Tk()

        self.master.title("Nico's Sudoku")
        self.master.geometry('476x530')
        self.master.config(bg='#3F3F44')
        self.master.resizable(0, 0)

        self.grid = self.set_grid(starting_point=(3, 3))

        self.solve = Button(self.master, text='Solve', font=('Arial', 26), relief='flat', activeforeground='#F8F8F8',
                            foreground='#F8F8F8', background='#7C7C86', activebackground='#7C7C86', command=solve)
        self.solve.place(height=46, width=102, x=3, y=480)

        self.clear = Button(self.master, text='Clear', font=('Arial', 26), relief='flat', activeforeground='#F8F8F8',
                            foreground='#F8F8F8', background='#7C7C86', activebackground='#7C7C86', command=self.clear)
        self.clear.place(height=46, width=102, x=371, y=480)

        self.set_num_auto()

    def set_grid(self, starting_point):
        grid = []

        def line(y):
            line = []
            for i in range(9):
                new_cell = Button(self.master, font=('Arial', 35), relief='flat', foreground='#3F3F44',
                                  activeforeground='#3F3F44', background='#F8F8F8', activebackground='#F8F8F8')
                if i in range(0, 3):
                    new_cell.place(height=50, width=50, x=starting_point[0] + 52 * (i % 9), y=y)
                elif i in range(3, 6):
                    new_cell.place(height=50, width=50, x=starting_point[0] + 52 * (i % 9) + 2, y=y)
                elif i in range(6, 9):
                    new_cell.place(height=50, width=50, x=starting_point[0] + 52 * (i % 9) + 4, y=y)
                index = (i, j)
                new_cell.config(command=lambda index=index: self.set_num_manual(index))
                line.extend([new_cell])
            return line

        for j in range(9):
            if j in range(0, 3):
                grid.extend(line(y=starting_point[1] + 52 * j))
            elif j in range(3, 6):
                grid.extend(line(y=starting_point[1] + 52 * j + 2))
            elif j in range(6, 9):
                grid.extend(line(y=starting_point[1] + 52 * j + 4))
        return grid

    def set_num_auto(self):
        for i in range(9):
            for j in range(9):
                if main_game.table[i, j] == 0:
                    self.grid[9 * i + j].config(text=' ')
                elif main_game.table[i, j] == main_game.table_copy[i, j]:
                    self.grid[9 * i + j].config(text=main_game.table[i, j])
                elif main_game.table[i, j] != main_game.table_copy[i, j]:
                    self.grid[9 * i + j].config(text=main_game.table[i, j], foreground='#93939D')

    def set_num_manual(self, n):
        main_game.table[(n[1], n[0])] = (main_game.table[(n[1], n[0])] + 1) % 10
        main_game.table_copy[(n[1], n[0])] = (main_game.table_copy[(n[1], n[0])] + 1) % 10
        if main_game.table[(n[1], n[0])] == 0:
            self.grid[9 * n[1] + n[0]].config(text=' ')
        else:
            self.grid[9 * n[1] + n[0]].config(text=main_game.table[(n[1], n[0])])

    def clear(self):
        main_game.table = np.zeros((9, 9), dtype=int)
        for element in self.grid:
            element.config(text=' ')
        self.master.update_idletasks()


main_game = s.Sudoku(table=np.zeros((9, 9), dtype=int))

game_window = Window()
game_window.master.mainloop()
