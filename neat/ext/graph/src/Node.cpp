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


double Node::call() {
    // Only compute if the function has not been cached. Prevents unnecessary recursions
    if (!cached) {
        if (active) {
            double result = bias;
            std::list<Edge *>::iterator it;
            for (it = connections.begin(); it != connections.end(); it++) {
                result += (*it)->call();
            }
            cache = result;

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

Node::Node(double bias) {
    Node::bias = bias;
}

Node::Node() {

}


void Node::reset() {
    cached = false;
    std::list<Edge *>::iterator it;
    for (it = connections.begin(); it != connections.end(); it++) {
        (*it)->reset();
    }
}

bool Node::isActive() const {
    return active;
}

void Node::setActive(bool active) {
    Node::active = active;
}
