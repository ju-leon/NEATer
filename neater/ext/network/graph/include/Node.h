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
    float bias;

    bool active;
    int id;

    float cache;
    bool cached;

    int dependencyLayer = -1;

    bool isOutput = false;

    std::function<float(float)> activation;
public:
    Node();

    Node(int id);

    Node(int id, bool output);

    Node(int id, const std::function<float(float)> &activation);

    Node(int id, float bias, const std::function<float(float)> &activation);

    Node(int id, float bias);

    virtual float call();

    virtual void resetCache();

    virtual int computeDependencyLayer();

    void resetDependencyLayer();

    virtual int getDependencyLayer();

    void addConnection(std::shared_ptr<Edge> edge);

    void resetConnections();

    bool isActive() const;

    void setActive(bool active);

    int getId() const;

    float getBias() const;

    void setBias(float bias);

    const std::function<float(float)> &getActivation() const;

    void setActivation(const std::function<float(float)> &activation);

    friend std::ostream &operator<<(std::ostream &os, const Node &node);

    const std::vector<std::shared_ptr<Edge>> &getConnections() const;

    bool isOutput1() const;

    void setIsOutput(bool isOutput);
};

#endif
