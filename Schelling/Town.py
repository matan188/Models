import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import random
import math
from Person import *

NUM_OF_NEIGHBORS = 8.0

class Town:
    def __init__(self, dimension=30, pop_ratios=(0.45, 0.45), thresholds=(0.5, 0.5)):
        self._dimension = dimension
        self._size = dimension*dimension
        self._thresholds = thresholds
        self._grid = self.create_new_town(self._size, pop_ratios)
        self._empty_coords = self.get_coords(-1)

    def get_person_at_coord(self, row, col):
        return self._grid[row][col]

    def get_coords(self, race):
        coords_arr = []
        for row in range(self._dimension):
            for col in range(self._dimension):
                if self.get_person_at_coord(row, col).get_race() == race:
                    coords_arr.append((row, col))
        return coords_arr

    def create_new_town(self, size, pop_ratios):
        race_nums = [math.floor(ratio * (size)) for ratio in pop_ratios]
        empties = self._size - sum(race_nums)

        # populate grid with empties
        grid = [Person(-1) for i in range(empties)]

        # populate grid with types
        grid += [Person(race_ind, self._thresholds[race_ind]) for race_ind in range(len(race_nums)) for runner in range(race_nums[race_ind])]

        # Shuffle randomly and rearrange to matrix
        random.shuffle(grid)
        grid = np.array(grid)
        return grid.reshape([self._dimension, self._dimension])

    def check_neighbors_satisfaction(self, person, row, col):
        pers_race = person.get_race()

        # If empty space return true
        if pers_race == -1:
            return True

        same_race_counter = 0
        if row - 1 >= 0:
            same_race_counter += (self.get_person_at_coord(row-1, col).equal_race(pers_race))
            if col + 1 < self._dimension:
                same_race_counter += (self.get_person_at_coord(row-1, col+1).equal_race(pers_race))
            if col - 1 >= 0:
                same_race_counter += (self.get_person_at_coord(row-1, col-1).equal_race(pers_race))
        if row + 1 < self._dimension:
            same_race_counter += (self.get_person_at_coord(row+1, col).equal_race(pers_race))
            if col + 1 < self._dimension:
                same_race_counter += (self.get_person_at_coord(row+1, col+1).equal_race(pers_race))
            if col - 1 >= 0:
                same_race_counter += (self.get_person_at_coord(row+1, col-1).equal_race(pers_race))
        if col + 1 < self._dimension:
            same_race_counter += (self.get_person_at_coord(row, col+1).equal_race(pers_race))
        if col - 1 >= 0:
            same_race_counter += (self.get_person_at_coord(row, col-1).equal_race(pers_race))
        print(same_race_counter)
        return (same_race_counter/NUM_OF_NEIGHBORS) >= person.get_threshold()

    def run_cycle(self):
        for row in self._dimension:
            for col in self._dimension:
                if self.check_neighbors_satisfaction(self.get_person_at_coord(row, col), row, col) == False:
                    self.transfer(row, col)

    def transfer(self, row, col):
        pass

    def display(self):
        to_show = [[float(self.get_person_at_coord(row, col)) for col in range(self._dimension)] for row in range(self._dimension)]
        cmap = colors.ListedColormap(['gray', 'yellow', 'blue'])
        print(cmap)
        plt.imshow(to_show, cmap=cmap, interpolation="nearest", extent=[0, self._dimension, 0, self._dimension])
        plt.show()

town = Town(dimension=3)
print(town._grid)
print(town.get_coords(-1))
print(town.check_neighbors_satisfaction(town.get_person_at_coord(1,1), 1,1))
town.display()