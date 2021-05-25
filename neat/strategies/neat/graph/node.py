import functools
from neat.strategies.neat.graph.edge import Edge


class Node():
    def __init__(self, id, activation) -> None:
        self.id = id
        self.inputs = []
        self.activation = activation
        self.layer_hierarchy = 0
        self.required_nodes = []

    def add_connection(self, edge: Edge) -> None:
        self.inputs.append(edge)

    @functools.lru_cache(maxsize=300)
    def call(self):
        result = 0
        for input in self.inputs:
            out = input.call()
            result += out

        return self.activation(result)

    @functools.lru_cache(maxsize=300)
    def get_dependencies(self):
        self.required_nodes = []
        for input in self.inputs:
            self.required_nodes += input.get_dependencies()

        return self.required_nodes + [self.id]

    def reset_cache(self):
        # if self.call.cache_info().misses > 0:
        #    print(self.call.cache_info())
        # if self.call.cache_info().hits > 0:
        #    print(self.call.cache_info())
        self.call.cache_clear()
        self.get_dependencies().clear()

    def __repr__(self) -> str:
        return "[Node {}, required={}]".format(self.id, self.required_nodes)


class InputNode(Node):
    def __init__(self, id) -> None:
        self.id = id
        self.layer_hierarchy = 1
        self.required_nodes = []

    def set_value(self, x):
        self.value = x

    def call(self) -> float:
        return self.value

    def get_dependencies(self):
        return [self.id]

    def __repr__(self) -> str:
        return "[InputNode {}]".format(self.id)
