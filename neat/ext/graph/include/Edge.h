//
// Created by Leon Jungemeyer on 01.06.21.
//

#ifndef NEATC_EDGE_H
#define NEATC_EDGE_H

#include "Node.h"

class Node;

class Edge {
private:
    Node *inputNode{};
    Node *outputNode{};
    double weight{};
    bool active{};
    int id{};
    int mutateToNode = -1;
public:
    Edge();

    Edge(int id, Node *, Node *);

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

};

#endif