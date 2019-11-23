# Group: DELMD
# Team member: Huy Minh Tran    (huymt2)
#              Fu Hui           (fhui2)

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
        self.MAX_DEPTH = 4
        self.run_time_depth = 3
        self.opponent = {1: 2, 2: 1}
        self.color = 2

    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1

        moves = self.board.get_all_possible_moves(self.color)
        move = self.best_move(moves)

        if self.col is 7:
            if self.color is 1:
                if self.board.black_count == (self.col // 2 + 1):
                    self.run_time_depth = 4
                if self.board.black_count == self.col // 2:
                    self.run_time_depth = 5
            else:
                if self.board.white_count == (self.col // 2 + 1):
                    self.run_time_depth = 4
                if self.board.black_count == self.col // 2:
                    self.run_time_depth = 5
        else:
            if self.color is 1:
                if self.board.black_count == (self.col // 2 + 1):
                    self.run_time_depth = 3
                if self.board.black_count == self.col // 2:
                    self.run_time_depth = 5
            else:
                if self.board.white_count == (self.col // 2 + 1):
                    self.run_time_depth = 3
                if self.board.black_count == self.col // 2:
                    self.run_time_depth = 5

        # Final match
        if (self.board.white_count + self.board.black_count) < self.board.row // 2:
            self.run_time_depth = 7

        self.board.make_move(move, self.color)
        return move

    # MINIMAX STARTS HERE
    def smart_move(self, all_moves) -> Move:
        best_move = Move([])
        root_value = -math.inf
        for checkers in all_moves:
            for move in checkers:
                self.board.make_move(move, self.color)
                new_value = self.mini_max(0, self.opponent[self.color])
                self.board.undo()
                if new_value > root_value:
                    root_value = new_value
                    best_move = Move(move)

        return best_move

    def mini_max(self, depth, player) -> float:
        all_moves = self.board.get_all_possible_moves(player)

        if not all_moves or depth == self.run_time_depth:
            return self.evaluate(player)

        if player is self.color:
            current_value = -math.inf
            for checkers in all_moves:
                for new_move in checkers:
                    self.board.make_move(new_move, player)
                    new_value = self.mini_max(depth + 1, self.opponent[player])
                    self.board.undo()
                    current_value = max(current_value, new_value)
            return current_value
        else:
            current_value = math.inf
            for checkers in all_moves:
                for new_move in checkers:
                    self.board.make_move(new_move, player)
                    new_value = self.mini_max(depth + 1, self.opponent[player])
                    self.board.undo()
                    current_value = min(current_value, new_value)
            return current_value

    def minimal_heuristic(self, player):
        if player is 1:
            return self.board.black_count - self.board.white_count
        return self.board.white_count - self.board.black_count

    # MINIMAX ENDS HERE

    # ALPHA BETA PRUNE STARTS HERE
    def best_move(self, all_moves) -> Move:
        smart_move = Move([])
        alpha = -math.inf
        beta = math.inf
        for checkers in all_moves:

            for move in checkers:
                self.board.make_move(move, self.color)
                heuristic = self.alpha_beta_prune(0, self.color, alpha, beta)
                self.board.undo()
                if heuristic > alpha:
                    alpha = heuristic
                    smart_move = Move(move)

        return smart_move

    def alpha_beta_prune(self, depth, player, alpha, beta) -> float:
        all_moves = self.board.get_all_possible_moves(player)
        
        if not all_moves or depth is self.MAX_DEPTH:
            return self.evaluate(player)

        if player is self.color:
            current_score = -math.inf
            for checker in all_moves:
                for move in checker:
                    self.board.make_move(move, player)
                    heuristic = self.alpha_beta_prune(depth + 1, self.opponent[player], alpha, beta)
                    self.board.undo()
                    current_score = max(heuristic, current_score)
                    alpha = max(current_score, alpha)
                    if alpha >= beta:
                        break
            return current_score
        else:
            current_score = math.inf
            for checker in all_moves:
                for move in checker:
                    self.board.make_move(move, player)
                    heuristic = self.alpha_beta_prune(depth + 1, self.opponent[player], alpha, beta)
                    self.board.undo()
                    current_score = min(heuristic, current_score)
                    beta = min(current_score, beta)
                    if alpha >= beta:
                        break
            return current_score

    def evaluate(self, player) -> float:
        white_king = 0
        white_chess = 0
        black_king = 0
        black_chess = 0

        for all_checkers in self.board.board:
            for checker in all_checkers:
                if checker.is_king:
                    if checker.color == "W":
                        white_king += 5
                    elif checker.color == "B":
                        black_king += 5
                else:
                    if checker.color == "w":
                        white_chess += 2
                    else:
                        black_chess += 2

        # all_our_moves = self.board.get_all_possible_moves(player)
        # all_opponent_moves = self.board.get_all_possible_moves(self.opponent[player])
        #
        # self.board.make_move(some_move, us)
        # self.board.make_move(some_move, opponent)
        # check if our checker has been captured
        # if captured => decrement score
        if player is 1:
            score = self.board.black_count - self.board.white_count
            score += (black_king - white_king + black_chess - white_chess) * 1.5
        else:
            score = self.board.white_count - self.board.black_count
            score += (white_king - black_king + white_chess - black_chess) * 1.5

        return score

    # ALPHA BETA PRUNE ENDS HERE
