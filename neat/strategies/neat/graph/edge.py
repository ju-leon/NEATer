class Edge():
    def __init__(self, id, input, output, weight) -> None:
        self.id = id
        self.input = input
        self.output = output
        self.weight = weight

        output.add_connection(self)
        self.active = False

        self.mutate_to_id = None

    def call(self):
        if self.active:
            out = self.input.call()
            return out * self.weight
        else:
            return 0

    def get_dependencies(self):
        return self.input.get_dependencies()

    def change_input(self, node):
        self.input = node

    def __repr__(self) -> str:
        return "\n {}=[{} -> {}]".format(self.id, self.input.id, self.output.id)
