from greed_simulator import Greed_Simulator
import random
import time

class Epsilon_Greedy(Greed_Simulator):
    def __init__(self, height, width):
        super().__init__(height, width)
        self.mode = "automagic"

    def move(self, input):
        time.sleep(0.5)
        # choose a random move   
        move = random.choice(self.legal_moves_arr)

        result = self.execute_move(move)
        if result != -1:
            return (move, result)
        else: return ((0, 0), 0)
    
e = Epsilon_Greedy(15, 20)
e.run_game()