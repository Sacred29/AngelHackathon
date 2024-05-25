import osmnx as ox
import heapq
import numpy as np
import folium # for now to generate map
import networkx as nx

# Define the place name for your area of interest
place_name = "Singapore"

# Load the road network
G_road = ox.graph_from_place(place_name, network_type='walk')

# Define MRT stations with their coordinates
mrt_stations = {
    'One-North': (1.2998, 103.7876),
    'Buona Vista': (1.3072, 103.7906),
    'City Hall': (1.2931, 103.8525),
    'Raffles Place': (1.2835, 103.8510),
    'Changi Airport': (1.3574, 103.9878)
}

# Add MRT stations as nodes to the road network
for station, coords in mrt_stations.items():
    nearest_node = ox.distance.nearest_nodes(G_road, coords[1], coords[0])
    print(f"Nearest node to {station}: {nearest_node}")
    G_road.add_node(station, y=coords[0], x=coords[1], pos=coords)
    G_road.add_edge(station, nearest_node, length=0.001, carbon_emissions=0.001)
    G_road.add_edge(nearest_node, station, length=0.001, carbon_emissions=0.001)

# Add carbon emissions as an additional weight to each edge (this will be our weight adder)
for u, v, key, data in G_road.edges(keys=True, data=True):
    distance = data['length']  # distance in meters
    emissions = distance * 0.2
    G_road[u][v][key]['carbon_emissions'] = emissions
    G_road[u][v][key]['combined_weight'] = distance + emissions  # Customize this formula as needed

# Shortest path algo
def dijkstra_custom(graph, start, end, weight='combined_weight'):
    queue = [(0, start, [])]
    visited = set()
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in visited:
            continue
        path = path + [node]
        if node == end:
            return (cost, path)
        visited.add(node)
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                edge_data = graph.get_edge_data(node, neighbor)
                new_cost = cost + edge_data[0][weight]  # Use the first edge data if there are multiple edges
                heapq.heappush(queue, (new_cost, neighbor, path))
    return (float("inf"), [])

# Get the route
def get_route(start, end):
    # Convert MRT stations to nearest nodes in the road network if they are the start or end points
    if start in mrt_stations:
        start = ox.nearest_nodes(G_road, mrt_stations[start][1], mrt_stations[start][0])
    if end in mrt_stations:
        end = ox.nearest_nodes(G_road, mrt_stations[end][1], mrt_stations[end][0])
    return dijkstra_custom(G_road, start, end, weight='combined_weight')

# Get the distance
def get_dist(start, end):
    # Convert MRT stations to nearest nodes in the road network if they are the start or end points
    if start in mrt_stations:
        start = ox.nearest_nodes(G_road, mrt_stations[start][1], mrt_stations[start][0])
    if end in mrt_stations:
        end = ox.nearest_nodes(G_road, mrt_stations[end][1], mrt_stations[end][0])
    return nx.shortest_path_length(G_road, start, end, weight="length")

def get_time(start, end):
    if start in mrt_stations:
        start = ox.nearest_nodes(G_road, mrt_stations[start][1], mrt_stations[start][0])
    if end in mrt_stations:
        end = ox.nearest_nodes(G_road, mrt_stations[end][1], mrt_stations[end][0])
    return nx.shortest_path_length(G_road, start, end, weight='travel_time')


# Example usage
start_node = 'Changi Airport'
end_node = 'Raffles Place'

distance = get_dist(start_node, end_node)
print (f"The distance between the points is {distance} meters.")

time = get_time(start_node, end_node)
print (f"The time between the points is {time} seconds.")
# time = get_time(start_node, end_node)

'''
cost, route = get_route(start_node, end_node)
print(f"The optimal path from {start_node} to {end_node} is {route} with a total cost of {cost} units.")



# Visualize the route using Folium
route_map = ox.plot_route_folium(G_road, route, route_map=folium.Map(location=[1.3521, 103.8198], zoom_start=12))

# Add start and end markers
folium.Marker(location=(G_road.nodes[route[0]]['y'], G_road.nodes[route[0]]['x']),
              popup='Start: Changi Airport', icon=folium.Icon(color='green')).add_to(route_map)
folium.Marker(location=(G_road.nodes[route[-1]]['y'], G_road.nodes[route[-1]]['x']),
              popup='End: Raffles Place', icon=folium.Icon(color='red')).add_to(route_map)

# Save the map to an HTML file
route_map.save("route_map1.html")

print("Route map saved to route_map.html")
'''
