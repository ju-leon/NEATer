from neater.strategies.strategy import Strategy
from numpy.core.defchararray import equal
import torch
from tqdm import trange
import numpy as np
import pickle


class Agent():
    def __init__(self, env, strategy, input_shape: int, output_shape: int,  discrete=True):
        self.input_shape = input_shape
        self.output_shape = output_shape

        self.discrete = discrete

        self.strategy = strategy
        self.strategy.init_population(env, input_shape, output_shape, discrete)

    def solve(self, max_generations=10, epoch_len=100, increase_rate=0, goal='min', render=False):
        for generation in range(max_generations):
            data = self.strategy.solve_epoch(
                epoch_len, render)
            
            print("\n\nGeneration {}/{}  ---  Best:{:6.2f}, Average:{:6.2f}, Species alive: {}".format(
                generation, max_generations,
                np.max(data["rewards"]),
                np.mean(data["rewards"]),
                data["num_species"]))

            epoch_len += increase_rate

    def get_network(self) -> None:
        return self.strategy.get_best_network()

    def predict(self, x: np.array) -> np.array:
        return self.strategy.predict_best(x)
