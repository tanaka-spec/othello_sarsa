from othello import Board
import random
import json


FOLDER_NAME = "datafile/"


class Othello_sarsa:
	def __init__(self, learning=0.5, discount=0.5, epsilon=0.5, reward=1000, reset=True):
		self.learning = learning
		self.discount = discount
		self.epsilon = epsilon
		self.qs = None
		self.reward = reward
		if reset:
			self.reset_qs()
		return


	def reset_qs(self, states=60):
		self.qs = [{} for i in range(states)]
		return


	def access_q(self, state, action):
		action = repr(action)
		if action not in self.qs[state]:
			return 0
		return self.qs[state][action]


	def update_q(self, state, action, reward, new_state, new_action):
		if action not in self.qs[state]:
			curr_val = 0
		else:
			curr_val = self.qs[state][action]
		if new_action not in self.qs[new_state]:
			new_val = 0
		else:
			new_val = self.qs[new_state][new_action]
		self.qs[state][action] = (1 - self.learning) * curr_val + self.learning * (reward + self.discount * new_val)
		return


	def place_board(self, board: Board, stone: chr):
		if not board.get_possible_actions(stone):
			return False
		if random.random() >= self.epsilon:
			state = board.num_turns
			max_val = None
			x, y = None, None
			for dest, new_board in board.get_possible_boards(stone):
				val = self.access_q(state, new_board)
				if max_val is None or max_val < val:
					max_val = val
					x, y = dest
		else:
			possible = board.get_possible_actions(stone)
			x, y = random.choice(list(possible))
		return board.place_stone(stone, x, y)


	def evaluation_function(self, board: Board, stone: chr):
		diff = board.get_difference(stone)
		if board.is_done():
			if diff < 0:
				return - self.reward
			if diff > 0:
				return self.reward
		return board.get_difference(stone)


	def load_qs(self, filename):
		try:
			with open(FOLDER_NAME + filename + '.json', "r") as read_file:
				self.qs = json.load(read_file)
		except FileNotFoundError:
			print('File Does Not Exist!')
			self.reset_qs()
		except json.decoder.JSONDecodeError:
			print('File is corrupted')
		return


	def save_qs(self, filename):
		with open(FOLDER_NAME + filename + '.json', 'w') as fout:
			json.dump(self.qs, fout)
		return
