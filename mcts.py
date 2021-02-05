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
        for i in range(1000):
            leaf = mcts.expand(self, root.board, player, root)
            result = mcts.rollout(self, leaf)
            mcts.backpropagate(self, leaf, root, result)
        return mcts.best_child(self, root)

    def expand(self, mx, player, root):
        leaf_potential = root
        plays = mcts.generate_states(self, mx, player)
        if root.visits == 0:
            for j in plays:
                root.children.append(j)
        for j in plays:
            if mcts.final(self, j.board, player):
                return j
        score = 0
        for j in root.children:
            if j.visits == 0:
                return j
            j.score = mcts.calculate_score(self, player, j.score, j.visits, root.visits)
            if j.score > score:
                score = j.score
                leaf_potential = j
        return leaf_potential

    def rollout(self, leaf):
        mx = leaf.board
        aux = 1
        while mcts.final(self, mx, "O") != True or mcts.final(self, mx, "X") != True:
            if aux == 1:
                possible_states = []
                for i in range(len(mx)):
                    for k in range(len(mx[i])):
                        if mx[i][k] == "-":
                            option = copy.deepcopy(mx)
                            option[i][k] = "X"
                            possible_states.append(option)
                if len(possible_states) == 1:
                    choice = 0
                else:
                    choice = random.randrange(0, len(possible_states)-1)
                mx = possible_states[choice]
            if aux == 0:
                possible_states = []
                for i in range(len(mx)):
                    for k in range(len(mx[i])):
                        if mx[i][k] == "-":
                            option = copy.deepcopy(mx)
                            option[i][k] = "O"
                            possible_states.append(option)
                if len(possible_states) == 1:
                    choice = 0
                else:
                    choice = random.randrange(0, len(possible_states)-1)
                mx = possible_states[choice]
            aux += 1
            aux = aux%2
        if mcts.final(self, mx, "O"):
            for i in range(len(mx)):
                for k in range(len(mx[i])):
                    if mx[i][k] == "-":
                        return 1
            return 0.5
        elif mcts.final(self, mx, "X"):
            for i in range(len(mx)):
                for k in range(len(mx[i])):
                    if mx[i][k] == "-":
                        return -1
            return 0.5

    def backpropagate(self, leaf, root, result):
        leaf.score += result
        leaf.visits += 1
        root.visits += 1
        leaf = root

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

    def calculate_score(self, player, score, child_visits, parent_visits):
        c = 2
        return score / child_visits + c * math.sqrt(math.log(parent_visits / child_visits))

    def best_child(self, root):
        treshold = 0
        for j in root.children:
            if j.visits >= treshold:
                win_choice = j
                treshold = j.visits
        return win_choice.board

#todo when generating states on rollout, make a function to avoid repetitive code
#todo don't forget to optimize the bot, it is really weak as of now
