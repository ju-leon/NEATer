class Individual():
    def __init__(self) -> None:
        self.node_genes = []
        self.edge_genes = []

    def add_edge(self, edge_gene):
        self.edge_genes.append(edge_gene)

    def add_node(self, node_gene):
        self.node_genes.append(node_gene)

    def apply(self):
        for node_gene in self.node_genes:
            node_gene.apply()

        for edge_gene in self.edge_genes:
            edge_gene.apply()

    def mutate(self):
        for edge_gene in self.edge_genes:
            edge_gene.mutate()

    def __repr__(self):
        return "[edge_genes: {}, node_genes: {}]".format([gene.id for gene in self.edge_genes], [gene.id for gene in self.node_genes])
