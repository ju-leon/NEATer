from neat.strategies.neat.graph.edge import Edge
from neat.strategies.neat.graph.node import Node
import numpy as np


class NodeGene():
    def __init__(self, id: int, node: Node, bias: float, activation) -> None:
        self.id = id
        self.node = node
        self.bias = bias
        self.activation = activation

    def apply(self):
        self.node.activation = self.activation
        self.node.bias = self.bias


class EdgeGene():
    def __init__(self, id: int, edge: Edge, weight: float) -> None:
        self.id = id
        self.edge = edge
        self.weight = weight

    def apply(self):
        self.edge.enabled = True
        self.edge.weight = self.weight

    def mutate(self, scale=1.0):
        self.weight += np.random.normal(scale=scale)
