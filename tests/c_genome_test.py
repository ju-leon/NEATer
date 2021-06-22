import unittest
from torch import nn

from _neat import Network, Node, Edge
from _neat import Genome, NodeGene, EdgeGene


class CGenomeTest(unittest.TestCase):

    def test_pointers(self):
        net = Network(2, 4, nn.ReLU())

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


if "__main__" == __name__:
    unittest.main()
