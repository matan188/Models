import random

MOVES = [30, 50, 70]
ERROR_RATE = 0.1

class Agent:
    def __init__(self, m=10, error_rate=ERROR_RATE, tag=0):
        self.memory = [random.choice(MOVES) for i in range(10)]
        self.m = m
        self.error_rate = error_rate
        self.tag = tag

    def update_memory(self, move):
        self.memory.pop()
        self.memory.append(move)

    def best_move(self):
        best_moves = []
        curr_max = 0
        # Epsilon probability
        if random.random() < self.error_rate:
            return random.choice(MOVES)

        # Else play according to memory
        for move_ind in range(len(MOVES)):
            move = MOVES[move_ind]
            outcome = sum([0 if (move+past)>100 else move for past in self.memory])
            if outcome == curr_max:
                best_moves.append(move)
            elif outcome > curr_max:
                best_moves = [move]
                curr_max = outcome
        return random.choice(best_moves)

    def play(self, opponent=None):
        if opponent is None:
            return self.best_move()
        else:
            pass
