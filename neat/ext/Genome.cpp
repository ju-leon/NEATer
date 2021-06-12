//
// Created by Leon Jungemeyer on 08.06.21.
//
#include  <random>
#include  <iterator>

#include "Genome.h"

template<typename Iter, typename RandomGenerator>
Iter select_randomly(Iter start, Iter end, RandomGenerator &g) {
    std::uniform_int_distribution<> dis(0, std::distance(start, end) - 1);
    std::advance(start, dis(g));
    return start;
}

template<typename Iter>
Iter select_randomly(Iter start, Iter end) {
    static std::random_device rd;
    static std::mt19937 gen(rd());
    return select_randomly(start, end, gen);
}


struct compareEdgeGenes {
    bool operator()(const std::shared_ptr<Edge> &edge,
                    const EdgeGene &gene) {
        return (edge->getId() < gene.getEdge()->getId());
    }

    bool operator()(const EdgeGene &gene,
                    const std::shared_ptr<Edge> &edge) {
        return (gene.getEdge()->getId() < edge->getId());
    }
};

struct compareNodeGenes {
    bool operator()(const std::shared_ptr<Node> &node,
                    const NodeGene &gene) {
        return (node->getId() < gene.getNode()->getId());
    }

    bool operator()(const NodeGene &gene,
                    const std::shared_ptr<Node> &node) {
        return (gene.getNode()->getId() < node->getId());
    }
};


Genome::Genome(const std::shared_ptr<Network> &network) : network(network) {

    nodeGenes.reserve(network->getInputNodes().size() + network->getOutputNodes().size());

    for (auto &it: network->getInputNodes()) {
        nodeGenes.emplace_back(it);
    }

    for (auto &it: network->getOutputNodes()) {
        nodeGenes.emplace_back(it);
    }

}

void Genome::mutateNode() {
    if (!edgeGenes.empty()) {
        auto edgeGene = *select_randomly(edgeGenes.begin(), edgeGenes.end());

        auto tuple = network->registerNode(edgeGene.getEdge()->getInputNode()->getId(),
                                           edgeGene.getEdge()->getOutputNode()->getId());

        auto edgeLeft = std::get<0>(tuple);
        auto nodeMiddle = std::get<1>(tuple);
        auto edgeRight = std::get<2>(tuple);

        if (!std::binary_search(std::begin(edgeGenes),
                                std::end(edgeGenes),
                                edgeLeft,
                                compareEdgeGenes())) {
            edgeGenes.emplace_back(edgeLeft);
            edgeGenes.back().setWeight(edgeGene.getWeight());
        }

        if (std::binary_search(std::begin(edgeGenes),
                               std::end(edgeGenes),
                               edgeRight,
                               compareEdgeGenes())) {
            edgeGenes.emplace_back(edgeRight);
            edgeGenes.back().setWeight(1);
        }

        if (std::binary_search(std::begin(nodeGenes),
                               std::end(nodeGenes),
                               nodeMiddle,
                               compareNodeGenes())) {
            nodeGenes.emplace_back(nodeMiddle);
        }

        edgeGene.setDisabled(true);

    }
}


void Genome::mutateEdge() {
    //TODO: Com dependencies once before all genomes can mutate
    network->computeDependencies();

    auto start = *select_randomly(nodeGenes.begin(), nodeGenes.end());
    auto end = *select_randomly(nodeGenes.begin(), nodeGenes.end());

    std::cout << "Start: " << start.getNode()->getId() << std::endl;
    std::cout << "Start Dependency: " << start.getNode()->getDependencyLayer() << std::endl;
    std::cout << "End: " << end.getNode()->getId() << std::endl;
    std::cout << "End Dependency: " << end.getNode()->getDependencyLayer() << std::endl;

    //TODO: Less or less equal?
    if (end.getNode()->getDependencyLayer() == -1 ||
        start.getNode()->getDependencyLayer() < end.getNode()->getDependencyLayer()) {
        auto edge = network->registerEdge(start.getNode()->getId(), end.getNode()->getId());

        // Make sure a valid edge is returned
        if (edge) {
            //Check if edge already in EdgeGene List
            if (std::binary_search(std::begin(edgeGenes), std::end(edgeGenes), edge, compareEdgeGenes())) {
                std::cout << " ------ Edge already exists, skipping" << std::endl;
            } else {
                edgeGenes.emplace_back(edge);
                // TODO: How to init weights?
                edgeGenes.back().setWeight(1);
                std::cout << " ------ Edge added" << std::endl;
            }
        }
    }

}
