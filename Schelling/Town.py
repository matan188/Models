import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import random
import math
from Schelling.Person import *

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
        self._empties = empties

        # populate grid with empties
        grid = [Person(-1) for i in range(empties)]

        # populate grid with types
        grid += [Person(race_ind, self._thresholds[race_ind]) for race_ind in range(len(race_nums)) for runner in range(race_nums[race_ind])]

        # Shuffle randomly and rearrange to matrix
        random.shuffle(grid)
        grid = np.array(grid)
        return grid.reshape([self._dimension, self._dimension])

    # Check if person is satisfied of its neighbors
    def check_neighbors_satisfaction(self, person, row, col):
        if self.get_person_at_coord(row, col).get_race() == -1:
            return True
        return (self.same_neighbors_perc(person, row, col)) >= person.get_threshold()

    def same_neighbors_perc(self, person, row, col):
        pers_race = person.get_race()

        neighbors_num = 0
        same_race_counter = 0
        empty_neighbors = 0

        if row - 1 >= 0:
            if self.get_person_at_coord(row-1, col).get_race() != -1:
                neighbors_num += 1
            same_race_counter += (self.get_person_at_coord(row-1, col).equal_race(pers_race))
            if col + 1 < self._dimension:
                if self.get_person_at_coord(row-1, col+1).get_race() != -1:
                    neighbors_num += 1
                same_race_counter += (self.get_person_at_coord(row-1, col+1).equal_race(pers_race))
            if col - 1 >= 0:
                if self.get_person_at_coord(row-1, col-1).get_race() != -1:
                    neighbors_num += 1
                same_race_counter += (self.get_person_at_coord(row-1, col-1).equal_race(pers_race))
        if row + 1 < self._dimension:
            if self.get_person_at_coord(row+1, col).get_race() != -1:
                neighbors_num += 1
            same_race_counter += (self.get_person_at_coord(row+1, col).equal_race(pers_race))
            if col + 1 < self._dimension:
                if self.get_person_at_coord(row+1, col+1).get_race() != -1:
                    neighbors_num += 1
                same_race_counter += (self.get_person_at_coord(row+1, col+1).equal_race(pers_race))
            if col - 1 >= 0:
                if self.get_person_at_coord(row+1, col-1).get_race() != -1:
                    neighbors_num += 1
                same_race_counter += (self.get_person_at_coord(row+1, col-1).equal_race(pers_race))
        if col + 1 < self._dimension:
            if self.get_person_at_coord(row, col+1).get_race() != -1:
                neighbors_num += 1
            same_race_counter += (self.get_person_at_coord(row, col+1).equal_race(pers_race))
        if col - 1 >= 0:
            if self.get_person_at_coord(row, col-1).get_race() != -1:
                neighbors_num += 1
            same_race_counter += (self.get_person_at_coord(row, col-1).equal_race(pers_race))

        if neighbors_num == 0:
            return 1
        return same_race_counter / float(neighbors_num)


    def run_cycle(self):
        for row in range(self._dimension):
            for col in range(self._dimension):
                if not self.check_neighbors_satisfaction(self.get_person_at_coord(row, col), row, col):
                    self.transfer(row, col)

    def run_n_cycles(self, n=10):
        for cycle in range(n):
            self.run_cycle()


    def set_person_to(self, person, row, col):
        self._grid[row][col] = person

    def transfer(self, row, col):
        rand_int = random.randint(0, len(self._empty_coords)-1)
        new_coords_ind = rand_int
        empty_row, empty_col = self._empty_coords[new_coords_ind]
        mover = self.get_person_at_coord(row, col)
        empty = self.get_person_at_coord(empty_row, empty_col)

        # swap
        self.set_person_to(mover, empty_row, empty_col)
        self.set_person_to(empty, row, col)

        self._empty_coords[new_coords_ind] = (row, col)


    def display(self):
        to_show = [[float(self.get_person_at_coord(row, col)) for col in range(self._dimension)] for row in range(self._dimension)]
        cmap = colors.ListedColormap(['gray', 'yellow', 'blue'])
        plt.imshow(to_show, cmap=cmap, interpolation="nearest", extent=[0, self._dimension, 0, self._dimension])
        plt.show()

    def plot(self):
        to_show = [[float(self.get_person_at_coord(row, col)) for col in range(self._dimension)] for row in
                   range(self._dimension)]
        cmap = colors.ListedColormap(['gray', 'yellow', 'blue'])
        print(cmap)
        plt.imshow(to_show, cmap=cmap, interpolation="nearest", extent=[0, self._dimension, 0, self._dimension])

    def show(self):
        plt.show()

    def segregation_level(self):
        segregated_persons = 0
        for row in range(self._dimension):
            for col in range(self._dimension):
                if self.same_neighbors_perc(self.get_person_at_coord(row, col), row, col) == 1:
                    segregated_persons += 1
        return segregated_persons / float(self._size - self._empties)


town = Town(dimension=5)
# print(town._grid)
print(town.segregation_level())
town.display()
town.run_n_cycles()
print(town.segregation_level())
town.display()