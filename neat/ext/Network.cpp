//
// Created by Leon Jungemeyer on 01.06.21.
//

#include "Network.h"
#include <memory>
#include <unordered_map>
#include "graph/include/Edge.h"


Network::Network(int inputs, int outputs) {
    edgeInnovationNumber = 0;
    nodeInnovationNumber = 0;
    for (int i = 0; i < inputs; i++) {
        int id = nodeInnovationNumber++;
        nodes[id] = std::unique_ptr<Node>(new InputNode(id));
        inputNodes.emplace_back(&(*nodes[id]));
    }

    for (int i = 0; i < inputs; i++) {
        int id = nodeInnovationNumber++;
        nodes[id] = std::make_unique<Node>(id);
        outputNodes.emplace_back(&(*nodes[id]));
    }

}

const std::vector<Node *> &Network::getOutputNodes() const {
    return outputNodes;
}

void Network::computeFeedforward() {
    for (auto &it: nodes) {
        it.second->resetDependencyLayer();
    }

    for (std::size_t i = 0; i < outputNodes.size(); ++i) {
        outputNodes[i]->computeDependencyLayer();
    }
}

int Network::registerEdge(int inId, int outId) {
    // Check if Nodes exist
    assert(nodes.find(inId) != nodes.end());
    assert(nodes.find(outId) != nodes.end());

    //Check if output node is not a input node
    assert(nodes.find(outId)->second->getDependencyLayer() != 0);

    //Check if the edge is a forward edge
    assert(nodes.find(inId)->second->getDependencyLayer() < nodes.find(outId)->second->getDependencyLayer() ||
           nodes.find(outId)->second->getDependencyLayer() == -1);


    Node *inputNode = &(*nodes[inId]);
    Node *outputNode = &(*nodes[outId]);
    std::pair<int, int> key(inId, outId);


    // If Edge does not yet exist, create a new edge. Otherwise, return original edge.
    if (edges.find(key) == edges.end()) {
        edges[key] = std::make_unique<Edge>(edgeInnovationNumber++, inputNode, outputNode);
        outputNode->addConnection(&(*edges[key]));
    }

    return edges[key]->getId();
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
std::tuple<int, int, int> Network::registerNode(int inId, int outId) {
    std::pair<int, int> key(inId, outId);

    // Make sure the edge to be mutated exists
    assert(edges.find(key) != edges.end());

    Edge *edge = &(*edges.find(key)->second);

    Node *middleNode;
    Edge *leftEdge;
    Edge *rightEdge;
    if (edge->getMutateToNode() == -1) {
        int id = nodeInnovationNumber++;
        nodes[id] = std::make_unique<Node>(id);
        middleNode = &(*nodes[id]);

        std::pair<int, int> leftKey(inId, middleNode->getId());
        edges[leftKey] = std::make_unique<Edge>(edgeInnovationNumber++, &(*nodes[inId]), middleNode);
        leftEdge = &(*edges[leftKey]);

        middleNode->addConnection(leftEdge);

        std::pair<int, int> rightKey(middleNode->getId(), outId);
        edges[rightKey] = std::make_unique<Edge>(edgeInnovationNumber++, middleNode, &(*nodes[outId]));
        rightEdge = &(*edges[rightKey]);

        (&(*nodes[outId]))->addConnection(rightEdge);

        edge->setMutateToNode(middleNode->getId());
    } else {
        middleNode = &(*nodes[edge->getMutateToNode()]);

        std::pair<int, int> leftKey(inId, middleNode->getId());
        leftEdge = &(*edges[leftKey]);

        std::pair<int, int> rightKey(middleNode->getId(), outId);
        rightEdge = &(*edges[rightKey]);
    }

    return std::make_tuple(leftEdge->getId(), middleNode->getId(), rightEdge->getId());
}
