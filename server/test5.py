import osmnx as ox
import networkx as nx
import heapq
import math
import polyline

# Download the road network
place_name = "Singapore"
G = ox.graph_from_place(place_name, network_type='drive')

# Define average speed in m/s (50 km/h = 13.89 m/s)
avg_speed_m_per_s = 50 * 1000 / 3600

# Add travel time (in seconds) to each edge in the graph
for u, v, data in G.edges(data=True):
    data['travel_time'] = data['length'] / avg_speed_m_per_s

# Heuristic function: straight-line distance divided by average speed
def heuristic(node1, node2, G):
    coord1 = (G.nodes[node1]['y'], G.nodes[node1]['x'])
    coord2 = (G.nodes[node2]['y'], G.nodes[node2]['x'])
    distance = ox.distance.euclidean_dist_vec(coord1[0], coord1[1], coord2[0], coord2[1])
    return distance / avg_speed_m_per_s

# A* algorithm implementation
def a_star_search(G, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {node: float('inf') for node in G.nodes}
    g_score[start] = 0
    f_score = {node: float('inf') for node in G.nodes}
    f_score[start] = heuristic(start, goal, G)
    
    while open_set:
        current = heapq.heappop(open_set)[1]
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, g_score[goal]
        
        for neighbor in G.neighbors(current):
            tentative_g_score = g_score[current] + G[current][neighbor][0]['travel_time']
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal, G)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return None, float('inf')

# Define start and destination locations (latitude, longitude)
start_location = (1.3574, 103.9878) # Changi
destination_location = (1.2835, 103.8510)  # Raffles

# Find the nearest nodes to the specified locations
orig_node = ox.distance.nearest_nodes(G, X=start_location[1], Y=start_location[0])
dest_node = ox.distance.nearest_nodes(G, X=destination_location[1], Y=destination_location[0])

# Use A* algorithm to find the shortest path by travel time
shortest_path, travel_time = a_star_search(G, orig_node, dest_node)

print("Shortest path:", shortest_path)
print("Travel time (seconds):", travel_time)

# Generate the list of coordinates for the path
path_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortest_path]

# Encode the polyline
encoded_polyline = polyline.encode(path_coords)

print("Encoded polyline:", encoded_polyline)

# Generate the Google Maps URL with the encoded polyline
google_maps_url = f"https://www.google.com/maps/dir/?api=1&travelmode=driving&path=enc:{encoded_polyline}"

print("Google Maps URL:", google_maps_url)
