from greed_simulator import Greed_Simulator

class Epsilon_Greedy(Greed_Simulator):
    def __init__(self, height, width):
        super().__init__(height, width)
        self.mode = "manual"

def move(self, input):
        # make the required move
        move = (0, 0)
        match input:
            case "w":
                move = (0, -1)
            case "a":
                move = (-1, 0)
            case "s":
                move = (0, 1)
            case "d":
                move = (1, 0)
            case "q":
                move = (-1, -1)
            case "e":
                move = (1, -1)
            case "z":
                move = (-1, 1)
            case "c":
                move = (1, 1)
        result = self.execute_move(move)
        if result != -1:
            return (move, result)
        else: return ((0, 0), 0)
        
e = Epsilon_Greedy(15, 20)
e.run_game()