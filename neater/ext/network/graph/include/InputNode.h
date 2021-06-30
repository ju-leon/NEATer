//
// Created by Leon Jungemeyer on 01.06.21.
//

#ifndef NEATC_INPUTNODE_H
#define NEATC_INPUTNODE_H
#include <memory>

#include "Node.h"

class InputNode : public Node {
    float value;

public:
    InputNode() {};

    InputNode(int id) : Node{id} {};

    float call() override;

    int computeDependencyLayer() override;

    virtual int getDependencyLayer() override;

    void resetCache() override;

    void setValue(float);

};

#endif
