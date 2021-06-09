//
// Created by Leon Jungemeyer on 08.06.21.
//

#include "NodeGene.h"

NodeGene::NodeGene(const std::shared_ptr<Node> &node) : node(node) {}


double NodeGene::getBias() const {
    return bias;
}

void NodeGene::setBias(double bias) {
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

