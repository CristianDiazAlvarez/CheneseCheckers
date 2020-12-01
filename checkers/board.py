import pygame
from .constants import BLACK, ROWS, COLS, RED, WHITE, GREY, BLUE, SQUARE_SIZE
from .piece import Piece


class Board:
    OUTLINE = 2
    PADDING = 10

    def __init__(self):
        self.board = []
        #  self.selected_piece = None
        self.red_left = self.white_left = 10
        self.create_board()

    def draw_squares(self, win):
        win.fill(WHITE)
        radius = SQUARE_SIZE // 2 - self.PADDING

        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(win, GREY, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                #  pygame.draw.circle(win, GREY, ((row *SQUARE_SIZE) + SQUARE_SIZE//2, (col *SQUARE_SIZE) + SQUARE_SIZE//2), radius + self.OUTLINE)
                pygame.draw.circle(win, WHITE, ((row * SQUARE_SIZE) + SQUARE_SIZE//2, (col * SQUARE_SIZE) + SQUARE_SIZE//2), radius)

    def move(self, piece, row, col):
        #  Se intercambian las posiciones
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        row_count = 8
        col_count = 4
        col_c = 21
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if (row < 4) and (col < col_count):
                    self.board[row].append(Piece(row, col, BLUE))
                elif (row >= row_count) and (col >= col_c):
                    self.board[row].append(Piece(row, col, RED))
                    row_count -= 1
                else:
                    self.board[row].append(0)
            col_c -= 1
            col_count -= 1

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        vert =  piece.col
        row = piece.row
        print(piece.color)

        if piece.color == RED:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
            moves.update((self._traverse_vert(row - 1, max(row - 3, -1), -1, piece.color, vert)))
            moves.update(self._traverse_just_left(row, max(row -3, -1), -1, piece.color, left))
            moves.update(self._traverse_just_right(row, max(row - 3, -1), -1, piece.color, right))

        if piece.color == BLUE:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
            moves.update((self._traverse_vert(row + 1, max(row + 3, ROWS), 1, piece.color, vert)))
            moves.update((self._traverse_just_left(row, max(row + 3, ROWS), 1, piece.color, left)))
            moves.update((self._traverse_just_right(row, max(row + 3, ROWS), 1, piece.color, right)))
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]

            if current == 0:
                if skipped and not last:
                    break # Valida que si ya salto y no hay otra ficha para saltar no mueve otra ficha
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)

                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                    moves.update(self._traverse_vert(r + step, row, step, color, left, skipped=last))
                    moves.update(self._traverse_just_left(r + step, row, step, color, left -1, skipped=last))
                    moves.update(self._traverse_just_right(r + step, row, step, color, left +1, skipped=last))
                break

            last = [current]
            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break  # Valida que si ya salto y no hay otra ficha para saltar no mueve otra ficha
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)

                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                    moves.update(self._traverse_vert(r + step, row, step, color, right, skipped=last))
                    moves.update(self._traverse_just_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_just_right(r + step, row, step, color, right + 1, skipped=last))
                break

            last = [current]
            right += 1
        return moves


    def _traverse_vert(self, start, stop, step, color, vert, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if vert < 0:
                break
            current = self.board[r][vert]
            if current == 0:
                if skipped and not last:
                    break  # Valida que si ya salto y no hay otra ficha para saltar no mueve otra ficha
                elif skipped:
                    moves[(r, vert)] = last + skipped
                else:
                    moves[(r, vert)] = last
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)

                    moves.update(self._traverse_left(r + step, row, step, color, vert - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, vert + 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, vert, skipped=last))
                    moves.update(self._traverse_just_left(r + step, row, step, color, vert - 1, skipped=last))
                    moves.update(self._traverse_just_right(r + step, row, step, color, vert + 1, skipped=last))
                break

            last = [current]
            vert += 1
        return moves

    def _traverse_just_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left <0:
                break
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break  # Valida que si ya salto y no hay otra ficha para saltar no mueve otra ficha
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)

                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                    moves.update(self._traverse_vert(r + step, row, step, color, left, skipped=last))
                    moves.update(self._traverse_just_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_just_right(r + step, row, step, color, left + 1, skipped=last))

                break

            last = [current]
            left += 1
        return moves

    def _traverse_just_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break  # Valida que si ya salto y no hay otra ficha para saltar no mueve otra ficha
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)

                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                    moves.update(self._traverse_vert(r + step, row, step, color, right, skipped=last))
                    moves.update(self._traverse_just_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_just_right(r + step, row, step, color, right + 1, skipped=last))

                break

            last = [current]
            right += 1
        return moves