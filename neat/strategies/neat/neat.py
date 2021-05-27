from neat.strategies.neat.species import Species
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

    def __init__(self, population_size=5, max_genetic_distance=4.0) -> None:
        self.population_size = population_size

        self.node_innovation_number = 0
        self.edge_innovation_number = 0

        self.num_survivors = 10

        self.max_genetic_distance = max_genetic_distance

    def init_population(self, env, input_shape, output_shape) -> None:
        self.env = env

        self.input_size = input_shape  # .flatten()
        self.output_size = output_shape  # .flatten()

        self.network = Network(self.input_size, self.output_size, relu)

        self.unassigned_genomes = []

        # Start with a single species containing all genomes of the current population
        self.species = [Species(self.network, env, Genome(self.network))]
        for _ in range(self.population_size):
            genome = Genome(self.network)
            genome.mutate()

            self.species[0].add_genome(genome)

    def solve_epoch(self, epoch_len, discrete, offset):
        # Assign all individuals to their species
        self.assign_species()

        # Evaluate all species
        rewards = []
        for species in tqdm(self.species):
            reward = species.evaluate(epoch_len, discrete, offset)
            rewards.append(reward)

        self.best_genome = self.species[np.argmax(rewards)].genomes[0]

        self.remove_extinct_species()
        self.kill_underperformer()

        self.reproduce()
        self.mutate()

        data = dict()

        data["rewards"] = np.array(rewards)
        data["num_species"] = len(self.species)
        return data

    def mutate(self):
        for species in self.species:
            species.mutate()

        for genome in self.unassigned_genomes:
            genome.mutate()

    def reproduce(self, fertility=0.8):
        number_genomes = len(self.unassigned_genomes)
        for species in self.species:
            number_genomes += len(species.genomes)

        allowed_offspring = self.population_size - number_genomes

        # The better a species performs, the more offspring it's allowed to produce
        self.species.sort()
        for species in self.species:
            allowed_offspring /= 2
            species.reproduce(int(allowed_offspring))

    def kill_underperformer(self, percentage=0.2):
        for species in self.species:
            species.kill_percentage(percentage)

    def remove_extinct_species(self, extinction_threshold=1):
        """
        Remove all species with fewer genomes than extinction_threshold.
        #TODO: Keep genomes from extinct species or let them die with the species?
        """
        # self.species = [species for species in self.species if len(
        #    species.genomes) > extinction_threshold]

        surviving_species = []
        for species in self.species:
            if len(species.genomes) > extinction_threshold:
                surviving_species.append(species)
            else:
                pass
                #self.unassigned_genomes += species.genomes

        self.species = surviving_species

        if len(self.species) == 0:
            print("EXTINCT")
            # TODO: Response to extinction?

    def assign_species(self):
        genomes = self.unassigned_genomes
        for species in self.species:
            genomes = genomes + species.reset()

        for genome in genomes:
            # If genome is already assigned to a a species do nothing
            # Should not happend with current architecture
            if genome.species != None:
                print("EROROROROROROR?")
                continue

            assigned = False
            for species in self.species:
                distance = species.distance(genome)
                if distance < self.max_genetic_distance:
                    species.add_genome(genome)
                    assigned = True
                    break

            if not assigned:
                new_species = Species(self.network, self.env, genome)
                self.species.append(new_species)

    def get_best_network(self):
        self.best_genome.apply()
        return self.network
