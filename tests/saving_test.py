import unittest
import pickle
import os
import shutil
from tensorflow import nn

from _neat import Network, Node, Edge


class CNetworkTest(unittest.TestCase):

    def setUp(self):
        if not os.path.exists(os.path.dirname("tests/temp/")):
            os.makedirs(os.path.dirname("tests/temp/"))

    def tearDown(self):
        shutil.rmtree("tests/temp/")

    def test_save_network(self):
        net = Network(3, 5, nn.relu)
        edge = net.register_edge(1, 4)
        edge.active = True
        edge.weight = -1

        self.assertEqual(net.forward([1, 1, 1]), [0, -1, 0, 0, 0])

        with open("tests/temp/net.neat", "wb") as file:
            pickle.dump(net, file)

        net = None

        with open("tests/temp/net.neat", "rb") as file:
            net = pickle.load(file)

        self.assertEqual(net.forward([1, 1, 1]), [0, -1, 0, 0, 0])


if "__main__" == __name__:
    unittest.main()

