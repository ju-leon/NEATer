//
// Created by Leon Jungemeyer on 01.06.21.
//

#include <memory>
#include <iostream>

#include "../include/InputNode.h"

float InputNode::call() {
    return value;
}

void InputNode::setValue(float x) {
    value = x;
}

void InputNode::resetCache() {}

int InputNode::computeDependencyLayer() {
    return 0;
}

int InputNode::getDependencyLayer() {
    return 0;
}

