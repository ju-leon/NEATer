from _neat import InputNode, Node
from _neat import Network

import numpy as np
import uuid
from random import choice
from typing import List

import _neat


def decide(p):
    return np.random.choice([True, False], p=[p, 1-p])


class GenomeWrapper():
    def __init__(self, network: Network) -> None:
        self.network = network
        self.genome = _neat.Genome(network)

        self.p_mutate_node = 0.2
        self.p_mutate_connection = 0.2
        self.p_mutate_weight_shift = 0.2
        self.p_mutate_weight_random = 0.2
        self.p_mutate_toggle_connection = 0.2
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
        bias = np.random.normal(0, 1)
        self.genome.mutate_node(bias)

    def mutate_connection(self, scale=0.8) -> None:
        weight = np.random.normal(0, scale)
        self.genome.mutate_edge(weight)

    def mutate_weight_shift(self, scale=0.2):
        shift = np.random.normal(0, scale)
        self.genome.mutate_weight_shift(shift)

    def mutate_weight_random(self, scale=0.8):
        weight = np.random.normal(0, scale)
        self.genome.mutate_weight_random(weight)

    def mutate_toggle_connection(self):
        self.genome.mutate_toggle_connection()

    def mutate_bias_shift(self, scale=0.5):
        shift = np.random.normal(0, scale)
        self.genome.mutate_bias_shift(shift)

    def mutate_bias_random(self, scale=0.5):
        bias = np.random.normal(0, scale)
        self.genome.mutate_bias_random(bias)

    def mutate_disable_node(self):
        self.genome.mutate_disable_node()

    def crossbreed(self, genome2):
        child = GenomeWrapper(self.network)
        child.genome = self.genome.crossbreed(genome2.genome)

        return child

    def distance(self, genome2):
        dist = self.genome.distance(genome2.genome, 20, 1, 1, 1)
        return dist

    def apply(self):
        self.genome.apply()

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __repr__(self):
        return "[Genome: fitness={}]".format(self.fitness)
        # return "[edge_genes: {}, node_genes: {}]".format([gene.edge.id for gene in self.edge_genes], [gene.node.id for gene in self.node_genes])
