import plotly.plotly as py
import plotly.graph_objs as go
import plotly
from Epstein.Agent import  *


class Framework:
    def __init__(self, num_agents=200.0):
        self.num_agents = num_agents
        self.agents = [Agent() for ag in range(int(num_agents))]
        self.move_percentages = []

    def round(self):
        reagents = []
        moves_track = dict({30: 0, 50: 0, 70: 0})
        while len(self.agents) > 0:
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
            moves_track[move1] += 1
            moves_track[move2] += 1
        self.agents = reagents
        print(moves_track)
        print(sum([moves_track[30], moves_track[50], moves_track[70]]))
        tup = (moves_track[30]/self.num_agents, moves_track[50]/self.num_agents, moves_track[70]/self.num_agents)
        print(tup)
        self.move_percentages.append(tup)
        return

    def run_n_rounds(self, n=100):
        for i in range(n):
            self.round()

fram = Framework()
fram.round()








#
# rawData = [
#     {'High':75,'Medium':25,'Low':0,'label':'point 1'},
#     {'High':70,'Medium':10,'Low':20,'label':'point 2'},
#     {'High':75,'Medium':20,'Low':5,'label':'point 3'},
#     {'High':5,'Medium':60,'Low':35,'label':'point 4'},
#     {'High':10,'Medium':80,'Low':10,'label':'point 5'},
#     {'High':10,'Medium':90,'Low':0,'label':'point 6'},
#     {'High':20,'Medium':70,'Low':10,'label':'point 7'},
#     {'High':10,'Medium':20,'Low':70,'label':'point 8'},
#     {'High':15,'Medium':5,'Low':80,'label':'point 9'},
#     {'High':10,'Medium':10,'Low':80,'label':'point 10'},
#     {'High':20,'Medium':10,'Low':70,'label':'point 11'},
# ];
#
# def makeAxis(title, tickangle):
#     return {
#       'title': title,
#       'titlefont': { 'size': 20 },
#       'tickangle': tickangle,
#       'tickfont': { 'size': 15 },
#       'tickcolor': 'rgba(0,0,0,0)',
#       'ticklen': 5,
#       'showline': True,
#       'showgrid': True
#     }
#
# data = [{
#     'type': 'scatterternary',
#     'mode': 'markers',
#     'a': [i for i in map(lambda x: x['High'], rawData)],
#     'b': [i for i in map(lambda x: x['Medium'], rawData)],
#     'c': [i for i in map(lambda x: x['Low'], rawData)],
#     'text': [i for i in map(lambda x: x['label'], rawData)],
#     'marker': {
#         'symbol': 100,
#         'color': '#000000',
#         'size': 5,
#         'line': { 'width': 1 }
#     },
#     }]
#
# layout = {
#     'ternary': {
#         'sum': 1,
#         'aaxis': makeAxis('High', 0),
#         'baxis': makeAxis('<br>Medium', 45),
#         'caxis': makeAxis('<br>Low', -45)
#     },
#     'annotations': [{
#       'showarrow': False,
#       'text': 'Simple Ternary Plot with Markers',
#         'x': 0.5,
#         'y': 1.3,
#         'font': { 'size': 15 }
#     }]
# }
#
# fig = {'data': data, 'layout': layout}
# # py.iplot(fig, validate=False)
# py.plot(fig)