//
// Created by Leon Jungemeyer on 01.06.21.
//

#ifndef NEATC_INPUTNODE_H
#define NEATC_INPUTNODE_H

#include "Node.h"

class InputNode : public Node
{
    double value;

public:
    InputNode() : Node(){};

    double call();

    void setValue(double);

    void reset();
};

#endif
