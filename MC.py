from greed_simulator import Greed_Simulator
import random
import time
import numpy as np

'''
class which encapsulates an agent moving randomly in Greed
'''


class MC(Greed_Simulator):

    def __init__(self, height=15, width=55, model = None, epsilon = 0.01, gamma = 1):
        super().__init__(height, width, True)
        self.mode = "automagic"
        self.colors = [self.term.color(i + 30) for i in range(9)]

        self.player_x = 27
        self.player_y = 7

        if model is not None:
            self.Q = np.load(model)
        else:
            self.Q = np.full((width, height, 8), 0, dtype=float)

        # initialize an array to keep track of the constants of the agent
        self.episodes = 1
        self.epsilon = epsilon
        self.GAMMA = gamma
        self.moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        # define other properties

        self.rng = np.random.default_rng()

        # returns array starts empty
        self.returns = []
        # initialize an arbitrary policy (all 0)
        self.pi = np.full((width, height), 0, dtype=float)
        # initialize an array that will keep track of the state, action, reward pair
        self.sar = []





    def move(self, input, sleep=True):
        if sleep:
            time.sleep(0.1)

        og_x = self.player_x
        og_y = self.player_y

        if self.rng.random() >= self.epsilon:
            move = self.moves[np.argmax(self.Q[self.player_x][self.player_y])]
        else:
            move =  self.moves[self.rng.integers(0, 8)]

        reward = self.execute_move(move)

        if reward != -1:
            self.sar.append([og_x, og_y, move, reward])
            return move, reward
        else:
            self.sar.append([og_x, og_y, move, reward])
            return (0, 0), -1

    # run the game a specified number of times and show the average score

    def train(self, episodes, save_name = None, verbose = True):
        #UPDATE_FREQUENCY = 1000
        #SAVE_FREQUENCY = 100000
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
            self.returns = []



            while len(self.legal_moves_arr) > 0:
                # make a move
                move = self.move(None, False)



            G = 0
            start = len(self.sar) - 2
            end = -1
            step = -1

            for j in range(start, end, step):
                # print(self.sar[i][3])
                G = G*self.GAMMA + self.sar[j][3]


                current_sar = self.sar[j]
                current_state = tuple(current_sar[0:2])
                tuples = [(sar[0],sar[1]) for sar in self.sar[:j]]
                if current_state in tuples:
                    # do nothing
                    pass
                else:
                    # append G to returns(st, at)
                    self.returns.append(G)
                    move_index = self.moves.index(current_sar[2])
                    self.Q[current_sar[0], current_sar[1]].put(move_index, float(np.average(self.returns)))
                    self.pi[current_sar[0]][current_sar[1]] = np.argmax(self.Q[current_sar[0]][current_sar[1]])


            #if verbose and i % UPDATE_FREQUENCY == 0 and i != 0:
                # plt.plot(self.runScores[:-UPDATE_FREQUENCY])
                # plt.show()
                #print("Episode %s: -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=" % i)
                #print("  Average Score in past: %s" % round(np.average(self.runScores[i - UPDATE_FREQUENCY:]), 2))
                #print("  Standard Deviation in past: %s" % round(np.std(self.runScores[i - UPDATE_FREQUENCY:]), 2))

            #if i % SAVE_FREQUENCY == 0 and i != 0:
                #np.save("sarsa_" + str(i), self.Q)

            self.runScores = np.append(self.runScores, self.score)
            print("episode finished")

        print("Average Score: %s" % (sum(self.runScores) / len(self.runScores)))
        print("Standard Deviation: %s" % round(np.std(self.runScores), 2))
        print("  Max Score: %s" % max(self.runScores))
        # save the final state-action values
        #if save_name is None:
            #np.save("MC_" + str(i), self.Q)
        #else:
            #np.save(save_name + "_" + str(i), self.Q)

        #return (np.average(self.runScores), np.std(self.runScores))


e = MC(15,55, "MC test.npy")
# e.train(10)
e.run_game()

