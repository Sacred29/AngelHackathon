import osmnx as ox
import networkx as nx
import heapq
import math
import folium

# Download the road network
place_name = "Manhattan, New York, USA"
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

# Yen's K-shortest paths algorithm implementation
def yen_k_shortest_paths(G, source, target, k):
    paths = []
    lengths = []
    shortest_path, shortest_length = a_star_search(G, source, target)
    paths.append(shortest_path)
    lengths.append(shortest_length)
    potential_paths = []

    for i in range(1, k):
        for j in range(len(paths[-1]) - 1):
            spur_node = paths[-1][j]
            root_path = paths[-1][:j + 1]

            edges_removed = []
            for path in paths:
                if len(path) > j and root_path == path[:j + 1]:
                    u = path[j]
                    v = path[j + 1]
                    if G.has_edge(u, v):
                        edges_removed.append((u, v, G.get_edge_data(u, v)))
                        G.remove_edge(u, v)

            spur_path, spur_length = a_star_search(G, spur_node, target)
            if spur_path:
                total_path = root_path[:-1] + spur_path
                total_length = lengths[-1] - nx.path_weight(G, root_path, weight='travel_time') + spur_length
                potential_paths.append((total_length, total_path))

            for u, v, edge_data in edges_removed:
                G.add_edge(u, v, edge_data)

        if potential_paths:
            potential_paths.sort()
            paths.append(potential_paths[0][1])
            lengths.append(potential_paths[0][0])
            potential_paths.pop(0)
        else:
            break

    return paths, lengths

# Define start and destination locations (latitude, longitude)
start_location = (40.748817, -73.985428)  # Example: Empire State Building
destination_location = (40.712776, -74.005974)  # Example: One World Trade Center

# Find the nearest nodes to the specified locations
orig_node = ox.distance.nearest_nodes(G, X=start_location[1], Y=start_location[0])
dest_node = ox.distance.nearest_nodes(G, X=destination_location[1], Y=destination_location[0])

# Use Yen's K-shortest paths algorithm to find multiple routes
k = 3  # Number of routes to find
routes, lengths = yen_k_shortest_paths(G, orig_node, dest_node, k)

# Create a map centered at the start location
m = folium.Map(location=start_location, zoom_start=14)

# Colors for different routes
colors = ['blue', 'green', 'red']

# Add the routes to the map
for i, route in enumerate(routes):
    path_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
    folium.PolyLine(path_coords, color=colors[i % len(colors)], weight=5, opacity=0.7, tooltip=f'Route {i+1}: {lengths[i]:.2f} seconds').add_to(m)

# Add markers for the start and end points
folium.Marker(location=start_location, popup='Start', icon=folium.Icon(color='green')).add_to(m)
folium.Marker(location=destination_location, popup='End', icon=folium.Icon(color='red')).add_to(m)

# Display the map
m.save('multiple_routes_map.html')
m
