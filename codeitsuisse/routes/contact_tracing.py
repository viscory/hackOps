import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/contact_trace', methods=['POST'])
def eval():
    data = request.get_json();
    print(data)
    # logging.info("data sent for evaluation {}".format(data))
    # print(result)
    # logging.info("My result :{}".format(result))
    return jsonify(contact(data))

import math

def difference(a, b):

  startDiff = 0
  middleDiff = 0

  splitA = a.split("-")
  splitB = b.split("-")

  for i in range(len(splitA)):
    smallA = splitA[i]
    smallB = splitB[i]

    if smallA[0] != smallB[0]:
      startDiff += 1
    
    if smallA[1] != smallB[1]:
      middleDiff += 1

    if smallA[2] != smallB[2]:
      middleDiff += 1

  totalDiff = startDiff + middleDiff

  return (totalDiff, startDiff)

def recursor(infected, genes, answer, path, visited):
  minimumDiff = math.inf
  possibilities = []
  finalChecker = []

  if(len(visited) == len(genes)):
    path = path+infected["name"]
    answer.append(path)
    # print(visited)
    return

  # if(infected["name"] == "metal"):
  #   path = path+infected["name"]
  #   answer.append(path)
  #   return

  for i in genes:

    if(i["name"] not in visited):
      # print("finding difference for ", i["name"])
      currentDiff = difference(infected["genome"], i["genome"])

      finalChecker.append((i, currentDiff))

      if currentDiff[0] < minimumDiff:
        minimumDiff = currentDiff[0]
  
  for i in finalChecker:
    if i[1][0] == minimumDiff:
      possibilities.append(i)
    
  for point in possibilities:
    # ["plastic* -> thread -> metal"]

    if (point[1][0] == 0):
      answer.append(path + infected["name"] + " -> " + point[0]["name"])
      continue

    if (point[1][1]> 0):
      recursor(point[0], genes, answer, path+infected["name"] + "* -> ", visited + [point[0]["name"]])
    else:
      recursor(point[0], genes, answer, path+infected["name"] + " -> ", visited + [point[0]["name"]])
    
    

def contact(request):
  infected = request.get("infected")

  origin = request.get("origin")

  cluster = request.get("cluster")

  genes = [origin] + [c for c in cluster] 

  # gene, non-Silent
  answer = []

  path = ""

  visited = []

  recursor(infected, genes, answer, path, visited)

  return answer

  




