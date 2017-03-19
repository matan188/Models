
class Person:
    def __init__(self, race, threshold=100):
        self._race = race
        self._threshold = threshold

    def __str__(self):
        return str(self._race)

    def __repr__(self):
        return str(self._race)

    def get_race(self):
        return self._race

    def get_threshold(self):
        return self._threshold

    def equal_race(self, race):
        return race == self._race

    def __float__(self):
        return float(self._race)