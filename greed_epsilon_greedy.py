from greed_simulator import Greed_Simulator

class Epsilon_Greedy(Greed_Simulator):
    def __init__(self, filename=None):
        super(Greed_Simulator, self).__init__()
        self["mode"] = "epsilon_greedy"

    def move(self):
        # implementing move logic here...
        return ((0, 0), 0)