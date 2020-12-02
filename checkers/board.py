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

    def draw_circles(self, win):
        win.fill(WHITE)
        radius = SQUARE_SIZE // 2 - self.PADDING

        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(win, GREY, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.circle(win, WHITE, ((row * SQUARE_SIZE) + SQUARE_SIZE//2, (col * SQUARE_SIZE) + SQUARE_SIZE//2), radius)

    def move(self, piece, row, col):
        #  Se intercambian las posiciones
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        row_count = 4
        col_count = 4
        col_c = 13
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
        self.draw_circles(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
    
    def get_neighborhood(self, row, col):
        neighborhood = [
            [row - 1, col],
            [row - 1, col + 1],
            [row, col - 1],
            [row, col + 1],
            [row + 1, col - 1],
            [row + 1, col]
            ]
        return neighborhood

    def get_valid_moves(self, piece):
        moves = {}
        col =  piece.col
        row = piece.row
        print(piece.color)
        
        neighborhood = self.get_neighborhood(row, col)

        moves.update(self._traverse(neighborhood))

        #moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        #moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
        #moves.update(self._traverse_Y(row, max(row - 3, -1), -1, piece.color, col))
        #moves.update(self._traverse_Y(row, max(row - 3, -1), 1, piece.color, col))
        #moves.update(self._traverse_Y(row, min(row + 3, ROWS), 1, piece.color, col))
        #moves.update(self._traverse_Y(row, min(row + 3, ROWS), -1, piece.color, col))

        return moves

    def _traverse(self, neighborhood, skipped=[]):
        moves = {}
        for idx, rowcol in enumerate(neighborhood):
            row = rowcol[0]
            col = rowcol[1]

            if self.is_inside_board(row, col):

                current = self.board[row][col]

                if current == 0 and not((row, col) in moves):
                    moves[(row, col)] = True
                else: #Si Current no es 0 hay una ficha que puedo saltar.
                    if idx == 1 or idx == 3:
                        col+=1
                    if idx == 2 or idx == 4:
                        col-=1
                    if idx == 0 or idx == 1:
                        row-=1
                    if idx == 4 or idx == 5:
                        row+=1
                    
                    if self.is_inside_board(row, col): # si esta fuera del tablero, pass
                        if self.board[row][col] == 0 and not((row, col) in moves):
                            moves[(row, col)] = True
                            self.check_jump(row, col, moves)
                
                
                #jump
                #check more jumps in new position

        return moves

    def is_inside_board(self, row, col):
        return not(col >= COLS or row >= ROWS or col < 0 or row < 0)

    def check_jump(self, row, col, moves):
        neighborhood = self.get_neighborhood(row, col)
        for idx, rowcol in enumerate(neighborhood):
            rowMove = rowcol[0]
            colMove = rowcol[1]
            if(self.is_inside_board(rowMove, colMove)):
                current = self.board[rowMove][colMove]            
                if current == 0:
                    pass
                else:
                    if idx == 1 or idx == 3:
                        colMove+=1
                    if idx == 2 or idx == 4:
                        colMove-=1
                    if idx == 0 or idx == 1:
                        rowMove-=1
                    if idx == 4 or idx == 5:
                        rowMove+=1
                    if self.is_inside_board(rowMove, colMove): # si esta fuera del tablero, pass
                        if self.board[rowMove][colMove] == 0 and not((rowMove, colMove) in moves):
                            moves[(rowMove, colMove)] = True
                            self.check_jump(rowMove, colMove, moves)
