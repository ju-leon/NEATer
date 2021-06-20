//
// Created by Leon Jungemeyer on 01.06.21.
//

#ifndef NEATC_NODE_H
#define NEATC_NODE_H

#include <vector>
#include <ostream>
#include <memory>

#include "Edge.h"

class Edge;

class Node {
    std::vector<std::shared_ptr<Edge>> connections;
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

    void addConnection(std::shared_ptr<Edge> edge);

    void resetConnections();

    bool isActive() const;

    void setActive(bool active);

    int getId() const;

    double getBias() const;

    void setBias(double bias);

    friend std::ostream &operator<<(std::ostream &os, const Node &node);

};

#endif
