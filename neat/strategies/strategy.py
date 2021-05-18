import abc


class Strategy():
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def init_population(self, input_shape, output_shape) -> None:
        pass

    @abc.abstractmethod
    def eval_population(self, data, validation, lossfunction) -> dict:
        pass

    @abc.abstractmethod
    def step(self, data):
        pass
