//
// Created by Leon Jungemeyer on 01.06.21.
//

#include <iostream>
#include "../include/Edge.h"

Edge::Edge(int id, std::shared_ptr<Node> in, std::shared_ptr<Node> out) : id(id) {
    inputNode = in;
    outputNode = out;

    weight = 0;
    active = false;
}

double Edge::call() {
    // Only compute if the function has not been cached. Prevents unnecessary recursions
    double result = 0;
    if (active) {
        result = weight * inputNode->call();
    }

    return result;
}

double Edge::getWeight() const {
    return weight;
}

void Edge::setWeight(double weight) {
    Edge::weight = weight;
}

bool Edge::isActive() const {
    return active;
}

void Edge::setActive(bool active) {
    Edge::active = active;
}

int Edge::getId() const {
    return id;
}

void Edge::setId(int id) {
    Edge::id = id;
}

int Edge::computeDependencyLayer() {
    return inputNode->computeDependencyLayer() + 1;
}

int Edge::getMutateToNode() const {
    return mutateToNode;
}

void Edge::setMutateToNode(int mutateToNode) {
    Edge::mutateToNode = mutateToNode;
}

const std::shared_ptr<Node> &Edge::getInputNode() const {
    return inputNode;
}

const std::shared_ptr<Node> &Edge::getOutputNode() const {
    return outputNode;
}

Edge::Edge() = default;

std::ostream &operator<<(std::ostream &os, const Edge &edge) {
    os << "inputNode: " << edge.inputNode << " outputNode: " << edge.outputNode << " weight: " << edge.weight
       << " active: " << edge.active << " id: " << edge.id << " mutateToNode: " << edge.mutateToNode;
    return os;
}



