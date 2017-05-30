from RebelRebel.Person import *

class Cop(Person):
    def __init__(self, v=7):
        super(Cop, self).__init__(v)

    def __str__(self):
        return "C"

    def __repr__(self):
        return "'C'"

    def arrest(self):
        pass

    def __float__(self):
        return 0.0
