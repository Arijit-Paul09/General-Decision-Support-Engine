# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
import random
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import time
import os

def solve_tsp(distance_matrix):
    global ort
    """Solves the TSP problem and prints the solution."""
    def print_solution(manager, routing, solution):
        global plan_output
        global rdor
        """Prints solution on console."""
        print(f"Objective: {solution.ObjectiveValue()} miles")
        index = routing.Start(0)
        plan_output = "Route for pipe:\n"
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += f" {manager.IndexToNode(index)} ->"
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        plan_output += f" {manager.IndexToNode(index)}\n"
        #print(plan_output)
        rdor= f"Route distance: {route_distance}\n"
        
    s=time.time()
    # Instantiate the data problem.
    data = {"distance_matrix": distance_matrix, "num_vehicles": 1, "depot": 0}

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data["distance_matrix"]), data["num_vehicles"], data["depot"])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        ort=time.time()-s
        print_solution(manager, routing, solution)

def generate_distance_matrix(num_cities):
    distance_matrix = []
    for i in range(num_cities):
        row = []
        for j in range(num_cities):
            if i == j:
                row.append(0)  # Distance from a city to itself is 0
            else:
                # Generate a random distance between 100 and 1000
                row.append(random.randint(100, 1000))
        distance_matrix.append(row)
    return distance_matrix

def tspdy(distance_matrix):
    global best_distance
    global dyt
    num_cities = len(distance_matrix)
    
    # Initialize memoization table
    memo = {}
    s=time.time()
    # Function to calculate shortest path from a city to another set of cities
    def dp(curr, visited):
        if (curr, visited) in memo:
            return memo[(curr, visited)]
        
        # Base case: If all cities have been visited
        if visited == (1 << num_cities) - 1:
            return distance_matrix[curr][0]
        
        ans = float('inf')
        for next_city in range(num_cities):
            # If next_city is not visited
            if (visited & (1 << next_city)) == 0:
                ans = min(ans, distance_matrix[curr][next_city] + dp(next_city, visited | (1 << next_city)))
        
        memo[(curr, visited)] = ans
        return ans
    
    # Starting from city 0
    best_distance = dp(0, 1)
    dyt=time.time()-s
    

app = Flask('_name_',template_folder='templates')
@app.route('/')
def index():
    return render_template('main.html')

@app.route('/function1', methods=['GET', 'POST'])
def p1():
    if request.method == 'POST':
        # Retrieve form data
        n = int(request.form['arg1'])
        d=generate_distance_matrix(n)
        solve_tsp(d)
        print(ort)
        tspdy(d)

        return render_template("preview.html",a="Dynamic Programming",b=plan_output,c='Route Distance: '+str(best_distance),d='Time Taken: '+str(dyt),e="Process Oriented modelling with OR Tools",f=rdor,g='Time Taken: '+str(ort),h=d)

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port,debug=True)
