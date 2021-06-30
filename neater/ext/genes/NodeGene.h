//
// Created by Leon Jungemeyer on 08.06.21.
//

#ifndef NEATC_NODEGENE_H
#define NEATC_NODEGENE_H

#include <memory>
#include "../network/graph/include/Node.h"


class NodeGene {
    std::shared_ptr<Node> node;
    float bias = 0;
    bool disabled;
public:

    NodeGene(std::shared_ptr<Node> node);

    NodeGene(const std::shared_ptr<Node> &node, float bias, bool disabled);

    NodeGene(float bias, bool disabled);

    const std::shared_ptr<Node> &getNode() const;

    void apply();

    void setNode(const std::shared_ptr<Node> &node);

    float getBias() const;

    void setBias(float bias);

    bool isDisabled() const;

    void setDisabled(bool disabled);

    int getId() const;

};


#endif //NEATC_NODEGENE_H
