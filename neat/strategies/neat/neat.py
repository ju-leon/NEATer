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

        self.species = []

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

        return rewards

    def assign_species(self):
        for species in self.species:
            species.reset()
        
        for genome in self.population:
            

    def get_best_network(self):
        self.best_network.apply()
        return self.network
