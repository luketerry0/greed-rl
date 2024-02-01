from greed_simulator import Greed_Simulator

class Greed_Logic():
    def __init__(self, mode):
        self.mode = mode
        match mode:
            case "manual":
                self.Make_Move = self.Make_Move_Manual

    def Make_Move_Manual(self, simulator : Greed_Simulator, input):
        # make the required move

        match input:
            case "w":
                move = (0, -1) # correct binding
            case "a":
                move = (-1, 0)
            case "s":
                move = (0, 1)
            case "d":
                move = (1, 0)

        
        result = simulator.move(move)
        if result != -1:
            return (move, result)
        else: return ((0, 0), 0)
 
