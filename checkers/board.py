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

    def  evaluarte(self):
        # Inventese algo chimba
        red_pieces = self.get_all_pieces(RED)
        blue_pieces = self.get_all_pieces(BLUE)
        red_distance = blue_distance = 0
        for i in range(len(red_pieces)):
            red_distance += abs((red_pieces[i].x-0)) + abs((red_pieces[i].y-0))
            blue_distance += abs((blue_pieces[i].x-SQUARE_SIZE)) + abs((blue_pieces[i].y-SQUARE_SIZE))
        return blue_distance//10 - red_distance//10

    def get_all_pieces(self, color):
        pieces =[]
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

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

    def validate_winner(self, row, col, color):
        piece = self.get_piece(row, col)
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



