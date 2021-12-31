from copy import copy, deepcopy


WHITE = 'w'
BLACK = 'b'
BLANK = ''
DIRECTIONS = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]


class Board:
	def __init__(self, size=8, reset=True):
		self.size = size
		self.array = None
		self.num_stones = 0
		if reset:
			self.reset_board()
		return


	def __eq__(self, other):
		if self.size != other.size or self.num_stones != other.num_stones:
			return False
		for x in range(self.size):
			for y in range(self.size):
				if self.array[x][y] != other.array[x][y]:
					return False
		return True


	def __str__(self):
		output = ""
		for y in range(self.size):
			for x in range(self.size):
				if '' == self.array[x][y]:
					output += '- '
				else:
					output += self.array[x][y] + ' '
			output += '\n'
		return output


	def __repr__(self):
		return repr(self.array)


	def __hash__(self):
		return hash(repr(self.array))


	def reset_board(self):
		self.array = [[BLANK for i in range(self.size)] for j in range(self.size)]
		self.array[3][4] = WHITE
		self.array[4][3] = WHITE
		self.array[3][3] = BLACK
		self.array[4][4] = BLACK
		self.num_stones = 4
		return


	def inside_board(self, x: int, y: int):
		return 0 <= x < self.size and 0 <= y < self.size


	def is_valid_move(self, stone: chr, init_x: int, init_y: int):
		if self.array[init_x][init_y] != BLANK and not self.inside_board(init_x, init_y):
			return False
		other_stone = get_other_stone(stone)
		flip_set = set()
		
		for xdirection, ydirection in DIRECTIONS:
			x = init_x
			y = init_y
			x += xdirection
			y += ydirection
			if inside_board(x, y) and board[x][y] == other_stone:
				x += xdirection
				y += ydirection
				if not inside_board(x, y):
					continue
				hold = set()
				while board[x][y] == other_stone:
					x += xdirection
					y += ydirection
					if not inside_board(x, y):
						break
					hold.add((x, y))
				if inside_board(x, y) and self.array[x][y] == stone:
					flip_set.update(hold)
		return flip_set


	def place_stone(self, stone: chr, init_x: int, init_y: int):
		flip_set = is_valid_move(stone, init_x, init_y)
		if flip_set:
			self.flip_stones(flip_set)
			self.num_stones += 1
			return True
		return False


	def flip_stones(self, array: set):
		for x, y in array:
			self.array[x][y] = get_other_stone(self.array[x][y])
		return


	def get_possible_boards(self, stone: chr):
		output = set()
		for x in range(self.size):
			for y in range(self.size):
				hold = self.copy()
				if hold.place_stone(stone, x, y):
					output.add((x, y), hold)
		return output


	def get_possible_actions(self, stone: chr):
		output = set()
		for x in range(self.size):
			for y in range(self.size):
				if is_valid_move(stone, x, y):
					output.add((x, y))
		return output


	def copy(self):
		output = Board(reset=False)
		output.size = self.size
		output.array = deepcopy(self.array)
		output.num_stones = self.num_stones
		return output


	def count(self, stone: chr):
		count = 0
		for x in range(self.size):
			for y in range(self.size):
				if self.array[x][y] == stone:
					count += 1
		return count


	def get_ratio(self, stone: chr):
		return self.count(stone) / self.num_stones


	def get_difference(self, stone: chr):
		return self.count(stone) - self.num_stones


	def is_done(self):
		if self.num_stones == self.size ** 2:
			return True
		if self.get_possible_actions(WHITE) or self.get_possible_actions(BLACK):
			return False
		return True


	def get_other_stone(color: chr):
		if color == WHITE:
			return BLACK
		if color == BLACK:
			return WHITE
		return BLANK