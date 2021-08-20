#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include <memory>
#include <functional>

#include "network/Network.h"
#include "graph/include/Node.h"
#include "Genome.h"
#include "genes/EdgeGene.h"
#include "genes/NodeGene.h"

namespace py = pybind11;

PYBIND11_MODULE(_neat, m)
{
    m.doc() = "pybind11 example plugin"; // optional module docstring

    py::class_<Node, std::shared_ptr<Node>>(m, "Node")
        .def(py::init<int, float, std::function<float(float)>>())
        .def_property("bias", &Node::getBias, &Node::setBias)
        .def_property("active", &Node::isActive, &Node::setActive)
        .def("get_layer", &Node::getDependencyLayer)
        .def("get_id", &Node::getId)
        .def("get_connections", &Node::getConnections)
        .def("get_dependency_layer", &Node::getDependencyLayer)
        .def(py::pickle(
                [](const Node &n) {
                    return py::make_tuple(n.getId(), n.getBias(), n.isActive());
                },
                [](py::tuple t) {
                    if (t.size() != 3)
                        throw std::runtime_error("Invalid state!");

                    Node node(t[0].cast<int>(), t[1].cast<float>());
                    node.setActive(t[2].cast<bool>());
                    return node;
                }
                ))
        .def("__repr__",
             [](const Node &a)
             {
                 return "<neater.Node id=" + std::to_string(a.getId()) + ">";
             });

    py::class_<InputNode, Node, std::shared_ptr<InputNode>>(m, "InputNode")
        .def(py::init<int>())
        .def("get_layer", &InputNode::getDependencyLayer)
        .def("set_value", &InputNode::setValue)
        .def("get_id", &Node::getId)
        .def(py::pickle(
                [](const InputNode &n) {
                    return py::make_tuple(n.getId());
                },
                [](py::tuple t) {
                    if (t.size() != 1)
                        throw std::runtime_error("Invalid state!");

                    InputNode node(t[0].cast<int>());
                    return node;
                }))
        .def("__repr__",
        [](const InputNode &a)
        {
        return "<neater.InputNode id=" + std::to_string(a.getId()) + ">";
        });

    py::class_<Edge, std::shared_ptr<Edge>>(m, "Edge")
        .def(py::init<int, std::shared_ptr<Node>, std::shared_ptr<Node>>())
        .def_property("weight", &Edge::getWeight, &Edge::setWeight)
        .def_property("active", &Edge::isActive, &Edge::setActive)
        .def("get_id", &Edge::getId)
        .def("get_input", &Edge::getInputNode)
        .def("get_output", &Edge::getOutputNode)
        .def(py::pickle(
                [](const Edge &e) {
                    return py::make_tuple(e.getId(),
                                          e.getInputNode(),
                                          e.getOutputNode(),
                                          e.getWeight(),
                                          e.isActive(),
                                          e.getMutateToNode());
                },
                [](py::tuple t) {
                    if (t.size() != 6)
                        throw std::runtime_error("Invalid state!");

                    Edge edge(t[0].cast<int>(), t[1].cast<std::shared_ptr<Node>>(), t[2].cast<std::shared_ptr<Node>>());

                    edge.setWeight(t[3].cast<float>());
                    edge.setActive(t[4].cast<bool>());
                    edge.setMutateToNode(t[5].cast<int>());

                    return edge;
                }))
        .def("__repr__",
             [](const Edge &a)
             {
                 return "<neater.Edge id=" + std::to_string(a.getId()) + ">";
             });

    // Include Network
    py::class_<Network, std::shared_ptr<Network>>(m, "Network")
        .def(py::init<int, int, std::function<float(float)>>())
        .def("forward", &Network::forward)
        .def("get_inputs", &Network::getInputs)
        .def("get_outputs", &Network::getOutputs)
        .def("register_node", &Network::registerNode)
        .def("register_edge", &Network::registerEdge)
        .def("get_input_nodes", &Network::getInputNodes)
        .def("get_output_nodes", &Network::getOutputNodes)
        .def("compute_dependencies", &Network::computeDependencies)
        .def("reset", &Network::reset)
        .def("set_activation", &Network::setActivation)
        .def(py::pickle(
                [](const Network &n) {
                    std::vector<int> inputIds;
                    for (auto &it: n.getInputNodes()) {
                        inputIds.push_back(it->getId());
                    }

                    std::vector<int> outputIds;
                    for (auto &it: n.getOutputNodes()) {
                        outputIds.push_back(it->getId());
                    }

                    std::vector<Node> nodes;
                    for (auto &it: n.getNodes()) {
                        nodes.push_back(*it.second);
                    }

                    std::vector<std::tuple<Edge, int, int>> edges;
                    for (auto &it: n.getEdges()) {
                        auto entry = std::make_tuple(*it.second, it.second->getInputNode()->getId(), it.second->getOutputNode()->getId());
                        edges.push_back(entry);
                    }

                    return py::make_tuple(inputIds,
                                          outputIds,
                                          nodes,
                                          edges,
                                          n.getNodeInnovationNumber(),
                                          n.getEdgeInnovationNumber());
                },
                [](py::tuple t) {
                    if (t.size() != 6)
                        throw std::runtime_error("Invalid state!");

                    Network net = Network::load(
                            t[0].cast<std::vector<int>>(),
                            t[1].cast<std::vector<int>>(),
                            t[2].cast<std::vector<Node>>(),
                            t[3].cast<std::vector<std::tuple<Edge, int, int>>>(),
                            t[4].cast<int>(),
                            t[5].cast<int>()
                            );


                    return net;
                }))
        .def("__repr__",
             [](const Network &a)
             {
                 return "<neater.Network>";
             });

    py::class_<EdgeGene>(m, "EdgeGene")
        .def(py::init<std::shared_ptr<Edge>>())
        .def_property("weight", &EdgeGene::getWeight, &EdgeGene::setWeight)
        .def_property("disabled", &EdgeGene::isDisabled, &EdgeGene::setDisabled)
        .def("get_id", &EdgeGene::getId)
        .def("apply", &EdgeGene::apply)
        .def("get_edge", &EdgeGene::getEdge)
        .def("__repr__",
            [](const EdgeGene &a)
            {
            return "<neater.EdgeGene id=" + std::to_string(a.getId()) + ">";
        });

    py::class_<NodeGene>(m, "NodeGene")
        .def(py::init<std::shared_ptr<Node>>())
        .def_property("bias", &NodeGene::getBias, &NodeGene::setBias)
        .def_property("disabled", &NodeGene::isDisabled, &NodeGene::setDisabled)
        .def("get_id", &NodeGene::getId)
        .def("apply", &NodeGene::apply)
        .def("get_node", &NodeGene::getNode)
        .def("__repr__",
            [](const NodeGene &a)
            {
            return "<neater.NodeGene id=" + std::to_string(a.getId()) + ">";
        });


    py::class_<Genome, std::shared_ptr<Genome>>(m, "Genome")
        .def(py::init<std::shared_ptr<Network>>())
        .def(py::init<std::shared_ptr<Network>,
                std::vector<std::tuple<int, float, bool>>,
                std::vector<std::tuple<int, int, float, bool>>
                >())
        .def("mutate_node", &Genome::mutateNode)
        .def("init_node_genes", &Genome::initNodeGenes)
        .def("mutate_edge", &Genome::mutateEdge)
        .def("mutate_weight_shift", &Genome::mutateWeightShift)
        .def("mutate_weight_random", &Genome::mutateWeightRandom)
        .def("mutate_toggle_connection", &Genome::mutateToggleConnection)
        .def("mutate_bias_shift", &Genome::mutateBiasShift)
        .def("mutate_bias_random", &Genome::mutateBiasRandom)
        .def("mutate_disable_node", &Genome::mutateDisableNode)
        .def("crossbreed", &Genome::crossbreed)
        .def("distance", &Genome::distance)
        .def("get_edge_genes", &Genome::getEdgeGenes)
        .def("get_node_genes", &Genome::getNodeGenes)
        .def("apply", &Genome::apply);


}
