import matplotlib.pyplot as plt
from matplotlib import colors
from RebelRebel.Agent import *
from RebelRebel.Cop import *
import math as math
import numpy as np

ROUNDS = 100


class Town:
    def __init__(self, dimension=40, density=0.7, cop_density=0.074, threshold=0.1, legitimacy=0.8,
                 k=2.3, aplha=0, j_max=10):
        self._legitimacy = legitimacy
        self._dimension = dimension
        self._agent_num = 0
        agent_density = density-cop_density
        self._size = dimension*dimension
        self._grid = self.create_town(cop_density, agent_density)
        self._j_max = j_max
        self._jail = []
        self._curr_round = 0
        self._rebellions_level = []

    def create_town(self, cop_density, agent_density):
        """ Creates a grid according to the cop density, agent density and the dimensions of the town """
        agent_num = math.floor(self._size * agent_density)
        self._agent_num = agent_num
        cop_num = math.floor(self._size * cop_density)
        empties = self._size - agent_num - cop_num
        grid = [Agent(self._legitimacy) for i in range(agent_num)]
        grid += [Cop() for i in range(cop_num)]
        grid += [-1 for i in range(empties)]

        rand.shuffle(grid)
        grid = np.array(grid)
        return grid.reshape([self._dimension, self._dimension])

    def print_town(self):
        """ Prints the town according to the symbol of each individual. A-agent, C-cop, -1 - empty space """
        for row in self._grid:
            print(row)

    def get_person_at_coord(self, row, col):
        """ Returns the object located at row, col"""
        return self._grid[row][col]

    def display(self):
        """ Display town map with colors """
        to_show = [[float(self.get_person_at_coord(row, col)) for col in range(self._dimension)] for row in range(self._dimension)]
        cmap = colors.ListedColormap(('gray', 'black', 'blue', 'red'))
        plt.imshow(to_show, cmap=cmap, interpolation="nearest", extent=[0, self._dimension, 0, self._dimension])
        plt.show()

    def person_action(self, row, col):
        """ If the spot at row, col is empty, then returns.
        If it's an agent, it will collect all that in its vision and then will prompt the agent to be active or
        inactive.
        If it's a cop, it will collect all that in its vision and then will prompt the cop arrest a random active, """
        p = self.get_person_at_coord(row, col)
        if p == -1 or p is None:
            return
        elif p.get_type() == "c":
            active_coord = []
            for i in range(row - p.get_vision(), row + p.get_vision()+1):
                curr_row = i % self._dimension
                curr_p = self.get_person_at_coord(curr_row, col)
                if curr_p != -1 and curr_p.get_type() == "a" and curr_p.is_active():
                    active_coord.append((curr_row, col))

            for j in range(col - p.get_vision(), col + p.get_vision()+1):
                curr_col = j % self._dimension
                curr_p = self.get_person_at_coord(row, curr_col)
                if curr_p != -1 and curr_p.get_type() == "a" and curr_p.is_active():
                    active_coord.append((row, curr_col))
            self.put_in_jail(p.arrest(active_coord))
        else:
            active_count = 0.0
            cop_count = 0.0
            for i in range(row - p.get_vision(), row + p.get_vision()+1):
                curr_row = i % self._dimension
                curr_p = self.get_person_at_coord(curr_row, col)
                if curr_p != -1 and curr_p.get_type() == "a" and curr_p.is_active():
                    active_count += 1
                elif curr_p != -1 and curr_p.get_type() == "c":
                    cop_count += 1

            for j in range(col - p.get_vision(), col + p.get_vision()+1):
                curr_col = j % self._dimension
                curr_p = self.get_person_at_coord(row, curr_col)
                if curr_p != -1 and curr_p.get_type() == "a" and curr_p.is_active():
                    active_count += 1
                elif curr_p != -1 and curr_p.get_type() == "c":
                    cop_count += 1
            p.set_state(active_count, cop_count)

    def put_in_jail(self, coord):
        """ Puts an agent in jail for a certain term. """
        if coord is None:
            return
        time = rand.randint(0, self._j_max)
        agent = self.get_person_at_coord(coord[0], coord[1])
        self._grid[coord[0]][coord[1]] = -1
        agent.set_time(time)
        self._jail.append(agent)

    def run_round(self):
        """ Runs a round where each individual is asked to take an action """
        for row in range(self._dimension):
            for col in range(self._dimension):
                curr_row, curr_col = row, col
                p = self.get_person_at_coord(curr_row, curr_col)
                if p != -1:
                    new_coord = self.move_person(curr_row, curr_col)
                    curr_row, curr_col = new_coord
                self.person_action(curr_row, curr_col)
        self.let_out_of_jail()

    def let_out_of_jail(self):
        """ Remove from jail the agents that made their time """
        to_remove = []
        for ind in range(len(self._jail)):
            ag = self._jail[ind]
            ag.decrease_time()
            if ag.get_time() < 0:
                coord = rand.choice(self.get_empties())
                self._grid[coord[0]][coord[1]] = ag
                to_remove.append(ind)

        for remove_ind in range(len(to_remove)-1, -1, -1):
            del self._jail[to_remove[remove_ind]]

    def move_person(self, row, col):
        """ Move person to a random empty spot in its vision range """
        vision = self.get_person_at_coord(row, col).get_vision()
        all_coords = self.get_vision_col(vision, row, col) + self.get_vision_row(vision, row, col)
        empties = [coord for coord in all_coords if self.get_person_at_coord(coord[0], coord[1]) == -1]
        if len(empties) > 0:
            chosen = rand.choice(empties)
            self._grid[chosen[0], chosen[1]] = self.get_person_at_coord(row, col)
            self._grid[row, col] = -1
            return chosen
        return row, col

    def get_vision_col(self, vision, row, col):
        """ Returns all indexes in an individual's vertical vision """
        return [(j % self._dimension, col) for j in range(row - vision, row + vision+1) if j != row]

    def get_vision_row(self, vision, row, col):
        """ Returns all indexes in an individual's horizontal vision """
        return [(row, i % self._dimension) for i in range(col - vision, col + vision+1) if i != col]

    def get_empties(self):
        """ Returns coordinates of all empty spaces in grid """
        empties = []
        for row in range(self._dimension):
            for col in range(self._dimension):
                if self.get_person_at_coord(row, col) == -1:
                    empties.append((row, col))
        return empties

    def run_n_rounds(self, n=100):
        for i in range(n):
            self.run_round()
            if i % 10 == 0:
                curr_rebel_level = self.get_rebelliousness_level()
                # print(curr_rebel_level)
                self._rebellions_level.append(curr_rebel_level)
                # self.display()

    def get_rebelliousness_level(self):
        """ Returns the ratio of active to total agents """
        actives = 0.0
        for row in range(self._dimension):
            for col in range(self._dimension):
                p = self.get_person_at_coord(row, col)
                if p != -1 and p.get_type() == 'a' and p.is_active():
                    actives += 1
        return actives / self._agent_num

    def get_rebel_average(self):
        """ Return the rebellion level average of all the rounds performed so far """
        return np.mean(self._rebellions_level)

    def get_jail_level(self):
        """ Returns the ratio between numbe of agents in jail and total number of agents  """
        return len(self._jail) / self._agent_num


def plots(rounds=100):
    """ Plots for question 3 """
    ### Cop Densities
    cop_densities = [0, 0.025, 0.05, 0.074, 0.1, 0.15, 0.2, 0.35, 0.5]
    level_for_cops = []
    for dens in cop_densities:
        town = Town(cop_density=dens)
        town.run_n_rounds(n=rounds)
        level_for_cops.append(town.get_rebel_average())

    plt.scatter(cop_densities, level_for_cops)
    plt.title("Rebelliousness Level per Cop Density")
    plt.ylabel("Rebelliousness Level (#Actives\#Agents)")
    plt.xlabel("Cop Density")
    plt.ylim(0, 1)
    plt.xlim(xmin=0)
    plt.show()

    ### Jail Terms
    max_jail_term = [0, 25, 50, 75, 100]
    level_for_jail_time = []
    for j in max_jail_term:
        town = Town(j_max=j)
        town.run_n_rounds(n=rounds)
        level_for_jail_time.append(town.get_rebel_average())
    plt.scatter(max_jail_term, level_for_jail_time)
    plt.title("Rebelliousness Level per Max Jail Term")
    plt.ylabel("Rebelliousness Level (#Actives\#Agents)")
    plt.xlabel("Max Jail Term")
    plt.ylim(0, 1)
    plt.xlim(xmin=0)
    plt.show()

    ### Legitimacy Levels
    legitimacy_levels = [0, 0.25, 0.5, 0.75, 1]
    level_per_legit =[]
    for leg in legitimacy_levels:
        town = Town(legitimacy=leg)
        town.run_n_rounds(n=rounds)
        level_per_legit.append(town.get_rebel_average())
    plt.scatter(legitimacy_levels, level_per_legit)
    plt.title("Rebelliousness Level per Legitimacy Level")
    plt.ylabel("Rebelliousness Level (#Actives\#Agents)")
    plt.xlabel("Legitimacy Level")
    plt.ylim(0, 1)
    plt.xlim(xmin=0)
    plt.show()


def full_factorial():
    """ Full Factorial for question 4 and 5 """
    cop_densities = [0, 0.025, 0.05, 0.1, 0.2, 0.35]
    max_jail_term = [0, 25, 50, 75, 100]
    legitimacy_levels = [0, 0.25, 0.5, 0.75, 1]

    for dens in cop_densities:
        for jail in max_jail_term:
            for leg in legitimacy_levels:
                town = Town(cop_density=dens, j_max=jail, legitimacy=leg)
                town.run_n_rounds()
                print(dens, jail, leg, town.get_rebel_average())


# plots()
# full_factorial()

# town = Town(cop_density=0.0)
# print(town.get_rebelliousness_level())
# town.run_n_rounds()
# print(town.get_rebelliousness_level())