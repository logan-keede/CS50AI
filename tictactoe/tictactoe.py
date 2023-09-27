"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    countx = 0
    counto = 0
    for i in board:
        for j in i:
            if j == X:
                countx+=1
            elif j == O:
                counto+=1

    if countx == counto:

        return X
    else:

        return O

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = []
    for i in range(3):
        for j in range(3):
            if board[i][j]==EMPTY:
                action.append((i,j))
    return action


    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board1 = [j[::] for j in board]

    board1[action[0]][action[1]] = player(board1)
    return board1
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in board:
        if i ==[X,X,X]:
            return X
        if i == [O,O,O]:
            return O
    diagonal = []
    diagonal2 = []
    length1 = []
    length2 = []
    length3 = []
    for i in range(3):
        length1.append(board[i][0])
        length2.append(board[i][1])
        length3.append(board[i][2])
        diagonal.append(board[i][i])
        diagonal2.append(board[2-i][i])
    if diagonal ==[X,X,X] or diagonal2 ==[X,X,X] or length1 ==[X,X,X] or length2 ==[X,X,X] or length3 ==[X,X,X] :
        return X
    if diagonal ==[O,O,O] or diagonal2 ==[O,O,O] or length1==[O,O,O] or length2==[O,O,O] or length3==[O,O,O]:
        return O
    return None
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # for i in board:
    #     if i ==[X,X,X]:
    #         return True
    #     if i == [O,O,O]:
    #         return True
    # diagonal = []
    # diagonal2 = []
    # for i in range(3):
    #     if board[i][0:3] == [X,X,X]:
    #         return True
    #     elif board[i][0:3] == [O,O,O]:
    #         return True
    #     diagonal.append(board[i][i])
    #     diagonal2.append(board[3-i][i])
    # if diagonal ==[X,X,X] or diagonal2 ==[X,X,X]:
    #     return True
    # if diagonal ==[O,O,O] or diagonal2 ==[O,O,O]:
    #     return True
    #
    # return False

    if winner(board) != None or actions(board) == []:
        return True
    else:
        return False

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    for i in board:
        if i ==[X,X,X]:
            return 1
        if i == [O,O,O]:
            return -1
    diagonal = []
    diagonal2 = []
    length1 = []
    length2 = []
    length3 = []
    for i in range(3):
        length1.append(board[i][0])
        length2.append(board[i][1])
        length3.append(board[i][2])
        diagonal.append(board[i][i])
        diagonal2.append(board[2-i][i])
    if diagonal ==[X,X,X] or diagonal2 ==[X,X,X] or length1 ==[X,X,X] or length2 ==[X,X,X] or length3 ==[X,X,X] :
        return 1
    if diagonal ==[O,O,O] or diagonal2 ==[O,O,O] or length1==[O,O,O] or length2==[O,O,O] or length3==[O,O,O]:
        return -1
    return 0
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # return check_utility(board, player(board))[1]
    if terminal(board):
        return None

    def maxValue(board):
        v = -math.inf
        if terminal(board):
            return utility(board)

        else:
            for action in actions(board):
                v = max(v, minValue(result(board, action)))
            return v
    def minValue(board):
        v = math.inf
        if terminal(board):
            return utility(board)

        else:
            for action in actions(board):
                v = min(v, maxValue(result(board, action)))
            return v

    if player(board) == X:
        v = maxValue(board)
        for action in actions(board):
            res = result(board, action)
            if minValue(res) == v:
                return action
    elif player(board) == O:
        v = minValue(board)
        for action in actions(board):
            res = result(board, action)
            if maxValue(res) == v:
                return action

    # for action in actions(board):
    #     res = result(board, action)
    #     util = check_utility(res, player(res))
    #     if util[0] == util1[0]:
    #         return action



    raise NotImplementedError

def check_utility(board, player):

    action_list = actions(board)
    utils = []

    for action in action_list:
        res = result(board,action)
        if terminal(res):
            utils.append([utility(res), action])
        else:
            player1 = X if player == O else O
            util = check_utility(res, player1)[0]
            utils.append([util, action])

            if player==X and util ==1: # added for alpa-beta_pruning
                return [util, action]
            if player==O and util ==-1:
                return [util, action]
    else:
        utils.sort(key = lambda x: x[0])
        return utils[0] if player == O else utils[-1]
