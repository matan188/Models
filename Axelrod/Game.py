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

    def reinit_players(self):
        length = len(self._players)
        self._players = [Player() for i in range(length)]

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
        bests = []
        medium = []
        new_players = []
        for player in self._players:
            if player.get_score() > average + std:
                bests.append(player)
                for i in range(2):
                    new_players.append(Player(player._boldness_binary, player._vengefulness_binary))
            elif player.get_score() > average - std and player.get_score() < average + std:
                medium.append(player)
                new_players.append(Player(player._boldness_binary, player._vengefulness_binary))

        if len(new_players)<20:
            for player in bests:
                new_players.append(Player(player._boldness_binary, player._vengefulness_binary))
        if len(new_players)<20:
            for player in medium:
                new_players.append(Player(player._boldness_binary, player._vengefulness_binary))
        if len(new_players) == 0:
            self.init_scores()
            return
        self._players = new_players[:20]

    def init_scores(self):
        for p in self._players:
            p.init_score()

    def run_n_generations(self, n=100):
        for curr_gen in range(n):
            self.run_round()
            self.print_score()
            self.new_generation()
            self.count += 1

    def run(self, times=5, generations=100):
        self.count = 0
        for i in range(times):
            self.run_n_generations(generations)
            self.reinit_players()
        print(self.count)

    def print_boldness(self):
        print([player.get_boldness_level() for player in self._players])

    def print_vengeance(self):
        print([player.get_vengefulness_level() for player in self._players])

    def print_score(self):
        print([player.get_score() for player in self._players])

    def split_to_bins(self):
        pass

game = Game()
game.run()