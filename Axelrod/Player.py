import random as rand

MUTATION_PROB = 0.01

class Player:
    def __init__(self, boldness=None, venge=None):
        if boldness == None:
            self._boldness_binary = [rand.randint(0, 1), rand.randint(0, 1), rand.randint(0, 1)]
            self._vengefulness_binary = [rand.randint(0, 1), rand.randint(0, 1), rand.randint(0, 1)]
        else:
            new_bold = []
            new_venge = []
            for i in range(len(boldness)):
                randi = rand.random()
                if randi < MUTATION_PROB:
                    new_bold.append(1 - boldness[i])
                else:
                    new_bold.append(boldness[i])
            for j in range(len(venge)):
                if rand.random() < MUTATION_PROB:
                    new_venge.append(1 - venge[j])
                else:
                    new_venge.append(venge[j])
            self._boldness_binary = new_bold
            self._vengefulness_binary = new_venge
        self._score = 0

    def init_score(self):
        self._score = 0

    def update_score(self, points):
        self._score += points

    def get_boldness_level(self):
        level = 0
        length = len(self._vengefulness_binary)
        for i in range(length):
            level += self._boldness_binary[i] * pow(2, length - i - 1)
        return level

    def boldness_probability(self):
        return self.get_boldness_level() / 7.0

    def is_defect(self):
        bold_threshold = rand.random()
        return self.boldness_probability() > bold_threshold

    def get_vengefulness_level(self):
        level = 0
        length = len(self._vengefulness_binary)
        for i in range(length):
            level += self._vengefulness_binary[i] * pow(2, length-i-1)
        return level

    def vengeance_probability(self):
        return self.get_vengefulness_level() / 7.0

    def is_punish(self):
        veng_threshold = rand.random()
        return veng_threshold < self.vengeance_probability()

    def get_score(self):
        return self._score
