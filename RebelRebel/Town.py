import matplotlib.pyplot as plt
from matplotlib import colors
from RebelRebel.Agent import *
from RebelRebel.Cop import *
import math as math
import numpy as np


class Town:
    def __init__(self, dimension=40, density=0.7, cop_density=0.074, threshold=0.1, legitimacy=0.8,
                 k=2.3, aplha=0, j_max=10):
        self._legitimacy = legitimacy
        self._dimension = dimension
        agent_density = density-cop_density
        self._size = dimension*dimension
        self._grid = self.create_town(cop_density, agent_density)

    def create_town(self, cop_density, agent_density):
        agent_num = math.floor(self._size * agent_density)
        cop_num = math.floor(self._size * cop_density)
        empties = self._size - agent_num - cop_num

        grid = [Agent(self._legitimacy) for i in range(agent_num)]
        grid += [Cop() for i in range(cop_num)]
        grid += [-1 for i in range(empties)]

        rand.shuffle(grid)
        grid = np.array(grid)
        return grid.reshape([self._dimension, self._dimension])

    def print_town(self):
        for row in self._grid:
            print(row)

    def get_person_at_coord(self, row, col):
        return self._grid[row][col]

    def display(self):
        """ Display town map """
        to_show = [[float(self.get_person_at_coord(row, col)) for col in range(self._dimension)] for row in range(self._dimension)]
        cmap = colors.ListedColormap(['gray',  'black', 'blue', 'red'])
        plt.imshow(to_show, cmap=cmap, interpolation="nearest", extent=[0, self._dimension, 0, self._dimension])
        plt.show()

    def person_action(self, row, col):
        p = self.get_person_at_coord(row, col)
        if p == -1:
            return
        elif p.get_type() == "c":
            active_coord = []
            for i in range(row - p.get_vision(), row + p.get_vision()):
                if i >= 0 or i < self._dimension:
                    curr_p = self.get_person_at_coord(i, col)
                    if curr_p != -1 and curr_p.get_type() == "a" and curr_p.is_active():
                        active_coord.append(i, col)

            for j in range(col - p.get_vision(), col + p.get_vision()):
                if i >= 0 or i < self._dimension:
                    curr_p = self.get_person_at_coord(i, row)
                    if curr_p != -1 and curr_p.get_type() == "a" and curr_p.is_active():
                        active_coord.append(j, row)

            p.arrest()


town = Town()
town.display()