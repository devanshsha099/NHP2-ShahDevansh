
from locations import *

 # Every location that the respective hub is in is basically a node in the graph that the algorithm will create
 # These nodes are operated on in this class

class Nodes(Location):
    def __init__(self):
        self.node_list = []
        self.adjacent_nodes = {}
        self.distance_to_node = {}

    # Every node is a hub which will be added to the node_list which can then be worked on by the hubs_ref
    def add_node(self, node):
        self.node_list.append(node)
        self.adjacent_nodes[node] = []

    def init_directed_edge(self, node, neighboring_node, weight=1.0):
        self.distance_to_node[(node, neighboring_node)] = weight
        from csvreader import hub
        self.adjacent_nodes[hub].append(neighboring_node)

    # Initialize the adding of all the individual routes created by the main Dijkstra
    def init_undirected_edge(self, node_a, node_b, weight=1.0):
        self.init_directed_edge(node_a, node_b, weight)
        self.init_directed_edge(node_b, node_a, weight)

    # Get the distance of the individual routes created from one node to the next
    def get_distance(self, node_a, node_b):
        if node_a < node_b:
            temp = node_b
            node_b = node_a
            node_a = temp
        return self.get_node(node_a).get_neighbor(node_b)

    #
    def get_node(self, index):
        return self.node_list[index]

    def get_node_by_index(self, index):
        return self.node_list[index]

    #
    def get_node_index(self, hub_address):
        for row in range(len(self.node_list)):
            if self.node_list[row].address == hub_address:
                return row
            else:
                return None

    #
    def get_node_address_by_id(self, hub_id):
        for row in range(len(self.node_list)):
            if self.node_list[row].index == hub_id:
                return self.node_list[row].address


