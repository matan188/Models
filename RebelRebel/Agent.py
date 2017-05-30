from RebelRebel.Person import *
import random as rand

class Agent(Person):
    def __init__(self, legitimacy, v=7):
        self._hardship = rand.random()
        self._risk = rand.random()
        self._legitimacy = legitimacy
        self._active = False

    def set_active(self, bool):
        self._active = bool

    def get_grievance(self):
        return self._hardship*(1 - self._legitimacy)

    def __str__(self):
        return "A"

    def __repr__(self):
        return "'A'"

    def __float__(self):
        return 1.0 if self._active == False else 2.0