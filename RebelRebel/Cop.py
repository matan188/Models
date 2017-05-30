from RebelRebel.Person import *
import random as rand

class Cop(Person):
    def __init__(self, v=7):
        super(Cop, self).__init__("c", v)

    def __str__(self):
        return "C"

    def __repr__(self):
        return "'C'"

    def arrest(self, active_indices_in_vision):
        return rand.choice(active_indices_in_vision)

    def __float__(self):
        return 0.0
