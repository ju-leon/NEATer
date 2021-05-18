from numpy.core.defchararray import equal
import torch
from tqdm import trange


class NeatOptimizer():
    def __init__(self, input_shape, output_shape, strategy, batch_size=32):
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.strategy = strategy
        self.batch_size = batch_size

        self.strategy.init_population(input_shape, output_shape)

    def fit(self, data, loss=torch.nn.MSELoss(), epochs=10, validation=None):
        X, Y = data

        X = torch.FloatTensor(X)
        Y = torch.FloatTensor(Y)

        if validation == None:
            val_X = val_Y = None
        else:
            val_X, val_Y = validation
            val_X = torch.FloatTensor(val_X)
            val_Y = torch.FloatTensor(val_Y)

        batch_start = 0

        t = trange(epochs, desc='Loss', leave=True)
        for _ in t:
            batch_X = torch.FloatTensor(
                X[batch_start:min([batch_start+self.batch_size, len(X)])])
            batch_Y = torch.FloatTensor(
                Y[batch_start:min([batch_start+self.batch_size, len(Y)])])

            batch_start = (batch_start + self.batch_size) % len(X)

            result = self.strategy.eval_population(
                (X, Y), (val_X, val_Y), loss)

            t.set_description("Population: loss_min={:.4f}, loss_avg={:.4f}".format(
                result['loss_min'], result['loss_avg']))
