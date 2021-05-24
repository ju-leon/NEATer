class Individual():
    def __init__(self) -> None:
        self.nodes = []
        self.edges = []

    def add_edge(self, edge):
        self.edges.append(edge)

    def add_node(self, node):
        self.nodes.append(node)
