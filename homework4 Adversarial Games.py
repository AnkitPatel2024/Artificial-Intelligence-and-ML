############################################################
# CIS 5210: Homework 4
############################################################

# Include your imports here, if any are used.

import collections
import copy
import itertools
import random
import math

import numpy as np

student_name = "Ankita Patel"

############################################################
# Section 1: Dominoes Game
############################################################


def create_dominoes_game(rows, cols):
    game = []
    for i in range(rows):
        game += [[False] * cols]
    return DominoesGame(game)


class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.leaf_counter = 0
        self.state = board
        self.rows = len(board)
        if self.rows == 0:
            self.cols = 0
        self.cols = len(board[0])

    def get_board(self):
        return self.state

    def reset(self):
        rows = self.rows
        cols = self.cols
        for i in range(rows):
            for j in range(cols):
                self.get_board()[i][j] = False

    def is_legal_move(self, row, col, vertical):
        if vertical:
            if row < 0 or row + 1 > self.rows - 1 or col < 0 \
                    or col > self.cols - 1:
                return False
            if self.get_board()[row][col] or self.get_board()[row + 1][col]:
                return False
        else:
            if col < 0 or col + 1 > self.cols - 1 or row < 0 \
                    or row > self.rows - 1:
                return False
            if self.get_board()[row][col] or self.get_board()[row][col + 1]:
                return False
        return True

    def legal_moves(self, vertical):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.is_legal_move(i, j, vertical):
                    yield i, j

    def perform_move(self, row, col, vertical):
        if self.is_legal_move(row, col, vertical):
            if vertical:
                self.state[row][col] = True
                self.state[row + 1][col] = True
            else:
                self.state[row][col] = True
                self.state[row][col + 1] = True
        return self

    def game_over(self, vertical):
        avail_moves = list(self.legal_moves(vertical))
        if len(avail_moves) == 0:
            return True
        return False

    def copy(self):
        game_copy = [[False] * self.cols for i in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                game_copy[i][j] = self.state[i][j]
        return DominoesGame(game_copy)

    def successors(self, vertical):
        for i in range(self.rows):
            for j in range(self.cols):
                self_copy = self.copy()
                if self.is_legal_move(i, j, vertical):
                    yield (i, j), self_copy.perform_move(i, j, vertical)

    def get_random_move(self, vertical):
        seq = list(self.legal_moves(vertical))
        return random.choice(seq)

    def evaluate_board(self, vertical):
        current_playerMoves = set(self.legal_moves(vertical))
        other_playerMovers = set(self.legal_moves(not vertical))
        return len(current_playerMoves) - len(other_playerMovers)

    def max_value(self, state, vertical, al, beta, lim):
        if state.game_over(vertical) or lim == 0:
            self.leaf_counter += 1
            return state.evaluate_board(vertical), None
        v = -np.inf
        for action, new_p in state.successors(vertical):
            new_ver = not vertical
            v2, a2 = self.min_value(new_p, new_ver, al, beta, lim - 1)
            if v2 > v:
                v, move = v2, action
                al = max(al, v)
            if v >= beta:
                return v, move
        return v, move

    def min_value(self, state, vertical, al, beta, lim):
        if state.game_over(vertical) or lim == 0:
            self.leaf_counter += 1
            return state.evaluate_board(not vertical),  None
        v = np.inf
        for action, new_p in state.successors(vertical):
            new_ver = not vertical
            v2, a2 = self.max_value(new_p, new_ver, al, beta, lim - 1)
            if v2 < v:
                self.bestMove = action
                v, move = v2, action
                beta = min(beta, v)
            if v <= al:
                return v, move
        return v, move

    def alpha_betaSearch(self, vertical, lim):
        self_copy = self.copy()
        val, b_move = self.max_value(self_copy, vertical, -np.inf, np.inf, lim)
        return b_move, val, self.leaf_counter

    # Required
    def get_best_move(self, vertical, lim):
        self_copy = self.copy()
        val, b_move = self.max_value(self_copy, vertical, -np.inf, np.inf, lim)
        return b_move, val, self.leaf_counter

############################################################
# Section 2: Feedback
############################################################


feedback_question_1 = 8

feedback_question_2 = """capturing number of leaf nodes"""

feedback_question_3 = """Maybe an easier way to capture leaf nodes."""
