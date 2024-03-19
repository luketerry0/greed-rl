from greed_simulator import Greed_Simulator
from multiprocessing import Queue
import random
import time
import numpy as np

'''
class which encapsulates an agent moving randomly in Greed
'''


class MC(Greed_Simulator):

    def __init__(self, height=15, width=55, model = None, epsilon = 0.075, gamma = .1):
        super().__init__(height, width, True)
        self.mode = "automagic"
        self.colors = [self.term.color(i + 30) for i in range(9)]

        self.player_x = 27
        self.player_y = 7

        if model is not None:
            self.Q = np.load(model)
        else:
            self.Q = np.full((width, height, 8), 0, dtype=float)

        # initialize all values and structures needed
        self.episodes = 1
        self.epsilon = epsilon
        self.GAMMA = gamma
        self.moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        # define other properties
        self.rng = np.random.default_rng()
        # need a 4 dimensional array for returns
        # will append to it like self.returns[x, y, action, G value]
        self.returns = np.full((width, height, 8, 1), 0, dtype=float)
        # append to with self.sar.append([(x,y), move, reward])
        self.sar = []


    def pi(self, x, y):
        # epsilon greedy policy
        move = None
        if self.rng.random() >= self.epsilon: 
            # use policy
            move =  self.moves[np.argmax(self.Q[x][y])]
        else: # explore every certain percentage with a random move
            move =  self.moves[self.rng.integers(0, 8)]
        
        return move




    def move(self, input, sleep=True):
        if sleep:
            time.sleep(0.1)

        # choose move based on the policy of this agent  
        move = self.pi(self.player_x, self.player_y)
        og_x, og_y = self.player_x, self.player_y

        # execute the move and get the reward
        distance = self.execute_move(move)
        if distance == -1:
            reward = -1
        else:
            reward = distance
        
        # we must store each step of the episode into self.sar, state as a tuple, move as a tuple, and reward
        if reward != -1:
            self.sar.append([(og_x,og_y), move, reward])
            return (move, distance)
        else: 
            self.sar.append([(og_x,og_y), move, reward])
            return ((0, 0), -1) 

    # run the game a specified number of times and show the average score

    def run_episode(self):
        init_x = self.player_x
        init_y = self.player_y

        self.reset_static_board()
        self.player_x = init_x
        self.player_y = init_y
        self.score = 0
        self.enumerate_legal_moves()

        # complete the episode until terminal
        while len(self.legal_moves_arr) > 0:
            # make a move
            move = self.move(None, False)
            
        # now that the episode has finished, go through each step and update values
        g = 0
        start = len(self.sar) -1
        end = -1
        step = -1

        for j in range(start, end, step):
            g = self.GAMMA*g + self.sar[j][2] # will be the reward

            # the current state, action, reward array
            current_sar = self.sar[j]
            # current state
            current_state = current_sar[0]
            current_action = current_sar[1]
            # the current state action pair St, At
            current_pair = tuple(current_sar[0:2])
            # the remaining state action pairs (leading up to the starting state action pair)
            remaining_tuples = [(sar[0],sar[1]) for sar in self.sar[:j]]

            # if the state and action pair exist in somewhere else down the road
            if current_pair in remaining_tuples:
                # do nothing
                pass
            else:
                # append G to its appropriate index in self.returns
                # will append to it like self.returns[x, y, action].append
                move_index = self.moves.index(current_action)
                np.append(self.returns[current_state[0], current_state[1], move_index], g)
                # set the Q value of current state and action to be the average of its returns at St, At
                self.Q[current_state[0], current_state[1]].put(move_index, 
                        float(np.average(self.returns[current_state[0], current_state[1], move_index])))

        return self.score

    def evaluate(self, num_episodes, return_queue: Queue):
        scores = np.array(1)
        for i in range(num_episodes):
            scores = np.append(scores, self.run_episode())
            if i % 50 == 0:
                print("episode %s complete" % i)

        return_queue.put([np.mean(scores), np.std(scores), self.GAMMA, self.epsilon])
        return

        


#e = MC(15,55,)
#e.train(10)
#e.run_game()

