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
        self.strategy.init_population(env, input_shape, output_shape)

    def solve(self, max_generations=10, epoch_len=100, increase_rate=0, goal='min', reward_offset=0, render=False):
        for generation in range(max_generations):
            data = self.strategy.solve_epoch(
                epoch_len, reward_offset, render)

            print("Generation {}/{}: Best={}, Average={}, Species={}".format(
                generation, max_generations,
                np.max(data["rewards"]),
                np.mean(data["rewards"]),
                data["num_species"]))

            epoch_len += increase_rate

    def get_network(self) -> None:
        return self.strategy.get_best_network()

    def predict(self, x: np.array) -> np.array:
        return self.strategy.predict_best(x)

    def save(self, path: str) -> None:
        with open(path, "wb") as output_file:
            pickle.dump(self.strategy, output_file)

    def load(self, path: str) -> None:
        with open(path, "wb") as input_file:
            self.strategy = pickle.load(input_file)
