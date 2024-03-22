from greed_simulator import Greed_Simulator
from multiprocessing import Queue
import random
import time
import numpy as np

'''
class which encapsulates an agent utilizing TD learning in Greed
'''
class TD(Greed_Simulator):
    
    def __init__(self, height=15, width=55, model = False, epsilon = 0.05, alpha = 0.5, gamma = 1):
        # initialize the display and simulator to listen here for input
        super().__init__(height, width, True)
        self.mode = "automagic"
        self.colors = [self.term.color(i+ 50) for i in range(9)] # colors for the display

        # fix the agent's position for each run
        self.player_x = 27
        self.player_y = 7


        # initialize an array to keep track of the values of each state
        if model:
            self.V = np.load(model)
        else:
            self.V = np.full((width, height), 0 ,dtype=float)

        self.episodes = 1
        self.epsilon = epsilon
        self.ALPHA = alpha
        self.GAMMA = gamma
        self.moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        # define other properties

        self.rng = np.random.default_rng()

    def moveV(self, move, x, y):
        # at each move, find the distance and which state it takes you to. 
        # Return its V value
        # THE BOARD STARTS AT 0,0 and moves positively right and down
        # MOVE MUST BE LEGAL
        if move in self.legal_moves_arr:
            if move == self.moves[0]:
                # up left
                distance = self.game_board[y-1][x-1]
                return self.V[x - distance][y - distance]
            if move == self.moves[1]:
                # up
                distance = self.game_board[y][x-1]
                return self.V[x - distance][y]
            if move == self.moves[2]:
                # up right
                distance = self.game_board[y+1][x-1]
                return self.V[x - distance][y + distance]
            if move == self.moves[3]:
                # left
                distance = self.game_board[y-1][x]
                return self.V[x][y - distance]
            if move == self.moves[4]:
                # right
                distance = self.game_board[y+1][x]
                return self.V[x][y + distance]
            if move == self.moves[5]:
                # down left
                distance = self.game_board[y-1][x+1]
                return self.V[x + distance][y - distance]
            if move == self.moves[6]:
                # down
                distance = self.game_board[y][x+1]
                return self.V[x + distance][y]
            if move == self.moves[7]:
                # DOWN RIGHT
                # Acess game board through board[y][x]
                distance = self.game_board[y+1][x+1]
                return self.V[x + distance][y + distance]
        
        # IF THE MOVE IS NOT LEGAL, RETURN S' = S
        else:
            return self.V[x][y]

    # define an epilon greedy policy
    def pi(self, x, y):
        move = None
        
        # our goal here is to iterate through legal moves and return the highest V(s')
        if self.rng.random() >= self.epsilon:
            # move that ends in state with highest V
            maxV = 0
            for i in self.legal_moves_arr:
                currentV = self.moveV(i, x, y)
                # check
                if (currentV >= maxV):
                    maxV = currentV
                    move = i
            
            
        else:
            move = self.moves[self.rng.integers(0, 8)]

        return move
    

    def move(self, input, sleep = True):
        if sleep:
            time.sleep(0.1)
        # choose move based on the policy of this agent  
        move = self.pi(self.player_x, self.player_y)
        og_x, og_y = self.player_x, self.player_y
        Vprime = self.moveV(move, og_x, og_y)

        # execute the move and get the reward
        distance = self.execute_move(move)
        if distance == -1:
            reward = -1
        else:
            reward =  distance # + (self.score * self.score_discount_factor)
        
        # update the V value for the current state (x,y)
        newV = self.V[og_x][og_y] + self.ALPHA*(reward + self.GAMMA*Vprime - self.V[og_x][og_y])
        self.V[og_x][og_y] = newV
              
        if reward != -1:
            return (move, distance)
        else: return ((0, 0), -1) 

    # run the game a specified number of times and show the average score

    def run_episode(self):

        init_x = self.player_x
        init_y = self.player_y
       
        # reset the game
        self.reset_static_board()
        self.player_x = init_x
        self.player_y = init_y
        self.score = 0
        self.enumerate_legal_moves()

        while len(self.legal_moves_arr) > 0:
            # make a move
            move = self.move(None, False)

        return self.score

    def evaluate(self, num_episodes, return_queue: Queue):
        scores = np.array(1)
        for i in range(num_episodes):
            scores = np.append(scores, self.run_episode())
            if i % 50 == 0:
                print("episode %s complete" % i)

        return_queue.put([np.mean(scores), np.std(scores), self.ALPHA, self.GAMMA, self.epsilon])
        return
    
    # trains for a specified number of episodes
    def train(self, episodes, save_name = None, verbose = True):
        UPDATE_FREQUENCY = 1000
        SAVE_FREQUENCY = 50000
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
                print("  Epsilon: %s" % self.epsilon)
            
            if i % SAVE_FREQUENCY == 0 and i != 0:
                np.save("TD_" + str(i), self.V)

            self.runScores = np.append(self.runScores, self.score)
            self.episodes += 1

        # print summary statistics
        print("  Average Score: %s" % (sum(self.runScores) / len(self.runScores)))
        print("  Max Score: %s" % max(self.runScores))

        # save the final state-action values
        if save_name is None:
            np.save("sarsa_" + str(i), self.V)
        else:
            np.save(save_name + "_" + str(i), self.V)

        return (np.average(self.runScores), np.std(self.runScores))

#e = TD(15, 55)
#e.train(10000)
# e.run_game()


    

