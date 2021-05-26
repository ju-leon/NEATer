from numpy.core.defchararray import equal
import torch
from tqdm import trange
import numpy as np


class NeatOptimizer():
    def __init__(self, input_shape, output_shape, strategy):
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.strategy = strategy

        self.strategy.init_population(input_shape, output_shape)

    def solve(self, environment, max_generations=10, epoch_len=100, goal='min', discrete=True):
        for generation in range(max_generations):
            rewards = self.strategy.solve_epoch(environment, epoch_len, discrete)
            print("Generation {}/{}. Best: {}, Average: {}".format(
                generation, max_generations, np.max(rewards), np.mean(rewards)))

    def fit(self, data, loss=torch.nn.MSELoss(), epochs=10, batch_size=32, validation=None):
        X, Y = data
        #X = torch.FloatTensor(X)
        #Y = torch.FloatTensor(Y)

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
