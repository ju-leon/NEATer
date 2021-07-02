import abc
import numpy as np
from neater.network import Network
from gym import Env


class Strategy():
    def __init__(self, **kwargs) -> None:
        pass

    @abc.abstractmethod
    def init_population(self, env: Env, input_shape: int, output_shape: int, discrete: bool) -> None:
        pass

    @abc.abstractmethod
    def solve_epoch(self, epoch_len: int, render: bool = False) -> dict:
        pass

    @abc.abstractmethod
    def predict_best(self, x: np.array) -> np.array:
        pass

    @abc.abstractmethod
    def save(self, path: str) -> None:
        pass

    @abc.abstractmethod
    def load(path: str, env: Env):
        pass

    @abc.abstractmethod
    def to_keras(self):
        pass
