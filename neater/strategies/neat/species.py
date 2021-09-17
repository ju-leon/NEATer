from typing import List
from _neat import Network
from neater.strategies.neat.genome import GenomeWrapper
from neater.strategies.neat.genes import NodeGene
import numpy as np
from random import choice
from gym import Env
import copy
import uuid


def copy_gene(gene):
    return copy.copy(gene)


class Species():
    def __init__(self, network: Network, env: Env,  genome, discrete=True, **kwargs):
        self.network = network
        self.env = env
        self.genomes = [genome]

        self.fitness = 0
        self.fitness_max = 0

        self.discrete = discrete

        self.id = str(uuid.uuid4())

    def add_genome(self, genome) -> None:
        self.genomes.append(genome)

    def evaluate(self, epoch_len, render=False):
        """
        Evaluate the fitness of all genomes in the species.
        """
        self.fitness = 0
        self.fitness_max = float("-inf")

        genome_fitness = []
        for genome in self.genomes:
            self.network.reset()
            genome.apply()
            current_reward = 0

            observation = self.env.reset()
            for _ in range(epoch_len):
                pred = self.network.forward(np.append(observation, [1]))

                if self.discrete:
                    pred = np.argmax(pred)
                if render:
                    self.env.render()

                observation, reward, done, info = self.env.step(pred)
                current_reward += reward
                if done:
                    break

            genome.fitness = current_reward

            genome_fitness.append(current_reward)

            self.fitness_max = max(self.fitness_max, current_reward)
            self.fitness += current_reward

        # self.fitness = self.fitness / len(self.genomes)

        return genome_fitness

    def reproduce(self, amount, stud=True):
        for _ in range(amount):
            if stud and len(self.genomes) > 1:

                num_genomes = len(self.genomes)

                propa1 = np.linspace(1.3, 0.7, num=num_genomes)
                propa1 /= np.sum(propa1)

                propa2 = np.linspace(1.3, 0.7, num=num_genomes - 1)
                propa2 /= np.sum(propa2)

                available = np.arange(0, len(self.genomes))

                index1 = np.random.choice(
                    available, p=propa1)

                available = np.delete(available, index1)

                index2 = np.random.choice(
                    available, p=propa2)
                parent1 = self.genomes[index1]
                parent2 = self.genomes[index2]

                #parent1 = self.genomes[0]
                #parent2 = choice(self.genomes)
            else:
                parent1 = choice(self.genomes)
                parent2 = choice(self.genomes)

            if parent1 != parent2:
                child = parent1.crossbreed(parent2)

                if child != None:
                    child.mutate()

                    self.genomes.append(child)

    def mutate(self, p):
        for genome in self.genomes:
            if np.random.choice([True, False], p=[p, 1-p]):
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

    def __lt__(self, other):
        """
        Compare the fitness of two species.
        """
        return self.fitness < other.fitness

    def __repr__(self):
        return "Species: genomes={:10.3f}, fitness={:10.3f}".format(len(self.genomes), self.fitness)
