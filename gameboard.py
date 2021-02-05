import math
import random
from copy import deepcopy
from mcts import *
mx = [["-","-","-"],
      ["-","-","-"],
      ["-","-","-"]]
playable = True
class board:
    def __init__(self, board = "current"):
        self.player1 = "X"
        self.player2 = "O"
    def reset(self, mx):
        for i in mx:
            for _ in i:
                _ = "-"
        return mx
    def endgame(self):
        global playable
        global mx
        if playable == False:
            repeat = input("Want to play again?\nY/N?: ")
            if repeat.upper() in "Y":
                playable = True
                mx = [["-", "-", "-"],
                      ["-", "-", "-"],
                      ["-", "-", "-"]]
                board.output_matrix(mx)
            else:
                print("Bye!")
    def move(self, x, y):
        mx[x][y] = self.player1
    def output_matrix(self,mx):
        printable_matrix = ("{0}\n{1}\n{2}").format(mx[0], mx[1], mx[2])
        print(printable_matrix, "\n")
    def final(self,mx, player):
        global playable
        possible_draw = 1
        for i in mx:
            if i == [player, player, player]:
                possible_draw = 0
                playable = False
                board.output_matrix(mx)
                print("Player ", player, " won!")
        if mx[0][0] == player:
            if mx[1][1] == player:
                if mx[2][2] == player:
                    possible_draw = 0
                    playable = False
                    board.output_matrix(mx)
                    print("Player ", player, " won!")
        if mx[0][2] == player:
            if mx[1][1] == player:
                if mx[2][0] == player:
                    playable = False
                    possible_draw = 0
                    board.output_matrix(mx)
                    print("Player ", player, " won!")
        for i in range(3):
            if mx[0][i] == player and mx[1][i] == player and mx[2][i] == player:
                playable = False
                possible_draw = 0
                board.output_matrix(mx)
                print("Player ", player, " won!")
        for i in range(3):
            for k in range(3):
                if mx[i][k] == "-":
                    possible_draw = 0
        if possible_draw == 1:
            playable = False
            board.output_matrix(mx)
            print("There's a draw!")
    def gameplay(self):
        global mx
        global playable
        print("\nHey! Let's play Tic-Tac-Toe! What's your first move?\nTell us in the format of (x,y) coordinates.\n"
              "To quit write the word 'stop'."
              "\nTake a look at the board!\n")
        board.output_matrix(mx)
        while playable:
            try:
                human_move = input("Choose your position: ")
                if human_move.upper() in "STOP":
                    break
                else:
                    pos = human_move.split(",")
                    row = int(pos[0])-1
                    collumn = int(pos[1]) -1
                    if mx[collumn][row] != "-" or collumn < 0 or row <0:
                        print("Illegal move, chief!")
                        continue
                    board.move(collumn, row)
                    board.final(mx, self.player1)
                    if playable == False:
                        board.endgame()
                    else:
                        mx = mcts.search(mx, self.player2)
                        board.final(mx, self.player2)
                        board.endgame()
                        if playable == False:
                            continue
                        else:
                            board.output_matrix(mx)
            except:
                print("That's not a valid input!")

mcts = mcts()
board = board()
board.gameplay()