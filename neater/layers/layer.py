import torch
import abc


class Layer():
    @abc.abstractmethod
    def forward(self, x):
        pass


class ExtendableLayer(Layer):
    def __init__(self, input_shape, output_shape, activation=torch.nn.Tanh()):
        self.weights = torch.zeros(input_shape, output_shape)

        # TODO: Initialize
        # = self.weights + \
        #    np.random.normal(size=(input_shape, output_shape), scale=0.3)

        # b_init = tf.keras.initializers.Zeros()
        # self.biases = tf.Variable(
        #    initial_value=b_init(shape=(output_shape,), dtype="float32"), trainable=True
        # )
        self.biases = torch.zeros(output_shape)

        self.activation = activation

        self.output_shape = output_shape
        self.input_shape = input_shape
        self.size = self.weights.shape

    def add_weights(self, weights):
        self.weights = self.weights + weights

    def add_biases(self, biases):
        self.biases = self.biases + biases

    def extend(self, weights, bias):
        self.weights = torch.cat((self.weights, weights), 1)
        self.biases = torch.cat((self.biases, bias), 0)

        self.output_shape += 1
        self.size = self.weights.shape

    def extend_input(self, weights):
        self.weights = torch.cat((self.weights, weights), 0)

        self.input_shape += 1
        self.size = self.weights.shape

    def decrease(self):
        self.weights = self.weights[:, :-1]
        self.biases = self.biases[:-1]
        self.output_shape -= 1
        self.size = self.weights.shape

    def decrease_input(self):
        self.weights = self.weights[:-1]
        self.input_shape -= 1
        self.size = self.weights.shape

    def change_output_size(self, size):
        while self.output_shape != size:
            if self.output_shape > size:
                self.decrease()
            elif self.output_shape < size:
                self.extend(
                    weights=torch.zeros(
                        (self.input_shape, 1)),
                    bias=torch.zeros(1,),
                )

    def forward(self, x):
        return self.activation(torch.matmul(x, self.weights) + self.biases)

    def __repr__(self):
        return "Layer: [shape=" + str(self.weights.shape) + "]"
