from neat.strategies.neat.genes import EdgeGene, NodeGene
from typing import List
from neat.strategies.neat.graph.node import InputNode, Node
from neat.strategies.neat.network import Network
from random import choice


def create_hash(start: NodeGene, end: NodeGene) -> str:
    return "{}->{}".format(start.node.id, end.node.id)


def create_edge_hash(edge_gene: EdgeGene) -> str:
    return "{}->{}".format(edge_gene.edge.input.id, edge_gene.edge.output.id)


class Genome():
    def __init__(self, graph: Network) -> None:
        self.graph = graph

        self.input_genes = []
        for node in graph.input_nodes:
            self.input_genes.append(NodeGene(node))

        self.output_genes = []
        for node in graph.output_nodes:
            self.output_genes.append(NodeGene(node))

        self.node_genes = []
        self.edge_genes = []

    def mutate(self) -> None:
        start = choice(self.node_genes + self.input_genes)
        end = choice(self.node_genes + self.output_genes)
        if start != end and not (end.node.id in start.node.required_nodes):
            # If a connection that already exists in this genome is selected, mutate a node on this connection
            edge_gene_ids = [(edge_gene.edge.input.id, edge_gene.edge.output.id)
                             for edge_gene in self.edge_genes]
            if (start.node.id, end.node.id) in edge_gene_ids:
                self.mutate_node_between(
                    start, end, edge_gene_ids.index((start.node.id, end.node.id)))
            # Otherwise add this connection
            else:
                self.mutate_connection(start, end)

    def mutate_node_between(self, start, end, index) -> None:
        edge_gene = self.edge_genes[index]
        del self.edge_genes[index]

        node, (edge_left, edge_right) = self.graph.register_node_between(
            start.node, end.node)

        self.node_genes.append(NodeGene(node))

        left_gene = EdgeGene(edge_left, weight=1)
        self.edge_genes.append(left_gene)

        right_gene = EdgeGene(edge_right, weight=edge_gene.edge.weight)
        self.edge_genes.append(right_gene)

    def mutate_connection(self, start: NodeGene, end: NodeGene) -> None:
        edge = self.graph.register_edge(start.node, end.node)

        # TODO: How to init weights?
        edgeGene = EdgeGene(edge, 1)

        self.edge_genes.append(edgeGene)

    def apply(self):
        for edge_gene in self.edge_genes:
            edge_gene.apply()

    def __repr__(self):
        return "[edge_genes: {}, node_genes: {}]".format([gene.edge.id for gene in self.edge_genes], [gene.node.id for gene in self.node_genes])
