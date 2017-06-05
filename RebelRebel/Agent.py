from RebelRebel.Person import *
import random as rand
import numpy as np
import math as math

K = 2.3
ALPHA = 0
MAX_JAIL = 100
THRESHOLD = 0.1

class Agent(Person):
    def __init__(self, legitimacy, v=7):
        super(Agent, self).__init__("a", v)
        self._hardship = rand.random()
        self._risk = rand.random()
        self._legitimacy = legitimacy
        self._active = False
        self._time_left = -1

    def decrease_time(self):
        self._time_left -= 1

    def get_time(self):
        return self._time_left

    def set_time(self, time):
        self._time_left = time

    def set_active(self, val):
        self._active = val

    def is_active(self):
        return self._active

    def get_grievance(self):
        return self._hardship*(1 - self._legitimacy)

    def set_state(self, num_active: float, num_cop: float):
        p = 1 - (1 - np.exp(-K * (num_cop/(1+num_active))))
        n = p * self._risk * math.pow(MAX_JAIL, ALPHA)
        g = self._hardship * (1 - self._legitimacy)
        if g - n > THRESHOLD:
            self._active = True
        else:
            self._active = False

    def __str__(self):
        return "A"

    def __repr__(self):
        return "'A'"

    def __float__(self):
        return 1.0 if self._active == False else 2.0