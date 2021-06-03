//
// Created by Leon Jungemeyer on 01.06.21.
//

#include <iostream>
#include "../include/InputNode.h"

double InputNode::call() {
    return value;
}

void InputNode::setValue(double x) {
    value = x;
}

void InputNode::resetCache() {
    return;
}

int InputNode::computeDependencyLayer() {
    return 0;
}

int InputNode::getDependencyLayer() {
    return 0;
}