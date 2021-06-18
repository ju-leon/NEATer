//
// Created by Leon Jungemeyer on 01.06.21.
//

#include <memory>

#include "../include/InputNode.h"

double InputNode::call() {
    return value;
}

void InputNode::setValue(double x) {
    value = x;
}

void InputNode::resetCache() {}

int InputNode::computeDependencyLayer() {
    return 0;
}

int InputNode::getDependencyLayer() {
    return 0;
}