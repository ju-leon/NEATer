//
// Created by Leon Jungemeyer on 08.06.21.
//

#ifndef NEATC_EDGEGENE_H
#define NEATC_EDGEGENE_H

#include <memory>
#include "../network/graph/include/Edge.h"

class EdgeGene {
    std::shared_ptr<Edge> edge;
    double weight = 0;
    bool disabled;

public:
    EdgeGene(const std::shared_ptr<Edge> &edge);

    const std::shared_ptr<Edge> &getEdge() const;

    void apply();

    double getWeight() const;

    void setWeight(double weight);

    bool isDisabled() const;

    void setDisabled(bool disabled);
};


#endif //NEATC_EDGEGENE_H
