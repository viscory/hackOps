import logging
import json

from collections import deque
from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

import math

def solve(data):
    answers = { "answers": {}}
    d = [(1,0), (0,1), (-1,0), (0,-1)]
    for key, value in data.items():
        # tuple
        start = value['start']
        end = value['end']
        grid = value['maze']

        q = deque([(start[1], start[0])])
        src = (start[1], start[0])
        dest = (end[1], end[0])
        n = len(grid)
        m = len(grid[0])
        mx = math.inf
        dist = [[mx for _ in range(m)] for j in range(n) ]
        dist[src[0]][src[1]] = 1

        while len(q):
            x, y = q.popleft()
            for i, j in d:
                if 0 <= x + i < n and 0 <= y + j < m:
                    nx = x + i
                    ny = y + j
                    if grid[nx][ny] == 0 and dist[x][y] + 1 < dist[nx][ny]:
                        dist[nx][ny] = dist[x][y] + 1
                        q.append((nx,ny))
        
        if dist[dest[0]][dest[1]] == mx:
            answers['answers'][key] = -1
        else:
            answers['answers'][key] = dist[dest[0]][dest[1]]

    return answers


@app.route('/supermarket', methods=['POST'])
def supermarket():
    data = request.get_data() 

    # logging.info("data from request {}".format(data))
    data = json.loads(data.decode('utf-8'))['tests'] 
    # logging.info("data sent for evaluation {}".format(data))
    return json.dumps(solve(data))