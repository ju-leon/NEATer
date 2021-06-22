import unittest
from tensorflow import nn

from _neat import Network, Node, Edge

class CNetworkTest(unittest.TestCase):
    def test_node(self):
        node = Node(2, 0.5, nn.relu)
        self.assertEqual(node.get_id(), 2)
        self.assertEqual(node.bias, 0.5)

        node.bias = -0.4
        self.assertEqual(node.bias, -0.4)

    def test_edge(self):
        node_in = Node(0, 0.5, nn.relu)
        node_out = Node(0, 0.5, nn.relu)

        edge = Edge(3, node_in, node_out)
        self.assertEqual(edge.get_id(), 3)
        self.assertEqual(edge.weight, 0)

        edge.weight = 1.25
        self.assertEqual(edge.weight, 1.25)
        self.assertEqual(edge.active, False)

    def test_register_edge(self):
        net = Network(3, 3, nn.relu)
        edge = net.register_edge(0, 3)
        edge.active = True
        edge.weight = 1

        self.assertEqual(net.forward([1, 0, 0]), [1, 0, 0])
        self.assertEqual(net.forward([1, 1, 0]), [1, 0, 0])
        self.assertEqual(net.forward([1, 0, 1]), [1, 0, 0])
        self.assertEqual(net.register_edge(0, 3), edge)

        edge.active = False
        self.assertEqual(net.forward([1, 1, 1]), [0, 0, 0])

        self.assertIsNone(net.register_edge(3, 0))
        self.assertIsNone(net.register_edge(0, 0))
        self.assertIsNone(net.register_edge(5, 5))

    def test_register_node(self):
        net = Network(2, 2, nn.relu)
        edge_left, node, edge_right = net.register_node(0, 3)
        self.assertIsNone(edge_left)
        self.assertIsNone(node)
        self.assertIsNone(edge_right)

        edge = net.register_edge(1, 2)
        edgeLeft, nodeMiddle, edgeRight = net.register_node(1, 2)
        self.assertEqual(edgeLeft.get_output(), nodeMiddle)
        self.assertEqual(edgeRight.get_input(), nodeMiddle)

        net.compute_dependencies()

        self.assertIsNone(net.register_edge(nodeMiddle.get_id(), 0))

        edge = net.register_edge(nodeMiddle.get_id(), 3)
        self.assertEqual(edge, net.register_edge(nodeMiddle.get_id(), 3))

    def test_forward(self):
        net = Network(2, 4, nn.relu)

        edge1 = net.register_edge(0, 2)
        edge2 = net.register_edge(1, 3)

        self.assertEqual(net.forward([1, 1]), [0, 0, 0, 0])

        edge1.active = True
        edge1.weight = 1
        self.assertEqual(net.forward([1, 1]), [1, 0, 0, 0])

        edge2.active = True
        edge2.weight = 1
        self.assertEqual(net.forward([1, 1]), [1, 1, 0, 0])
        self.assertEqual(net.forward([1, -1]), [1, -1, 0, 0])
        self.assertEqual(net.forward([1, 0.5]), [1, 0.5, 0, 0])

        edge2.weight = 0.1
        self.assertEqual(net.forward([1, 1]), [1, 0.1, 0, 0])

        edgeLeft, nodeMiddle, edgeRight = net.register_node(1, 3)
        edgeLeft.active = True
        edgeLeft.weight = 1

        edgeRight.active = False
        edgeRight.weight = 1

        nodeMiddle.active = True

        self.assertEqual(net.forward([1, 1]), [1, 0.1, 0, 0])

        edgeInternal = net.register_edge(nodeMiddle.get_id(), 4)
        edgeInternal.active = True
        edgeInternal.weight = 1

        self.assertEqual(net.forward([1, 1]), [1, 0.1, 1, 0])


if "__main__" == __name__:
    unittest.main()
