# NEAT

The NEAT module is an implementation of Kenneth O. Stanley's proposal on [Evolving Neural Networks through
Augmenting Topologies](http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf).

In some cases, the algorithm was slightly altered to enhance computational performance. 
All performance critical part of this module are written in C++ to increase computation speed. 
Parts not performance critical are kept in Python for easy maintenance. 

The NEAT module implements the strategy interface. Interactions with the neat module will be performed through this interface.

## init

::: neater.strategies.Neat

`__init__(self, activation, population_size=100, max_genetic_distance=5, **kwargs)`

Init a 

## solve_epoch

## save

## load

## to_keras

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