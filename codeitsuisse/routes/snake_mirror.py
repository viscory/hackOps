import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


def slsm(boardSize, player, jumps):
    board = [i for i in range(boardSize + 1)]
    ans = []

    for jump in jumps:
        temp = jump.split(":")
        if int(temp[0]) == 0:
            board[int(temp[1])] = '+'
        elif int(temp[1]) == 0:
            board[int(temp[0])] = '-'
        elif int(temp[0]) > int(temp[1]):
            board[int(temp[1])] = int(temp[0])
        elif int(temp[0]) < int(temp[1]):
            board[int(temp[1])] = int(temp[1])

    def findmax(k):
        from_mirror = False
        mx = 0
        mx_ind = -1
        next6 = board[k + 1:k + 1 + 6]
        for i, x in enumerate(next6):
            if x != '+' and x != '-' and x > mx:
                mx = x
                mx_ind = i + 1
                from_mirror = False
            if x == '+':
                for j, y in enumerate(board[i + k + 1:i + k + 1 + 6]):
                    if y != '+' and y != '-' and y > mx:
                        mx = y
                        mx_ind = j + 1
                        prev_ind = i + 1
                        from_mirror = True

        if from_mirror:
            return [[prev_ind, mx_ind], mx]
        else:
            return [[mx_ind], mx]

    def findmin(k):
        mn = 100000
        mn_ind = 0
        for i, x in enumerate(board[k + 1:k + 1 + 6]):
            if x != '+' and x != '-' and x < mn:
                mn = x
                mn_ind = i + 1
        return [[mn], mn_ind]

    x = 1
    y = 1
    shortest_path = []

    while x != boardSize:
        next_6 = board[x + 1:x + 6 + 1]

        next_6_l = board[y + 1:y + 6 + 1]
        best_choice_l = findmin(y)
        for _ in range(player - 1):
            shortest_path.extend(best_choice_l[0])
        y = best_choice_l[1]

        best_choice = findmax(x)
        shortest_path.extend(best_choice[0])
        x = best_choice[1]
        ans.append(x)
    print(ans)
    return shortest_path

@app.route('/slsm', methods=['POST'])
def evaluateSlsm():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    boardSize = data.get("boardSize")
    players = data.get("players")
    jumps = data.get("jumps")
    result = slsm(boardSize, players, jumps)
    logging.info("My result :{}".format(result))
    return jsonify(result)

