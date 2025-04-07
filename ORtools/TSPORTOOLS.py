"""Simple Travelling Salesperson Problem (TSP) between cities."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import time

def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = [
        [0, 593, 995, 563, 660, 485, 577, 260, 271, 385, 361, 635, 986, 170, 658, 815, 585, 690, 902, 223],
[732, 0, 767, 299, 226, 422, 485, 765, 936, 518, 241, 822, 494, 494, 268, 348, 362, 470, 142, 853],
[109, 396, 0, 246, 739, 866, 239, 272, 816, 335, 855, 100, 427, 915, 352, 377, 755, 277, 604, 952],
[642, 535, 764, 0, 107, 218, 492, 834, 998, 746, 749, 478, 409, 472, 202, 155, 461, 525, 846, 100],
[625, 395, 497, 539, 0, 657, 512, 883, 547, 498, 455, 635, 682, 577, 691, 475, 375, 898, 184, 162],
[534, 743, 539, 405, 279, 0, 806, 871, 459, 393, 165, 195, 838, 793, 793, 820, 579, 731, 543, 799],
[344, 319, 192, 982, 696, 510, 0, 292, 498, 282, 125, 834, 807, 408, 150, 542, 632, 933, 777, 618],
[302, 945, 154, 812, 330, 220, 290, 0, 179, 268, 354, 205, 806, 433, 823, 383, 197, 742, 829, 480],
[621, 271, 915, 830, 340, 671, 796, 922, 0, 525, 224, 100, 459, 798, 124, 425, 359, 577, 913, 758],
[877, 183, 353, 625, 335, 250, 280, 939, 457, 0, 453, 964, 651, 704, 838, 517, 759, 650, 894, 389],
[155, 143, 692, 172, 689, 287, 281, 644, 198, 277, 0, 364, 263, 399, 106, 295, 263, 997, 384, 846],
[312, 793, 790, 289, 309, 890, 287, 886, 617, 793, 440, 0, 825, 418, 979, 648, 733, 242, 928, 270],
[944, 842, 107, 278, 347, 933, 619, 192, 382, 934, 757, 896, 0, 404, 997, 612, 425, 383, 203, 355],
[873, 302, 463, 812, 815, 278, 856, 382, 441, 760, 393, 492, 149, 0, 620, 296, 347, 987, 782, 973],
[769, 118, 383, 535, 650, 538, 831, 101, 807, 656, 795, 143, 600, 953, 0, 371, 455, 284, 496, 720],
[919, 276, 203, 799, 678, 237, 250, 726, 197, 767, 327, 256, 332, 772, 732, 0, 574, 225, 291, 271],
[979, 881, 686, 498, 903, 665, 845, 714, 747, 291, 234, 144, 426, 393, 529, 130, 0, 860, 266, 734],
[650, 816, 898, 471, 653, 283, 595, 177, 440, 964, 789, 649, 673, 199, 928, 328, 776, 0, 330, 528],
[507, 110, 316, 173, 473, 615, 664, 933, 857, 890, 659, 963, 397, 770, 168, 198, 744, 594, 0, 583],
[513, 144, 136, 751, 346, 299, 120, 976, 395, 466, 873, 702, 533, 334, 550, 761, 361, 470, 239, 0],
    ]
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data


def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()} miles")
    index = routing.Start(0)
    plan_output = "Route for vehicle 0:\n"
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += f" {manager.IndexToNode(index)} ->"
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += f" {manager.IndexToNode(index)}\n"
    print(type(plan_output))
    plan_output += f"Route distance: {route_distance}miles\n"


"""Entry point of the program."""
# Instantiate the data problem.
s=time.time()
data = create_data_model()

# Create the routing index manager.
manager = pywrapcp.RoutingIndexManager(
    len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
)

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
search_parameters.first_solution_strategy = (
    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
)

# Solve the problem.
solution = routing.SolveWithParameters(search_parameters)

# Print solution on console.
if solution:
    print("Time Taken by OR Tools ",time.time()-s)
    print_solution(manager, routing, solution)

