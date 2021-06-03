//
// Created by Leon Jungemeyer on 01.06.21.
//

#ifndef NEATC_INPUTNODE_H
#define NEATC_INPUTNODE_H

#include "Node.h"

class InputNode : public Node {
    double value;

public:
    InputNode(int id) : Node{id} {};

    double call() override;

    int computeDependencyLayer() override;

    virtual int getDependencyLayer() override;

    void resetCache() override;

    void setValue(double);

};

#endif
