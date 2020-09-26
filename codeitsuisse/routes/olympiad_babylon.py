import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

from ortools.linear_solver import pywraplp

def create_data_model(numberOfBooks, numberOfDays, books, days):
    """Create the data for the example."""
    data = {}
    weights = books
    values = [1] * numberOfBooks
    data['weights'] = weights
    data['values'] = values
    data['items'] = list(range(len(weights)))
    data['num_items'] = len(weights)
    num_bins = numberOfDays
    data['bins'] = list(range(num_bins))
    data['bin_capacities'] = days
    return data


def babylon(numberOfBooks, numberOfDays, books, days):
    data = create_data_model(numberOfBooks, numberOfDays, books, days)

    # Create the mip solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('multiple_knapsack_mip', 'CBC')

    # Variables
    # x[i, j] = 1 if item i is packed in bin j.
    x = {}
    for i in data['items']:
        for j in data['bins']:
            x[(i, j)] = solver.IntVar(0, 1, 'x_%i_%i' % (i, j))

    # Constraints
    # Each item can be in at most one bin.
    for i in data['items']:
        solver.Add(sum(x[i, j] for j in data['bins']) <= 1)
    # The amount packed in each bin cannot exceed its capacity.
    for j in data['bins']:
        solver.Add(
            sum(x[(i, j)] * data['weights'][i]
                for i in data['items']) <= data['bin_capacities'][j])

    # Objective
    objective = solver.Objective()

    for i in data['items']:
        for j in data['bins']:
            objective.SetCoefficient(x[(i, j)], data['values'][i])
    objective.SetMaximization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        total_weight = 0
        for j in data['bins']:
            bin_weight = 0
            bin_value = 0
            for i in data['items']:
                if x[i, j].solution_value() > 0:
                    bin_weight += data['weights'][i]
                    bin_value += data['values'][i]
            total_weight += bin_weight
        return total_weight
    else:
        return None

@app.route('/olympiad-of-babylon', methods=['POST'])
def olympiad_of_babylon():
  input = request.get_json()

  logging.info("data sent for evaluation {}".format(input))

  numberOfBooks = input["numberOfBooks"]
  numberOfDays = input["numberOfDays"]
  books = input["books"]
  days = input["days"]

  answer = babylon(numberOfBooks, numberOfDays, books, days)

  result={'optimalNumberOfBooks':answer}

  logging.info("My result :{}".format(result))
  
  return json.dumps(result)
