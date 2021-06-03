//
// Created by Leon Jungemeyer on 01.06.21.
//

#ifndef NEATC_NODE_H
#define NEATC_NODE_H

#include <list>
#include "Edge.h"

class Edge;

class Node {
    std::list<Edge *> connections;
    double bias;

    bool active;
    int id;

    double cache;
    bool cached;

    int dependencyLayer = -1;
public:
    Node();

    Node(int id);

    Node(int id, double bias);

    virtual double call();

    virtual void resetCache();

    virtual int computeDependencyLayer();

    void resetDependencyLayer();

    virtual int getDependencyLayer();

    void addConnection(Edge *);

    bool isActive() const;

    void setActive(bool active);

    int getId() const;

    double getBias() const;

    void setBias(double bias);
};

#endif
