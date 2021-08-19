from neater.strategies.strategy import Strategy
from numpy.core.defchararray import equal
import torch
from tqdm import trange
import numpy as np
import pickle

import matplotlib.pyplot as plt


class Agent():
    def __init__(self, env, strategy, input_shape: int, output_shape: int,  discrete=True):
        self.input_shape = input_shape
        self.output_shape = output_shape

        self.discrete = discrete

        self.strategy = strategy
        self.strategy.init_population(env, input_shape, output_shape, discrete)

    def solve(self, max_generations=10, epoch_len=100, increase_rate=0, goal='min', render=False, stat_intervall=None):
        history = []

        for generation in range(max_generations):
            data = self.strategy.solve_epoch(
                epoch_len, render)

            history.append(data)

            print("\n\nGeneration {}/{}  ---  Best:{:6.2f}, Average:{:6.2f}, Species alive: {}".format(
                generation, max_generations,
                np.max(data["rewards"]),
                np.mean(data["rewards"]),
                data["num_species"]))

            epoch_len += increase_rate

            if stat_intervall != None and generation % stat_intervall == 0:
                self.strategy.plot(
                    "stats/generation-{}.png".format(generation))

                self.plot_species(history,
                                  "stats/species-{}.png".format(generation))

        return history

    def plot_species(self, histogram, path):
        species_histogram = dict()
        for entry, start in zip(histogram, range(len(histogram))):
            for species in entry["species"]:
                if species in species_histogram:
                    species_histogram[species].append(
                        entry["species"][species]["size"])
                else:
                    species_histogram[species] = [0] * start
                    species_histogram[species].append(
                        entry["species"][species]["size"])

        for key in species_histogram:
            species_histogram[key] = species_histogram[key] + \
                ([0] * (len(histogram) - len(species_histogram[key])))

        plt.stackplot(list(range(len(histogram))), species_histogram.values(),
                      labels=species_histogram.keys())

        plt.savefig(path, bbox_inches='tight')
        plt.close()

    def get_network(self) -> None:
        return self.strategy.get_best_network()

    def predict(self, x: np.array) -> np.array:
        return self.strategy.predict_best(x)
