import random
import math
import copy

class tree:
    def __init__(self, board):
        self.board = board
        self.visits = 0
        self.score = 0
        self.children = []
class mcts:
    def search(self, mx, player,):
        root = tree(mx)
        for i in range(10000):
            leaf = mcts.expand(self, root.board, player, root)
            result = mcts.rollout(self, leaf)
            mcts.backpropagate(self, leaf, root, result)
        return mcts.best_child(self, root).board

    def expand(self, mx, player, root):
        plays = mcts.generate_states(self, mx, player)
        if root.visits == 0:
            for j in plays:
                root.children.append(j)
        for j in root.children:
            if j.visits == 0:
                return j
        for j in plays:
            if mcts.final(self, j.board, player):
                return j
        return mcts.best_child(self, root)

    def rollout(self, leaf):
        mx = leaf.board
        aux = 1
        while mcts.final(self, mx, "O") != True:
            if aux == 1:
                possible_states = []
                for i in range(len(mx)):
                    for k in range(len(mx[i])):
                        if mx[i][k] == "-":
                            option = copy.deepcopy(mx)
                            option[i][k] = "X"
                            possible_states.append(option)

                if len(possible_states) == 1:
                    mx = possible_states[0]
                else:
                    found = False
                    for j in possible_states:
                        if mcts.final(self, j, "X"): #check if there's a state where the adversary wins
                            mx = j
                            found = True
                    if found == False:
                        choice = random.randrange(0, len(possible_states) - 1)
                        mx = possible_states[choice]
                if mcts.final(self, mx, "X") == True:
                    break
            elif aux == 0:
                possible_states = []
                for i in range(len(mx)):
                    for k in range(len(mx[i])):
                        if mx[i][k] == "-":
                            option = copy.deepcopy(mx)
                            option[i][k] = "O"
                            possible_states.append(option)
                if len(possible_states) == 1:
                    mx = possible_states[0]
                else:
                    found = False
                    for j in possible_states:
                        if mcts.final(self, j, "O") and found == False: #check if there's a state where he wins
                            mx = j
                            found = True
                    if not found:
                        choice = random.randrange(0, len(possible_states) - 1)
                        mx = possible_states[choice]

            aux += 1
            aux = aux%2
        if mcts.final(self, mx, "X"):
            for i in range(len(mx)):
                for k in range(len(mx[i])):
                    if mx[i][k] == "-":
                        return -1
            return 0.3
        elif mcts.final(self, mx, "O"):
            for i in range(len(mx)):
                for k in range(len(mx[i])):
                    if mx[i][k] == "-":
                        return 1


    def backpropagate(self, leaf, root, result):
        leaf.score += result
        leaf.visits += 1
        if root.visits == 0:
            root.visits += 1

    def generate_states(self, mx, player):
        possible_states = []
        for i in range(len(mx)):
            for k in range(len(mx[i])):
                if mx[i][k] == "-":
                    option = copy.deepcopy(mx)
                    option[i][k] = player
                    child_node = tree(option)
                    possible_states.append(child_node)
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

    def calculate_score(self, score, child_visits, parent_visits, c):
        return score / child_visits + c * math.sqrt(math.log(parent_visits) / child_visits)

    def best_child(self, root):
        treshold = -100000
        for j in root.children:
            potential = mcts.calculate_score(self, j.score, j.visits, root.visits, 2)
            if potential > treshold:
                win_choice = j
                treshold = potential
        return win_choice

#todo the AI takes too long for each play, optimize that by finding the optimal approach in the rollout phase
