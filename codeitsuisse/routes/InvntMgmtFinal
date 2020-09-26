import logging
import json
from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/inventory-management', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for dict1 in data:
        target = dict1["searchItemName"]
        temtarget = target
        target = target.upper()
        items = dict1["items"]
        items = [item.upper() for item in items]
        ans = []
        for item in items:
            ans.append(MinDist(target, item))

        ans = [(ans[i][0], items[i], ans[i][1]) for i in range(len(ans))]
        ans.sort()
        ans = [i[2] for i in ans][0:10]

        result.append({"searchItemName": temtarget, "searchResult": ans})

    return json.dumps(result)

def MinDist(word1, word2):
    n, m = len(word1), len(word2)
    matrix = [[(0, "") for i in range(m + 5)] for j in range(n + 5)]
    for i in range(n + 1):
            for j in range(m + 1):
                if i == 0:
                    matrix[i][j] = (j, ''.join(["+" + c for c in word2[:j]]))
                elif j == 0:
                    matrix[i][j] = (i, ''.join(["-" + c for c in word1[:i]]))
                elif (word1[i - 1] == word2[j - 1]):
                    tup = matrix[i - 1][j - 1]
                    matrix[i][j] = (tup[0], tup[1] + word2[j - 1])
                else:
                    tup1, tup2, tup3 = matrix[i][j -
                                        1], matrix[i - 1][j], matrix[i - 1][j - 1]

                    matrix[i][j] = min((1 + tup1[0], tup1[1] + "+" + word2[j - 1]),
                                (1 + tup2[0], tup2[1] +
                                 "-" + word1[i - 1]),
                        (1 + tup3[0], tup3[1] + word2[j - 1])
                    )
    return matrix[n][m]
