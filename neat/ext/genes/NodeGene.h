//
// Created by Leon Jungemeyer on 08.06.21.
//

#ifndef NEATC_NODEGENE_H
#define NEATC_NODEGENE_H

#include <memory>
#include "../network/graph/include/Node.h"

class NodeGene {
    std::shared_ptr<Node> node;
    double bias = 0;
    bool disabled;
public:

    NodeGene(std::shared_ptr<Node> node);

    const std::shared_ptr<Node> &getNode() const;

    void apply();

    void setNode(const std::shared_ptr<Node> &node);

    double getBias() const;

    void setBias(double bias);

    bool isDisabled() const;

    void setDisabled(bool disabled);
};


#endif //NEATC_NODEGENE_H
