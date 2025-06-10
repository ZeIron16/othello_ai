from config_ui import WHITE, BLACK, EMPTY
from copy import deepcopy

class Board:
    def __init__(self):
        self.board = [[EMPTY for _ in range(8)] for _ in range(8)]
        self.board[3][3] = WHITE
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[4][4] = WHITE
        self.valid_moves = []

    def convert_board(self):
        new_board = []
        for i in range(8):
            new_board.append([])
            for j in range(8):
                if self.board[i][j] == WHITE:
                    new_board[i].append('W')
                elif self.board[i][j] == BLACK:
                    new_board[i].append('B')
                else:
                    new_board[i].append('.')
        return new_board
    
    def get_valid_moves(self, color):
        opponent = WHITE if color == BLACK else BLACK
        valid_moves = []

        for row in range(8):
            for col in range(8):
                if self.board[row][col] != EMPTY:
                    continue

                for dx, dy in [(-1, 0), (-1, 1), (0, 1), (1, 1),
                               (1, 0), (1, -1), (0, -1), (-1, -1)]:
                    x, y = row + dx, col + dy
                    flips = []

                    while self._on_board(x, y) and self.board[x][y] == opponent:
                        flips.append((x, y))
                        x += dx
                        y += dy

                    if flips and self._on_board(x, y) and self.board[x][y] == color:
                        valid_moves.append((row, col))
                        break  # No need to check other directions

        self.valid_moves = valid_moves
        return valid_moves

    def _lookup(self, row, col, color, opponent):
        directions = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                    (1, 0), (1, -1), (0, -1), (-1, -1)]
        valid = []

        for dx, dy in directions:
            x, y = row + dx, col + dy
            has_opponent_between = False

            while self._on_board(x, y) and self.board[x][y] == opponent:
                x += dx
                y += dy
                has_opponent_between = True

            if has_opponent_between and self._on_board(x, y) and self.board[x][y] == EMPTY:
                valid.append((x, y))

        return valid
    
    def apply_move(self, move, color):
        if move not in self.valid_moves:
            return False

        flips_total = []
        opponent = WHITE if color == BLACK else BLACK
        directions = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                    (1, 0), (1, -1), (0, -1), (-1, -1)]

        for dx, dy in directions:
            x, y = move[0] + dx, move[1] + dy
            flips = []

            while self._on_board(x, y) and self.board[x][y] == opponent:
                flips.append((x, y))
                x += dx
                y += dy

            if flips and self._on_board(x, y) and self.board[x][y] == color:
                flips_total.extend(flips)

        if not flips_total:
            return False  # Ce coup ne retourne rien, donc invalide

        self.board[move[0]][move[1]] = color
        for fx, fy in flips_total:
            self.board[fx][fy] = color

        self.valid_moves = []  # Optionnel selon le besoin de GUI
        return True


    def count_stones(self):
        whites = sum(row.count(WHITE) for row in self.board)
        blacks = sum(row.count(BLACK) for row in self.board)
        empties = sum(row.count(EMPTY) for row in self.board)
        return whites, blacks, empties

    def game_over(self):
        whites, blacks, empties = self.count_stones()
        if whites == 0 or blacks == 0 or empties == 0:
            return True
        if not self.get_valid_moves(BLACK) and not self.get_valid_moves(WHITE):
            return True
        return False

    def _on_board(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def print_board(self):
        print("  ", end="")
        for i in range(8):
            print(i, end=" ")
        print()
        for i in range(8):
            print(i, end=" ")
            for j in range(8):
                if self.board[i][j] == BLACK:
                    print("B", end=" ")
                elif self.board[i][j] == WHITE:
                    print("W", end=" ")
                else:
                    print(".", end=" ")
            print()