from collections import defaultdict
from othello import Board
import random


class Othello_sarsa:
	def __init__(self, learning=0.5, discount=0.5, epsilon=0.1, reward=100):
		self.learning = learning
		self.discount = discount
		self.epsilon = epsilon
		self.qs = None
		self.reward = reward
		self.reset_qs()
		return


	def reset_qs(self, states=60):
		self.qs = [defaultdict(lambda: 0) for i in range(states)]
		return


	def update_q(state, action, reward, new_state, new_action):
		self.qs[state][action] = (1 - self.learning) * qs[state][action] 
		+ self.learning * (reward + self.discount * qs[new_state][new_action])
		return


	def place_board(board: Board, stone: chr):
		if random.random() >= self.epsilon:
			state = board.num_stones - 4
			max_val = None
			x, y = None
			for dest, new_board in get_possible_boards(stone):
				val = qs[state][new_board]
				if max_val is None or max_val < val:
					max_val = val
					x, y = dest
		else:
			possible = board.get_possible_actions(stone)
			x, y = random.choice(possible)

		return board.place_stone(stone, x, y)


	def evaluation_function(board: Board, stone: chr):
		if board.is_done():
			ratio = board.get_ratio(stone)
			if ratio == 0.5:
				return 0
			elif ratio < 0.5:
				return -1 * ratio * self.reward
			elif ratio > 0.5:
				return ratio * self.reward
		return board.get_difference(stone)