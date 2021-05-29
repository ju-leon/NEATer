from typing import List
from neat.strategies.neat.network import Network
from neat.strategies.neat.genome import Genome
from neat.strategies.neat.genes import NodeGene
import numpy as np
from random import choice
from gym import Env
import copy


def copy_gene(gene):
    return copy.copy(gene)


class Species():
    def __init__(self, network: Network, env: Env,  genome):
        self.network = network
        self.env = env
        self.genomes = [genome]

        self.fitness = 0
        self.fitness_max = 0

    def add_genome(self, genome) -> None:
        self.genomes.append(genome)

    def evaluate(self, epoch_len, discrete=True, offset=0, render=False):
        """
        Evaluate the fitness of all genomes in the species.
        """
        self.fitness = 0
        self.fitness_max = 0.0
        for genome in self.genomes:
            self.network.reset()
            genome.apply()
            current_reward = offset

            observation = self.env.reset()
            for _ in range(epoch_len):
                pred = self.network.foreward(observation)
                if discrete:
                    pred = np.argmax(pred)
                if render:
                    self.env.render()

                observation, reward, done, info = self.env.step(pred)
                current_reward += reward
                if done:
                    break

            genome.fitness = current_reward

            self.fitness_max = max(self.fitness_max, current_reward)
            self.fitness += current_reward

        self.fitness = self.fitness / len(self.genomes)
        if self.fitness < 0:
            print("\033[93m Warning: Negative rewards are harmful to species performance. Please specify an offset to prevent negative rewards. \033[0m")

        # The best genome always leads the species
        self.genomes.sort()
        self.genomes = list(reversed(self.genomes))

        return self.fitness

    def reproduce(self, amount):
        for _ in range(amount):
            parent1 = choice(self.genomes)
            parent2 = choice(self.genomes)

            if parent1 != parent2:
                child = self.crossbreed(parent1, parent2)

                if child != None:
                    self.genomes.append(child)

    def mutate(self):
        for genome in self.genomes:
            genome.mutate()

    def reset(self) -> List:
        # Select random element to keep in species
        head = choice(self.genomes)

        # Remove all other elements from species
        self.genomes.remove(head)
        unassigned_genomes = self.genomes
        for genome in unassigned_genomes:
            genome.species = None

        self.genomes = [head]

        return unassigned_genomes

    def kill_percentage(self, percentage) -> None:
        """
        Kill the genomes with the lowest fitness in the population
        """
        self.genomes.sort()

        index = int(len(self.genomes) * percentage)
        self.genomes = list(reversed(self.genomes[index:]))

    def distance(self, genome, gene_normalize_threshold=20, c1=1.0, c2=1.0, c3=1.0) -> float:
        best_genome = self.genomes[0]

        if len(genome.edge_genes) == 0 or len(best_genome.edge_genes) == 0:
            return 1.0

        # Make sure genome1 always has the highest invoation number
        if genome.edge_genes[-1].edge.id < best_genome.edge_genes[-1].edge.id:
            genome1 = best_genome
            genome2 = genome
        else:
            genome1 = genome
            genome2 = best_genome

        weight_diff = 0.0
        num_similar = 0
        num_disjoint = 0

        index1 = 0
        index2 = 0
        while index1 < len(genome1.edge_genes) and index2 < len(genome2.edge_genes):
            gene1 = genome1.edge_genes[index1]
            gene2 = genome2.edge_genes[index2]
            if gene1.edge.id == gene2.edge.id:
                weight_diff += np.abs(gene1.weight - gene2.weight)
                num_similar += 1
                index1 += 1
                index2 += 1
            elif gene1.edge.id < gene2.edge.id:
                num_disjoint += 1
                index1 += 1
            else:
                num_disjoint += 1
                index2 += 1

        if num_similar != 0:
            weight_diff = weight_diff / num_similar

        num_excess = len(genome1.edge_genes) - index1

        N = max(len(genome1.edge_genes), len(genome2.edge_genes))
        if N < gene_normalize_threshold:
            N = 1.0

        return (c1 * num_disjoint / N) + (c2 * num_excess / N) + (c3 * weight_diff)

    def crossbreed(self, genomeA, genomeB) -> Genome:
        if len(genomeA.edge_genes) == 0 or len(genomeB.edge_genes) == 0:
            return

        child = Genome(self.network)

        # Make sure genome1 always has the highest invoation number
        if genomeA.edge_genes[-1].edge.id < genomeB.edge_genes[-1].edge.id:
            genome1 = genomeB
            genome2 = genomeA
        else:
            genome1 = genomeA
            genome2 = genomeB

        child_nodes = set()

        index1 = 0
        index2 = 0
        while index1 < len(genome1.edge_genes) and index2 < len(genome2.edge_genes):
            # TODO: COPY GENES!!!!!!(/!/!/!/!/!/!/!)
            gene1 = genome1.edge_genes[index1]
            gene2 = genome2.edge_genes[index2]
            if gene1.edge.id == gene2.edge.id:
                if choice([True, False]):
                    child.edge_genes.append(copy_gene(gene1))
                    child_nodes.add(gene1.edge.input)
                    child_nodes.add(gene1.edge.output)
                else:
                    child.edge_genes.append(copy_gene(gene2))
                    child_nodes.add(gene2.edge.input)
                    child_nodes.add(gene2.edge.output)

                index1 += 1
                index2 += 1
            # TODO: Randomly chose if disjoin gene is kept or not
            elif gene1.edge.id < gene2.edge.id:
                # Disjoint genes of genome1
                index1 += 1
            else:
                # Disjoint genes of genome2
                child.edge_genes.append(copy_gene(gene2))
                index2 += 1

        # Append excess genes
        while index1 < len(genome1.edge_genes):
            child.edge_genes.append(copy_gene(genome1.edge_genes[index1]))

            child_nodes.add(genome1.edge_genes[index1].edge.input)
            child_nodes.add(genome1.edge_genes[index1].edge.output)

            index1 += 1

        # Add all required nodes
        for node in list(child_nodes):
            name = str(node.id)
            if not (name.startswith("input") or name.startswith("output")):
                child.node_genes.append(copy_gene(NodeGene(node)))

        return child

    def __lt__(self, other):
        """
        Compare the fitness of two species.
        """
        return self.fitness < other.fitness

    def __repr__(self):
        return "Species: genomes={}, fitness={}".format(len(self.genomes), self.fitness)
