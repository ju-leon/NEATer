from neat.strategies.neat.genes import EdgeGene, NodeGene
from neat.strategies.neat.individual import Individual
from random import choice

from neat.strategies.neat.genome import Genome
from neat.strategies.strategy import Strategy
from itertools import zip_longest
import copy
import numpy as np


class Neat(Strategy):

    def __init__(self, population_size=5) -> None:
        self.population_size = population_size
        self.p_mutate_node = 0.1
        self.p_mutate_connection = 0.1

    def init_population(self, input_shape, output_shape) -> None:
        self.input_size = input_shape.flatten()
        self.output_size = output_shape.flatten()

        self.network = Genome(self.input_size, self.output_size)

        self.population = []
        for _ in range(self.population_size):
            self.population.append(Individual())

    def solve_epoch(self, env, epoch_len, discrete):
        for individual in self.population:
            if np.random.choice([True, False], p=[self.p_mutate_connection, 1-self.p_mutate_connection]):
                edge = self.network.mutate_connection()
                edgeGene = EdgeGene(edge, np.random.normal(size=(1,)))
                individual.add_edge(edgeGene)

            if np.random.choice([True, False], p=[self.p_mutate_node, 1-self.p_mutate_node]):
                node, edge = self.network.mutate_node()
                nodeGene = NodeGene(node, bias=0, activation=None)
                edgeGene = EdgeGene(edge, np.random.normal(size=(1,)))
                individual.add_edge(edgeGene)
                individual.add_node(nodeGene)
        
        

    def crossbreed(self, genome1, genome2):
        pass
