//
// Created by Leon Jungemeyer on 01.06.21.
//

#ifndef NEATC_NODE_H
#define NEATC_NODE_H

#include <list>
#include "Edge.h"

class Edge;

class Node
{
    std::list<Edge *> connections;
    double bias;

    bool active;
    int id;

    double cache;
    bool cached;

public:
    Node();

    Node(double b);

    virtual double call();

    virtual void reset();

    void addConnection(Edge *);

    bool isActive() const;

    void setActive(bool active);

    void setBias(double);

    double getBias();
};

#endif
