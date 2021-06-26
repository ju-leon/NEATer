//
// Created by Leon Jungemeyer on 01.06.21.
//

#ifndef NEATC_NODE_H
#define NEATC_NODE_H

#include <vector>
#include <ostream>
#include <memory>
#include <functional>

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

    std::function<double(double)> activation;
public:
    Node();

    Node(int id);

    Node(int id, const std::function<double(double)> &activation);

    Node(int id, double bias, const std::function<double(double)> &activation);

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

    const std::function<double(double)> &getActivation() const;

    void setActivation(const std::function<double(double)> &activation);

    friend std::ostream &operator<<(std::ostream &os, const Node &node);

    const std::vector<std::shared_ptr<Edge>> &getConnections() const;
};

#endif
