import pygame
from .constants import RED, BLUE, BLACK, SQUARE_SIZE
from checkers.board import Board


class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            print(self.valid_moves)
            return True
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            self.change_turn()
        else:
            return False
        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLACK,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLUE:
            self.turn = RED
        else:
            self.turn = BLUE

    def validate_winner(self, row, col, color):
        piece = self.board.get_piece(row, col)
        if piece != 0:
            if piece.color == color:
                return True
        return False

    def winner(self):
        r0_c0 = self.validate_winner(0, 0, RED)
        r1_c0 = self.validate_winner(1, 0, RED)
        r0_c1 = self.validate_winner(0, 1, RED)
        r1_c1 = self.validate_winner(1, 1, RED)
        r0_c2 = self.validate_winner(0, 2, RED)
        r2_c0 = self.validate_winner(2, 0, RED)
        r0_c3 = self.validate_winner(0, 3, RED)
        r3_c0 = self.validate_winner(3, 0, RED)
        r2_c1 = self.validate_winner(2, 1, RED)
        r1_c2 = self.validate_winner(1, 2, RED)
        if r0_c0 and r1_c0 and r0_c1 and r1_c1 and r0_c2 and r2_c0 and r0_c3 and r3_c0 and r2_c1 and r1_c2:
            print('#########################################')
            print('######### Gano el Jugador ROJO ##########')
            print('#########################################')
            return RED

        r8_c8 = self.validate_winner(8, 8, BLUE)
        r7_c8 = self.validate_winner(7, 8, BLUE)
        r8_c7 = self.validate_winner(8, 7, BLUE)
        r7_c7 = self.validate_winner(7, 7, BLUE)
        r8_c6 = self.validate_winner(8, 6, BLUE)
        r6_c8 = self.validate_winner(6, 8, BLUE)
        r8_c5 = self.validate_winner(8, 5, BLUE)
        r5_c8 = self.validate_winner(5, 8, BLUE)
        r6_c7 = self.validate_winner(6, 7, BLUE)
        r7_c6 = self.validate_winner(7, 6, BLUE)
        if r8_c8 and r7_c8 and r8_c7 and r7_c7 and r8_c6 and r6_c8 and r8_c5 and r5_c8 and r6_c7 and r7_c6:
            print('#########################################')
            print('######### Gano el Jugador AZUL ##########')
            print('#########################################')
            return BLUE

        return None

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()

