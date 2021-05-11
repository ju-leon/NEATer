class Genome():
    def __init__(self, source, destination, identifier, weight):
        self.source = source
        self.destination = destination
        self.identifier = identifier
        self.weight = weight
        self.bias = 0

    def __repr__(self):
        return "(" + str(self.source) + "," + str(self.destination) + ")"
