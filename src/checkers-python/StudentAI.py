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
        self.run_time_depth = 3
        self.opponent = {1: 2, 2: 1}
        self.color = 2

    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1

        move = self.best_move()
        self.board.make_move(move, self.color)
        return move

    # ALPHA BETA PRUNE STARTS HERE
    def best_move(self) -> Move:
        moves = self.board.get_all_possible_moves(self.color)
        smart_move = Move([])
        alpha = -math.inf
        beta = math.inf
        for checkers in moves:
            for move in checkers:
                self.board.make_move(move, self.color)
                heuristic = self.alpha_beta_prune(1, self.opponent[self.color], alpha, beta)
                self.board.undo()
                if heuristic > alpha:
                    alpha = heuristic
                    smart_move = Move(move)

        return smart_move

    def alpha_beta_prune(self, depth, player, alpha, beta) -> float:
        all_moves = self.board.get_all_possible_moves(player)

        if not all_moves or depth is self.run_time_depth:
            return self.evaluate()

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

    def evaluate(self) -> float:
        white_king = 0
        white_chess = 0
        black_king = 0
        black_chess = 0

        white_king_list = list()
        black_king_list = list()

        white_chess_list = []
        black_chess_list = []

        for all_checkers in self.board.board:
            for checker in all_checkers:
                if checker.color == "W":
                    if checker.is_king:
                        white_king += 1
                        white_king_list.append(checker)
                    else:
                        white_chess_list.append(checker)
                        white_chess += 1
                    if checker.col == 0 or checker.col == self.col - 1:
                        white_chess += 1
                    if checker.col - 1 > 0 and checker.row - 1 > 0:
                        if self.board.board[checker.row - 1][checker.col - 1].color == "W":
                            white_chess += 0.5
                    if checker.col - 1 > 0 and checker.row + 1 <= self.row - 1:
                        if self.board.board[checker.row + 1][checker.col - 1].color == "W":
                            white_chess += 0.5
                    if checker.col + 1 <= self.col - 1 and checker.row - 1 > 0:
                        if self.board.is_in_board(checker.row - 1, checker.col + 1) and \
                                self.board.board[checker.row - 1][checker.col + 1].color == "W":
                            white_chess += 0.5
                    if checker.col + 1 <= self.col - 1 and checker.row + 1 <= self.row - 1:
                        if self.board.is_in_board(checker.row + 1, checker.row + 1) and \
                                self.board.board[checker.row + 1][checker.row + 1].color == "W":
                            white_chess += 0.5
                if checker.color == "B":
                    if checker.is_king:
                        black_king_list.append(checker)
                        black_king += 1
                    else:
                        black_chess_list.append(checker)
                        black_chess += 1
                    if checker.col == 0 or checker.col == self.col - 1:
                        black_chess += 1
                    if checker.col - 1 > 0 and checker.row - 1 > 0:
                        if self.board.board[checker.row - 1][checker.col - 1].color == "B":
                            black_chess += 0.5
                    if checker.col - 1 > 0 and checker.row + 1 <= self.row - 1:
                        if self.board.board[checker.row + 1][checker.col - 1].color == "B":
                            black_chess += 0.5
                    if checker.col + 1 <= self.col - 1 and checker.row - 1 > 0:
                        if self.board.is_in_board(checker.row - 1, checker.col + 1) and \
                                self.board.board[checker.row - 1][checker.col + 1].color == "B":
                            black_chess += 0.5
                    if checker.col + 1 <= self.col - 1 and checker.row + 1 <= self.row - 1:
                        if self.board.is_in_board(checker.row + 1, checker.row + 1) and \
                                self.board.board[checker.row + 1][checker.row + 1].color == "B":
                            black_chess += 0.5

        king_dis = 1
        if self.color == 1:
            score = (black_king * 8 + black_chess) - (white_chess + white_king * 5)
            for checker in black_king_list:
                for opponent in white_chess_list:
                    king_dis += self.calculate_distance(checker.row, checker.col, opponent.row, opponent.col)
            # for checker in black_chess_list:
            #    chess_dis += self.row - 1 - checker.row
            score = score / king_dis
        else:
            score = (white_king * 8 + white_chess) - (black_chess + black_king * 5)
            for checker in white_king_list:
                for opponent in black_chess_list:
                    king_dis += self.calculate_distance(checker.row, checker.col, opponent.row, opponent.col)

            # for checker in white_chess_list:
            #    chess_dis += checker.row
            score = score / king_dis

        return score

    def calculate_distance(self, first_row, first_col, second_row, second_col) -> float:
        a = abs(first_row - second_row)
        b = abs(first_col - second_col)
        dis = max(a, b)
        return dis

    # ALPHA BETA PRUNE ENDS HERE
