from neat.strategies.neat.network import Network
from neat.strategies.neat.genes import NodeGene
from neat.strategies.neat.genome import Genome
import numpy as np
from random import choice


class Species():
    def __init__(self, network: Network, genome: Genome):
        self.network = network
        self.best_genome = genome

    def distance(self, genome: Genome, gene_normalize_threshold=20, c1=1, c2=1, c3=1) -> float:
        # Make sure genome1 always has the highest invoation number
        if genome.edge_genes[-1].edge.id < self.best_genome.edge_genes[-1].edge.id:
            genome1 = self.best_genome
            genome2 = genome
        else:
            genome1 = genome
            genome2 = self.best_genome

        weight_diff = 0
        num_similar = 0
        num_disjoint = 0

        index1 = 0
        index2 = 0
        while index1 < len(self.best_genome.edge_genes) and index2 < len(self.best_genome.edge_genes):
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
            elif gene1.edge.id > gene2.edge.id:
                num_disjoint += 1
                index2 += 1

        weight_diff = weight_diff / num_similar
        num_excess = len(genome1.edge_genes) - index1

        N = np.max(len(genome1.edge_genes), len(genome2.edge_genes))
        if N < gene_normalize_threshold:
            N = 1

        return (c1 * num_disjoint / N) + (c2 * num_excess / N) + (c3 * weight_diff)

    def crossbreed(self, genomeA, genomeB):
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
        while index1 < len(self.best_genome.edge_genes) and index2 < len(self.best_genome.edge_genes):
            gene1 = genome1.edge_genes[index1]
            gene2 = genome2.edge_genes[index2]
            if gene1.edge.id == gene2.edge.id:
                if choice([True, False]):
                    child.edge_genes.append(gene1)
                    child_nodes.add(gene1.edge.input)
                    child_nodes.add(gene1.edge.output)
                else:
                    child.edge_genes.append(gene2)
                    child_nodes.add(gene2.edge.input)
                    child_nodes.add(gene2.edge.output)

                index1 += 1
                index2 += 1
            # TODO: Randomly chose if disjoin gene is kept or not
            elif gene1.edge.id < gene2.edge.id:
                # Disjoint genes of genome1
                index1 += 1
            elif gene1.edge.id > gene2.edge.id:
                # Disjoint genes of genome2
                child.edge_genes.append(gene2)
                index2 += 1

        # Append excess genes
        while index1 < len(self.best_genome.edge_genes):
            child.edge_genes.append(genome1.edge_genes[index1])

        # Add all required nodes
        for node in list(child_nodes):
            child.node_genes.append(NodeGene(node))
