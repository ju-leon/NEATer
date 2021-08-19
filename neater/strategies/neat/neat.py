from os import kill
import networkx as nx
import pickle
from tensorflow import keras
from operator import attrgetter
import random
from tqdm import tqdm
import numpy as np
import copy
from itertools import zip_longest
from neater.strategies.strategy import Strategy
from random import choice
from neater.strategies.neat.genome import GenomeWrapper
from _neat import Network, Genome
from neater.strategies.neat.species import Species
from numpy.core.fromnumeric import argmax
import matplotlib
# matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from matplotlib import cm


class Neat(Strategy):

    def __init__(self, **kwargs) -> None:
        """Creates a new Neat population

        Inits a new neat population. Accepts tuning parameters for evolving genomes later. The parameters are passed down into the genomes

        Parameters:
            activation (float->float): Activation function
            population_size (int): Population size (default is 100)
        """
        self.activation = kwargs.get('activation')

        self.population_size = kwargs.get('population_size', 100)
        self.max_genetic_distance = kwargs.get('max_genetic_distance', 5)

        self.kill_percentage = kwargs.get('kill_percentage', 0.5)

        self.p_mutation = kwargs.get('p_mutation', 0.8)

        self.fitness_decay = kwargs.get('fitness_decay', 0.8)

        self.kwargs = kwargs

        self.species = []
        self.unassigned_genomes = []

    def init_population(self, env, input_shape, output_shape, discrete=True) -> None:
        self.env = env

        input_size = input_shape  # .flatten()
        output_size = output_shape  # .flatten()

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

    def solve_epoch(self, epoch_len, render=False):
        data = dict()
        data["species"] = dict()

        # Reset the best genome every generation. This is important in gyms with randomness
        self.best_genome = None

        # Evaluate all species
        rewards = []
        for species in self.species:
            reward = species.evaluate(epoch_len, render)
            rewards.append(reward)

        rewards = np.array(rewards)

        self.kill_underperformer()

        # OpenAi often uses negative rewards(punishments) which will affect the shared species rewards.
        # Fixed by allways setting the lowest reward of any species to 0
        # min_reward = np.min(rewards)
        for species in self.species:
            fitness = 0

            importance_factor = 1.0
            for genome in species.genomes:
                fitness += genome.fitness * importance_factor
                importance_factor = importance_factor * self.fitness_decay

            species.fitness = fitness

            print("- Species Fitness: {:6.3f}, Best Genome: {:6.3f}, Size: {}".format(
                species.fitness,
                species.fitness_max,
                len(species.genomes),
            ))

            data["species"][species.id] = dict()
            data["species"][species.id]["fitness"] = species.fitness
            data["species"][species.id]["fitness_max"] = species.fitness
            data["species"][species.id]["size"] = len(species.genomes)

        self.reproduce()
        self.mutate()

        # Assign all individuals to their species
        self.assign_species()
        self.remove_extinct_species()

        data["rewards"] = np.mean(rewards, axis=-1)
        data["num_species"] = len(self.species)

        return data

    def mutate(self):
        for species in self.species:
            species.mutate(self.p_mutation)

        for genome in self.unassigned_genomes:
            if np.random.choice([True, False], p=[self.p_mutation, 1-self.p_mutation]):
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

    def kill_underperformer(self):
        for species in self.species:
            species.kill_percentage(self.kill_percentage)

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
                self.network, self.env, unassigned_genomes.pop(), self.discrete)

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
                new_species = Species(
                    self.network, self.env, genome, self.discrete)
                self.species.append(new_species)

    def get_best_genome(self):
        best_genome = None
        for species in self.species:
            for genome in species.genomes:
                if best_genome == None or genome.fitness >= best_genome.fitness:
                    best_genome = genome
        return best_genome

    def get_best_network(self):
        best_genome = self.get_best_genome()
        self.network.reset()
        best_genome.apply()
        return self.network

    def predict_best(self, x: np.array):
        # self.network.reset()
        # self.best_genome.apply()
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
        neat.network.set_activation(kwargs.get("activation"))

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
        for x in range(max([x.get_node().get_dependency_layer() for x in node_genes]) + 1):
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
            dense_layer = keras.layers.Dense(len(layer), activation=self.activation,
                                             kernel_initializer='zeros',
                                             bias_initializer='zeros')
            x = dense_layer(skip_connections)
            skip_connections = keras.layers.Concatenate()(
                [skip_connections, x])

            weights, bias = dense_layer.get_weights()

            layer_ids = []

            node_ids += layer
            for node_id in layer:
                for con in node_genes[node_gene_ids.index(node_id)].get_node().get_connections():
                    if con.active:
                        weights[node_ids.index(con.get_input().get_id())][layer.index(
                            node_id)] = con.weight

                bias[layer.index(node_id)] = node_genes[node_gene_ids.index(
                    node_id)].get_node().bias

            dense_layer.set_weights([weights, bias])

        output_layer = keras.layers.Dense(
            self.network.get_outputs(), activation=None, kernel_initializer='zeros', bias_initializer='zeros')
        output = output_layer(skip_connections)

        weights, zeros = output_layer.get_weights()
        for node, index in zip(self.network.get_output_nodes(), range(self.network.get_outputs())):
            if node.get_id() in node_ids:
                weights[node_ids.index(node.get_id())][index] = 1

            output_layer.set_weights([weights, zeros])

        model = keras.Model(input, output, name="NEAT_resnet")

        return model

    def plot(self, path, labels=False):
        best_genome = self.get_best_genome()
        best_genome.apply()
        self.network.compute_dependencies()

        node_genes = best_genome.genome.get_node_genes()

        layers = []
        for x in range(max([x.get_node().get_dependency_layer() for x in node_genes]) + 1):
            layers.append([])

        node_gene_ids = []
        for node_gene in node_genes:
            node_gene_ids.append(node_gene.get_id())
            layer = node_gene.get_node().get_dependency_layer()
            if layer >= 0:
                layers[layer].append(node_gene.get_id())

        # Remove all empty layers
        layers = [layer for layer in layers if layer != []]

        print(layers)

        G = nx.Graph()

        for index, layer in zip(range(len(layers)), layers):
            for node_id in layer:
                G.add_node(node_id, layer=index)
                for con in node_genes[node_gene_ids.index(node_id)].get_node().get_connections():
                    if con.active:
                        G.add_edge(con.get_input().get_id(),
                                   con.get_output().get_id(), weight=round(con.weight, 3))

        for node, index in zip(self.network.get_output_nodes(), range(self.network.get_outputs())):
            G.add_node("output_" +
                       str(node.get_id()), layer=len(layers) + 1)

            if not node.get_id() in G.nodes:
                G.add_node(node.get_id(), layer=len(layers))

            G.add_edge(node.get_id(), "output_" +
                       str(node.get_id()), weight=1)

        # Remove unconnected nodes
        # to_be_removed = [x for x in G.nodes() if G.degree(
        #    x) == 0 and x >= self.network.get_inputs()]

        to_be_removed = [node for (node, layer)
                         in G.nodes(data="layer") if layer == None]

        for x in to_be_removed:
            G.remove_node(x)

        # Position start and end nodes
        pos = nx.multipartite_layout(G, subset_key="layer")

        # Optional spring layout between the layers
        #fixed_nodes = []
        #fixed_nodes += list(range(self.network.get_inputs()))
        # for node in self.network.get_output_nodes():
        #    fixed_nodes.append("output_" + str(node.get_id()))
        #pos = nx.spring_layout(G, pos=pos, fixed=fixed_nodes, weight='weight')

        edges = G.edges()
        weights = [G[u][v]['weight'] for u, v in edges]

        plt.figure()  # figsize=(8, 8))
        nx.draw(G, pos, with_labels=labels, node_shape=">",
                node_color="#1c1c1c", edge_cmap=cm.get_cmap('coolwarm'), node_size=20, edge_color=weights)

        if labels:
            labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        plt.savefig(path, bbox_inches='tight')
        plt.close()
