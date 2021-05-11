MAXINT = 1000


class Network():
    def __init__(self, input_shape, output_shape):
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.in_ids = torch.arange(0, input_shape)
        self.out_ids = torch.arange(MAXINT - output_shape, MAXINT)

    def feed_forward_graph(self, genomes):
        last_layer = torch.arange(self.output_shape)

        genomes.sort(key=lambda x: x.destination)

        layers = []
        current_layer = []
        current_output = self.out_ids
        next_output = []
        for gene in reversed(genomes):
            if gene.destination in current_output:
                current_layer = [gene] + current_layer
                next_output.append(gene.source)
            else:
                current_output = next_output
                next_output = []
                layers = [current_layer] + layers
                current_layer = [gene]

        layers = [current_layer] + layers

        return layers

    def dense_layers(self, graph):

        layer_weights = []
        layer_biases = []

        for x in range(len(graph)):
            if x == 0:
                in_shape = self.input_shape
            else:
                in_shape = len(graph[x])

            if x == len(graph) - 1:
                out_shape = self.output_shape
            else:
                out_shape = len(graph[x+1])

            weights = torch.zeros(in_shape, out_shape)
            biases = torch.zeros(out_shape)
            input_ids = []
            output_ids = []
            for gene in graph[x]:
                if gene.source not in input_ids:
                    input_ids.append(gene.source)

                if gene.destination not in output_ids:
                    output_ids.append(gene.destination)

                weights[input_ids.index(gene.source), output_ids.index(
                    gene.destination)] = gene.weight
                biases[output_ids.index(gene.destination)] = gene.bias

            layer_weights.append(weights)
            layer_biases.append(biases)

        self.layer_weigths = layer_weights
        self.layer_biases = layer_biases
