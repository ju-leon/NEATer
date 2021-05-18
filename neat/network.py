import torch
from neat.layers.layer import ExtendableLayer


class Network():
    def __init__(self, input_shape):
        self.layers = []
        self.input_shape = input_shape

    def add_dense_layer(self, size, weights=None, biases=None, activation="relu"):
        if len(self.layers) == 0:
            self.layers.append(
                ExtendableLayer(
                    self.input_shape,
                    size,
                )
            )
        else:
            self.layers.append(
                ExtendableLayer(
                    self.layers[-1].output_shape,
                    size,
                )
            )

    def add_layer(self, layer):
        self.layers.append(layer)

    def predict(self, sample):
        result = sample
        for layer in self.layers:
            result = layer.forward(result)
        return result

    def __repr__(self):
        return "Network: Layers= \n" + str(self.layers)
