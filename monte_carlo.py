from greed_simulator import Greed_Simulator
import random
import time
import numpy as np

'''
class which encapsulates an agent moving with a Monte-Carlo Strategy in Greed
'''
class MonteCarlo(Greed_Simulator):

    def __init__(self, height=15, width=55):
        super().__init__(height, width, True)
        self.mode = "automagic"
        self.colors = [self.term.color(i+ 30) for i in range(9)]

        # initialize an array to keep track of the rewards for each state action
        #self.Q = np.full((width, height, 9), 0 ,dtype=float)
        self.Q = np.load("monte_carlo_1000.npy")
        self.Returns = np.full((width, height, 9, 1), 0, dtype=float)
        self.state_action_rewards = []     
        self.moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1), (0,0)]

        self.rng = np.random.default_rng()
        self.epsilon = 0.1
        self.gamma = 1



        # initial state
        self.player_x, self.player_y = 27, 7
        self.init_x , self.init_y = self.player_x, self.player_y


    def move(self, input=None, sleep = True):
        if sleep:
            time.sleep(0.01)
        # choose a move according to an epsilon greedy value
        if self.rng.random() >= self.epsilon:
            move =  self.moves[np.argmax(self.Q[self.player_x][self.player_y])]
        else:
            move =  self.moves[self.rng.integers(0, 8)]

        result = self.execute_move(move)
        if result != -1:
            self.score += result
            return (move, result)
        else: return ((0, 0), -1)

    def run_episode(self):
        # reset game
        self.player_x, self.player_y = self.init_x, self.init_y
        self.reset_static_board()
        self.score = 0
        self.enumerate_legal_moves()
        while len(self.legal_moves_arr) > 0:
            # make a move
            chosen_move = self.move()

            # record the state_action pair
            self.state_action_rewards.append([(self.player_x, self.player_y), chosen_move[0], chosen_move[1]])

    def train(self, episodes):
        for episode_number in range(episodes):
            # enumerate an episode
            self.run_episode()
            print("completed episode %s with score %s" % (episode_number, self.score))

            # iterate backwards over the state-action pairs, updating the Q values based on the new averages
            states_visited = {}
            G = 0
            R_next_state = self.state_action_rewards[0][2]
            for sar in reversed(self.state_action_rewards[:-1]):
                # update the estimate for each state
                curr_x, curr_y, curr_move, curr_reward = sar[0][0], sar[0][1], self.moves.index(sar[1]), sar[2]
                G += (self.gamma*G) + R_next_state
                np.append(self.Returns[curr_x][curr_y][curr_move], G)
                
                self.Q[curr_x][curr_y][curr_move] = np.average(self.Returns[curr_x][curr_y][curr_move])
                R_next_state = curr_reward
        np.save("monte_carlo_" + str(episodes), self.Q)
    
e = MonteCarlo()
#e.train(100000)
e.run_game()