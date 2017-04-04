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
        for i in range(len(self._boldness_binary)):
            level += self._boldness_binary[i] * pow(2, i)
        return level

    def is_defect(self):
        s = rand.random()
        bold = self.get_boldness_level() / 7.0
        return  bold > s

    def get_vengefulness_level(self):
        level = 0
        for i in range(len(self._vengefulness_binary)):
            level += self._vengefulness_binary[i] * pow(2, i)
        return level

    def is_punish(self):
        v = rand.random()
        veng = self.get_vengefulness_level() / 7.0
        return veng > v

    def get_score(self):
        return self._score
