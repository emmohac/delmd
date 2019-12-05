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
        self.number_of_move = 0
        self.EARLY_GAME = 10
        self.MID_GAME = 20
        self.END_GAME = 30
        self.run_time_depth = 5
        self.opponent = {1: 2, 2: 1}
        self.color = 2

    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1

        move = self.best_move()

        if self.board.row == self.board.col:
            self.run_time_depth = self.get_depth(True)
        if self.board.row != self.board.col:
            self.run_time_depth = self.get_depth(False)

        self.board.make_move(move, self.color)
        self.number_of_move += 1
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
                #if len(self.board.get_all_possible_moves(self.opponent[self.color])) == 1:
                #       heuristic -= 100000
                self.board.undo()
                if heuristic > alpha:
                    alpha = heuristic
                    smart_move = Move(move)

        return smart_move

    def alpha_beta_prune(self, depth, player, alpha, beta) -> float:
        all_moves = self.board.get_all_possible_moves(player)

        if depth is self.run_time_depth:
            return self.evaluate()
        
        if not all_moves:
            winplayer = self.board.is_win(self.opponent[player])
            if winplayer == self.color:
                return 100000
            elif winplayer == self.opponent[self.color]:
                return -100000
            else:
                return 0

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

    # make new function to evaluate king
    def evaluate(self) -> float:
        white_king = 0
        white_chess = 0
        black_king = 0
        black_chess = 0

        white_king_list = list()
        black_king_list = list()

        white_chess_list = list()
        black_chess_list = list()

        for all_checkers in self.board.board:
            for checker in all_checkers:
                if checker.is_king:
                    if checker.color == "W":
                        white_king += 1
                        white_king_list.append(checker)
                    if checker.color == "B":
                        black_king += 1
                        black_king_list.append(checker)
                else:
                    if checker.color == "W":
                        white_chess += 2
                        white_chess_list.append(checker)
                    if checker.color == "B":
                        black_chess += 2
                        black_chess_list.append(checker)

                white_chess, black_chess = self.get_score(checker, white_chess, black_chess)

        king_dis = 1
        if self.color == 1:
            score = self.board.black_count - self.board.white_count + (black_king * 8 + black_chess) - (white_chess + white_king * 5)
            for checker in black_king_list:
                for opponent in white_chess_list:
                    king_dis += self.calculate_distance(checker.row, checker.col, opponent.row, opponent.col)
        else:
            score = 1 + self.board.white_count - self.board.black_count + (white_king * 8 + white_chess) - (black_chess + black_king * 5)
            for checker in white_king_list:
                for opponent in black_chess_list:
                    king_dis += self.calculate_distance(checker.row, checker.col, opponent.row, opponent.col)

        return score / king_dis

    def calculate_distance(self, first_row, first_col, second_row, second_col) -> float:
        a = abs(first_row - second_row)
        b = abs(first_col - second_col)
        return max(a, b)

    def get_depth(self, is_equal):
        if self.number_of_move != 0:
            if is_equal:
                if self.number_of_move <= 5:
                    return 3
                if self.number_of_move <= self.EARLY_GAME:
                    return 5
                if self.number_of_move <= self.END_GAME:
                    return 7
                return 3
            else:
                if 1 <= self.number_of_move <= 5:
                    return 3
                if 6 <= self.number_of_move <= 10:
                    return 5
                if self.number_of_move % 2 == 0:
                    return 5
                return 3
        return 3

    def get_score(self, checker, white_chess, black_chess):
        if checker.col == 0 or checker.col == self.col - 1:
            if checker.color == "W":
                white_chess += 1
            if checker.color == "B":
                black_chess += 1
        if checker.col - 1 > 0 and checker.row - 1 > 0:
            if self.board.board[checker.row-1][checker.col-1].color == "W":
                white_chess += 0.5
            if self.board.board[checker.row-1][checker.col-1].color == "B":
                black_chess += 0.5
        if checker.col-1 > 0 and checker.row + 1 <= self.row - 1:
            if self.board.board[checker.row+1][checker.col-1].color == "W":
                white_chess += 0.5
            if self.board.board[checker.row+1][checker.col-1].color == "B":
                black_chess += 0.5
        if checker.col + 1 <= self.col -1 and checker.row - 1 > 0:
            if self.board.is_in_board(checker.row - 1, checker.col + 1):
                if self.board.board[checker.row-1][checker.col+1].color == "W":
                    white_chess += 0.5
                if self.board.board[checker.row-1][checker.col+1].color == "B":
                    black_chess += 0.5
        if checker.col + 1 < self.col - 1 and checker.row + 1 <= self.row - 1:
            if self.board.is_in_board(checker.row+1, checker.col+1):
                if self.board.board[checker.row+1][checker.col+1] == "W":
                    white_chess += 0.5
                if self.board.board[checker.row+1][checker.col+1] == "B":
                    black_chess += 0.5

        return white_chess, black_chess
    # ALPHA BETA PRUNE ENDS HERE
