import random
class Person:
    def __init__(self, race, threshold=100):
        """ Person's initialization """
        self._race = race
        self._threshold = threshold
        self._timer = random.randint(2, 6)

    def __str__(self):
        """ String conversion of person """
        return str(self._race)

    def __repr__(self):
        """ Return String Representation of person"""
        return str(self._race)

    def get_race(self):
        """ Returns person's race """
        return self._race

    def get_threshold(self):
        """ Returns person's threshold """
        return self._threshold

    def equal_race(self, race):
        """ Returns True if is of race race, else False"""
        return race == self._race

    def is_satisfied(self, perc_same_neighbors):
        """ Returns True if person is happy with where it lives else False """
        time_satisfaction = False
        if self._timer < 0:
            self._timer = random.randint(1, 6)
        else:
            self._timer -= 1
            time_satisfaction = True
        # return time_satisfaction and perc_same_neighbors >= self.get_threshold()
        return perc_same_neighbors >= self.get_threshold()

    def __float__(self):
        """ Implementation of float casting for plotting """
        return float(self._race)