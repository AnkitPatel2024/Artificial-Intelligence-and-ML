############################################################
# CIS 521: Homework 3
############################################################

import queue
from queue import PriorityQueue
import random
import math

student_name = "Ankita Patel."


############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    puzzle_board = []
    for i in range(rows):
        puzzle_board = puzzle_board + [[0] * cols]
    start_num = 1
    for i in range(0, rows):
        for j in range(0, cols):
            puzzle_board[i][j] = start_num
            start_num += 1
    puzzle_board[rows - 1][cols - 1] = 0
    return TilePuzzle(puzzle_board)


class TilePuzzle(object):
    # Required
    def __init__(self, board):
        self.state = board
        self.rows = len(board)
        if self.rows == 0:
            self.columns = 0
        self.columns = len(board[0])
        self.empty_row = 0
        self.empty_column = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if board[i][j] == 0:
                    self.empty_row = i
                    self.empty_column = j

    def get_board(self):
        return self.state

    def perform_move(self, direction):
        empty_row = self.empty_row
        empty_column = self.empty_column
        directions = ("up", "down", "right", "left")
        if direction not in directions:
            return False
        if direction == "up":
            if empty_row == 0:
                return False
            else:
                self.get_board()[empty_row][empty_column] = \
                    self.get_board()[empty_row - 1][empty_column]
                self.get_board()[empty_row - 1][empty_column] = 0
                self.empty_row = empty_row - 1
        if direction == "down":
            if empty_row >= self.rows - 1:
                return False
            else:
                self.get_board()[empty_row][empty_column] = \
                    self.get_board()[empty_row + 1][empty_column]
                self.get_board()[empty_row + 1][empty_column] = 0
                self.empty_row = empty_row + 1
        if direction == "left":
            if empty_column <= 0:
                return False
            else:
                self.get_board()[empty_row][empty_column] = \
                    self.get_board()[empty_row][empty_column - 1]
                self.get_board()[empty_row][empty_column - 1] = 0
                self.empty_column = empty_column - 1
        if direction == "right":
            if empty_column >= self.columns - 1:
                return False
            else:
                self.get_board()[empty_row][empty_column] = \
                    self.get_board()[empty_row][empty_column + 1]
                self.get_board()[empty_row][empty_column + 1] = 0
                self.empty_column = empty_column + 1
        return True

    def scramble(self, num_moves):
        choices = ["up", "down", "left", "right"]
        for i in range(num_moves):
            direction = random.choice(choices)
            self.perform_move(direction)

    def is_solved(self):
        no_rows = self.rows
        no_cols = self.columns
        puzzle_copy = create_tile_puzzle(no_rows, no_cols)
        for i in range(0, no_rows):
            for j in range(0, no_cols):
                if (self.get_board()[i][j] != puzzle_copy.get_board()[i][j]):
                    return False
        return True

    def copy(self):
        deep_copy = [[0] * self.columns for i in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.columns):
                deep_copy[i][j] = self.state[i][j]
        return TilePuzzle(deep_copy)

    def successors(self):
        moves = ["up", "down", "left", "right"]
        for direction in moves:
            tile_puzzleCopy = self.copy()
            if tile_puzzleCopy.perform_move(direction):
                yield direction, tile_puzzleCopy

    # Required
    def iddfs_helper(self, limit, moves):
        if limit > len(moves):
            copy = self.copy()
            for move, new_p in copy.successors():
                for item in new_p.iddfs_helper(limit, moves + [move]):
                    yield item
        if self.is_solved():
            yield moves

    def find_solutions_iddfs(self):
        limit = 0
        sol = []
        while len(sol) == 0:
            sol = list(self.iddfs_helper(limit, []))
            limit += 1
            for s in sol:
                yield s

    # Required
    def calculate_h(self):
        rows = self.rows
        cols = self.columns
        solved = create_tile_puzzle(rows, cols)
        distance = 0
        for r1 in range(rows):
            for c1 in range(cols):
                value = self.get_board()[r1][c1]
                for r2 in range(rows):
                    for c2 in range(cols):
                        if solved.get_board()[r2][c2] == value:
                            distance = distance + abs(c2 - c1) + abs(r2 - r1)
        return distance

    def find_solution_a_star(self):
        sol = []
        if self.is_solved():
            return sol
        visited = set()
        puzzle_states = set()
        steps_puzzleStates = {}
        frontier = PriorityQueue()
        f_n = 0
        my_tuple = (f_n, tuple(tuple(x) for x in self.copy().get_board()))
        frontier.put(my_tuple)
        while True:
            if frontier.empty():
                return None
            node = frontier.get()
            puzzle = TilePuzzle(list(node[1]))
            visited.add(node)
            for direction, puzzle_state in puzzle.successors():
                moves_list = []
                key = tuple(tuple(x) for x in puzzle.get_board())
                if key in steps_puzzleStates:
                    previous_stepsList = steps_puzzleStates[key]
                    for x in previous_stepsList:
                        moves_list.append(x)
                if puzzle.is_solved():
                    return moves_list
                moves_list.append(direction)
                visited.add(node)
                h_n = puzzle_state.calculate_h()
                f_n = len(moves_list) + h_n
                if (f_n, puzzle_state) in visited:
                    continue
                else:
                    tupe1 = tuple(puzzle_state.get_board())
                    key = tuple(tuple(x) for x in puzzle_state.get_board())
                    if tupe1 not in (x.get_board() for x in puzzle_states):
                        puzzle_states.add(TilePuzzle(tupe1))
                        steps_puzzleStates[key] = moves_list
                        frontier.put((f_n, key))
                    else:
                        prev_steps = steps_puzzleStates[key]
                        current_cost = len(prev_steps)
                        if current_cost + h_n > f_n:
                            steps_puzzleStates[key] = moves_list
                            frontier.put((f_n, key))

############################################################
# Section 2: Grid Navigation
############################################################


def make_moves(point, move, scene):
    row = point[0]
    col = point[1]
    if scene[row][col]:
        return False
    if move == "up":
        if row == 0 or scene[row - 1][col]:
            return False
        point = row - 1, col
        return point
    if move == "down":
        if row >= (len(scene) - 1) or scene[row + 1][col]:
            return False
        point_n = row + 1, col
        return point_n
    if move == "left":
        if col == 0 or scene[row][col - 1]:
            return False
        point = row, col - 1
        return point
    if move == "right":
        if col == len(scene[0]) - 1 or scene[row][col + 1]:
            return False
        point = row, col + 1
        return point
    if move == "up-left":
        if row == 0 or col == 0 or scene[row - 1][col - 1]:
            return False
        point = row - 1, col - 1
        return point
    if move == "up-right":
        if row == 0 or col == len(scene[0]) - 1 or scene[row - 1][col + 1]:
            return False
        point = row - 1, col + 1
        return point
    if move == "down-left":
        if row >= len(scene) - 1 or col == 0 or scene[row + 1][col - 1]:
            return False
        point = row + 1, col - 1
        return point
    if move == "down-right":
        if row >= len(scene) - 1 or col == len(scene[0]) - 1 or \
                scene[row + 1][col + 1]:
            return False
        point = row + 1, col + 1
        return point


def get_copy(point):
    r = point[0]
    c = point[1]
    point_copy = (r, c)
    return point_copy


def get_successors(point, scene):
    r = point[0]
    c = point[1]
    if scene[r][c]:
        return False
    moves = ["up", "down", "right", "left", "up-left", "up-right", "down-left",
             "down-right"]
    ending = get_copy(point)
    for move in moves:
        if make_moves(ending, move, scene):
            yield point, move, make_moves(point, move, scene)


def get_eucDist(point1, point2):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    distance = math.sqrt(((y2 - y1) ** 2) + ((x2 - x1) ** 2))
    return distance


def find_path(start, goal, scene):
    if scene[start[0]][start[1]] or scene[goal[0]][goal[1]]:
        return None
    visited = set()
    puzzle_states = set()
    frontier = PriorityQueue()
    f_n = 0
    my_tuple = (f_n, start)
    frontier.put(my_tuple)
    current_cost = 0
    steps_puzzleState = {start: ([start], current_cost)}
    while (True):
        if frontier.empty():
            return None
        node = frontier.get()
        visited.add(node)
        puzzle_states.add(node[1])
        puzzle = node[1]
        for starting, move, end_state in get_successors(puzzle, scene):
            path_list = []
            key = puzzle
            prev_cost = 0
            if key in steps_puzzleState:
                previous_paths = steps_puzzleState[key][0]
                for x in previous_paths:
                    path_list.append(x)
                prev_cost = steps_puzzleState[puzzle][1]
            if puzzle == goal:
                return path_list
            if move in ["up", "down", "left", "right"]:
                step_cost = 1
            else:
                step_cost = math.sqrt(2)
            path_list.append(end_state)
            h_n = get_eucDist(end_state, goal)
            current_cost = prev_cost + step_cost
            f_n = current_cost + h_n
            if (f_n, end_state) in visited:
                continue
            else:
                if end_state not in puzzle_states:
                    puzzle_states.add(end_state)
                    steps_puzzleState[end_state] = path_list, current_cost
                    frontier.put((f_n, end_state))
                else:
                    if current_cost < steps_puzzleState[end_state][1]:
                        steps_puzzleState[end_state] = path_list, current_cost
                        frontier.put((f_n, end_state))

############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################


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


def successors_distinct(grid):
    for i in range(0, len(grid)):
        for j in (-2, -1, 1, 2):
            grid_copy = copy(grid)
            if make_move(grid_copy, i, j):
                yield (i, i + j), grid_copy


def make_solved(length, n):
    linear_grid = [0] * length
    for i in range(-n, 0):
        linear_grid[i] = i * -1
    return linear_grid


def calculate_distance(grid, n):
    grid_len = len(grid)
    puzzle_solved = make_solved(grid_len, n)
    distance = 0
    for i in range(grid_len):
        value = puzzle_solved[i]
        if value != 0:
            for j in range(grid_len):
                if grid[j] == value:
                    distance = distance + abs(j - i)
    return distance


def solve_distinct_disks(length, n):
    linear_grid = distinctDisks_puzzle(length, n)
    if isSolved_distinct(linear_grid, n):
        return []
    visited = set()
    puzzle_states = set()
    frontier = PriorityQueue()
    my_tuple = (0, tuple(copy(linear_grid)))
    frontier.put(my_tuple)
    steps_puzzleState = {tuple(linear_grid): []}
    while frontier != []:
        if frontier.empty():
            return None
        node = frontier.get()
        puzzle = list(node[1])
        for move, puzzle_state in successors_distinct(puzzle):
            move_list = []
            key = tuple(puzzle)
            if key in steps_puzzleState:
                previous_steps = steps_puzzleState[key]
                for x in previous_steps:
                    move_list.append(tuple(x))
            if isSolved_distinct(puzzle, n):
                return move_list
            move_list.append(tuple(move))
            visited.add(node)
            h_n = calculate_distance(puzzle_state, n)
            f_n = len(move_list) + h_n
            if (f_n, tuple(puzzle_state)) in visited:
                continue
            else:
                if tuple(puzzle_state) not in puzzle_states:
                    puzzle_states.add(tuple(puzzle_state))
                    steps_puzzleState[tuple(puzzle_state)] = move_list
                    frontier.put((f_n, tuple(puzzle_state)))
                else:
                    prev_cost = len(steps_puzzleState[tuple(puzzle_state)])
                    if f_n < prev_cost + h_n:
                        steps_puzzleState[tuple(puzzle_state)] = move_list
                        frontier.put((f_n, tuple(puzzle_state)))
    else:
        return None


############################################################
# Section 4: Feedback
############################################################

# Just an approximation is fine.
feedback_question_1 = 20

feedback_question_2 = """
Really none for this assignment.
"""

feedback_question_3 = """
part 2 Grid Navigation felt most interesting. I think assignment is good.
"""
