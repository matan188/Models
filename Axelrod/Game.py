from Axelrod.Player import *
import random as rand
import numpy as np

TEMPTATION = 3
PUNISHMENT = -9
HURT = -1
ENFORCEMENT = -2
METAPUNISHMENT = 0

class Game:
    # TODO change default to 40
    def __init__(self, num_players=20):
        self._players = [Player() for i in range(num_players)]
        self.T = TEMPTATION
        self.P = PUNISHMENT
        self.H = HURT
        self.E = ENFORCEMENT
        self.M = 0

    def run_round(self):
        """ Goes through each player, checks if defects and activate other players accordingly """
        s = rand.random()
        for player in self._players:
            if player.boldness_probability() > s:
                player.update_score(TEMPTATION)
                got_punished = False
                for other in self._players:
                    if other != player:
                        other.update_score(self.H)
                        if rand.random() < s:
                            if other.is_punish():
                                if not got_punished:
                                    got_punished = True
                                    player.update_score(PUNISHMENT)
                                other.update_score(ENFORCEMENT)
                            elif self.M != 0:
                                got_meta = False
                                for meta_punisher in self._players:
                                    if meta_punisher != other and meta_punisher != player:
                                        if meta_punisher.is_punish():
                                            if got_meta:
                                                other.update_score(self.M)
                                                got_meta = True
                                            meta_punisher.update_score(self.E)


    def new_generation(self):
        scores = np.array([player.get_score() for player in self._players])
        average = scores.mean()
        std = scores.std()
        new_players = []
        for player in self._players:
            if player.get_score() > average + std:
                for i in range(2):
                    new_players.append(Player(player._boldness_binary, player._vengefulness_binary))
            elif player.get_score() > average - std and player.get_score() < average + std:
                new_players.append(Player(player._boldness_binary, player._vengefulness_binary))

        self._players = new_players[:20]

    def print_boldness(self):
        print([player.get_boldness_level() for player in self._players])

    def print_vengeance(self):
        print([player.get_vengefulness_level() for player in self._players])

    def print_score(self):
        print([player.get_score() for player in self._players])

    def split_to_bins(self):
        pass

game = Game()
game.print_boldness()
game.print_vengeance()
game.print_score()
game.run_round()
game.print_score()
game.new_generation()
print(len(game._players))
game.print_boldness()
