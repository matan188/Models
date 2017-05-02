import random
import numpy as np

MOVES = [30, 50, 70]
EPSILON = 0.1

class Agent:
    def __init__(self, m=10, epsilon=EPSILON, tag=0):
        self.memory = [random.choice(MOVES) for i in range(10)]
        self.m = m
        self.epsilon = epsilon
        self.tag = tag

    def update_memory(self, move):
        self.memory.pop()
        self.memory.append(move)

    def best_move(self):
        best_moves = []
        curr_max = 0
        for move_ind in range(len(MOVES)):
            move = MOVES[move_ind]
            outcome = sum([0 if (move+past)>100 else move for past in self.memory])
            if outcome == curr_max:
                best_moves.append(move)
            elif outcome > curr_max:
                best_moves = [move]
                curr_max = outcome
        return random.choice(best_moves)

    def get_history_percentage(self):
        """ Returns a dictionary with history percentages """
        dic = dict()
        dic["Low"] = self.memory.count(MOVES[0])/10.0
        dic["Medium"] = self.memory.count(MOVES[1])/10.0
        dic["High"] = self.memory.count(MOVES[2])/10.0
        dic["label"] = "Agent"
        return dic


    def play(self, opponent=None):
        if opponent is None:
            # Epsilon probability
            if random.random() < self.epsilon:
                return random.choice(MOVES)
            # Else play according to memory
            return self.best_move()
        else:
            pass
