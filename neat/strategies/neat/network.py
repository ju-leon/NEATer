from typing import List, Tuple
from neat.strategies.neat.genes import EdgeGene, NodeGene
from random import choice
from neat.strategies.neat.graph import node
from neat.strategies.neat.graph.edge import Edge
from neat.strategies.neat.graph.node import InputNode, Node
import numpy as np


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

        new_node = Node(self.node_innovation, self.activation)
        self.nodes.append(new_node)
        self.node_innovation += 1

        edge_left = self.register_edge(start, new_node)
        edge_right = self.register_edge(new_node, end)

        return (new_node, (edge_left, edge_right))

    """
    TODO: Move to individual
    def mutate_connection(self) -> Edge:
        start = choice(self.nodes + self.input_nodes)
        end = choice(self.nodes + self.output_nodes)

        if (start != end) and not (end.id in start.required_nodes):
            edge = Edge(self.edge_conter, start, end, 1)
            self.edge_conter += 1
            self.edges[create_hash(edge)] = edge

            return edge
        else:
            return None

    def mutate_node(self):
        if self.edges != []:
            edge = choice(self.edges)

            new_node = Node(self.node_conter, relu)
            self.node_conter += 1
            new_node.layer_hierarchy = edge.input.layer_hierarchy

            new_edge = Edge(self.edge_conter, edge.input, new_node, 1)
            self.edge_conter += 1
            edge.change_input(new_node)

            #print("New edges:")
            # print(new_edge)
            # print(edge)

            self.nodes.append(new_node)
            self.edges.append(new_edge)

            return new_node, new_edge
        else:
            return None, None
    """

    def reset(self):
        for edge in self.edges.values():
            edge.enabled = False

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
