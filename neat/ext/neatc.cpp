#include <pybind11/pybind11.h>

#include "graph/include/Node.h"

namespace py = pybind11;

int add(int i, int j)
{
    return i + j;
}

PYBIND11_MODULE(neatc, m)
{
    m.doc() = "pybind11 example plugin"; // optional module docstring
    m.def("add", &add, "A function which adds two numbers");
    py::class_<Node>(m, "Node")
        .def(py::init<double &>())
        .def("reset", &Node::reset);
}