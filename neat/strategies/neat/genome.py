from random import choice
from neat.strategies.neat.graph import node
from neat.strategies.neat.graph.edge import Edge
from neat.strategies.neat.graph.node import InputNode, Node
import numpy as np


def relu(x):
    return max(0, x)


class Genome():
    def __init__(self, inputs, outputs) -> None:
        self.input_nodes = []
        for i in range(inputs):
            name = "input_" + str(i)
            self.input_nodes.append(InputNode(name))

        self.output_nodes = []
        for i in range(outputs):
            name = "output_" + str(i)
            self.output_nodes.append(Node(name, relu))

        self.nodes = []
        self.edges = []

        self.counter = 0

    def add_edge(self, input, output):
        self.edges.append(Edge(input, output, 1))

    def mutate_connection(self):
        start = choice(self.nodes + self.input_nodes)
        end = choice(self.nodes + self.output_nodes)

        if (start != end) and not (end.id in start.required_nodes):
            edge = Edge(start, end, 1)
            self.edges.append(edge)

    def mutate_node(self):
        if self.edges != []:
            edge = choice(self.edges)

            name = "inner_" + str(self.counter)
            new_node = Node(name, relu)
            new_node.layer_hierarchy = edge.input.layer_hierarchy
            new_edge = Edge(edge.input, new_node, 1)
            edge.change_input(new_node)

            #print("New edges:")
            # print(new_edge)
            # print(edge)

            self.nodes.append(new_node)
            self.edges.append(new_edge)
            self.counter += 1

    def foreward(self, inputs):
        # Reset cache of all nods before prediction
        for node in self.nodes + self.output_nodes:
            node.reset_cache()

        for x in range(len(inputs)):
            self.input_nodes[x].set_value(inputs[x])

        output = []
        for node in self.output_nodes:
            output.append(node.call()[0])

        return np.array(output)
