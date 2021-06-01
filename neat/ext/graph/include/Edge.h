//
// Created by Leon Jungemeyer on 01.06.21.
//

#ifndef NEATC_EDGE_H
#define NEATC_EDGE_H

#include "Node.h"

class Node;

class Edge
{
private:
    Node *inputNode;
    Node *outputNode;
    double weight;
    bool active;
    int id;

    double cache;
    bool cached;

public:
    Edge(Node *, Node *);

    double call();

    void reset();

    double getWeight() const;

    void setWeight(double weight);

    bool isActive() const;

    void setActive(bool active);
};

#endif