//
// Created by Leon Jungemeyer on 08.06.21.
//

#include "EdgeGene.h"

EdgeGene::EdgeGene(const std::shared_ptr<Edge> &edge) : edge(edge) {}

const std::shared_ptr<Edge> &EdgeGene::getEdge() const {
    return edge;
}

double EdgeGene::getWeight() const {
    return weight;
}

void EdgeGene::setWeight(double weight) {
    EdgeGene::weight = weight;
}

bool EdgeGene::isDisabled() const {
    return disabled;
}

void EdgeGene::setDisabled(bool disabled) {
    EdgeGene::disabled = disabled;
}

void EdgeGene::apply() {
    edge->setWeight(weight);
    edge->setActive(!disabled);
}
