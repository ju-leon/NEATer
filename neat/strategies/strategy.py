import abc
from neat.network import Network


class Strategy():
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def init_population(self, input_shape, output_shape) -> None:
        pass

    @abc.abstractmethod
    def eval_population(self, data, validation, loss) -> dict:
        pass

    @abc.abstractmethod
    def step(self, data):
        pass

    @abc.abstractmethod
    def get_best_network(self) -> Network:
        pass
