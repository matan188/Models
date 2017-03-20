import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import random
import math
from Schelling.Person import *


class Town:

    def __init__(self, dimension=30, pop_ratios=(0.45, 0.45), thresholds=(0.5, 0.5)):
        """ Initialize town object """
        self.check_arguments(dimension, pop_ratios, thresholds)
        self._race_num = len(pop_ratios)
        self._dimension = dimension
        self._size = dimension*dimension
        self._thresholds = thresholds
        self._grid = self.create_new_town(self._size, pop_ratios)
        self._empty_coords = self.get_coords(-1)

    def check_arguments(self, dimension, pop_ratios, thresholds):
        assert dimension > 0
        assert len(pop_ratios) == len(thresholds)
        assert sum(pop_ratios) <= 1


    def get_person_at_coord(self, row, col):
        """ Returns the person at coordinate (row,col) """
        if row < 0 or row >= self._dimension or col < 0 or col >= self._dimension:
            return None
        return self._grid[row][col]

    def get_coords(self, race):
        """ Returns an array with all the coordinates of people of race race """
        coords_arr = []
        for row in range(self._dimension):
            for col in range(self._dimension):
                if self.get_person_at_coord(row, col).get_race() == race:
                    coords_arr.append((row, col))
        return coords_arr

    def create_new_town(self, size, pop_ratios):
        """ Creates a new town with population placed randomly according to ratios """
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

    def check_neighbors_satisfaction(self, person, row, col):
        """ Check if person is satisfied of its neighbors """
        if self.get_person_at_coord(row, col).get_race() == -1:
            return True
        return person.is_satisfied(self.same_neighbors_perc(row, col))

    def same_neighbors_perc(self, row, col):
        """ Returns the percentage of neighbors that are of same race as person """
        pers_race = self.get_person_at_coord(row, col).get_race()
        neighbors_num = 0
        same_race_counter = 0

        for prev_row in range(row - 1, row + 2):
            for prev_col in range(col-1, col + 2):
                if prev_row != row or prev_col != col:
                    curr = self.get_person_at_coord(prev_row, prev_col)
                    if curr == None:
                        continue
                    same_race_counter += 1 if curr.equal_race(pers_race) else 0
                    neighbors_num += 1 if curr.get_race() != -1 else 0

        if neighbors_num == 0:  # If no neighbors, person is happy
            return 1
        return same_race_counter / float(neighbors_num)

    def run_cycle(self):
        """ A cycle means going through all the population and transfer to random empty space if needed """
        someone_transferred = False
        for row in range(self._dimension):
            for col in range(self._dimension):
                if not self.check_neighbors_satisfaction(self.get_person_at_coord(row, col), row, col):
                    self.transfer(row, col)
                    someone_transferred = True
        return someone_transferred

    def run_n_cycles(self, n=10):
        """ Run n cycles or until convergence """
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
        """ Display town map """
        to_show = [[float(self.get_person_at_coord(row, col)) for col in range(self._dimension)] for row in range(self._dimension)]
        cmap = colors.ListedColormap(['gray', 'yellow', 'blue', 'green', 'orange', 'pink', 'red'][0:self._race_num+1])
        plt.imshow(to_show, cmap=cmap, interpolation="nearest", extent=[0, self._dimension, 0, self._dimension])
        plt.show()

    # Plot town map
    def plot(self):
        to_show = [[float(self.get_person_at_coord(row, col)) for col in range(self._dimension)] for row in
                   range(self._dimension)]
        cmap = colors.ListedColormap(['gray', 'yellow', 'blue'])
        print(cmap)
        plt.imshow(to_show, cmap=cmap, interpolation="nearest", extent=[0, self._dimension, 0, self._dimension])

    # Show plot
    def show(self):
        plt.show()

    # Calculate town's segregation level
    def segregation_level(self):
        """ Returns town's segregation level (Number of persons surrounded uniquely by persons of same type """
        segregated_persons = 0
        for row in range(self._dimension):
            for col in range(self._dimension):
                if self.same_neighbors_perc(row, col) == 1:
                    segregated_persons += 1
        return segregated_persons / float(self._size - self._empties), segregated_persons


town = Town(dimension=10, pop_ratios=(0.40, 0.40), thresholds=(0.5, 0.5))
print(town.segregation_level())
town.display()
print(town.run_n_cycles(30))
print(town.segregation_level())
town.display()