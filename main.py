from othello import WHITE, BLACK, Board
from sarsa import Othello_sarsa


def main():
	name, stone = user_initial_inputs()

	if stone == BLACK:
		player = True
	else:
		player = False

	comp_stone = Board.get_other_stone(stone)

	s = Othello_sarsa(reset=False, epsilon=0)
	s.load_qs(name)
	board = Board()

	while not board.is_done():
		
		print(board)

		if player:
			x, y = user_placement_input(board, stone)
			board.place_stone(stone, x, y)
		else:
			s.place_board(board, comp_stone)
		player = not player

	print(board)
	print('Black:', board.count(BLACK))
	print('White:', board.count(WHITE))

	return


def user_placement_input(board: Board, stone: chr):
	pos = board.get_possible_actions(stone)
	print(pos)
	correct = False
	while not correct:
		try:
			x = int(input('x: '))
			y = int(input('y: '))
		except ValueError:
			continue
		if (x, y) in pos:
			correct = True
	return x, y


def user_initial_inputs():
	name = input("Name of file (exclude .json): ")

	correct = False
	while not correct:
		stone = input(f"What color do you want? ({WHITE}/{BLACK}): ")
		if stone == WHITE or stone == BLACK:
			correct = True
	return name, stone


if __name__ == '__main__':
	main()