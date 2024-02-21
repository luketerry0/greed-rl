from greed_simulator import Greed_Simulator
import random
import time

'''
class which encapsulates an agent moving randomly in Greed
'''
class Random(Greed_Simulator):

    def __init__(self, height=15, width=55):
        super().__init__(height, width, True)
        self.mode = "automagic"
        self.colors = [self.term.color(i+ 30) for i in range(9)]

        # initialize an array 

    def move(self, input):
        time.sleep(0.1)
        # choose a random move   
        move = random.choice(self.legal_moves_arr)

        result = self.execute_move(move)
        if result != -1:
            return (move, result)
        else: return ((0, 0), 0)
    
e = Random()
e.run_game()