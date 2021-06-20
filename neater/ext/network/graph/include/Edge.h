//
// Created by Leon Jungemeyer on 01.06.21.
//

#ifndef NEATC_EDGE_H
#define NEATC_EDGE_H

#include <ostream>
#include <memory>

#include "Node.h"

class Node;

class Edge {
private:
    std::shared_ptr<Node> inputNode;
    std::shared_ptr<Node> outputNode;
    double weight;
    bool active;
    int id;
    int mutateToNode = -1;
public:
    Edge();

    Edge(int id, std::shared_ptr<Node>, std::shared_ptr<Node>);

    double call();

    double getWeight() const;

    void setWeight(double weight);

    bool isActive() const;

    void setActive(bool active);

    int getId() const;

    void setId(int id);

    int computeDependencyLayer();

    int getMutateToNode() const;

    void setMutateToNode(int mutateToNode);

    const std::shared_ptr<Node> &getInputNode() const;

    const std::shared_ptr<Node> &getOutputNode() const;

    void setInputNode(const std::shared_ptr<Node> &inputNode);

    void setOutputNode(const std::shared_ptr<Node> &outputNode);

    friend std::ostream &operator<<(std::ostream &os, const Edge &edge);

};

#endif