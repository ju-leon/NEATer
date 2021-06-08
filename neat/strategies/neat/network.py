from typing import List, Tuple
from neat.strategies.neat.genes import EdgeGene, NodeGene
from random import choice
from neat.strategies.neat.graph import node
from neat.strategies.neat.graph.edge import Edge
from neat.strategies.neat.graph.node import InputNode, Node
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from 


def create_hash(start: Node, end: Node) -> str:
    return "{}->{}".format(start.id, end.id)


class Network():
    def __init__(self, inputs: int, outputs: int, activation) -> None:
        self.input_nodes = []
        for i in range(inputs):
            name = "input_" + str(i)
            self.input_nodes.append(InputNode(name))

        self.output_nodes = []
        for i in range(outputs):
            name = "output_" + str(i)
            self.output_nodes.append(Node(name, activation))

        self.nodes = []
        self.edges = dict()

        self.node_innovation = 0
        self.edge_innovation = 0

        self.activation = activation

    def update_dependencies(self) -> None:
        for output_node in self.output_nodes:
            output_node.get_dependencies()

    def register_edge(self, start: Node, end: Node) -> Edge:
        """
        Registers a new edge between start and end nodes and updates the dependency graph.
        """

        assert (
            start.id != end.id), "Start and end of connection cannot be the same node"
        assert (not (end.id in start.required_nodes)
                ), "Connection would create cycle"

        hash = create_hash(start, end)
        if hash in self.edges:
            return self.edges[hash]
        else:
            # Register new edge
            edge = Edge(self.edge_innovation, start, end, 1)
            self.edge_innovation += 1
            self.edges[hash] = edge

            # Update dependency graph
            self.update_dependencies()
            return edge

    def register_node_between(self, start: Node, end: Node) -> Tuple[Node, Tuple[Edge, Edge]]:
        """
        Creates a new node on the specified edge. New edges between start, new_node, end are created.
        The old edge from start to end remains untouched.
        """

        hash = create_hash(start, end)

        assert hash in self.edges, "Edge does not exist"

        edge = self.edges[hash]
        if edge.mutate_to_id == None:
            innovation_number = self.node_innovation
            edge.mutate_to_id = innovation_number
            self.node_innovation += 1

            new_node = Node(innovation_number, self.activation)
            self.nodes.append(new_node)

            edge_left = self.register_edge(start, new_node)
            edge_right = self.register_edge(new_node, end)

        else:
            innovation_number = edge.mutate_to_id
            new_node = self.nodes[innovation_number]

            assert new_node.id == innovation_number, "Nodes should be indexed by innovation number"

            edge_left = self.edges[create_hash(start, new_node)]
            edge_right = self.edges[create_hash(new_node, end)]

        return (new_node, (edge_left, edge_right))

    def reset(self):
        for edge in self.edges.values():
            edge.active = False

        for node in self.nodes + self.output_nodes:
            node.active = False

    def foreward(self, inputs):
        # Reset cache of all nods before prediction
        for node in self.nodes + self.output_nodes:
            node.reset_cache()

        for x in range(len(inputs)):
            self.input_nodes[x].set_value(inputs[x])

        output = []
        for node in self.output_nodes:
            output.append(node.call())

        return np.array(output)

    def get_graph(self):
        self.update_dependencies()

        checked_nodes = [node.id for node in self.input_nodes]
        unchecked_nodes = self.nodes + self.output_nodes

        layers = [self.input_nodes]
        while unchecked_nodes != []:
            current_layer = []
            for node in unchecked_nodes:
                data_available = True
                for required in node.required_nodes:
                    if not (required in checked_nodes):
                        data_available = False
                        break

                if data_available:
                    checked_nodes.append(node.id)
                    unchecked_nodes.remove(node)

                    current_layer.append(node)

            layers.append(current_layer)

        G = nx.Graph()

        for x in reversed(range(len(layers))):
            layer = layers[x]

            for node in layer:
                G.add_node(node.id, layer=x)

        for edge in self.edges.values():
            G.add_edge(edge.input.id, edge.output.id)

        return G
