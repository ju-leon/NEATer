import torch
from neat.layers.layer import Layer


class ReLu(Layer):
    def __init__(self):
        self.activation = torch.nn.ReLU()

    def forward(self, x):
        return self.activation(x)


class Tanh(Layer):
    def __init__(self):
        self.activation = torch.nn.Tanh()

    def forward(self, x):
        return self.activation(x)
