//
// Created by Leon Jungemeyer on 08.06.21.
//

#ifndef NEATC_GENOME_H
#define NEATC_GENOME_H

#import "network/Network.h"
#include "genes/EdgeGene.h"
#include "genes/NodeGene.h"

class Genome {
private:
    std::shared_ptr<Network> network;

    std::vector<EdgeGene> edgeGenes;
    std::vector<NodeGene> nodeGenes;

public:
    Genome(const std::shared_ptr<Network> &network);

    int mutateNode(double bias);

    int mutateEdge(double weight);

    int mutateWeightShift(double weight);

    int mutateWeightRandom(double weight);

    int mutateToggleConnection();

    int mutateBiasShift(double bias);

    int mutateBiasRandom(double bias);

    int mutateDisableNode();

    void apply();

};


#endif //NEATC_GENOME_H
