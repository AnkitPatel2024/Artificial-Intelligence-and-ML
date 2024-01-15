import random
import math

############################################################
# CIS 521: Homework 2
############################################################

student_name = "Ankita Patel."


############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    if n == 0:
        return n
    result = 1
    if n == 1:
        return result
    result = math.factorial(n ** 2) / (math.factorial((n ** 2) - n)
                                       * math.factorial(n))
    return result


def num_placements_one_per_row(n):
    if n == 0:
        return n
    return n ** n


def n_queens_valid(board):
    board_set = set(board)
    if len(board_set) < len(board):
        return False
    master_queens = set()
    for i in range(0, len(board_set)):
        tuple = i, board[i]
        master_queens.add(tuple)
    for i in range(0, len(board_set)):
        row_id = i
        column_id = board[i]
        current_tuple = i, board[i]
        other_queens = master_queens
        other_queens.remove(current_tuple)
        # check diagonally left upwards
        while (row_id >= 0 and column_id >= 0):
            cell = row_id, column_id
            for x in other_queens:
                if cell == x:
                    return False
            row_id = row_id - 1
            column_id = column_id - 1
        # check diagonally right upwards
        row_id = i
        column_id = board[i]
        while (row_id >= 0 and column_id < len(board)):
            cell = row_id, column_id
            for x in other_queens:
                if cell == x:
                    return False
            row_id -= 1
            column_id += 1
        # check diagonally left downwards
        row_id = i
        column_id = board[i]
        while (row_id < len(board) and column_id >= 0):
            cell = row_id, column_id
            for x in other_queens:
                if cell == x:
                    return False
            row_id += 1
            column_id -= 1
        # check diagonally right downwards
        row_id = i
        column_id = board[i]
        while (row_id < len(board) and column_id < len(board)):
            cell = row_id, column_id
            for x in other_queens:
                if cell == x:
                    return False
            row_id += 1
            column_id += 1
    return True


def n_queens_solutions(n):
    columns = [False] * n
    diagon_right = set()
    diagon_left = set()
    sol = []

    def place_queen(i, puzzle):
        if i == n:
            sol.append(puzzle)
            return
        for c in range(n):
            if columns[c] or (c + i) in diagon_right or (c - i) in diagon_left:
                continue
            columns[c] = True
            diagon_right.add(c + i)
            diagon_left.add(c - i)
            place_queen(i + 1, puzzle + [c])
            columns[c] = False
            diagon_right.remove(c + i)
            diagon_left.remove(c - i)
    place_queen(0, [])
    return sol


############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.state = board
        self.rows = len(board)
        if self.rows == 0:
            self.columns = 0
        self.columns = len(board[0])

    def get_board(self):
        return self.state

    def perform_move(self, row, col):
        i = row
        j = col
        m = self.rows
        n = self.columns
        if i < 0 or i >= m or col < 0 or col >= n:
            return
        if self.state[i][j]:
            self.state[i][j] = False
        else:
            self.state[i][j] = True
        if j < n - 1:
            if self.state[i][j + 1]:
                self.state[i][j + 1] = False
            else:
                self.state[i][j + 1] = True
        if j > 0:
            if self.state[i][j - 1]:
                self.state[i][j - 1] = False
            else:
                self.state[i][j - 1] = True
        if i > 0:
            if self.state[i - 1][j]:
                self.state[i - 1][j] = False
            else:
                self.state[i - 1][j] = True
        if i < m - 1:
            if self.state[i + 1][j]:
                self.state[i + 1][j] = False
            else:
                self.state[i + 1][j] = True

    def scramble(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if random.random() < 0.5:
                    self.perform_move(i, j)

    def is_solved(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.get_board()[i][j]:
                    return False
        return True

    def copy(self):
        deep_copy = [[0] * self.columns for i in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.columns):
                deep_copy[i][j] = self.state[i][j]
        return LightsOutPuzzle(deep_copy)

    def successors(self):
        for i in range(self.rows):
            for j in range(self.columns):
                puzzle_copy = self.copy()
                puzzle_copy.perform_move(i, j)
                yield (i, j), puzzle_copy

    def find_solution(self):
        if self.is_solved():
            return []
        frontier = [self.copy()]
        steps_puzzleState = {}
        solution = []
        board_states = set()
        while frontier != []:
            node = frontier.pop(0)
            for move, puzzle_state in node.successors():
                move_list = []
                key = tuple(tuple(x) for x in node.get_board())
                if key in steps_puzzleState:
                    previous_stepsList = steps_puzzleState[key]
                    for x in previous_stepsList:
                        move_list.append(x)
                move_list.append(move)
                if puzzle_state.is_solved():
                    key = LightsOutPuzzle(tuple(puzzle_state.get_board()))
                    return move_list
                else:
                    if tuple(puzzle_state.get_board()) not in (x.get_board()
                       for x in board_states):
                        tuple_1 = tuple(puzzle_state.get_board())
                        board_states.add(LightsOutPuzzle(tuple_1))
                        key = tuple(tuple(x) for x in puzzle_state.get_board())
                        steps_puzzleState[key] = move_list
                        frontier.append(puzzle_state)
        else:
            return None


def create_puzzle(rows, cols):
    puzzle_board = []
    for i in range(rows):
        puzzle_board = puzzle_board + [[False] * cols]
    return LightsOutPuzzle(puzzle_board)


############################################################
# Section 3: Linear Disk Movement
############################################################

def identicalDisks_puzzle(length, n):
    if n > length:
        return
    linear_grid = [0] * length
    for i in range(n):
        linear_grid[i] = 1
    return linear_grid


def distinctDisks_puzzle(length, n):
    if n > length:
        return
    linear_grid = [0] * length
    for i in range(n):
        linear_grid[i] = i + 1
    return linear_grid


def make_move(grid, cell, stepsize):
    if (cell + stepsize) < 0 or (cell + stepsize) >= len(grid) or \
            grid[cell] == 0 or grid[cell + stepsize] != 0:
        return False
    if stepsize == 2:
        if grid[cell + 1] == 0:
            return False
    if stepsize == -2:
        if grid[cell - 1] == 0:
            return False
    grid[cell + stepsize] = grid[cell]
    grid[cell] = 0
    return grid


def copy(grid):
    deep_copy = []
    for i in range(len(grid)):
        deep_copy.append(grid[i])
    return deep_copy


def isSolved_identical(grid, n):
    length = len(grid)
    for i in range(length - n, length):
        if grid[i] != 1:
            return False
    count = 0
    for x in grid:
        if x != 0:
            count += 1
    if count != n:
        return False
    return True


def isSolved_distinct(grid, n):
    length = len(grid)
    for i in range(-n, 0):
        if grid[i] != i * -1:
            return False
    count = 0
    for x in grid:
        if x != 0:
            count += 1
    if count != n:
        return False
    return True


def successors_identical(grid):
    for i in range(0, len(grid)):
        for j in range(1, 3):
            grid_copy = copy(grid)
            if make_move(grid_copy, i, j):
                yield (i, i + j), grid_copy


def successors_distinct(grid):
    for i in range(0, len(grid)):
        for j in (-2, -1, 1, 2):
            grid_copy = copy(grid)
            if make_move(grid_copy, i, j):
                yield (i, i + j), grid_copy


def solve_identical_disks(length, n):
    linear_grid = identicalDisks_puzzle(length, n)
    if isSolved_identical(linear_grid, n):
        return []
    frontier = [copy(linear_grid)]
    steps_puzzleState = {tuple(linear_grid): []}
    puzzle_states = set()
    while frontier != []:
        node = frontier.pop(0)
        for move, puzzle in successors_identical(node):
            move_list = []
            key = tuple(node)
            if key in steps_puzzleState:
                previous_steps = steps_puzzleState[key]
                for x in previous_steps:
                    move_list.append(tuple(x))
            move_list.append(tuple(move))
            if isSolved_identical(puzzle, n):
                return move_list
            else:
                if tuple(puzzle) not in puzzle_states:
                    puzzle_states.add(tuple(puzzle))
                    steps_puzzleState[tuple(puzzle)] = move_list
                    frontier.append(puzzle)
    else:
        return None


def solve_distinct_disks(length, n):
    linear_grid = distinctDisks_puzzle(length, n)
    if isSolved_distinct(linear_grid, n):
        return []
    frontier = [copy(linear_grid)]
    steps_puzzleState = {tuple(linear_grid): []}
    puzzle_states = set()
    while frontier != []:
        node = frontier.pop(0)
        for move, puzzle in successors_distinct(node):
            move_list = []
            key = tuple(node)
            if key in steps_puzzleState:
                previous_steps = steps_puzzleState[key]
                for x in previous_steps:
                    move_list.append(tuple(x))
            move_list.append(tuple(move))
            if isSolved_distinct(puzzle, n):
                return move_list
            else:
                if tuple(puzzle) not in puzzle_states:
                    puzzle_states.add(tuple(puzzle))
                    steps_puzzleState[tuple(puzzle)] = move_list
                    frontier.append(puzzle)
    else:
        return None


###############################################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """approximately 3 days (6 -8 hours per day)."""

feedback_question_2 = """all 15 point questions required little brainstorming
but no stumple blocks.Atleast yet in this course.I wish there was not that much
Homework as it takes good amount of time just for homework for this class."""

feedback_question_3 = """ All problems were very interesting. I liked the part
that lightsout vs lineardisks are implemented.Using mostly the same methods but
one as OOPs and other one as not OOP. Really liked comparing them."""
