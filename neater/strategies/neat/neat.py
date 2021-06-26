from numpy.core.fromnumeric import argmax
from neater.strategies.neat.species import Species
from _neat import Network, Genome
from neater.strategies.neat.genome import GenomeWrapper
from random import choice

from neater.strategies.strategy import Strategy
from itertools import zip_longest
import copy
import numpy as np
from tqdm import tqdm
import random
from operator import attrgetter
from tensorflow import keras

import pickle
# TODO: MOVE TO TENSORFLOW ACTIVATION


class Neat(Strategy):

    def __init__(self, **kwargs) -> None:
        self.activation = kwargs.get('activation')

        self.population_size = kwargs.get('population_size', 100)
        self.max_genetic_distance = kwargs.get('max_genetic_distance', 5)

        self.kwargs = kwargs

        self.species = []
        self.unassigned_genomes = []
        self.best_genome = None

    def init_population(self, env, input_shape, output_shape, discrete=True) -> None:
        self.env = env

        input_size = input_shape  # .flatten()
        output_size = output_shape  # .flatten()

        # TODO: Pass AF, self.activation)
        self.network = Network(input_size, output_size, self.activation)

        self.unassigned_genomes = []

        self.discrete = discrete

        # Start with a single species containing all genomes of the current population
        self.species = [
            Species(self.network, env, GenomeWrapper(self.network, **self.kwargs), self.discrete, **self.kwargs)]
        for _ in range(self.population_size):
            genome = GenomeWrapper(self.network, **self.kwargs)
            genome.mutate()
            self.species[0].add_genome(genome)

    def solve_epoch(self, epoch_len, offset, render=False):

        # Reset the best genome every generation. This is important in gyms with randomness
        self.best_genome = None

        # Evaluate all species
        rewards = []
        for species in self.species:
            reward = species.evaluate(epoch_len, offset, render)
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

    def predict_best(self, x: np.array):
        self.network.reset()
        self.best_genome.apply()
        return self.network.forward(x)

    def save(self, path):
        best_genome = None
        best_genome_index = (0, 0)

        # Iterate over all species and save the node genes and edge genes as tuples
        species_index = 0
        species_list = []
        for species in self.species:
            genome_index = 0
            genome_list = []
            for genome in species.genomes:
                # Save the index of the best genome seperately
                if best_genome == None or genome.fitness >= best_genome.fitness:
                    best_genome = genome
                    best_genome_index = (species_index, genome_index)

                # For each node gene, save the id of the corresponding node and the state
                node_list = []
                for node_gene in genome.genome.get_node_genes():
                    node_list.append(
                        (node_gene.get_id(), node_gene.bias, node_gene.disabled))

                # For each edge gene, save the id of the corresponding input and output nodes and the state
                edge_list = []
                for edge_gene in genome.genome.get_edge_genes():
                    edge_list.append(
                        (edge_gene.get_edge().get_input().get_id(), edge_gene.get_edge().get_output().get_id(), edge_gene.weight, edge_gene.disabled))

                genome_list.append((node_list, edge_list))
                genome_index += 1

            species_list.append(genome_list)
            species_index += 1

        # Iterate over all unassigned genomes and do the same
        genome_index = 0
        unassigned_genome_list = []
        for genome in self.unassigned_genomes:
            # If the best genome is in the unassigned genomes, mark it by setting species to -1
            if best_genome == None or genome.fitness >= best_genome.fitness:
                best_genome = genome
                best_genome_index = (-1, genome_index)

            node_list = []
            for node_gene in genome.genome.get_node_genes():
                node_list.append(
                    (node_gene.get_id(), node_gene.bias, node_gene.disabled))

            edge_list = []
            for edge_gene in genome.genome.get_edge_genes():
                edge_list.append(
                    (edge_gene.get_edge().get_input().get_id(), edge_gene.get_edge().get_output().get_id(), edge_gene.weight, edge_gene.disabled))

            unassigned_genome_list.append((node_list, edge_list))
            genome_index += 1

        with open(path, "wb") as file:
            pickle.dump((species_list, unassigned_genome_list,
                        self.discrete, self.network, best_genome_index, self.kwargs), file)

    def load(path, env):
        with open(path, "rb") as file:
            species_list, unassigned_genome_list, discrete, network, best_genome_index, kwargs = pickle.load(
                file)

        neat = Neat(**kwargs)

        neat.network = network
        network.set_activation(kwargs.get("activation"))

        neat.discrete = discrete

        species_index = 0
        for species_entry in species_list:
            species = Species(neat.network, env, None, neat.discrete, **kwargs)

            genome_index = 0
            species.genomes = []
            for genome_entry in species_entry:
                genome_wrapper = GenomeWrapper(neat.network, **kwargs)

                genome_wrapper.genome = Genome(
                    neat.network, genome_entry[0], genome_entry[1])

                # If the current genome was marked as the best, tag it as best genome
                if best_genome_index == (species_index, genome_index):
                    neat.best_genome = genome_wrapper

                species.add_genome(genome_wrapper)
                genome_index += 1

            neat.species.append(species)
            species_index += 1

        genome_index = 0
        for genome_entry in unassigned_genome_list:
            genome_wrapper = GenomeWrapper(neat.network, **kwargs)

            genome_wrapper.genome = Genome(
                neat.network, genome_entry[0], genome_entry[1])

            # If the current genome was marked as the best, tag it as best genome
            if best_genome_index == (-1, genome_index):
                neat.best_genome = genome_wrapper

            neat.unassigned_genomes.append(genome_wrapper)
            genome_index += 1

        return neat

    def to_keras(self):
        self.best_genome.apply()
        self.network.compute_dependencies()

        node_genes = self.best_genome.genome.get_node_genes()
        node_gene_ids = []
        for node_gene in node_genes:
            node_gene_ids.append(node_gene.get_id())

        layers = []
        for x in range(len(node_genes)):
            layers.append([])

        for node_gene in node_genes:
            layer = node_gene.get_node().get_dependency_layer()
            if layer >= 0:
                layers[layer].append(node_gene.get_id())

        # Remove all empty layers
        layers = [layer for layer in layers if layer != []]

        input = keras.Input(shape=(len(layers[0]),))

        node_ids = []
        for input_node_gene in layers[0]:
            node_ids.append(input_node_gene)

        skip_connections = input
        for layer in layers[1:]:
            dense_layer = keras.layers.Dense(len(layer), activation='relu',
                                             kernel_initializer='zeros',
                                             bias_initializer='zeros')
            x = dense_layer(skip_connections)
            skip_connections = keras.layers.Concatenate()(
                [x, skip_connections])

            weights, bias = dense_layer.get_weights()

            layer_ids = []

            node_ids += layer
            for node_id in layer:

                for con in node_genes[node_gene_ids.index(node_id)].get_node().get_connections():
                    if con.active:
                        weights[node_ids.index(con.get_input().get_id())][layer.index(
                            con.get_output().get_id())] = con.weight
                        bias[layer.index(con.get_output().get_id())
                             ] = con.get_output().bias

            dense_layer.set_weights([weights, bias])

        output_layer = keras.layers.Dense(
            self.network.get_outputs(), activation=None, kernel_initializer='zeros', bias_initializer='zeros')
        output = output_layer(skip_connections)

        weights, _ = output_layer.get_weights()
        for node, index in zip(self.network.get_output_nodes(), range(self.network.get_outputs())):
            if node.get_id() in node_ids:
                weights[node_ids.index(node.get_id())][index] = 1

        model = keras.Model(input, output, name="NEAT_resnet")

        return model
