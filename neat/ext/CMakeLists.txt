cmake_minimum_required(VERSION 3.19)
project(neatc)

set(CMAKE_CXX_STANDARD 14)

add_executable(neatc neatc.cpp graph/src/Node.cpp graph/include/Node.h graph/src/Edge.cpp graph/include/Edge.h graph/src/InputNode.cpp graph/include/InputNode.h)