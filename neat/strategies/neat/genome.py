from _neat import InputNode, Node
from _neat import Network

import numpy as np
import uuid
from random import choice
from typing import List

from neat.strategies.neat.genes import EdgeGene, NodeGene


def create_hash(start: NodeGene, end: NodeGene) -> str:
    return "{}->{}".format(start.node.get_id(), end.node.get_id())


def create_edge_hash(edge_gene: EdgeGene) -> str:
    return "{}->{}".format(edge_gene.edge.input.get_id(), edge_gene.edge.output.get_id())


def decide(probability: float) -> bool:
    return np.random.choice([True, False], p=[probability, 1 - probability])


class Genome():
    def __init__(self, graph: Network) -> None:
        self.graph = graph

        self.input_genes = []
        for node in graph.get_input_nodes():
            self.input_genes.append(NodeGene(node, 0))

        self.output_genes = []
        for node in graph.get_output_nodes():
            self.output_genes.append(NodeGene(node, 0))

        self.node_genes = []
        self.edge_genes = []

        self.p_mutate_node = 0.1
        self.p_mutate_connection = 0.5
        self.p_mutate_weight_shift = 0.7
        self.p_mutate_weight_random = 0.1
        self.p_mutate_toggle_connection = 0.5
        self.p_mutate_bias = 0.1
        self.p_mutate_toggle_node = 0.1

        self.fitness = 0

    def mutate(self) -> None:
        if decide(self.p_mutate_node):
            self.mutate_node()

        if decide(self.p_mutate_connection):
            self.mutate_connection()

        if decide(self.p_mutate_weight_shift):
            self.mutate_weight_shift()

        if decide(self.p_mutate_weight_random):
            self.mutate_weight_random()

        if decide(self.p_mutate_toggle_connection):
            self.mutate_toggle_connection()

        if decide(self.p_mutate_bias):
            self.mutate_bias_shift()

        if decide(self.p_mutate_toggle_node):
            self.mutate_disable_node()

    def mutate_node(self) -> None:
        if len(self.edge_genes) > 0:
            edge_gene = choice(self.edge_genes)
            self.edge_genes.remove(edge_gene)

            edge_left, node, edge_right = self.graph.register_node(
                edge_gene.edge.get_input().get_id(), edge_gene.edge.get_output().get_id())

            # Abort if the edge selected does not exist
            if edge_left == None:
                print("SELECTED ILLEGAL EDGE")
                return

            if not node.get_id() in [node_gene.node.get_id() for node_gene in self.node_genes]:
                # TODO: Make init parameter
                self.node_genes.append(NodeGene(node, np.random.normal(0, 1)))

            if not edge_left.get_id() in [edge_gene.edge.get_id() for edge_gene in self.edge_genes]:
                left_gene = EdgeGene(edge_left, weight=1)
                self.edge_genes.append(left_gene)

            if not edge_right.get_id() in [edge_gene.edge.get_id() for edge_gene in self.edge_genes]:
                right_gene = EdgeGene(edge_right, weight=edge_gene.edge.weight)
                self.edge_genes.append(right_gene)

    def mutate_connection(self, scale=0.8) -> None:
        start = choice(self.node_genes + self.input_genes)
        end = choice(self.node_genes + self.output_genes)

        edge = self.graph.register_edge(start.node.get_id(), end.node.get_id())

        # Only mutate connection if it does not create a cycle
        if edge != None:
            # TODO: How to init weights?
            edgeGene = EdgeGene(edge, weight=np.random.normal(scale=scale))

            self.edge_genes.append(edgeGene)

    def mutate_weight_shift(self, scale=0.2):
        if len(self.edge_genes) > 0:
            edgeGene = choice(self.edge_genes)
            edgeGene.weight += np.random.normal(scale=scale)

    def mutate_weight_random(self, scale=0.8):
        if len(self.edge_genes) > 0:
            edgeGene = choice(self.edge_genes)
            edgeGene.weight = np.random.normal(scale=scale)

    def mutate_toggle_connection(self):
        if len(self.edge_genes) > 0:
            edgeGene = choice(self.edge_genes)
            edgeGene.disabled = not edgeGene.disabled

    def mutate_bias_shift(self, scale=0.5):
        if len(self.node_genes + self.output_genes) > 0:
            nodeGene = choice(self.node_genes + self.output_genes)
            nodeGene.bias = np.random.normal(scale=scale)

    def mutate_disable_node(self):
        if len(self.node_genes) > 0:
            nodeGene = choice(self.node_genes + self.output_genes)
            nodeGene.disabled = True

    def apply(self):
        for edge_gene in self.edge_genes:
            edge_gene.apply()

        for node_gene in self.node_genes + self.output_genes:
            node_gene.apply()

    def __lt__(self, other):
        """
        Compare the fitness of two genomes.
        """
        return self.fitness < other.fitness

    def __repr__(self):
        return "[Genome: fitness={}]".format(self.fitness)
        # return "[edge_genes: {}, node_genes: {}]".format([gene.edge.id for gene in self.edge_genes], [gene.node.id for gene in self.node_genes])
