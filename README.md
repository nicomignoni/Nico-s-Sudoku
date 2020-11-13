# Nico's Sudoku 

This is a simple Python implementation of the [Crook's Algorithm](https://www.ams.org/notices/200904/tx090400460p.pdf) for solving sudoku. 

## Description

There are two main functions that constitute the core of the program. The `deterministic_attempt` function is the straightforward implementation of the aforementioned algorithm. For most of the easy sudoku this is sufficient to solve it completely.

When the this procedure can't ultimate the grid (even though it manages to fill some cells) the `guessing_list` generates a list of candidate numbers to be inserted in a set of cells and than, within the `play` function, the `deterministic_attempt` function tries to finish up the filling. The *guessing* process is optimized in order to limit the number of attempt needed to find the right combination of numbers that, placed in the right grid, allows the program to win the game. 



