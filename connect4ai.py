import numpy as np
import random
import pygame
import sys
import math


BLUE = (0,0,200)
BLACK = (0,0,0)
GREEN = (0,238,255)
YELLOW = (255,255,0)

ROWS = 6
COLUMNS = 7

SQUARESIZE = 100
width = COLUMNS * SQUARESIZE
height = (ROWS+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

AGENT = 1
HUMAN = 0


EMPTY = 0
HUMAN_PIECE = 1
AGENT_PIECE = 2

WINDOW_LENGTH = 4

#connect4 board

def create_board():
	board = np.zeros((ROWS,COLUMNS))
	return board

def get_board(board):
	for c in range(COLUMNS):
		for r in range(ROWS):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMNS):
		for r in range(ROWS):		
			if board[r][c] == HUMAN_PIECE:
				pygame.draw.circle(screen, GREEN, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == AGENT_PIECE: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()
	
def print_board(board):
	print(np.flip(board, 0))

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def valid_location(board, col):
	return board[ROWS-1][col] == 0

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMNS):
		if valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def get_next_open_row(board, col):
	for r in range(ROWS):
		if board[r][col] == 0:
			return r
#moves

def best_move(board, piece):

	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		board2 = board.copy()
		drop_piece(board2, row, col, piece)
		score = score_location(board2, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col

def game_move(board, piece):
	#for horizontal,vertical and sloped diagonal locations 
	for c in range(COLUMNS-3):
		for r in range(ROWS):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	for c in range(COLUMNS):
		for r in range(ROWS-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	for c in range(COLUMNS-3):
		for r in range(ROWS-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	for c in range(COLUMNS-3):
		for r in range(3, ROWS):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def evaluation_window(window, piece):
	score = 0
	opp_piece = HUMAN_PIECE
	if piece == HUMAN_PIECE:
		opp_piece = AGENT_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_location(board, piece):
	score = 0

	center_array = [int(i) for i in list(board[:, COLUMNS//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	for r in range(ROWS):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMNS-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluation_window(window, piece)

	for c in range(COLUMNS):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROWS-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluation_window(window, piece)

	for r in range(ROWS-3):
		for c in range(COLUMNS-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluation_window(window, piece)

	for r in range(ROWS-3):
		for c in range(COLUMNS-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluation_window(window, piece)

	return score

def terminal_node(board):
	return game_move(board, HUMAN_PIECE) or game_move(board, AGENT_PIECE) or len(get_valid_locations(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if game_move(board, AGENT_PIECE):
				return (None, 100000000000000)
			elif game_move(board, HUMAN_PIECE):
				return (None, -10000000000000)
			else: 
				return (None, 0)
		else: # Depth is zero
			return (None, score_location(board, AGENT_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			copy = board.copy()
			drop_piece(copy, row, col, AGENT_PIECE)
			new_score = minimax(copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: 
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			copy = board.copy()
			drop_piece(copy, row, col, HUMAN_PIECE)
			new_score = minimax(copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value





board = create_board()
print_board(board)
game_over = False

pygame.init()

screen = pygame.display.set_mode(size)
get_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 50)

turn = random.randint(HUMAN, AGENT)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == HUMAN:
				pygame.draw.circle(screen, GREEN, (posx, int(SQUARESIZE/2)), RADIUS)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			if turn == HUMAN:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, HUMAN_PIECE)

					if game_move(board, HUMAN_PIECE):
						label = myfont.render("Player 1 wins!!", 1, GREEN)
						screen.blit(label, (40,10))
						game_over = True

					turn += 1
					turn = turn % 2

					print_board(board)
					get_board(board)


	if turn == AGENT and not game_over:				

		col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

		if valid_location(board, col):
			
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, AGENT_PIECE)

			if game_move(board, AGENT_PIECE):
				label = myfont.render("Player 2 wins!!", 1, YELLOW)
				screen.blit(label, (40,10))
				game_over = True

			print_board(board)
			get_board(board)

			turn += 1
			turn = turn % 2

	if game_over:
		pygame.time.wait(3000)

