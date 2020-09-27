import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def f(n,m,s):
    tt = 1
    for i in range(m):
        tt*=(n-i)

    def dfs(s, nowlevel, factor):
        if(nowlevel == m):
            return 0
        maxx = 0
        tem = []
        for i in range(len(s)):
            x = (1 if (s[i] == 'Y') else 0)
            tem.append(tt*x + dfs(s[:i]+s[i+1:], nowlevel+1, 1/(len(s)-1)))
        #print(tem)
        for i in range(len(s)):
            maxx += max(tem[i], tem[len(s)-1-i])
            
        return factor*maxx
            
    return (dfs(s, 0, 1/len(s))/tt)     

@app.route('/yin-yang', methods=['POST'])
def evaluate_yinyang():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    n = data.get("number_of_elements")
    m = data.get("number_of_operations")
    s = data.get("elements")
    
     
    result = {'result':f(n,m,s)}
    logging.info("My result :{}".format(result))
    return json.dumps(result)