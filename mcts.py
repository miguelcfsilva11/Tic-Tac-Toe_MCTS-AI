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
        for i in range(1200):
            leaf = mcts.expand(self, root.board, player, root)
            result = mcts.rollout(self, leaf)
            mcts.backpropagate(self, leaf, root, result)
        return mcts.best_child(self, root).board

    def expand(self, mx, player, root):
        plays = mcts.generate_states(self, mx, player) #all possible plays
        if root.visits == 0:
            for j in plays:
                root.children.append(j) #create child_nodes in case they havent been created yet
        for j in root.children:
            if j.visits == 0:
                return j #first iterations of the loop
        return mcts.expansion_choice(self, root) #choose the one with most potential

    def rollout(self, leaf):
        mx = leaf.board
        swap = 1
        while mcts.final(self, mx, "O") == 0:
            if swap == 1: # "X" playing
                possible_states = []
                possible_nodes = mcts.generate_states(self, mx, "X")
                for i in possible_nodes:
                    possible_states.append(i.board)
                if len(possible_states) == 1:
                    mx =  possible_states[0]
                    if mcts.final(self, mx, "X") == 2:
                        return -1 #loss
                    elif mcts.final(self, mx, "X") == 1:
                        return 0.5 #tie
                else:
                    choice = random.randrange(0, len(possible_states))
                    mx = possible_states[choice]
                    print(mcts.final(self, mx, "X"))
                    if mcts.final(self, mx, "X") == 2:
                        return -1
                    if mcts.final(self, mx, "X") == 1:
                        return 0.5
            elif swap == 0: # "O" playing
                possible_states = []
                possible_nodes = mcts.generate_states(self, mx, "O")
                for i in possible_nodes:
                    possible_states.append(i.board)
                if len(possible_states) == 1: mx =  possible_states[0]
                else:
                    choice = random.randrange(0, len(possible_states))
                    mx = possible_states[choice]
            swap += 1
            swap = swap % 2
        if mcts.final(self, mx, "O") == 2:
            return 1 #win
        elif mcts.final(self, mx, "O") == 1:
            return 0.5


    def backpropagate(self, leaf, root, result): # updating our prospects stats
        leaf.score += result
        leaf.visits += 1
        print(leaf.visits)
        root.visits += 1

    def generate_states(self, mx, player):
        possible_states = [] #generate child_nodes
        for i in range(len(mx)):
            for k in range(len(mx[i])):
                if mx[i][k] == "-":
                    option = copy.deepcopy(mx)
                    option[i][k] = player
                    child_node = tree(option)
                    possible_states.append(child_node)
        return possible_states

    def final(self,mx, player): #check result
        possible_draw = True
        win = False
        for i in mx: #lines
            if i == [player, player, player]:
                win = True
                possible_draw = False
        if mx[0][0] == player: #diagonals
            if mx[1][1] == player:
                if mx[2][2] == player:
                    win = True
                    possible_draw = False
        if mx[0][2] == player:
            if mx[1][1] == player:
                if mx[2][0] == player:
                    win = True
                    possible_draw = False
        for i in range(3): #collumns
            if mx[0][i] == player and mx[1][i] == player and mx[2][i] == player:
                win = True
                possible_draw = False
        for i in range(3):
            for k in range(3):
                if mx[i][k] == "-":
                    possible_draw = False
        if possible_draw: #outputs
            return 1
        if win:
            return 2
        return 0

    def calculate_score(self, score, child_visits, parent_visits, c): #UCB1
        return score / child_visits + c * math.sqrt(math.log(parent_visits) / child_visits)

    def expansion_choice(self, root): #returns most promising node
        threshold = -1*10**6
        for j in root.children:
            potential = mcts.calculate_score(self, j.score, j.visits, root.visits, 1.414)
            if potential > threshold:
                choice = j
                threshold = potential
        return choice

    def best_child(self,root):
        threshold = -1*10**6
        for j in root.children:
            if j.visits > threshold:
                win_choice = j
                threshold = j.visits
        return win_choice
