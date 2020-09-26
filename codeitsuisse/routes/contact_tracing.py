import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/contact_trace', methods=['POST'])
def evaluateContactTrace():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    infected = data.get("infected")
    infectedGenome = infected.get("genome")
    origin = data.get("origin")
    originGenome = origin.get("genome")
    cluster = data.get("cluster")
    clusterGenome = cluster[0].get("genome")
    result = []

    count1 = 0
    silentCheck1 = True
    count2 = 0
    silentCheck2 = True
    i=0
    for a,b in zip(infectedGenome,clusterGenome):
        if a != b:
            count1 += 1
            if (i+1)%3 == 0 :
                silentCheck1 = False
        i += 1
    i=0
    for a,b in zip(clusterGenome,originGenome):
        if a != b:
            count2 += 1
            if (i+1)%3 == 0 :
                silentCheck1 = False
        i += 1

    if count1 <= 2 and count2 <= 2:
        if count1 == 0 and count2 == 0:
            result.append(infected.get("name") + " -> " + cluster[0].get("name"))
            result.append(infected.get("name") + " -> " + origin.get("name"))
        elif silentCheck1 == True and silentCheck2 == True:
            result.append(infected.get("name") + " -> " + cluster[0].get("name") + " -> " + origin.get("name"))
        elif silentCheck1 == False and silentCheck2 == True:
            result.append(infected.get("name") + "* -> " + cluster[0].get("name") + " -> " + origin.get("name"))
        elif silentCheck1 == True and silentCheck2 == False:
            result.append(infected.get("name") + " -> " + cluster[0].get("name") + "* -> " + origin.get("name"))
        else:
            result.append(infected.get("name") + "* -> " + cluster[0].get("name") + "* -> " + origin.get("name"))
        logging.info("My result :{}".format(result))
        return json.dumps(result);


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

  




