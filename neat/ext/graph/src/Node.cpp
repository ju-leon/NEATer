//
// Created by Leon Jungemeyer on 01.06.21.
//
#include <iostream>
#include "../include/Node.h"

double clamped(double input) {
    if (input < -1) {
        return -1;
    } else if (input > 1) {
        return 1;
    } else {
        return input;
    }
}

Node::Node(int id, double bias) : id(id) {
    Node::bias = bias;
    Node::cached = false;
    Node::active = false;
    Node::cache = 0;
}

Node::Node(int id) : id(id) {
    Node::bias = 0;
    Node::cached = false;
    Node::active = false;
    Node::cache = 0;
}

Node::Node() : id(-1) {
    Node::bias = 0;
    Node::cached = false;
    Node::active = false;
    Node::cache = 0;
}

double Node::call() {
    // Only compute if the function has not been cached. Prevents unnecessary recursions
    if (!cached) {
        if (active) {
            double result = bias;
            std::list<Edge *>::iterator it;
            for (it = connections.begin(); it != connections.end(); it++) {
                result += (*it)->call();
            }
            cache = clamped(result);

        } else {
            cache = 0;
        }
        cached = true;
    }

    return cache;
}

void Node::addConnection(Edge *edge) {
    connections.push_back(edge);
}


void Node::resetCache() {
    cached = false;
    cache = 0;
}

bool Node::isActive() const {
    return active;
}

void Node::setActive(bool active) {
    Node::active = active;
}

int Node::getId() const {
    return id;
}

/**
 * Recursively computes the layer of the node.
 * Layers are assigned in a feed-forward fashion.
 * It is save to add edges from a lower to a higher layer.
 *
 * Layers are cached. If the network topology is changed,
 * Node::resetDependencyLayer() needs to be called first.
 *
 * @return Layer of node. -1 if the node has no connections.
 */
int Node::computeDependencyLayer() {
    std::list<Edge *>::iterator it;
    if (dependencyLayer == -1) {
        for (it = connections.begin(); it != connections.end(); it++) {
            int layer = (*it)->computeDependencyLayer();
            if (layer > dependencyLayer) {
                dependencyLayer = layer;
            }
        }
    }
    return dependencyLayer;
}

void Node::resetDependencyLayer() {
    dependencyLayer = -1;
}

int Node::getDependencyLayer() {
    return dependencyLayer;
}



