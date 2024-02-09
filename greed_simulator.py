import random
import math
import blessed

# class to simulate a greed board
class Greed_Simulator:
    def __init__(self, height, width):
        # game mode, or algorithm used to make moves
        self.mode = "manual"

        # create the game board
        self.game_board = [[math.floor(random.random() * 9) + 1 for x in range(width)] for y in range(height)]

        # define where the player is
        self.player_x = math.floor(random.random() * width)
        self.player_y = math.floor(random.random() * height)
        self.game_board[self.player_y][self.player_x] = 0

        # define the legal moves
        self.legal_moves_arr = []
        self.enumerate_legal_moves()

        # initialize player score
        self.score = 0

        # initialize the display of the board
        self.term = blessed.Terminal()
        self.colors = [self.term.color(i + 100) for i in range(9)]

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
                else:
                    magnitude = self.game_board[self.player_y + y_dir][self.player_x + x_dir]
                    if magnitude == 0:
                        legal = False
        
                
                if legal:
                    # if the magnitude of the move would take you off the board or onto another zero, it's illegal
                    for step in range(1, magnitude + 1):
                        # taken off the game board
                        if (self.player_x + (step * x_dir) < 0 or self.player_x + (step * x_dir) >= len(self.game_board[0])) or (self.player_y + (step * y_dir) < 0 or self.player_y + (step * y_dir) >= len(self.game_board)) or self.game_board[self.player_y + (step * y_dir)][self.player_x + (step * x_dir)] == 0:
                            legal = False

                if legal:
                    legal_moves_arr.append((x_dir, y_dir))
        self.legal_moves_arr = legal_moves_arr

    def execute_move(self,direction):
        # moves in a direction as given by a tuple (0,0)
        # returns a -1 if the move is illegal, and the number of spaces moved if the move is legal
        if direction in self.legal_moves_arr:
            magnitude = self.game_board[self.player_y + direction[1]][self.player_x + direction[0]]

            # move the player
            for i in range(1, magnitude + 1):
                self.game_board[self.player_y + i * direction[1]][self.player_x + i * direction[0]] = 0
            
            #update the player's location
            self.player_x = self.player_x + magnitude * direction[0]
            self.player_y = self.player_y + magnitude * direction[1]

            # update score
            self.score += magnitude

            #return
            return magnitude
        else:
            return -1

    def move(self, input):
        print("manual move")
        # make the required move
        move = (0, 0)
        match input:
            case "w":
                move = (0, -1)
            case "a":
                move = (-1, 0)
            case "s":
                move = (0, 1)
            case "d":
                move = (1, 0)
            case "q":
                move = (-1, -1)
            case "e":
                move = (1, -1)
            case "z":
                move = (-1, 1)
            case "c":
                move = (1, 1)
        result = self.execute_move(move)
        if result != -1:
            return (move, result)
        else: return ((0, 0), 0)
    def ugly_run_game(self):

        # run game with bad display (for testing graphics)
        while self.legal_moves_arr != []:
            self.enumerate_legal_moves()
            print(self.legal_moves_arr)
            self.display_board()

            key = input()
            
            move = self.move(key)
            print(self.execute_move(move))

    def run_game(self):
        with self.term.fullscreen():
            # draw the numbers
            for row_number in range(len(self.game_board)): 
                for col_number in range(len(self.game_board[row_number])):
                    # read the number
                    number = self.game_board[row_number][col_number]

                    #display the number
                    print(self.term.move(row_number, col_number) +
                        self.colors[number - 1](str(number)), end = " ")
                print()

            # draw the player
            print(self.term.mediumorchid1_on_seashell2 + self.term.move(self.player_y, self.player_x) + '@')

            # game loop -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
            # loop the game, making moves and updating the board, until the game is lost

            self.enumerate_legal_moves()
            while len(self.legal_moves_arr) > 0:
                if self.mode == "manual":
                    with self.term.cbreak(), self.term.hidden_cursor():
                        input_key = self.term.inkey()
                else:
                    input_key = None

                # make a move
                move = self.move(input_key)
                
                # update the board
                self.update_board(move[0], move[1])
                
                self.enumerate_legal_moves()


        print("Game Over, Score: %s" % self.score)

        return self.score

    def update_board(self, direction, magnitude):
        # update the board with the move

        for step in range(magnitude + 1):
            #display the path
            print(self.term.move(self.player_y + direction[1]*-1*step , self.player_x + direction[0]*-1*step) +
                self.term.gray60_on_dodgerblue4  +
                '@'
                , end = "")
                
        #draw the player
        print(self.term.mediumorchid1_on_seashell2 + self.term.move(self.player_y, self.player_x) + '@')



# g = Greed_Simulator(10, 15)
# g.run_game()
