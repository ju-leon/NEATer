from neat.strategies.neat.graph.edge import Edge
from neat.strategies.neat.graph.node import Node
import numpy as np


class NodeGene():
    def __init__(self, node: Node) -> None:
        self.node = node

    def __repr__(self):
        return "NodeGene: node_id={}".format(self.node.id)


class EdgeGene():
    def __init__(self, edge: Edge, weight: float, disabled: bool = False) -> None:
        self.edge = edge
        self.weight = weight
        self.disabled = disabled

    def apply(self):
        self.edge.enabled = True
        self.edge.weight = self.weight

    def mutate(self, scale=1.0):
        self.weight += np.random.normal(scale=scale)
