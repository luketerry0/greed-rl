import random
import math

# class to simulate a greed board
class Greed_Simulator:
    def __init__(self, height, width):
        # create the game board
        self.game_board = [[math.floor(random.random() * 9) + 1 for x in range(width)] for y in range(height)]

        # define where the player is
        self.player_x = math.floor(random.random() * width)
        self.player_y = math.floor(random.random() * height)
        self.game_board[self.player_y][self.player_x] = 0


    def display_board(self):
        # print the game board in an ugly way (for debugging)
        for row in self.game_board:
            print(row)

    def enumerate_legal_moves(self):
        # catalogue legal moves
        legal_moves_arr = []
        for x_dir in range(-1, 2):
            for y_dir in range(-1, 2):  
                # assume the move is legal and traverse in every direction to find out
                legal = True

                # standing still is illegal
                if (x_dir == 0 and y_dir == 0):
                    legal = False
                
                # if reading the magnitude of the move takes you off the board, it's illegal
                if (self.player_x + x_dir < 0 or self.player_x + x_dir >= len(self.game_board[0])) or (self.player_y + y_dir < 0 or self.player_y + y_dir >= len(self.game_board)):
                    legal = False
                
                if legal:
                    # if the magnitude of the move would take you off the board or onto another zero, it's illegal
                    for step in range(1, self.game_board[self.player_y + y_dir][self.player_x + x_dir] + 1):
                        # taken off the game board
                        if (self.player_x + step * x_dir < 0 or self.player_x + step * x_dir >= len(self.game_board[0])) or (self.player_y + step * y_dir < 0 or self.player_y + step * y_dir >= len(self.game_board)) or self.game_board[self.player_y + step * y_dir][self.player_x + step * x_dir] == 0:
                            legal = False

                        if legal and (self.game_board[self.player_y + step * y_dir][self.player_x + step * x_dir] == 0):
                            legal = False
                if legal:
                    legal_moves_arr.append((x_dir, y_dir))
        return legal_moves_arr

    def move(self,direction):
        # moves in a direction as given by a tuple (0,0)
        # returns a -1 if the move is illegal, and the number of spaces moved if the move is legal
        if direction in self.enumerate_legal_moves():
            magnitude = self.game_board[self.player_y + direction[1]][self.player_x + direction[0]]

            # move the player
            for i in range(magnitude + 1):
                self.game_board[self.player_y + i * direction[1]][self.player_x + i * direction[0]] = 0
            
            #update the player's location
            self.player_x = self.player_x + magnitude * direction[0]
            self.player_y = self.player_y + magnitude * direction[1]

            #return
            return magnitude
        else:
            return -1

# g = Greed_Simulator(10, 15)
# g.display_board()

# print()
# print(g.enumerate_legal_moves())
