import unittest
import tensorflow as tf
import numpy as np

from _neat import Network, Node, Edge
from _neat import Genome, NodeGene, EdgeGene


def node_to_tuple(node):
    return (node.get_id(), node.bias, node.active)


def edge_to_tuple(edge):
    return (edge.get_input().get_id(), edge.get_output().get_id(), edge.weight, edge.active)


class CGenomeTest(unittest.TestCase):

    def test_pointers(self):
        net = Network(2, 4, tf.nn.relu)

        edge1 = net.register_edge(0, 2)

        gene1 = EdgeGene(edge1)
        gene2 = EdgeGene(edge1)

        # Test independence
        self.assertEqual(gene1.weight, 0)
        self.assertEqual(gene2.weight, 0)

        gene1.weight = 1.0

        self.assertEqual(gene1.weight, 1.0)
        self.assertEqual(gene2.weight, 0)

        self.assertFalse(gene1.disabled)
        self.assertFalse(gene2.disabled)

        gene2.disabled = True

        self.assertFalse(gene1.disabled)
        self.assertTrue(gene2.disabled)

        # Test application
        self.assertEqual(edge1.weight, 0)

        gene1.apply()

        self.assertEqual(edge1.weight, 1.0)
        self.assertTrue(edge1.active)

        gene2.apply()

        self.assertEqual(edge1.weight, 0.0)
        self.assertFalse(edge1.active)

        # Test reference
        self.assertEqual(gene1.get_edge(), edge1)
        self.assertEqual(gene2.get_edge(), edge1)
        self.assertEqual(gene1.get_edge(), gene2.get_edge())

    def test_genomes(self):
        net = Network(2, 2, tf.nn.relu)

        edge1 = net.register_edge(0, 2)
        edge2 = net.register_edge(1, 3)

        edge_left, node, edge_right = net.register_node(1, 3)

        print(node)

        default_nodes = [(0, 0.0, False), (1, 0.0, False),
                         (2, 0.0, False), (3, 0.0, False)]

        genome1 = Genome(net, [(4, 0.0, True)] + default_nodes, [
                         (0, 2, 1.0, False), (1, 3,  0.5, False)])

        genome2 = Genome(net, [(4, 1.0, False)] + default_nodes, [
            (0, 2, -1.0, False), (1, 3, 0.5, True), (1, 4, 1.0, False), (4, 3, 1.0, False)])

        # Check references
        self.assertEqual(genome1.get_node_genes()[0].get_node(),
                         genome2.get_node_genes()[0].get_node())

        self.assertEqual(genome1.get_edge_genes()[0].get_edge(),
                         genome2.get_edge_genes()[0].get_edge())

        genome1.apply()
        np.testing.assert_array_almost_equal(net.forward([0, 0]), [0, 0])
        np.testing.assert_array_almost_equal(net.forward([1, 1]), [1, 0.5])
        np.testing.assert_array_almost_equal(
            net.forward([1, -1]), [1, -0.5])
        np.testing.assert_array_almost_equal(
            net.forward([12, 1]), [12, 0.5])


        genome2.apply()
        np.testing.assert_array_almost_equal(net.forward([0, 0]), [0, 1])
        np.testing.assert_array_almost_equal(net.forward([1, 1]), [-1, 2])
        np.testing.assert_array_almost_equal(
            net.forward([1, -2]), [-1, 0])
        np.testing.assert_array_almost_equal(
            net.forward([12, 1]), [-12, 2])

        genome1.apply()
        np.testing.assert_array_almost_equal(net.forward([0, 0]), [0, 0])
        np.testing.assert_array_almost_equal(net.forward([1, 1]), [1, 0.5])
        np.testing.assert_array_almost_equal(
            net.forward([1, -1]), [1, -0.5])
        np.testing.assert_array_almost_equal(
            net.forward([12, 1]), [12, 0.5])


if "__main__" == __name__:
    unittest.main()
