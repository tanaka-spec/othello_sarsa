from sarsa import Othello_sarsa
from othello import Board, WHITE, BLACK, BLANK


def train():
	board = Board()
	stone = BLACK
	s = Othello_sarsa(reset=False)
	s.load_qs('test')
	b_prev_state = None
	b_prev_board = None
	w_prev_state = None
	w_prev_board = None
	while not board.is_done():
		able = s.place_board(board, stone)
		curr_board = repr(board)
		curr_state = board.num_turns - 1
		reward = s.evaluation_function(board, stone)
		if stone == BLACK:
			if able:
				if b_prev_board is not None and b_prev_state is not None:
					s.update_q(b_prev_state, b_prev_board, reward, curr_state, curr_board)
				b_prev_board = curr_board
				b_prev_state = curr_state
		elif stone == WHITE:
			if able:
				if w_prev_board is not None and w_prev_state is not None:
					s.update_q(w_prev_state, w_prev_board, reward, curr_state, curr_board)
				w_prev_board = curr_board
				w_prev_state = w_prev_state
		stone = Board.get_other_stone(stone)
	# print(s.qs)
	s.save_qs('test')


if __name__ == '__main__':
	train()