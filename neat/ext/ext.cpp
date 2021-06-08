#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>
#include <pybind11/stl.h>

#include "Network.h"
#include "graph/include/Node.h"

namespace py = pybind11;

PYBIND11_MODULE(_neat, m)
{
    m.doc() = "pybind11 example plugin"; // optional module docstring

    py::class_<Node, std::shared_ptr<Node>>(m, "Node")
        .def(py::init<int, double>())
        .def_property("bias", &Node::getBias, &Node::setBias)
        .def_property("active", &Node::isActive, &Node::setActive)
        .def("get_layer", &Node::getDependencyLayer)
        .def("get_id", &Node::getId)
        .def("__repr__",
             [](const Node &a)
             {
                 return "<neat.Node id=" + std::to_string(a.getId()) + ">";
             });

    py::class_<InputNode, Node, std::shared_ptr<InputNode>>(m, "InputNode")
        .def(py::init<int>())
        .def("get_layer", &InputNode::getDependencyLayer)
        .def("set_value", &InputNode::setValue)
        .def("get_id", &Node::getId)
        .def("__repr__",
        [](const InputNode &a)
        {
        return "<neat.InputNode id=" + std::to_string(a.getId()) + ">";
        });

    py::class_<Edge, std::shared_ptr<Edge>>(m, "Edge")
        .def(py::init<int, std::shared_ptr<Node>, std::shared_ptr<Node>>())
        .def_property("weight", &Edge::getWeight, &Edge::setWeight)
        .def_property("active", &Edge::isActive, &Edge::setActive)
        .def("get_id", &Edge::getId)
        .def("get_input", &Edge::getInputNode)
        .def("get_output", &Edge::getOutputNode)
        .def("__repr__",
             [](const Edge &a)
             {
                 return "<neat.Edge id=" + std::to_string(a.getId()) + ">";
             });

    // Include Network
    py::class_<Network, std::shared_ptr<Network>>(m, "Network")
        .def(py::init<int, int>())
        .def("forward", &Network::forward)
        .def("register_node", &Network::registerNode)
        .def("register_edge", &Network::registerEdge)
        .def("get_input_nodes", &Network::getInputNodes)
        .def("get_output_nodes", &Network::getOutputNodes)
        .def("compute_dependencies", &Network::computeDependencies)
        .def("reset", &Network::reset)
        .def("__repr__",
             [](const Network &a)
             {
                 return "<neat.Network>";
             });
}
