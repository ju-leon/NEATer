//
// Created by Leon Jungemeyer on 08.06.21.
//

#include "EdgeGene.h"

EdgeGene::EdgeGene(std::shared_ptr<Edge> edge) {
    EdgeGene::edge = edge;
    disabled = false;
}

const std::shared_ptr<Edge> &EdgeGene::getEdge() const {
    return edge;
}

float EdgeGene::getWeight() const {
    return weight;
}

void EdgeGene::setWeight(float weight) {
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

int EdgeGene::getId() const {
    return edge->getId();
}

void EdgeGene::setEdge(const std::shared_ptr<Edge> &edge) {
    EdgeGene::edge = edge;
}

EdgeGene::EdgeGene(const std::shared_ptr<Edge> &edge, float weight, bool disabled) : edge(edge), weight(weight),
                                                                                      disabled(disabled) {}
