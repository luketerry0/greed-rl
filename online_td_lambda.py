from multiprocessing import Queue
from greed_simulator import Greed_Simulator
import random
import time
import numpy as np # used for efficient arrays

'''
class which encapsulates an agent moving using on-line td_lambda for Greed
'''
class TrueOnlineTDLambda(Greed_Simulator):

    def __init__(self, height=15, width=55, model = False, GAMMA = 1, ALPHA = 0.5, EPSILON = 0.1, LAMBDA = 0.5):
        super().__init__(height, width, True)
        self.mode = "automagic"
        self.colors = [self.term.color(i+ 30) for i in range(9)]

        self.e = np.full((width, height), 0, dtype=float)
        if model:
            self.V = np.load(model)
        else:
            self.V = np.full((width, height), 0, dtype=float)

        self.init_x, self.init_y = 27, 7
        self.player_x, self.player_y = self.init_x, self.init_y

        #params....
        self.GAMMA = GAMMA
        self.ALPHA = ALPHA
        self.EPSILON = EPSILON
        self.LAMBDA = LAMBDA

        self.rng = np.random.default_rng()



    def move(self, input=None, sleep = True):
        if sleep:
            time.sleep(0.1)

        # epsilon greedy move strategy
            
        self.enumerate_legal_moves()
        best_move = None
        best_val = -10000 # due to the dimensions of the board, the moves should never be less than this
        for move in self.legal_moves_arr:
            # evaluate the coordinates where the move would end
            magnitude = self.game_board[self.player_y + move[1]][self.player_x + move[0]]

            new_x = self.player_x + move[0]*magnitude
            new_y = self.player_y + move[1]*magnitude

            # check the value of the new move
            if self.V[new_x][new_y] < best_val:
                best_move = move

        if self.rng.random() <= self.EPSILON:
            move = self.legal_moves_arr[self.rng.integers(0, len(self.legal_moves_arr))]

        reward = self.execute_move(move)
        return (move, reward, self.player_x, self.player_y)

    def run_episode(self):
        # reset eligibility traces
        self.e = np.full((len(self.game_board[0]), len(self.game_board)), 0, dtype=float)

        # reset board
        self.reset_static_board()
        self.player_x, self.player_y = self.init_x, self.init_y
        self.score = 0
        self.enumerate_legal_moves()

        # run game loop
        while len(self.legal_moves_arr) > 0:
            #note the current value of the state
            curr_value = self.V[self.player_x][self.player_y]

            # make a move
            _, reward, next_x, next_y = self.move(False)

            next_value = self.V[next_x][next_y]
            delta = reward + self.GAMMA*next_value - curr_value
            self.e[self.player_x][self.player_y] = self.e[self.player_x][self.player_y] + 1

            # iterate over all s
            for x_iter in range(len(self.game_board[0])):
                for y_iter in range(len(self.game_board)):
                    self.V[x_iter][y_iter] = self.V[x_iter][y_iter] + self.ALPHA*delta*self.e[x_iter][y_iter]
                    self.e[x_iter][y_iter] = self.GAMMA*self.LAMBDA*self.e[x_iter][y_iter]
        return self.score

    def evaluate(self, num_episodes, return_queue: Queue):
        scores = np.array(1)
        for i in range(num_episodes):
            scores = np.append(scores, self.run_episode())
            if i % 100 == 0:
                print("episode %s complete" % i)

        return_queue.put([np.mean(scores), np.std(scores), self.ALPHA, self.GAMMA, self.EPSILON, self.LAMBDA])
        return
            #print("completed episode %s, score %s, epsilon %s" % (i, self.score, self.EPSILON))

            # if i % save_interval == 0 and i != 0:
            #     np.save("td_lambda_" + str(i), self.V)



    
# e = TrueOnlineTDLambda()#model="td_lambda_100.npy")
# e.train(10000, 100)
# e.run_game()