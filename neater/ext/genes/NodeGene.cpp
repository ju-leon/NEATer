//
// Created by Leon Jungemeyer on 08.06.21.
//

#include "NodeGene.h"

NodeGene::NodeGene(std::shared_ptr<Node> node) {
    NodeGene::node = node;
    disabled = false;
    bias = 0;
}


float NodeGene::getBias() const {
    return bias;
}

void NodeGene::setBias(float bias) {
    NodeGene::bias = bias;
}

bool NodeGene::isDisabled() const {
    return disabled;
}

void NodeGene::setDisabled(bool disabled) {
    NodeGene::disabled = disabled;
}

const std::shared_ptr<Node> &NodeGene::getNode() const {
    return node;
}

void NodeGene::setNode(const std::shared_ptr<Node> &node) {
    NodeGene::node = node;
}

void NodeGene::apply() {
    node->setActive(!disabled);
    node->setBias(bias);
}

int NodeGene::getId() const {
    return node->getId();
}

NodeGene::NodeGene(float bias, bool disabled) : bias(bias), disabled(disabled) {
    NodeGene::node = nullptr;
}

NodeGene::NodeGene(const std::shared_ptr<Node> &node, float bias, bool disabled) : node(node), bias(bias),
                                                                                   disabled(disabled) {}

