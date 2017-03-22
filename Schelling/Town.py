import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import random
import math
from Schelling.Person import *


class Town:

    def __init__(self, dimension=30, pop_ratios=(0.45, 0.45), thresholds=(0.5, 0.5)):
        """ Initialize town object
        :param dimension: the length of each axis of the town
        :param pop_ratios: ratio of population of each race. sum should be <=1
        :param thresholds: bottom limit of same race neighbors. each threshold should be >=0 and <=1"""
        self.check_arguments(dimension, pop_ratios, thresholds)
        self._race_num = len(pop_ratios)
        self._dimension = dimension
        self._grid = self.create_new_town(self.size(), pop_ratios, thresholds)
        self._empty_coords = self.get_coords(-1)
        self._empties = 0

    def size(self):
        """ :return town's size """
        return self._dimension * self._dimension

    def check_arguments(self, dimension, pop_ratios, thresholds):
        """ Assert given arguments conform to API
        :param dimension: the length of each axis of the town
        :param pop_ratios: ratio of population of each race. sum should be <=1
        :param thresholds: bottom limit of same race neighbors. each threshold should be >=0 and <=1"""
        assert dimension > 0
        assert len(pop_ratios) == len(thresholds)
        assert sum(pop_ratios) <= 1
        thresh_check = [thresh for thresh in thresholds if thresh < 0 or thresh > 1]
        assert len(thresh_check) == 0  # Checks no threshold is below 0 or above 1

    def get_person_at_coord(self, row, col):
        """ get person at grid[row][col]
        :param row: row index
        :param col: col index
        :return the person at coordinate (row,col) """
        if row < 0 or row >= self._dimension or col < 0 or col >= self._dimension:
            return None
        return self._grid[row][col]

    def get_coords(self, race):
        """ :param race: which race to take in account
        :return an array with all the coordinates of people of race race """
        coords_arr = []
        for row in range(self._dimension):
            for col in range(self._dimension):
                if self.get_person_at_coord(row, col).get_race() == race:
                    coords_arr.append((row, col))
        return coords_arr

    def create_new_town(self, size, pop_ratios, thresholds):
        """ Creates a new town with population placed randomly according to ratios
            :param size: # of cells in town. (dimension*dimension)
            :param pop_ratios: ratio of population of each race. sum should be <=1
            :param thresholds: bottom limit of same race neighbors. each threshold should be >=0 and <=1
            :return 2D array representing a town populated with persons """
        race_nums = [math.floor(ratio * (size)) for ratio in pop_ratios]
        empties = self.size() - sum(race_nums)
        self._empties = empties

        # populate grid with empties
        grid = [Person(-1) for i in range(empties)]

        # populate grid with types
        grid += [Person(race_ind, thresholds[race_ind]) for race_ind in range(len(race_nums)) for runner in range(race_nums[race_ind])]

        # Shuffle randomly and rearrange to matrix
        random.shuffle(grid)
        grid = np.array(grid)
        return grid.reshape([self._dimension, self._dimension])

    def check_neighbors_satisfaction(self, person, row, col):
        """ :return True if person is satisfied\wants to move else False """
        if self.get_person_at_coord(row, col).get_race() == -1:
            return True
        return person.is_satisfied(self.same_neighbors_perc(row, col))

    def same_neighbors_perc(self, row, col):
        """ :return the percentage of neighbors that are of same race as person """
        pers_race = self.get_person_at_coord(row, col).get_race()
        neighbors_num = 0
        same_race_counter = 0

        for prev_row in range(row - 1, row + 2):
            for prev_col in range(col-1, col + 2):
                if prev_row != row or prev_col != col:
                    curr = self.get_person_at_coord(prev_row, prev_col)
                    if curr == None:
                        continue
                    if curr.equal_race(pers_race):
                        same_race_counter += 1
                    if curr.get_race() != -1:
                        neighbors_num += 1

        if neighbors_num == 0:  # If no neighbors, person is happy
            return 1
        return same_race_counter / float(neighbors_num)

    def get_neighbors_array(self, row, col):
        neighbors = []
        for prev_row in range(row - 1, row + 2):
            for prev_col in range(col-1, col + 2):
                if prev_row != row or prev_col != col:
                    curr = self.get_person_at_coord(prev_row, prev_col)
                    if curr == None:
                        continue
                    neighbors.append(curr.get_race())
        return neighbors

    def run_cycle(self):
        """ A cycle means going through all the population and transfer to random empty space if needed
            :return True if a person was transferred, else False"""
        someone_transferred = False
        for row in range(self._dimension):
            for col in range(self._dimension):
                if not self.check_neighbors_satisfaction(self.get_person_at_coord(row, col), row, col):
                    self.transfer(row, col)
                    someone_transferred = True
        return someone_transferred

    def run_n_cycles(self, n=10):
        """ Run n cycles or until convergence
            :return Number of cycles that ran"""
        cycles = 0
        for cycle in range(n):
            cycles += 1
            if not self.run_cycle():
                return cycles
        return cycles

    def set_person_to(self, person, row, col):
        """ Set person to coordinate """
        self._grid[row][col] = person

    def transfer(self, row, col):
        """ Swap person with random empty space using the empty spaces coordinates array """
        # Pick coordination of one of empties
        rand_int = random.randint(0, len(self._empty_coords)-1)
        empty_row, empty_col = self._empty_coords[rand_int]

        # Get moving person and empty "person"
        mover = self.get_person_at_coord(row, col)
        empty = self.get_person_at_coord(empty_row, empty_col)

        # swap
        self.set_person_to(mover, empty_row, empty_col)
        self.set_person_to(empty, row, col)

        # sets new coordination in empty coords array
        self._empty_coords[rand_int] = (row, col)

    def display(self):
        """ Display town map """
        to_show = [[float(self.get_person_at_coord(row, col)) for col in range(self._dimension)] for row in range(self._dimension)]
        cmap = colors.ListedColormap(['gray', 'yellow', 'blue', 'green', 'orange', 'pink', 'red'][0:self._race_num+1])
        plt.imshow(to_show, cmap=cmap, interpolation="nearest", extent=[0, self._dimension, 0, self._dimension])
        plt.show()

    def segregation_level(self):
        """ :return town's segregation level (Number of persons surrounded uniquely by persons of same type """
        segregated_persons = 0
        for row in range(self._dimension):
            for col in range(self._dimension):
                if self.same_neighbors_perc(row, col) == 1:
                    segregated_persons += 1
        return segregated_persons / float(self.size() - self._empties), segregated_persons

    def satisfaction_level(self):
        """ :return the percentage of persons satisfied by their neighbors (according to their threshold) """
        satisfied_persons = 0
        for row in range(self._dimension):
            for col in range(self._dimension):
                if self.get_person_at_coord(row, col).neighbors_satisfaction(self.same_neighbors_perc(row, col)):
                    satisfied_persons += 1
        return satisfied_persons / float(self.size() - self._empties), satisfied_persons

    def run_experiment(self):
        pass


def thresholds_experiment(dimension=30, pop_ratios=(0.4, 0.4)):
    thresholds = [0, 0.1, 0.2, 0.33, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    segregation_level = []
    satisfaction_level = []
    cycles_num = []
    for i in range(len(thresholds)):
        curr_thresh = thresholds[i]
        curr_town = Town(dimension, pop_ratios, thresholds=[curr_thresh, curr_thresh])
        cycles_num.append(curr_town.run_n_cycles(30))
        segregation_level.append(curr_town.segregation_level()[0])
        satisfaction_level.append(curr_town.satisfaction_level()[0])
        if curr_thresh == 0.3:
            curr_town.display()

    fig = plt.figure()
    satisfaction_plot = fig.add_subplot(221)
    satisfaction_plot.plot([100 * value for value in thresholds], [100 * value for value in satisfaction_level])
    satisfaction_plot.set_ylim([0, 100])
    satisfaction_plot.set_xlabel("Threshold Value")
    satisfaction_plot.set_ylabel("Satisfaction Level %")

    segregation_plot = fig.add_subplot(223)
    segregation_plot.set_ylim([0, 100])
    segregation_plot.plot([100 * value for value in thresholds], [100 * value for value in segregation_level])
    segregation_plot.set_xlabel("Threshold Value")
    segregation_plot.set_ylabel("Segregation Level %")

    cycles_to_convergence = fig.add_subplot(122)
    cycles_to_convergence.plot([100 * value for value in thresholds], cycles_num)
    cycles_to_convergence.set_ylim([0, 30])
    cycles_to_convergence.set_xlabel("Threshold Value")
    cycles_to_convergence.set_ylabel("# of Cycles to Convergence")

    plt.show()


thresholds_experiment(dimension=30, pop_ratios=(0.40, 0.40))


# town = Town(dimension=30, pop_ratios=(0.40, 0.40), thresholds=(0.5, 0.5))
# print(town.satisfaction_level())
# town.display()
# print('cycles', town.run_n_cycles(30))
# print('segregation', town.segregation_level())
# print('satisfaction', town.satisfaction_level())
# town.display()
