from neat.visualize.plot import Plotter
from numpy.core.defchararray import equal
import torch
from tqdm import trange
import numpy as np


class NeatOptimizer():
    def __init__(self, env, input_shape, output_shape, strategy):
        self.input_shape = input_shape
        self.output_shape = output_shape

        self.strategy = strategy
        self.strategy.init_population(env, input_shape, output_shape)

        self.plotter = Plotter(self.strategy.network)

    def solve(self, max_generations=10, epoch_len=100, increase_rate=0, goal='min', discrete=True, reward_offset=0, render=False):
        for generation in range(max_generations):
            data = self.strategy.solve_epoch(
                epoch_len, discrete, reward_offset, render)

            if render:
                self.plotter.plot()

            print("Generation {}/{}: Best={}, Average={}, Species={}".format(
                generation, max_generations,
                np.max(data["rewards"]),
                np.mean(data["rewards"]),
                data["num_species"]))

            epoch_len += increase_rate

    def fit(self, data, loss=torch.nn.MSELoss(), epochs=10, batch_size=32, validation=None):
        X, Y = data

        if validation == None:
            val_X = val_Y = None
        else:
            val_X, val_Y = validation

        batch_start = 0

        t = trange(epochs, desc='Loss', leave=True)
        for _ in t:
            batch_X = X[batch_start:min([batch_start+batch_size, len(X)])]
            batch_Y = Y[batch_start:min([batch_start+batch_size, len(Y)])]

            batch_start = (batch_start + batch_size) % len(X)

            result = self.strategy.eval_population(
                (batch_X, batch_Y), (val_X, val_Y), loss)

            if validation == None:
                t.set_description("Population: loss_min={:.4f}, loss_avg={:.4f}".format(
                    result['loss_min'], result['loss_avg']))
            else:
                t.set_description("Population: loss_min={:.4f}, loss_avg={:.4f}, val_loss={:.4f}".format(
                    result['loss_min'], result['loss_avg'], result['val_loss_min']))

    def get_network(self):
        return self.strategy.get_best_network()
