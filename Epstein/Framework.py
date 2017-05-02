import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import plotly.figure_factory as ff
from Epstein.Agent import  *


class Framework:
    def __init__(self, num_agents=200.0):
        self.num_agents = num_agents
        self.agents = [Agent() for ag in range(int(num_agents))]
        self.move_percentages = []

    def round(self):
        reagents = []
        while len(self.agents) > 1:
            idx1 = random.randrange(0, len(self.agents))
            p1 = self.agents.pop(idx1)
            idx2 = random.randrange(0, len(self.agents))
            p2 = self.agents.pop(idx2)
            reagents.append(p1)
            reagents.append(p2)
            move1 = p1.play()
            move2 = p2.play()
            p1.update_memory(move2)
            p2.update_memory(move1)
        self.agents = reagents

    def update_percentages(self):
        self.move_percentages.append(self.get_moves_percentages())

    def get_moves_percentages(self):
        moves_track = dict({30: 0, 50: 0, 70: 0})

        for ag in self.agents:
            moves_track[ag.best_move()] += 1
        tup = (moves_track[30] / self.num_agents, moves_track[50] / self.num_agents, moves_track[70] / self.num_agents)
        return tup

    def get_memory_percentages(self):
        moves_track = dict({30: 0, 50: 0, 70: 0})

        for ag in self.agents:
            for mem in ag.memory:
                moves_track[mem] += 1
        tup = (moves_track[30] / (self.num_agents*10), moves_track[50] / (self.num_agents*10),
               moves_track[70] / (self.num_agents*10))
        return tup

    def run_n_rounds(self, n=100):
        print("memory percentages:",self.get_memory_percentages())
        self.update_percentages()
        print("{}: {}".format(0, self.move_percentages[0]))
        for i in range(n):
            self.round()
            self.update_percentages()
            percentages = self.move_percentages[-1]
            if percentages[0] > percentages[1] or percentages[2] > percentages[1]:
                print("Fractious")
                print(percentages)
                self.display_players()
        print("{}: {}".format(i+1, self.move_percentages[i]))

    def run_simulations(self, num=20):
        pass

    def display_players(self):
        raw_data = []
        for agent in self.agents:
            raw_data.append(agent.get_history_percentage())

        data = [{
            'type': 'scatterternary',
            'mode': 'markers',
            'a': [i for i in map(lambda x: x['High'], raw_data)],
            'b': [i for i in map(lambda x: x['Medium'], raw_data)],
            'c': [i for i in map(lambda x: x['Low'], raw_data)],
            'text': [i for i in map(lambda x: x['label'], raw_data)],
            'marker': {
                'symbol': 100,
                'color': '#000000',
                'size': 5,
                'line': {'width': 1}
            },
        }]

        layout = {
            'ternary': {
                'sum': 1,
                'aaxis': self.make_axis('High', 0),
                'baxis': self.make_axis('<br>Medium', 45),
                'caxis': self.make_axis('<br>Low', -45)
            },
            'annotations': [{
                'showarrow': False,
                'text': 'Simple Ternary Plot with Markers',
                'x': 0.5,
                'y': 1.3,
                'font': {'size': 15}
            }]
        }

        fig = {'data': data, 'layout': layout}
        py.plot(fig)

    def make_axis(self, title, tickangle):
        return {
            'title': title,
            'titlefont': {'size': 20},
            'tickangle': tickangle,
            'tickfont': {'size': 15},
            'tickcolor': 'rgba(0,0,0,0)',
            'ticklen': 5,
            'showline': True,
            'showgrid': True
        }

    def display_first_table(self):
        memory = self.get_memory_percentages()
        moves = self.get_moves_percentages()
        table_data = [["", "Low", "Medium", "High"],
                 ["Memory distribution", memory[0], memory[1], memory[2]],
                 ["Moves distribution", moves[0], moves[1], moves[2]]]
        table = ff.create_table(table_data)
        py.plot(table)


# fram = Framework(num_agents=100)
# print(fram.get_memory_percentages())
# print(fram.get_moves_percentages())
# fram.display_first_table()
# fram.display_players()
# fram.run_n_rounds(20)
# print(fram.move_percentages[-1])
# fram.display_players()


ag = Agent()
print(ag.memory)
print(ag.get_history_percentage())
print(ag.get_move_gains())


