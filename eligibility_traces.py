from greed_simulator import Greed_Simulator
import random
import time
import numpy as np

'''
class which encapsulates an agent moving with true online TD(\lambda) methods in Greed
'''
class Elibibility_Traces(Greed_Simulator):

    def __init__(self, height=15, width=55):
        super().__init__(height, width, True)
        self.mode = "automagic"
        self.colors = [self.term.color(i+ 180) for i in range(9)]

        self.moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        # fix the agent's position for each run
        self.player_x = 27
        self.player_y = 7


        # use the simple linear function approximation where the inner product of w and x is v
        # features will correspond to the numbers immediately around the head
        self.NUM_FEATURES = 8
        self.w = np.full(self.NUM_FEATURES, 0 ,dtype=float) # weights
        self.z = np.full(self.NUM_FEATURES, 0 ,dtype=float) # eligibility traces
        self.last_v = 0

        self.rng = np.random.default_rng()
        self.epsilon = 0.3


        # initial feature vector
        self.x = self.get_feature_vector(self.player_x, self.player_y)

        # parameters...
        self.ALPHA = 0.5 # step size
        self.LAMBDA = 0.6 # trace decay rate
        self.GAMMA = 0.9 # future discount rate...

    def get_feature_vector(self, x, y):
        # get the feature vector for the current state
        i = 0
        features = np.full(self.NUM_FEATURES, 0 ,dtype=float)
        for y_idx in range(-1, 2):
            for x_idx in range(-1, 2):
                if x_idx == 0 and y_idx == 0:
                    continue

                if x + x_idx < 0 or x + x_idx >= len(self.game_board[0]) or y + y_idx < 0 or y + y_idx >= len(self.game_board):
                    features[i] = 0
                    i += 1
                    continue

                number = self.game_board[y + y_idx][x + x_idx]
                features[i] = number
                i += 1
        return features   
    
    def pi(self, x, y):
        # use an epsilon greedy policy based on the current estimated value funtion for the states
        curr_max = -1
        best_move = ((0, 0), 0)
        self.enumerate_legal_moves()
        for move in self.legal_moves_arr:
            # look ahead and estimate the value based on features of the new state
            magnitude = self.game_board[y + move[1]][x + move[0]]
            if magnitude != 0:
                y_post = y + magnitude*move[1]
                x_post = x + magnitude*move[0]

                new_features = self.get_feature_vector(x_post, y_post)
                estimated_value = self.w.dot(new_features)
                if estimated_value > curr_max:
                    curr_max = estimated_value
                    best_move = (move, magnitude)

        if True: #self.rng.random() >= self.epsilon:
            return best_move
        else:
            move =  (self.legal[self.rng.integers(0, 8)], 0)

    def move(self, input, sleep = True):
        if sleep:
            time.sleep(0.5)

        # choose a move, observe feature vector of next state
        move = self.pi(self.player_x, self.player_y) 
        next_coords = (self.player_x + move[0][0]*move[1], self.player_y + move[0][1]*move[1])
        next_features = self.get_feature_vector(next_coords[0], next_coords[1])
        curr_value = self.w.dot(self.x)
        next_value = self.w.dot(next_features)

        result = self.execute_move(move[0])

        delta = result + self.GAMMA*next_value - curr_value
        self.z = self.GAMMA*self.LAMBDA*self.z + (1 - (self.ALPHA*self.GAMMA*self.LAMBDA*(self.z.dot(self.x))))*self.x
        self.w = self.w + self.ALPHA*(delta + curr_value - self.last_v)*self.z - self.ALPHA*(curr_value - self.last_v)*self.x
        print(self.ALPHA*(curr_value - self.last_v)*self.x)
        self.last_v = next_value

        self.x = next_features

        
        if result != -1:
            return (move[0], result)
        else: return ((0, 0), 0)
    
    def train(self, episodes):
        for episode_number in range(episodes):
            # reset game
            self.reset_static_board()
            self.player_x = 27
            self.player_y = 7
            self.score = 0
            self.z = np.full(self.NUM_FEATURES, 0 ,dtype=float) # eligibility traces

            self.enumerate_legal_moves()
            while len(self.legal_moves_arr) > 0:
                # make a move
                move = self.move(None, False)
                #print(move)
            
            print("completed episode %s with score %s" % (episode_number, self.score))


  
e = Elibibility_Traces()
e.train(100)