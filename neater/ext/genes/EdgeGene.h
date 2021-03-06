//
// Created by Leon Jungemeyer on 08.06.21.
//

#ifndef NEATC_EDGEGENE_H
#define NEATC_EDGEGENE_H

#include <memory>
#include "../network/graph/include/Edge.h"

class EdgeGene {
    std::shared_ptr<Edge> edge;
    float weight = 0;
    bool disabled;

public:
    explicit EdgeGene(std::shared_ptr<Edge> edge);

    EdgeGene(const std::shared_ptr<Edge> &edge, float weight, bool disabled);

    void setEdge(const std::shared_ptr<Edge> &edge);

    const std::shared_ptr<Edge> &getEdge() const;

    void apply();

    float getWeight() const;

    void setWeight(float weight);

    bool isDisabled() const;

    void setDisabled(bool disabled);

    int getId() const;
};


#endif //NEATC_EDGEGENE_H
