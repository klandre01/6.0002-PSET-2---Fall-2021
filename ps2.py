# 6.0002 Problem Set 2 Fall 2021
# Graph Optimization
# Name: Karen Andre
# Collaborators: Angelica Whipple
# Time: 5:00

#
# Finding shortest paths to drive from home to work on a road network
#

from graph import DirectedRoad, Node, RoadMap


# PROBLEM 2: Building the Road Network
#
# PROBLEM 2a: Designing your Graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the times
# represented?
#
# Write your answer below as a comment:
# The graph's nodes represent intersections
# The graph's edges represent roads
# The travel times are represented in the edges as the weight

# PROBLEM 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a road map (graph).

    Travel time and traffic multiplier should be cast to a float.

    Parameters:
        map_filename : String
            name of the map file

    Assumes:
        Each entry in the map file consists of the following format, separated by spaces:
            source_node destination_node travel_time road_type traffic_multiplier

        Note: hill road types always are uphill in the source to destination direction and
              downhill in the destination to the source direction. Downhill travel takes
              half as long as uphill travel. The travel_time represents the time to travel
              from source to destination (uphill).

        e.g.
            N0 N1 10 highway 1
        This entry would become two directed roads; one from 'N0' to 'N1' on a highway with
        a weight of 10.0, and another road from 'N1' to 'N0' on a highway using the same weight.

        e.g.
            N2 N3 7 hill 2
        This entry would become to directed roads; one from 'N2' to 'N3' on a hill road with
        a weight of 7.0, and another road from 'N3' to 'N2' on a hill road with a weight of 3.5.

    Returns:
        a directed road map representing the inputted map
    """
    f = open(map_filename, 'r')
    edges = f.readlines()
    map = RoadMap()
    for e in edges:
        attr = e.split(' ')
        source = attr[0]
        source_node = Node(source)
        dest = attr[1]
        dest_node = Node(dest)
        time = float(attr[2])
        road_type = attr[3]
        traffic = float(attr[4])
        # adds source and dest to nodes if not already there
        if not map.contains_node(source_node):
            map.insert_node(source_node)
        if not map.contains_node(dest_node):
            map.insert_node(dest_node)
        # source to dest road
        road1 = DirectedRoad(source_node, dest_node, time, road_type, traffic)
        map.insert_road(road1)
        # dest to source road
        if (road_type == "hill"):
            time /= 2
        road2 = DirectedRoad(dest_node, source_node, time, road_type, traffic)
        map.insert_road(road2)
    return map

# PROBLEM 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out after testing

# road_map = load_map("maps/test_load_map.txt")
# print(road_map)



# PROBLEM 3: Finding the Shortest Path using Optimized Search Method



# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
# Objective function: travel time
# Constraint: shortest amount of travel time
#

# PROBLEM 3b: Implement find_optimal_path
def find_optimal_path(roadmap, start, end, restricted_roads, has_traffic=False):
    """
    Finds the shortest path between start and end nodes on the road map,
    without using any restricted roads,
    following traffic conditions.
    Use Dijkstra's algorithm.

    Parameters:
    roadmap - RoadMap
        The graph on which to carry out the search
    start - Node
        node at which to start
    end - Node
        node at which to end
    restricted_roads - list[string]
        Road Types not allowed on path
    has_traffic - boolean
        flag to indicate whether to get shortest path during traffic or not

    Returns:
    A tuple of the form (best_path, best_time).
        The first item is the shortest path from start to end, represented by
        a list of nodes (Nodes).
        The second item is a float, the length (time traveled)
        of the best path.

    If there exists no path that satisfies constraints, then return None.
    """
    if not (roadmap.contains_node(start) and roadmap.contains_node(end)): # nodes not in map
        return None
    if start == end:
        return ([start], 0)

    unvisited = roadmap.get_all_nodes() # nodes we haven't visited
    time_to = {node: float('inf') for node in roadmap.get_all_nodes()} # how long it takes to get to current node
    time_to[start] = 0
    best_path = {node: None for node in roadmap.get_all_nodes()} # best way to get to each node (immediate predecessor)

    while len(unvisited) != 0:
        current = min(unvisited, key = lambda x: time_to[x])
        if time_to[current] == float('inf'):
            break
        if current == end:
            break

        for road in roadmap.get_reachable_roads_from_node(current, restricted_roads):
            neighbor = road.get_destination_node() # neighboring node
            
            temp_time_to = time_to[current] + road.get_travel_time(has_traffic) # time to the next node
            if temp_time_to < time_to[neighbor]:
                time_to[neighbor] = temp_time_to
                best_path[neighbor] = current
        
        unvisited.remove(current)
    
    optimal_path = []
    current = end
    while best_path[current] != None:
        optimal_path.insert(0, current)
        current = best_path[current]
    if len(optimal_path) != 0:
        optimal_path.insert(0, current)
    else: # optimal_path could not be constructed
        return None
    return (optimal_path, time_to[end])


# PROBLEM 4a: Implement optimal_path_no_traffic
def find_optimal_path_no_traffic(filename, start, end):
    """
    Finds the shortest path from start to end during conditions of no traffic.

    You must use find_optimal_path and load_map.

    Parameters:
    filename - name of the map file that contains the graph
    start - Node, node object at which to start
    end - Node, node object at which to end

    Returns:
    list of Node objects, the shortest path from start to end in normal traffic.
    If there exists no path, then return None.
    """
    return find_optimal_path(load_map(filename), start, end, [])[0]

# PROBLEM 4b: Implement optimal_path_restricted
def find_optimal_path_restricted(filename, start, end):
    """
    Finds the shortest path from start to end when local roads and hill roads cannot be used.

    You must use find_optimal_path and load_map.

    Parameters:
    filename - name of the map file that contains the graph
    start - Node, node object at which to start
    end - Node, node object at which to end

    Returns:
    list of Node objects, the shortest path from start to end given the aforementioned conditions,
    If there exists no path that satisfies constraints, then return None.
    """
    return find_optimal_path(load_map(filename), start, end, ['hill', 'local'])[0]


# PROBLEM 4c: Implement optimal_path_heavy_traffic
def find_optimal_path_in_traffic_no_toll(filename, start, end):
    """
    Finds the shortest path from start to end when toll roads cannot be used and in traffic,
    i.e. when all roads' travel times are multiplied by their traffic multipliers.

    You must use find_optimal_path and load_map.

    Parameters:
    filename - name of the map file that contains the graph
    start - Node, node object at which to start
    end - Node, node object at which to end; you may assume that start != end

    Returns:
    The shortest path from start to end given the aforementioned conditions,
    represented by a list of nodes (Nodes).

    If there exists no path that satisfies the constraints, then return None.
    """
    return find_optimal_path(load_map(filename), start, end, ['toll'], has_traffic=True)[0]


if __name__ == '__main__':

    # UNCOMMENT THE FOLLOWING LINES TO DEBUG
    pass
    # rmap = load_map('./maps/small_map.txt')

    # start = Node('N0')
    # end = Node('N4')
    # restricted_roads = []

    # print(find_optimal_path(rmap, start, end, restricted_roads))
