from numpy.core.fromnumeric import argmax
from neat.strategies.neat.species import Species
from _neat import Network
from neat.strategies.neat.genome import GenomeWrapper
from random import choice

from neat.strategies.strategy import Strategy
from itertools import zip_longest
import copy
import numpy as np
from tqdm import tqdm
import random
from operator import attrgetter

# TODO: MOVE TO TENSORFLOW ACTIVATION


class Neat(Strategy):

    def __init__(self, activation, population_size=5, max_genetic_distance=6) -> None:
        self.activation = activation

        self.population_size = population_size

        self.node_innovation_number = 0
        self.edge_innovation_number = 0

        self.num_survivors = 10

        self.max_genetic_distance = max_genetic_distance

    def init_population(self, env, input_shape, output_shape) -> None:
        self.env = env

        self.input_size = input_shape  # .flatten()
        self.output_size = output_shape  # .flatten()

        self.network = Network(
            self.input_size, self.output_size)  # TODO: Pass AF, self.activation)

        self.unassigned_genomes = []

        # Start with a single species containing all genomes of the current population
        self.species = [
            Species(self.network, env, GenomeWrapper(self.network))]
        for _ in range(self.population_size):
            genome = GenomeWrapper(self.network)
            genome.mutate()
            self.species[0].add_genome(genome)

    def solve_epoch(self, epoch_len, discrete, offset, render=False):



        # Reset the best genome every generation. This is important in gyms with randomness
        self.best_genome = None

        # Evaluate all species
        rewards = []
        for species in self.species:
            reward = species.evaluate(epoch_len, discrete, offset, render)
            rewards.append(reward)

            if self.best_genome == None or species.genomes[0].fitness >= self.best_genome.fitness:
                self.best_genome = species.genomes[0]

            print("Best Genome: {}, Population Fitness: {}, Max Fitness: {}, Size: {}".format(
                species.genomes[0].fitness,
                species.fitness,
                species.fitness_max,
                len(species.genomes),
            ))

        # Assign all individuals to their species
        self.assign_species()
        self.kill_underperformer()
        self.remove_extinct_species()

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

    def reproduce(self):
        number_genomes = len(self.unassigned_genomes)
        for species in self.species:
            number_genomes += len(species.genomes)

        allowed_offspring = self.population_size - number_genomes

        print("Genomes Alive: {}, Allowed Offspring: {}".format(
            number_genomes, allowed_offspring))

        allowed_offspring = max(0, allowed_offspring)
        # The better a species performs, the more offspring it's allowed to produce
        self.species.sort()
        for species in reversed(self.species):
            allowed_offspring /= 2

            # Allow every species at least one offspring
            species.reproduce(int(allowed_offspring) + 1)

    def kill_underperformer(self, percentage=0.5):
        for species in self.species:
            species.kill_percentage(percentage)

    def remove_extinct_species(self, extinction_threshold=2):
        """
        Remove all species with fewer genomes than extinction_threshold.
        #TODO: Keep genomes from extinct species or let them die with the species?
        """
        # self.species = [species for species in self.species if len(
        #    species.genomes) > extinction_threshold]

        unassigned_genomes = []

        surviving_species = []
        for species in self.species:
            if len(species.genomes) > extinction_threshold:
                surviving_species.append(species)
            else:
                unassigned_genomes += species.genomes
        self.species = surviving_species

        if unassigned_genomes != []:
            collector_species = Species(
                self.network, self.env, unassigned_genomes.pop())

            for genome in unassigned_genomes:
                collector_species.genomes.append(genome)

            self.species.append(collector_species)

        if len(self.species) == 0:
            print("EXTINCT")
            # TODO: Response to extinction?

    def assign_species(self):
        genomes = []

        for species in self.species:
            genomes = genomes + species.reset()

        for genome in genomes:
            assigned = False
            for species in self.species:
                distance = species.genomes[0].distance(genome)
                if distance < self.max_genetic_distance:
                    species.add_genome(genome)
                    assigned = True
                    break

            if not assigned:
                new_species = Species(self.network, self.env, genome)
                self.species.append(new_species)

    def get_best_network(self):
        self.network.reset()
        self.best_genome.apply()
        return self.network
