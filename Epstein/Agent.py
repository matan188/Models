import random
import numpy as np

MOVES = [30, 50, 70]
EPSILON = 0.1

class Agent:
    def __init__(self, m=10, epsilon=EPSILON, tag=0):
        self.memory = []
        # self.memory.append([30 if tag==1 else 70 for i in range(10)])
        # self.memory.append([70 if tag==0 else 30 for i in range(10)]) #random.choice(MOVES)
        self.memory.append([50 if tag == 0 else 30 for i in range(10)])
        self.memory.append([50 if tag == 1 else 70 for i in range(10)])  # random.choice(MOVES)
        self.m = m
        self.epsilon = epsilon
        self.tag = tag

    def update_memory(self, move, tag=0):
        self.memory[tag].pop(0)
        self.memory[tag].append(move)

    def best_move(self, tag=0):
        best_moves = []
        curr_max = 0
        for move_ind in range(len(MOVES)):
            move = MOVES[move_ind]
            outcome = sum([0 if (move+past)>100 else move for past in self.memory[tag]])
            if outcome == curr_max:
                best_moves.append(move)
            elif outcome > curr_max:
                best_moves = [move]
                curr_max = outcome
        return random.choice(best_moves)

    def get_move_gains(self):
        gains = []
        for move_ind in range(len(MOVES)):
            move = MOVES[move_ind]
            gains.append(sum([0 if (move+past)>100 else move for past in self.memory]))
        return gains

    def get_tag(self):
        return self.tag

    def get_history_percentage(self, tag=0):
        """ Returns a dictionary with history percentages """
        dic = dict()
        dic["Low"] = self.memory[tag].count(MOVES[0])/10.0
        dic["Medium"] = self.memory[tag].count(MOVES[1])/10.0
        dic["High"] = self.memory[tag].count(MOVES[2])/10.0
        dic["label"] = "Agent {}".format(self.tag)
        return dic

    def play(self, tag=0):
        # Epsilon probability
        if random.random() < self.epsilon:
            return random.choice(MOVES)
        # Else play according to memory
        return self.best_move(tag=tag)
