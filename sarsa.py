from greed_simulator import Greed_Simulator
import time
import numpy as np
import matplotlib.pyplot as plt


'''
A class which encapsulates a simple SARSA temporal difference learning agent playing Greed
'''
class SARSA(Greed_Simulator):

    def __init__(self, height=15, width=55, model = None, alpha = 0.01, epsilon = 0.01, gamma = 1):
        # initialize the display and simulator to listen here for input
        super().__init__(height, width, True)
        self.mode = "automagic"
        self.colors = [self.term.color(i+ 50) for i in range(9)] # colors for the display

        # fix the agent's position for each run
        self.player_x = 27
        self.player_y = 7


        # initialize an array to keep track of the values and state-action values of each state
        if model is not None:
            self.Q = np.load(model)
        else:
            self.Q = np.full((width, height, 8), 0 ,dtype=float)

        # initialize an array to keep track of the constants of the agent
        self.episodes = 1
        self.epsilon = epsilon
        self.ALPHA = alpha
        self.GAMMA = gamma
        self.moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        # define other properties

        self.rng = np.random.default_rng()

    # define the policy of the agent
    def pi(self, x, y):
        #epsilon greedy, choose the best move with probability 1 - epsilon
        if self.rng.random() >= self.epsilon:
            return self.moves[np.argmax(self.Q[x][y])]
        else:
            return self.moves[self.rng.integers(0, 8)]
            
    def move(self, input, sleep = True):
        if sleep:
            time.sleep(0.1)
        # choose move based on the policy of this agent  
        move = tuple(self.pi(self.player_x, self.player_y))
        og_x, og_y = self.player_x, self.player_y

        # execute the move and get the reward
        distance = self.execute_move(move)
        if distance == -1:
            reward = -1
        else:
            reward =  distance # + (self.score * self.score_discount_factor)
        
        # update the state-action values based on the move chosen
        newQ = self.Q[og_x][og_y][self.moves.index(move)] + self.ALPHA * (reward + self.GAMMA * np.max(self.Q[self.player_x][self.player_y]) - self.Q[og_x][og_y][self.moves.index(move)])
        self.Q[og_x, og_y].put(self.moves.index(move), newQ)
              
        if reward != -1:
            return (move, distance)
        else: return ((0, 0), -1)

    # trains for a specified number of episodes
    def train(self, episodes, save_name = None, verbose = True):
        UPDATE_FREQUENCY = 1000
        SAVE_FREQUENCY = 100000
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
            if verbose and i % UPDATE_FREQUENCY == 0 and i != 0:
                # plt.plot(self.runScores[:-UPDATE_FREQUENCY])
                # plt.show()
                print("Episode %s: -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=" % i)
                print("  Average Score in past: %s" % round(np.average(self.runScores[i - UPDATE_FREQUENCY:]), 2))
                print("  Standard Deviation in past: %s" % round(np.std(self.runScores[i - UPDATE_FREQUENCY:]), 2))

            if i % SAVE_FREQUENCY == 0 and i != 0:
                np.save("sarsa_" + str(i), self.Q)

            self.runScores = np.append(self.runScores, self.score)
        # print summary statistics
        print("  Average Score: %s" % (sum(self.runScores) / len(self.runScores)))
        print("  Max Score: %s" % max(self.runScores))

        # save the final state-action values
        if save_name is None:
            np.save("sarsa_" + str(i), self.Q)
        else:
            np.save(save_name + "_" + str(i), self.Q)

        return (np.average(self.runScores), np.std(self.runScores))

            

            

    
e = SARSA(15, 55)# "sarsa_999.npy")
e.train(10000000)

# e = SARSA(15, 55, "sarsa_100000.npy")
# e.run_game()

