############################################################
# CIS 5210: Homework 5
############################################################

# Include your imports here, if any are used.

import collections
import copy
import itertools
import random
import math

student_name = "Ankita Patel"

############################################################
# Sudoku Solver
############################################################


def sudoku_cells():
    cells = []
    for i in range(9):
        for j in range(9):
            cell = i, j
            cells.append(cell)
    return cells


def get_block_neighbours(cell):
    row = cell[0]
    col = cell[1]
    neighbours = set()
    if row < 3:
        if col < 3:
            for i in range(3):
                for j in range(3):
                    if (i, j) != cell:
                        tuple_n = (cell, (i, j))
                        if tuple_n not in neighbours:
                            neighbours.add(tuple_n)
        if col > 2 and col < 6:
            for i in range(3):
                for j in range(3, 6):
                    if (i, j) != cell:
                        tuple_n = (cell, (i, j))
                        if tuple_n not in neighbours:
                            neighbours.add(tuple_n)
        if col > 5:
            for i in range(3):
                for j in range(6, 9):
                    if (i, j) != cell:
                        tuple_n = (cell, (i, j))
                        if tuple_n not in neighbours:
                            neighbours.add(tuple_n)
    if row > 2 and row < 6:
        if col < 3:
            for i in range(3, 6):
                for j in range(3):
                    if (i, j) != cell:
                        tuple_n = (cell, (i, j))
                        if tuple_n not in neighbours:
                            neighbours.add(tuple_n)
        if col > 2 and col < 6:
            for i in range(3, 6):
                for j in range(3, 6):
                    if (i, j) != cell:
                        tuple_n = (cell, (i, j))
                        if tuple_n not in neighbours:
                            neighbours.add(tuple_n)
        if col > 5:
            for i in range(3, 6):
                for j in range(6, 9):
                    if (i, j) != cell:
                        tuple_n = (cell, (i, j))
                        if tuple_n not in neighbours:
                            neighbours.add(tuple_n)
    if row > 5:
        if col < 3:
            for i in range(6, 9):
                for j in range(3):
                    if (i, j) != cell:
                        tuple_n = (cell, (i, j))
                        if tuple_n not in neighbours:
                            neighbours.add(tuple_n)
        if col > 2 and col < 6:
            for i in range(6, 9):
                for j in range(3, 6):
                    if (i, j) != cell:
                        tuple_n = (cell, (i, j))
                        if tuple_n not in neighbours:
                            neighbours.add(tuple_n)
        if col > 5:
            for i in range(6, 9):
                for j in range(6, 9):
                    if (i, j) != cell:
                        tuple_n = (cell, (i, j))
                        if tuple_n not in neighbours:
                            neighbours.add(tuple_n)
    return neighbours


def get_all_neighbours(cell):
    row = cell[0]
    col = cell[1]
    neighbours = get_block_neighbours(cell)
    for i in range(9):
        if i != col:
            tuple_r = (cell, (row, i))
            if tuple_r not in neighbours:
                neighbours.add(tuple_r)
    for i in range(9):
        if i != row:
            tuple_c = (cell, (i, col))
            if tuple_c not in neighbours:
                neighbours.add(tuple_c)
    return neighbours


def rowcol_neighbours(cell):
    row = cell[0]
    col = cell[1]
    neighbours = set()
    for i in range(9):
        if i != col:
            tuple_r = (cell, (row, i))
            if tuple_r not in neighbours:
                neighbours.add(tuple_r)
    for i in range(9):
        if i != row:
            tuple_c = (cell, (i, col))
            if tuple_c not in neighbours:
                neighbours.add(tuple_c)
    return neighbours


def row_neighbours(cell):
    row = cell[0]
    col = cell[1]
    neighbours = set()
    for i in range(9):
        if i != col:
            tuple_r = (row, i)
            if tuple_r not in neighbours:
                neighbours.add(tuple_r)
    return neighbours


def col_neighbours(cell):
    row = cell[0]
    col = cell[1]
    neighbours = set()
    for i in range(9):
        if i != row:
            tuple_c = (i, col)
            if tuple_c not in neighbours:
                neighbours.add(tuple_c)
    return neighbours


def sudoku_arcs():
    arcs = []
    for i in range(9):
        for j in range(9):
            cell_arcs = get_all_neighbours((i, j))
            for neighbour_pair in cell_arcs:
                arcs.append(neighbour_pair)
    return arcs


def read_board(path):
    f = open(path, "r")
    lines = []
    for line in f:
        lines.append(line.strip())
    f.close()
    domain = []
    for i in range(1, 10):
        domain.append(i)
    board_dict = {}
    for i in range(9):
        for j in range(9):
            value_list = []
            key = (i, j)
            value = lines[i][j]
            if value == '*':
                value_list = domain
            else:
                value = int(value)
                value_list.append(value)
            board_dict[key] = value_list
    return board_dict


class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board = board

    def get_values(self, cell):
        cell_values = self.board[cell]
        value_set = set(cell_values)
        return value_set

    def remove_inconsistent_values(self, cell1, cell2):
        cell1_val = self.get_values(cell1)
        original_mem = len(cell1_val)
        cell1_copy = set()
        for x in cell1_val:
            cell1_copy.add(x)
        cell2_val = self.get_values(cell2)
        for val in cell1_val:
            if len(cell2_val) == 1:
                if val in cell2_val:
                    cell1_copy.remove(val)
        self.board[cell1] = cell1_copy
        if len(cell1_copy) < original_mem:
            return True
        else:
            return False

    def infer_ac3(self):
        q = []
        for arc in Sudoku.ARCS:
            q.append(arc)
        while q != []:
            xi, xj = q.pop(0)
            if self.remove_inconsistent_values(xi, xj):
                if len(self.get_values(xi)) == 0:
                    return False
                neighbours = get_all_neighbours(xi)
                for cel, neighbour in neighbours:
                    if neighbour != xj:
                        q.append((neighbour, cel))
        return True

    def infer_improved(self):
        extra_inference = True
        while extra_inference:
            self.infer_ac3()
            extra_inference = False
            for ce in Sudoku.CELLS:
                uniqval = False
                if len(self.get_values(ce)) != 1:
                    for v in self.get_values(ce):
                        row_neighbour = row_neighbours(ce)
                        for rn in row_neighbour:
                            if v not in self.get_values(rn):
                                uniqval = True
                            else:
                                uniqval = False
                                break
                        if uniqval:
                            self.board[ce] = {v}
                            extra_inference = True
                            break
                        col_neighbour = col_neighbours(ce)
                        for cn in col_neighbour:
                            if v not in self.get_values(cn):
                                uniqval = True
                            else:
                                uniqval = False
                                break
                        if uniqval:
                            self.board[ce] = {v}
                            extra_inference = True
                            break
                        block_neighbours = get_block_neighbours(ce)
                        for cell, block_n in block_neighbours:
                            if v not in self.get_values(block_n):
                                uniqval = True
                            else:
                                uniqval = False
                                break
                        if uniqval:
                            self.board[ce] = {v}
                            extra_inference = True
                            break

    def get_copy(self):
        board_copy = {}
        for c in Sudoku.CELLS:
            board_copy[c] = self.get_values(c)
        return Sudoku(board_copy)

    def is_solved(self):
        for c in Sudoku.CELLS:
            if len(self.get_values(c)) != 1:
                return False
            neighbours = get_all_neighbours(c)
            for ce, n in neighbours:
                if len(self.get_values(n)) != 1:
                    return False
                if self.get_values(n) == self.get_values(ce):
                    return False
        return True

    def infer_with_guessing(self):
        self.infer_improved()
        for cell in Sudoku.CELLS:
            cell_possibleVals = self.get_values(cell)
            if len(cell_possibleVals) != 1:
                for x in cell_possibleVals:
                    self_copy = self.get_copy()
                    self.board[cell] = {x}
                    self.infer_with_guessing()
                    if self.is_solved():
                        break
                    else:
                        for cell in Sudoku.CELLS:
                            self.board[cell] = self_copy.get_values(cell)
                return

############################################################
# Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = 20

feedback_question_2 = """
The hard puzzles. Infer_with_guessing() method logic.
"""

feedback_question_3 = """
Some more help on understanding the logic for last method
"""
