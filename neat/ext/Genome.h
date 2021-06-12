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

    void mutateNode();

    void mutateEdge();

    void mutateWeightShift();

    void mutateWeightRandom();

    void mutateToggleConnection();

    void mutateBiasShift();

    void mutateDisableNode();

    void apply();

};


#endif //NEATC_GENOME_H
