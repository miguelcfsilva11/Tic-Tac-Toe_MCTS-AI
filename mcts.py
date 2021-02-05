import random
import math
import copy

class mcts:
    def search(self, mx, player):
        return mcts.pick(self, mx, player)

    def pick(self, mx, player):
        plays = mcts.generate_states(self, mx, player)
        for j in plays:
            if mcts.final(self, j, player):
                return j
        random_pick = random.randrange(0, len(plays)-1)
        return plays[random_pick]

    def generate_states(self, mx, player):
        possible_states = []
        for i in range(len(mx)):
            for k in range(len(mx[i])):
                if mx[i][k] == "-":
                    option = copy.deepcopy(mx)
                    option[i][k] = player
                    possible_states.append(option)
        return possible_states

    def final(self,mx, player):
        possible_draw = True
        win = False
        for i in mx:
            if i == [player, player, player]:
                win = True
                possible_draw = False
        if mx[0][0] == player:
            if mx[1][1] == player:
                if mx[2][2] == player:
                    win = True
                    possible_draw = False
        if mx[0][2] == player:
            if mx[1][1] == player:
                if mx[2][0] == player:
                    win = True
                    possible_draw = False
        for i in range(3):
            if mx[0][i] == player and mx[1][i] == player and mx[2][i] == player:
                win = True
                possible_draw = False
        for i in range(3):
            for k in range(3):
                if mx[i][k] == "-":
                    possible_draw = False
        if possible_draw:
            return possible_draw
        return win