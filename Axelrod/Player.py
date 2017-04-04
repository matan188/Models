import random as rand

class Player:
    def __init__(self, bold_level=None, venge_level=None):
        if bold_level == None:
            self._boldness_level = rand.randint(0, 7)
            self._vengefulness_level = rand.randint(0, 7)
            self._score = 0
        else:
            pass

    def update_score(self, points):
        self._score += points

    def get_boldness_level(self):
        return self._boldness_level

    def is_defect(self):
        s = rand.random()
        bold = self._boldness_level / 7.0
        return  bold > s

    def get_vengefulness_level(self):
        return self._vengefulness_level

    def is_punish(self):
        v = rand.random()
        veng = self._vengefulness_level / 7.0
        return veng > v

    def get_score(self):
        return self._score
