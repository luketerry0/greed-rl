from greed_simulator import Greed_Simulator
import random
import time
import numpy as np

'''
class which encapsulates an agent moving randomly in Greed
'''
class Random(Greed_Simulator):

    def __init__(self, height=15, width=55):
        super().__init__(height, width, True)
        self.mode = "automagic"
        self.colors = [self.term.color(i+ 30) for i in range(9)]

        # initialize an array 

    def move(self, input, sleep = True):
        if sleep:
            time.sleep(0.1)
        # choose a random move   
        move = random.choice(self.legal_moves_arr)

        result = self.execute_move(move)
        if result != -1:
            return (move, result)
        else: return ((0, 0), 0)

    # run the game a specified number of times and show the average score
    def evaluate(self, episodes = 1000):
        self.runScores = np.array([])

        init_x = self.player_x
        init_y = self.player_y
        for i in range(episodes):
            # reset the game
            self.reset_static_board()
            self.player_x = init_x
            self.player_y = init_y
            self.score = 0
            self.enumerate_legal_moves()
            #self.episodes += 1

            #self.Q = np.full(self.Q.shape, -1 ,dtype=float)


            while len(self.legal_moves_arr) > 0:
                # make a move
                move = self.move(None, False)
                #print(move)
            

            self.runScores = np.append(self.runScores, self.score)
        # print summary statistics
        print("Average Score: %s" % (sum(self.runScores) / len(self.runScores)))
        print("Standard Deviation: %s" % round(np.std(self.runScores), 2))


    
e = Random()
# e.evaluate()
e.run_game()