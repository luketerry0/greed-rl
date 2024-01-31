import curses
import random
import math
import time

curses.initscr()
def main(stdscr):
    #define colors for the display
    curses.start_color()
    if curses.can_change_color():
        curses.init_pair(1, 9, curses.COLOR_BLACK)
        curses.init_pair(2, 38, curses.COLOR_BLACK)
        curses.init_pair(3, 76, curses.COLOR_BLACK)
        curses.init_pair(4, 80, curses.COLOR_BLACK)
        curses.init_pair(5, 158, curses.COLOR_BLACK)
        curses.init_pair(6, 86, curses.COLOR_BLACK)
        curses.init_pair(7, 161, curses.COLOR_BLACK)
        curses.init_pair(8, 203, curses.COLOR_BLACK)
        curses.init_pair(9, 208, curses.COLOR_BLACK)
        curses.init_pair(10, 197, curses.COLOR_BLACK)
    else:
        for i in range(0, 10):
            curses.init_pair(i + 1, i, curses.COLOR_BLACK)

        curses.init_pair(11, curses.COLOR_RED, curses.COLOR_WHITE)

    #create the game board
    BOARD_HEIGHT = 15
    BOARD_WIDTH = 50

    #2D array to store the board
    board_arr = [[0 for x in range(BOARD_WIDTH + 2)] for y in range(BOARD_HEIGHT + 2)]

    #create the board display
    board_disp = curses.newwin(BOARD_HEIGHT , BOARD_WIDTH + 1, 1, 1)
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):

            #generate starting numbers
            number = math.floor(random.random() * 9) + 1
            #store the number
            board_arr[i + 1][j + 1] = number

            #display the number
            board_disp.addch(i, j, str(number), curses.color_pair(number + 1))

    #decide where the player begins
    player_x = math.floor(random.random() * BOARD_WIDTH)
    player_y = math.floor(random.random() * BOARD_HEIGHT)

    #display the player and record the position
    board_arr[player_y + 1][player_x + 1] = 0
    board_disp.addch(player_y, player_x, '@', curses.color_pair(11))
    board_disp.move(player_y, player_x)

    board_disp.refresh()

    #game loop
    moves = 0
    curses.noecho()
    board_disp.nodelay(True)
    while True:
        # catalogue legal moves
        legal_moves_arr = legal_moves(board_arr=board_arr, player_x=player_x, player_y=player_y)
        # print(legal_moves_arr)
        # time.sleep(99999)
        if (len(legal_moves_arr) == 0): # (0, 0) is always a legal move...
            break
        
        key = board_disp.getch()

        if key != -1:
            # read the key
            move = (0, 0)
            if key == ord('w') and (0, -1) in legal_moves_arr:      # up
                move = (0, -1)
            elif key == ord('s') and (0, 1) in legal_moves_arr:     # down
                move = (0, 1)
            elif key == ord('a') and (-1, 0) in legal_moves_arr:    # left
                move = (-1, 0)
            elif key == ord('d') and (-1, 0) in legal_moves_arr:    # right
                move = (1, 0)
            elif key == ord('q') and (-1, -1) in legal_moves_arr:    # up-left
                move = (-1, -1)
            elif key == ord('e') and (1, -1) in legal_moves_arr:     # up-right
                move = (1, -1)
            elif key == ord('z') and (-1, 1) in legal_moves_arr:    # down-left
                move = (-1, 1)
            elif key == ord('c') and (-1, 1) in legal_moves_arr:    # down-right
                move = (-1, 1)


            # move the @
            magnitude = board_arr[player_y + move[1]][player_x + move[0]]
            for i in range(magnitude + 1):
                    board_disp.addch(player_y + move[1]*i, player_x + move[0]*i, '@', curses.color_pair(11))
                    board_arr[player_y + move[1]*i + 1][player_x + move[0]*i + 1] = 0
            player_y = player_y + (magnitude * move[1])
            player_x = player_x + (magnitude * move[0])
            moves += magnitude


            
        
        board_disp.move(player_y, player_x)

    print("Finished with %s moves" % moves)


#helper function to compile legal moves
def legal_moves(board_arr, player_x, player_y):
    legal_moves_arr = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            #assume that you can move
            legal = True
            try:
                if x != 0 or y != 0:
                    for curr_magnetude in range(board_arr[player_y + y][player_x + x] + 1):
                        if board_arr[player_y + (y*curr_magnetude) + 1][player_x + (x*curr_magnetude) + 1] == '0':
                            legal = False
                            break
                else:
                    legal = False   
            except:
                legal = False

            if legal:
                legal_moves_arr.append((x, y))

    return legal_moves_arr
                

curses.wrapper(main)