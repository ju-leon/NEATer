class Plotter():

    def __init__(self, network):
        self.network = network

    def plot(self):
        graph = self.network.get_graph()
        