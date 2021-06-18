import abc
from neat.network import Network


class Strategy():
    def __init__(self, **kwargs) -> None:
        pass

    @abc.abstractmethod
    def init_population(self, env, input_shape, output_shape, discrete: bool) -> None:
        pass

    @abc.abstractmethod
    def solve_epoch(self, epoch_len: int, offset: float, render: bool = False) -> dict:
        pass
