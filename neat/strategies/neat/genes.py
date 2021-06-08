from _neat import Edge
from _neat import Node
import numpy as np


class NodeGene():
    def __init__(self, node: Node, bias: float, disabled: bool = False) -> None:
        self.node = node
        self.bias = bias
        self.disabled = disabled

    def apply(self):
        if not self.disabled:
            self.node.active = True
            self.node.bias = self.bias
        else:
            self.node.active = False
            self.node.bias = self.bias

    def __repr__(self):
        return "NodeGene: node_id={}".format(self.node.id)


class EdgeGene():
    def __init__(self, edge: Edge, weight: float, disabled: bool = False) -> None:
        self.edge = edge
        self.weight = weight
        self.disabled = disabled

    def apply(self):
        if not self.disabled:
            self.edge.active = True
            self.edge.weight = self.weight
        else:
            self.edge.active = False
            self.edge.weight = self.weight
