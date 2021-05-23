from neat.strategies.neat.genome import Genome
from neat.strategies.strategy import Strategy


class Neat(Strategy):

    def __init__(self, population_size=5) -> None:
        self.population_size = population_size

    def init_population(self, input_shape, output_shape) -> None:
        self.input_size = input_shape.flatten()
        self.output_size = output_shape.flatten()

        self.population = []
        for _ in range(self.population_size):
            self.population.append(Genome(self.input_size, self.output_size))
