from Axelrod.Player import *
import random as rand
import numpy as np

TEMPTATION = 3
PUNISHMENT = -9
HURT = -1
ENFORCEMENT = -2

class Game:
    # TODO change default to 40
    def __init__(self, num_players=20):
        self._players = [Player() for i in range(num_players)]
        self.T = TEMPTATION
        self.P = PUNISHMENT
        self.H = HURT
        self.E = ENFORCEMENT

    def run_round(self):
        for player in self._players:
            if player.is_defect():
                player.update_score(TEMPTATION)
                for other in self._players:
                    if other != player:
                        other.update_score(self.H)
                        if other.is_punish():
                            player.update_score(PUNISHMENT)
                            other.update_score(ENFORCEMENT)

    def new_generation(self):
        scores = np.array([player.get_score() for player in self._players])
        average = scores.mean()
        std = scores.std()
        new_players = []
        for player in self._players:
            if player.get_score() > average + std:
                new_players.append(Player(player.get_boldness_level(), player.get_vengefulness_level()))


    def print_score(self):
        print([player.get_score() for player in self._players])

game = Game()
game.print_score()
game.run_round()
game.print_score()
game.new_generation()



