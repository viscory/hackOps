import math
import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/social_distancing', methods=['POST'])
def social_distance():
    data = request.get_json();
    print(data)
    print(type(data))
    result = dict()
    result['answers'] = socialDistancing(data.get('tests'))
    return jsonify(result)

def combinations(n, r):
  return math.factorial(n)//math.factorial(r)//math.factorial(n-r)

def helper(seats, people, spaces):

  if ((seats - people)//spaces) <(people -1):
    return 0
  answer = combinations(seats - people + 2 - (people-1)*(spaces-1)-1, people)

  return answer

def socialDistancing(inputs):
  # data = request.get_json()

  # inputs = data.get("tests")



  answers = {}

  for key, value in inputs.items():
    answers[key] = helper(value["seats"], value["people"], value["spaces"])

  # jsonify({"answers": answers})

  return answers
