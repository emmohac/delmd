from random import randint
import math
from BoardClasses import Move
from BoardClasses import Board


# The following part should be completed by students.
# Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    def __init__(self, col, row, p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col, row, p)
        self.board.initialize_game()
        self.MAX_DEPTH = 3
        self.opponent = {1: 2, 2: 1}
        self.color = 2

    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)
        move = self.smart_move(moves)
        self.board.make_move(move, self.color)
        return move

    def smart_move(self, all_moves) -> Move:
        best_move = Move([])
        root_value = -math.inf
        for checkers in all_moves:
            for move in checkers:
                new_value = self.mini_max(0, move, self.color)
                if new_value > root_value:
                    root_value = new_value
                    best_move = Move(move)

        return best_move

    def mini_max(self, depth, move, player) -> int:
        wc = self.board.white_count
        bc = self.board.black_count

        if depth == self.MAX_DEPTH:
            if self.color == player:
                return bc - wc
            else:
                return wc - bc

        self.board.make_move(move, self.color)
        all_moves = self.board.get_all_possible_moves(self.color)

        if player is self.color:
            current_value = -math.inf
            for checkers in all_moves:
                for new_move in checkers:
                    new_value = self.mini_max(depth+1, new_move, self.opponent[self.color])
                    current_value = max(current_value, new_value)
            self.board.undo()
            return current_value
        else:
            current_value = math.inf
            for checkers in all_moves:
                for new_move in checkers:
                    new_value = self.mini_max(depth+1, new_move, self.opponent[self.color])
                    current_value = min(current_value, new_value)
            self.board.undo()
            return current_value
