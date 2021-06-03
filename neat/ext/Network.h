//
// Created by Leon Jungemeyer on 01.06.21.
//

#ifndef NEATC_NETWORK_H
#define NEATC_NETWORK_H

#include <unordered_map>
#include <list>
#include "graph/include/InputNode.h"
#include <iostream>
#include <vector>

struct hash_pair {
    template<class T1, class T2>
    size_t operator()(const std::pair<T1, T2> &p) const {
        auto hash1 = std::hash<T1>{}(p.first);
        auto hash2 = std::hash<T2>{}(p.second);
        return hash1 ^ hash2;
    }
};

class Network {


public:
    Network(int inputs, int outputs);

    Edge *registerEdge(int inId, int outId);

    std::tuple<Edge *, Node *, Edge *> registerNode(int inId, int outId);

    const std::vector<Node *> &getOutputNodes() const;

    void computeDependencies();

    std::vector<double> forward(std::vector<double> x);

private:
    std::unordered_map<std::pair<int, int>, std::unique_ptr<Edge>, hash_pair> edges;
    std::unordered_map<int, std::unique_ptr<Node>> nodes;

    std::vector<InputNode *> inputNodes;
    std::vector<Node *> outputNodes;


    int nodeInnovationNumber;
    int edgeInnovationNumber;


};


#endif //NEATC_NETWORK_H
