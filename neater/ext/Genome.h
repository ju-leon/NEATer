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

    Genome(const std::shared_ptr<Network> &network,
           const std::vector<std::tuple<int, float, bool>> &nodeGenes,
           const std::vector<std::tuple<int, int, float, bool>> &edgeGenes);

    int mutateNode(float bias);

    int mutateEdge(float weight);

    int mutateWeightShift(float weight);

    int mutateWeightRandom(float weight);

    int mutateToggleConnection();

    int mutateBiasShift(float bias);

    int mutateBiasRandom(float bias);

    int mutateDisableNode();

    void apply();

    const std::vector<EdgeGene> &getEdgeGenes() const;

    const std::vector<NodeGene> &getNodeGenes() const;

    Genome crossbreed(const Genome &genome);

    float distance(const Genome &genome, int threshold, float c1, float c2, float c3);

    void appendNodeGene(const NodeGene &gene);

    void appendEdgeGene(const EdgeGene &gene);

    void initNodeGenes();
};


#endif //NEATC_GENOME_H
