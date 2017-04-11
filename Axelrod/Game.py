from Axelrod.Player import *
import random as rand
import numpy as np
import matplotlib.pyplot as plt
import math

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
        self.pop_stats = []
        self.bins = dict()
        self.post_bins = dict()
        self.cycle_bold_averages = []
        self.cycle_venge_averages = []

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

    def update_initial_stats(self):
        boldness_avg = np.mean([player.get_boldness_level() for player in self._players])
        venge_avg = np.mean([player.get_vengefulness_level() for player in self._players])
        self.pop_stats.append((boldness_avg, venge_avg))

    def run_n_generations(self, n=100):
        for curr_gen in range(n):
            self.update_initial_stats()
            self.run_round()
            self.new_generation()

    def run(self, times=5, generations=100):
        for i in range(times):
            self.run_n_generations(generations)
            self.update_cycle_averages()
            self.reinit_players()

    def update_cycle_averages(self):
        bold_avg = np.mean([player.get_boldness_level() for player in self._players])
        venge_avg = np.mean([player.get_vengefulness_level() for player in self._players])
        self.cycle_bold_averages.append(bold_avg)
        self.cycle_venge_averages.append(venge_avg)

    def print_boldness(self):
        print([player.get_boldness_level() for player in self._players])

    def print_vengeance(self):
        print([player.get_vengefulness_level() for player in self._players])

    def print_score(self):
        print([player.get_score() for player in self._players])

    def pop_to_bins(self):
        for ind in range(len(self.pop_stats)):
            if (ind+1) % 100 == 0:  # ignore when starting new round of generations
                continue
            stat = self.pop_stats[ind]
            post_stat =  self.pop_stats[ind+1]
            b = math.floor(stat[0]) if math.floor(stat[0]) < 7 else 6
            v = math.floor(stat[1]) if math.floor(stat[1]) < 7 else 6
            if (b, v) in self.bins:
                self.bins[(b, v)].append(stat)
                self.post_bins[(b, v)].append(post_stat)
            else:
                self.bins[(b, v)] = [stat]
                self.post_bins[(b, v)] = [post_stat]

    def bins_to_arrow_tuples(self):
        arrows = []
        for key in self.bins:
            bold = []
            venge = []
            bold_next = []
            venge_next = []
            for ind in range(len(self.bins[key])):
                bold.append(self.bins[key][ind][0])
                venge.append(self.bins[key][ind][1])
                bold_next.append(self.post_bins[key][ind][0])
                venge_next.append(self.post_bins[key][ind][1])
            b = np.mean(bold)
            v = np.mean(venge)
            db = b-np.mean(bold_next)
            dv = v-np.mean(venge_next)
            arrow = (b, v, db, dv)
            arrows.append(arrow)
        return arrows

    def display(self):
        arrows = self.bins_to_arrow_tuples()
        # x = np.arange(8)
        # y = x
        # plt.plot(x, y)
        ax = plt.gca()
        for arr in arrows:
            patch = plt.Arrow(arr[0], arr[1], arr[2], arr[3], width=0.3)
            ax.add_patch(patch)
        plt.scatter(self.cycle_bold_averages, self.cycle_venge_averages, edgecolors='black')
        plt.show()


game = Game()
game.run()
game.pop_to_bins()
game.display()

