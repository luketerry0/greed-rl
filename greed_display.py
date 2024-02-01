import math
import blessed
import time
from greed_simulator import Greed_Simulator
from greed_logic import Greed_Logic

class Greed_Display:
    def __init__(self, width, height):
        self.sim = Greed_Simulator(width, height)
        self.logic = Greed_Logic("manual")

        self.term = blessed.Terminal()

        # set the display colors
        self.colors = [self.term.color(i + 100) for i in range(9)]

        # initialize the board
        self.start_game()

    def start_game(self):
        with self.term.fullscreen():
            # draw the numbers
            for row_number in range(len(self.sim.game_board)): 
                for col_number in range(len(self.sim.game_board[row_number])):
                    # read the number
                    number = self.sim.game_board[row_number][col_number]

                    #display the number
                    print(self.term.move(row_number, col_number) +
                        self.colors[number - 1](str(number)), end = " ")
                print()

            # draw the player
            print(self.term.mediumorchid1_on_seashell2 + self.term.move(self.sim.player_y, self.sim.player_x) + '@')

            self.game_loop()

    def game_loop(self):
        # loop the game, making moves and updating the board, until the game is lost
        legal_moves_arr = self.sim.enumerate_legal_moves()

        listen_for_input = self.logic.mode = "manual"

        while len(legal_moves_arr) > 0:

            if listen_for_input:
                with self.term.cbreak(), self.term.hidden_cursor():
                    input_key = self.term.inkey()
            else:
                input_key = None

            # make a move
            move = self.logic.Make_Move(self.sim, input_key)
            # update the board
            self.update_board(move[0], move[1])

    def update_board(self, direction, magnitude):
        # update the board with the move

        for step in range(magnitude):
            #display the path
            print(self.term.move(self.sim.player_y + direction[1]*-1*step , self.sim.player_x + direction[0]*-1*step) +
                self.term.gray60_on_dodgerblue4  +
                '@'
                , end = "")
                
        #draw the player
        print(self.term.mediumorchid1_on_seashell2 + self.term.move(self.sim.player_y, self.sim.player_x) + '@')

        



        

g =  Greed_Display(10, 12)
