from neat.strategies.neat.network import Network
from neat.strategies.neat.genome import Genome
from neat.strategies.neat.genes import EdgeGene, NodeGene
from random import choice

from neat.strategies.strategy import Strategy
from itertools import zip_longest
import copy
import numpy as np
from tqdm import tqdm
import random

# TODO: MOVE TO TENSORFLOW ACTIVATION


def relu(x):
    return max(0, x)


class Neat(Strategy):

    def __init__(self, population_size=5) -> None:
        self.population_size = population_size

        self.p_mutate_weight = 0.5
        self.p_mutate_node = 0.5
        self.p_mutate_connection = 0.8

        self.node_innovation_number = 0
        self.edge_innovation_number = 0

        self.num_survivors = 10

    def init_population(self, input_shape, output_shape) -> None:
        self.input_size = input_shape  # .flatten()
        self.output_size = output_shape  # .flatten()

        self.network = Network(self.input_size, self.output_size, relu)

        self.population = []
        for _ in range(self.population_size):
            self.population.append(Genome(self.network))

    def solve_epoch(self, env, epoch_len, discrete):
        # Evaluate all individuals
        rewards = []
        for genome in tqdm(self.population):
            self.network.reset()
            genome.apply()
            current_reward = 0
            observation = env.reset()
            for _ in range(epoch_len):
                pred = self.network.foreward(observation)
                if discrete:
                    pred = np.argmax(pred)

                observation, reward, done, info = env.step(pred)
                current_reward += reward
                if done:
                    break

            rewards.append(current_reward)

            genome.mutate()

        rewards = np.array(rewards)

        """
        # Crossbreed the best individuals
        # Negative for descending
        idx = np.argsort(-rewards)

        survivors = [self.population[x] for x in idx[:self.num_survivors]]
        self.best_network = self.population[idx[0]]

        self.population = [self.best_network]
        for parent1 in random.sample(survivors, 3):
            for parent2 in random.sample(survivors, 3):
                child = self.crossbreed(parent1, parent2)

                if np.random.choice([True, False], p=[self.p_mutate_weight, 1-self.p_mutate_weight]):
                    child.mutate()

                if np.random.choice([True, False], p=[self.p_mutate_connection, 1-self.p_mutate_connection]):
                    edge = self.network.mutate_connection()
                    if edge == None:
                        continue
                    edgeGene = EdgeGene(
                        edge.id, edge, np.random.normal(scale=1.0))
                    child.add_edge(edgeGene)

                if np.random.choice([True, False], p=[self.p_mutate_node, 1-self.p_mutate_node]):
                    node, edge = self.network.mutate_node()
                    if node == None:
                        continue
                    nodeGene = NodeGene(node.id, node, bias=0, activation=relu)
                    edgeGene = EdgeGene(
                        edge.id, edge, np.random.normal(scale=1.0))
                    child.add_edge(edgeGene)
                    child.add_node(nodeGene)

                self.network.update_dependencies()
                print(child)
                self.population.append(child)

        print("NUM_NODES: {}, NUM_EDGES: {}".format(
            len(self.network.nodes), len(self.network.edges)))

        print(self.network.edges)
        """

        return rewards


    """
    def crossbreed(self, individual1, individual2):
        child = Individual()

        ####
        # EDGES
        ####
        index1 = 0
        index2 = 0
        # Iterate over all edge genes. Randomly select edges from parent1 or parent2
        while index1 < len(individual1.edge_genes) and index2 < len(individual2.edge_genes):
            if individual1.edge_genes[index1].id == individual2.edge_genes[index2].id:
                edge_gene = choice([individual1.edge_genes[index1],
                                    individual2.edge_genes[index2]])
                # Shallow copy to preserve references to main genome
                edge_gene = copy.copy(edge_gene)
                child.add_edge(edge_gene)

                index1 += 1
                index2 += 1
            elif individual1.edge_genes[index1].id < individual2.edge_genes[index2].id:
                edge_gene = copy.copy(individual1.edge_genes[index1])

                # Choose weather to keep this gene or not
                if choice([True, False]):
                    child.add_edge(edge_gene)

                index1 += 1
            elif individual1.edge_genes[index1].id > individual2.edge_genes[index2].id:
                edge_gene = copy.copy(individual2.edge_genes[index2])

                # Choose weather to keep this gene or not
                if choice([True, False]):
                    child.add_edge(edge_gene)

                index2 += 1
        # For the genome with more genes, randomly add some of the remaining
        while index1 < len(individual1.edge_genes) or index2 < len(individual2.edge_genes):
            if index1 < len(individual1.edge_genes):
                edge_gene = copy.copy(individual1.edge_genes[index1])

                # Choose weather to keep this gene or not
                if choice([True, False]):
                    child.add_edge(edge_gene)

                index1 += 1
            elif index2 < len(individual2.edge_genes):
                edge_gene = copy.copy(individual2.edge_genes[index2])

                # Choose weather to keep this gene or not
                if choice([True, False]):
                    child.add_edge(edge_gene)

                index2 += 1

        ####
        # NODES
        ####
        index1 = 0
        index2 = 0
        # Iterate over all node genes. Randomly select nodes from parent1 or parent2
        while index1 < len(individual1.node_genes) and index2 < len(individual2.node_genes):
            if individual1.node_genes[index1].id == individual2.node_genes[index2].id:
                node_gene = choice(
                    [individual1.node_genes[index1], individual2.node_genes[index2]])
                # Shallow copy to preserve references to main genome
                node_gene = copy.copy(node_gene)
                child.add_node(node_gene)

                index1 += 1
                index2 += 1
            elif individual1.node_genes[index1].id < individual2.node_genes[index2].id:
                node_gene = copy.copy(individual1.node_genes[index1])

                # Choose weather to keep this gene or not
                if choice([True, False]):
                    child.add_node(node_gene)

                index1 += 1
            elif individual1.node_genes[index1].id > individual2.node_genes[index2].id:
                node_gene = copy.copy(individual2.node_genes[index2])

                # Choose weather to keep this gene or not
                if choice([True, False]):
                    child.add_node(node_gene)

                index2 += 1

        # For the genome with more genes, randomly add some of the remaining
        while index1 < len(individual1.node_genes) or index2 < len(individual2.node_genes):
            if index1 < len(individual1.node_genes):
                node_gene = copy.copy(individual1.node_genes[index1])

                # Choose weather to keep this gene or not
                if choice([True, False]):
                    child.add_node(node_gene)

                index1 += 1
            elif index2 < len(individual2.node_genes):
                node_gene = copy.copy(individual2.node_genes[index2])

                # Choose weather to keep this gene or not
                if choice([True, False]):
                    child.add_node(node_gene)

                index2 += 1

        return child

    """

    def get_best_network(self):
        self.best_network.apply()
        return self.network
