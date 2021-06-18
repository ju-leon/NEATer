from neater.layers.layer import ExtendableLayer
from neater.layers.activation import ReLu
from neater.strategies.strategy import Strategy
from neater.network import Network
import torch
from numpy import random
import copy


class DenseNeat(Strategy):

    def __init__(self, num_survivors=10, num_children=10, activation=ReLu()) -> None:
        self.num_survivors = num_survivors
        self.num_children = num_children
        self.activation = activation
        self.networks = []
        self.best_network = None

    def init_population(self, input_shape, output_shape) -> None:
        for _ in range(self.num_survivors * self.num_children):
            net = Network(input_shape=input_shape)
            net.add_dense_layer(output_shape)

            self.networks.append(net)

    def get_best_network(self) -> Network:
        return self.best_network

    def eval_population(self, data, validation, loss) -> torch.Tensor:
        X, Y = data
        val_X, val_Y = validation

        losses = []
        for network in self.networks:
            losses.append(loss(network.predict(X), Y))

        losses = torch.FloatTensor(losses)

        idx = torch.argsort(losses)

        survivors = [self.networks[x] for x in idx[:self.num_survivors]]

        self.best_network = self.networks[idx[0]]

        # Mutate all surviors and use them as the new networks
        # The best network survives
        self.networks = [self.best_network]
        for survivor in survivors:
            for _ in range(self.num_children):
                child = copy.deepcopy(survivor)
                self.mutate_topology(child)
                self.mutate_layers(child)
                self.mutate_weights(child)
                self.networks.append(child)

        results = dict()
        results['loss_avg'] = torch.mean(losses)
        results['loss_min'] = torch.min(losses)
        if validation != None:
            results['val_loss_min'] = loss(
                self.best_network.predict(val_X), val_Y)

        return results

    def mutate_weights(self, network, intensity=0.05):
        for layer in network.layers:
            layer.add_weights(torch.normal(
                mean=0, std=intensity, size=layer.size))
            layer.add_biases(torch.normal(
                mean=0, std=intensity, size=(layer.output_shape,)))

    def mutate_layers(self, network, propa=0.5, intensity=0.2):
        for i in range(len(network.layers)-1):
            if random.choice([True, False], p=[propa, 1-propa]):
                network.layers[i].extend(
                    weights=torch.normal(
                        mean=0,
                        std=intensity,
                        size=(network.layers[i].input_shape, 1)),
                    bias=torch.normal(mean=0, std=intensity, size=(1,)),
                )

                network.layers[i+1].extend_input(
                    weights=torch.normal(
                        mean=0,
                        std=intensity,
                        size=(1, network.layers[i+1].output_shape))
                )
            elif random.choice([True, False], p=[propa, 1-propa]):
                if network.layers[i].output_shape > 3:
                    network.layers[i].decrease()
                    network.layers[i+1].decrease_input()

    def mutate_topology(self, network, propa=0.2, activation="tanh"):
        choice = random.choice([0, 1], p=[propa, 1-propa])
        # Add a Layer
        if choice == 0:
            if len(network.layers) == 1:
                index = 1
                layer = ExtendableLayer(
                    input_shape=network.layers[0].output_shape,
                    output_shape=network.layers[0].output_shape,
                )
            else:
                index = random.randint(1, len(network.layers))
                layer = ExtendableLayer(input_shape=network.layers[index-1].output_shape,
                                        output_shape=network.layers[index].input_shape,
                                        )

            network.layers.insert(index, layer)
        # Remove a layer
        elif choice == 1:
            if len(network.layers) > 2:
                index = random.randint(1, len(network.layers) - 1)
                network.layers[index -
                               1].change_output_size(network.layers[index+1].input_shape)
                del network.layers[index]
