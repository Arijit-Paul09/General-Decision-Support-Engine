import random

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

# Define the number of cities
num_cities = 20

# Generate the distance matrix
distance_matrix = generate_distance_matrix(num_cities)

print(distance_matrix)
