cmake_minimum_required(VERSION 3.19)
project(neatc)

set(CMAKE_CXX_STANDARD 14)

add_executable(neatc main.cpp network/graph/src/Node.cpp network/graph/include/Node.h network/graph/src/Edge.cpp network/graph/include/Edge.h network/graph/src/InputNode.cpp network/graph/include/InputNode.h main.cpp network/Network.cpp network/Network.h Species.cpp Species.h)