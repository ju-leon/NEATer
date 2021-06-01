//
// Created by Leon Jungemeyer on 01.06.21.
//

#include <iostream>
#include "../include/Edge.h"


Edge::Edge(Node *in, Node *out) {
    inputNode = in;
    outputNode = out;


    outputNode->addConnection(this);
}

double Edge::call() {
    // Only compute if the function has not been cached. Prevents unnecessary recursions
    if (!cached) {
        if (active) {
            cache = weight * inputNode->call();
        } else {
            cache = 0;
        }
        cached = true;
    }

    return cache;
}

double Edge::getWeight() const {
    return weight;
}

void Edge::setWeight(double weight) {
    Edge::weight = weight;
}

void Edge::reset() {
    cached = false;
    inputNode->reset();
}


