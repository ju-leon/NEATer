from neat.strategies.neat.graph.edge import Edge
from neat.strategies.neat.graph.node import Node


class NodeGene():
    def __init__(self, node: Node, bias: float, activation) -> None:
        self.node = node
        self.bias = bias
        self.activation = activation


class EdgeGene():
    def __init__(self, edge: Edge, weight: float) -> None:
        self.edge = edge
        self.weight = weight
