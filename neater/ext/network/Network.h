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
#include <memory>
#include <functional>

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

    Network(int inputs, int outputs, const std::function<double(double)> &activation);

    static Network load(std::vector<int> inputNodes,
                        std::vector<int> outputNodes,
                        std::vector<Node> nodes,
                        std::vector<std::tuple<Edge, int, int>> edges,
                        int nodeInnovationNumber,
                        int edgeInnovationNumber);

    std::shared_ptr<Edge> registerEdge(int inId, int outId);

    std::tuple<std::shared_ptr<Edge>, std::shared_ptr<Node>, std::shared_ptr<Edge>> registerNode(int inId, int outId);

    void computeDependencies();

    std::vector<double> forward(std::vector<double> x);

    const std::vector<std::shared_ptr<Node>> &getOutputNodes() const;

    const std::vector<std::shared_ptr<InputNode>> &getInputNodes() const;

    const std::unordered_map<std::pair<int, int>, std::shared_ptr<Edge>, hash_pair> &getEdges() const;

    const std::unordered_map<int, std::shared_ptr<Node>> &getNodes() const;

    void reset();

    int getInputs() const;

    int getOutputs() const;

    int getNodeInnovationNumber() const;

    int getEdgeInnovationNumber() const;

    const std::function<double(double)> &getActivation() const;

    void setActivation(const std::function<double(double)> &activation);

private:
    std::unordered_map<std::pair<int, int>, std::shared_ptr<Edge>, hash_pair> edges;
    std::unordered_map<int, std::shared_ptr<Node>> nodes;

    std::vector<std::shared_ptr<InputNode>> inputNodes;
    std::vector<std::shared_ptr<Node>> outputNodes;

    int nodeInnovationNumber;
    int edgeInnovationNumber;

    int inputs;
    int outputs;

    std::function<double(double)> activation;
};


#endif //NEATC_NETWORK_H
