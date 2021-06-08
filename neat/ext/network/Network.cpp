//
// Created by Leon Jungemeyer on 01.06.21.
//

#include "Network.h"
#include <memory>
#include <unordered_map>
#include <cassert>

#include "graph/include/Edge.h"


Network::Network(int inputs, int outputs) {
    edgeInnovationNumber = 0;
    nodeInnovationNumber = 0;
    for (int i = 0; i < inputs; i++) {
        int id = nodeInnovationNumber++;
        std::shared_ptr<Node> node = std::make_shared<InputNode>(id);
        nodes[id] = node;
        inputNodes.push_back(std::static_pointer_cast<InputNode>(node));
    }

    for (int i = 0; i < outputs; i++) {
        int id = nodeInnovationNumber++;
        nodes[id] = std::make_unique<Node>(id);
        outputNodes.emplace_back(nodes[id]);
    }

}

const std::vector<std::shared_ptr<Node>> &Network::getOutputNodes() const {
    return outputNodes;
}

void Network::computeDependencies() {
    for (auto &it: nodes) {
        it.second->resetDependencyLayer();
    }

    for (std::size_t i = 0; i < outputNodes.size(); ++i) {
        outputNodes[i]->computeDependencyLayer();
    }
}

std::shared_ptr<Edge> Network::registerEdge(int inId, int outId) {
    // Check if Nodes exist
    assert(nodes.find(inId) != nodes.end());
    assert(nodes.find(outId) != nodes.end());

    //Check if output node is not a input node
    if (nodes.find(outId)->second->getDependencyLayer() == 0) {
        return nullptr;
    }

    //Check if the edge is a forward edge
    if (nodes.find(inId)->second->getDependencyLayer() > nodes.find(outId)->second->getDependencyLayer() &&
        nodes.find(outId)->second->getDependencyLayer() != -1) {
        return nullptr;
    }

    // Prevent loops
    if (inId == outId) {
        return nullptr;
    }

    std::shared_ptr<Node> inputNode = nodes[inId];
    std::shared_ptr<Node> outputNode = nodes[outId];
    std::pair<int, int> key(inId, outId);


    // If Edge does not yet exist, create a new edge. Otherwise, return original edge.
    if (edges.find(key) == edges.end()) {
        edges[key] = std::make_shared<Edge>(edgeInnovationNumber++, inputNode, outputNode);
        outputNode->addConnection(edges[key]);
    }

    return edges[key];
}

/**
 * Adds a node on an existing edge.
 * The edge between input and output is not deleted.
 * Edges from input to the new node("leftEdge") and from the new node
 * to the output node("rightEdge") are added.
 *
 * @param inId Id of the input node
 * @param outId Id of the output node
 * @return Returns the ids of the newly created nodes and edges: <leftEdge.id, node.id, rightEdge.id>
 */
std::tuple<std::shared_ptr<Edge>, std::shared_ptr<Node>, std::shared_ptr<Edge>>
Network::registerNode(int inId, int outId) {
    std::pair<int, int> key(inId, outId);

    // Make sure the edge to be mutated exists
    if (edges.find(key) == edges.end()) {
        return std::make_tuple(nullptr, nullptr, nullptr);
    }

    std::shared_ptr<Edge> edge = edges.find(key)->second;

    std::shared_ptr<Node> middleNode;
    std::shared_ptr<Edge> leftEdge;
    std::shared_ptr<Edge> rightEdge;
    if (edge->getMutateToNode() == -1) {
        int id = nodeInnovationNumber++;
        nodes[id] = std::make_unique<Node>(id);
        middleNode = nodes[id];

        std::pair<int, int> leftKey(inId, middleNode->getId());
        edges[leftKey] = std::make_shared<Edge>(edgeInnovationNumber++, nodes[inId], middleNode);
        leftEdge = edges[leftKey];

        middleNode->addConnection(leftEdge);

        std::pair<int, int> rightKey(middleNode->getId(), outId);
        edges[rightKey] = std::make_shared<Edge>(edgeInnovationNumber++, middleNode, nodes[outId]);
        rightEdge = edges[rightKey];

        nodes[outId]->addConnection(rightEdge);

        edge->setMutateToNode(middleNode->getId());
    } else {
        middleNode = nodes[edge->getMutateToNode()];

        std::pair<int, int> leftKey(inId, middleNode->getId());
        leftEdge = edges[leftKey];

        std::pair<int, int> rightKey(middleNode->getId(), outId);
        rightEdge = edges[rightKey];
    }

    return std::make_tuple(leftEdge, middleNode, rightEdge);
}

std::vector<double> Network::forward(std::vector<double> x) {
    assert(x.size() == inputNodes.size());

    for (auto &it: nodes) {
        it.second->resetCache();
    }

    for (auto &it: outputNodes) {
        it->setActive(true);
    }

    for (std::size_t i = 0; i < x.size(); ++i) {
        inputNodes[i]->setValue(x[i]);
    }

    std::vector<double> result;
    result.reserve(outputNodes.size());

    for (std::size_t i = 0; i < outputNodes.size(); ++i) {
        result.push_back(outputNodes[i]->call());
    }

    return result;
}

const std::vector<std::shared_ptr<InputNode>> &Network::getInputNodes() const {
    return inputNodes;
}

void Network::reset() {
    for (auto &it: nodes) {
        it.second->setActive(false);
    }

    for (auto &it: edges) {
        it.second->setActive(false);
    }
}
