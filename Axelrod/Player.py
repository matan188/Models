import random as rand

class Player:
    def __init__(self, bold_level=None, venge_level=None):
        if bold_level == None:
            self._boldness_binary = [rand.randint(0, 1), rand.randint(0, 1), rand.randint(0, 1)]
            self._vengefulness_binary = [rand.randint(0, 1), rand.randint(0, 1), rand.randint(0, 1)]
            self._score = 0
        else:
            pass

    def update_score(self, points):
        self._score += points

    def get_boldness_level(self):
        level = 0
        length = len(self._vengefulness_binary)
        for i in range(length):
            level += self._boldness_binary[i] * pow(2, length - i - 1)
        return level

    def get_boldness(self):
        return self.get_boldness_level() / 7.0

    def is_defect(self):
        bold_threshold = rand.random()
        return self.get_boldness() > bold_threshold

    def get_vengefulness_level(self):
        level = 0
        length = len(self._vengefulness_binary)
        for i in range(length):
            level += self._vengefulness_binary[i] * pow(2, length-i-1)
        return level

    def get_vengefulness(self):
        return self.get_vengefulness_level() / 7.0

    def is_punish(self):
        veng_threshold = rand.random()
        return self.get_vengefulness() > veng_threshold

    def get_score(self):
        return self._score
