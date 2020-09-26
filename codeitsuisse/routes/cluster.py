import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/cluster', methods=['POST'])
def cluster_finder():
    data = request.get_json()
    print(type(data))
    result = dict()
    result['answer'] = findingClusters(data)
    return result

def dfs(i, j, n, m, area):
    area[i][j] = "*"
    lst = [-1, 0, 1]
    for i1 in lst:
        for j1 in lst:
            if (isValid(i + i1, j + j1, n, m) and area[i + i1][j + j1] != "*"):
                dfs(i + i1, j + j1, n, m, area)

def isValid(i, j, n, m):
    return (i >= 0 and i < n and j >= 0 and j < m)
               
def findingClusters(area):
    count = 0
    n = len(area)
    m = len(area[0])
    for i in range(n):
        for j in range(m):
            if(area[i][j] == "1"):
                dfs(i, j, n, m, area)
                count += 1
    return count
