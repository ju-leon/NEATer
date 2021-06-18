//
// Created by Leon Jungemeyer on 08.06.21.
//
#include <random>
#include <iterator>
#include <algorithm>
#include <cmath>

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


Genome::Genome(const std::shared_ptr<Network> &network) : network(network), edgeGenes() {

    nodeGenes.reserve(network->getInputNodes().size() + network->getOutputNodes().size());

    for (auto &it: network->getInputNodes()) {
        nodeGenes.emplace_back(it);
    }

    for (auto &it: network->getOutputNodes()) {
        nodeGenes.emplace_back(it);
    }

}

/**
 * Randomly mutates an edge on an existing node.
 * @param bias Bias assigned to new node
 * @return 0 if a node was successfully mutated, -1 otherwise
 */
int Genome::mutateNode(double bias) {
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

        return 0;
    }

    return -1;
}

/**
 * Mutates a new edge between 2 random nodes.
 * @param weight Weight assigned to the new edge.
 * @return 0 if an edge was successfully inserted, -1 otherwise
 */
int Genome::mutateEdge(double weight) {
    //TODO: Com dependencies once before all genomes can mutate
    network->computeDependencies();

    auto start = *select_randomly(nodeGenes.begin(), nodeGenes.end());
    // Exclude inputs from selectable output genes
    auto end = *select_randomly(nodeGenes.begin() + network->getInputs(), nodeGenes.end());

    //TODO: Less or less equal?
    if (end.getNode()->getDependencyLayer() == -1 ||
        start.getNode()->getDependencyLayer() < end.getNode()->getDependencyLayer()) {

        auto edge = network->registerEdge(start.getNode()->getId(), end.getNode()->getId());

        // Make sure a valid edge is returned
        if (edge) {
            //Check if edge already in EdgeGene List
            if (std::binary_search(std::begin(edgeGenes), std::end(edgeGenes), edge, compareEdgeGenes())) {
                // Edge already exists
            } else {
                edgeGenes.emplace_back(edge);
                edgeGenes.back().setWeight(weight);
                return 0;
            }
        }
    }

    return -1;
}

int Genome::mutateWeightShift(double weight) {
    if (!edgeGenes.empty()) {
        auto edgeGene = select_randomly(edgeGenes.begin(), edgeGenes.end());

        edgeGene->setWeight(edgeGene->getWeight() + weight);

        return 0;
    }
    return -1;
}

int Genome::mutateWeightRandom(double weight) {
    if (!edgeGenes.empty()) {
        auto edgeGene = select_randomly(edgeGenes.begin(), edgeGenes.end());

        edgeGene->setWeight(weight);
        return 0;
    }
    return -1;
}

int Genome::mutateToggleConnection() {
    if (!edgeGenes.empty()) {
        auto edgeGene = select_randomly(edgeGenes.begin(), edgeGenes.end());

        edgeGene->setDisabled(!edgeGene->isDisabled());

        return 0;
    }
    return -1;
}

int Genome::mutateBiasShift(double bias) {
    if (!nodeGenes.empty()) {
        auto nodeGene = select_randomly(nodeGenes.begin(), nodeGenes.end());

        nodeGene->setBias(nodeGene->getBias() + bias);

        return 0;
    }
    return -1;
}

int Genome::mutateBiasRandom(double bias) {
    if (!nodeGenes.empty()) {
        auto nodeGene = select_randomly(nodeGenes.begin(), nodeGenes.end());

        nodeGene->setBias(bias);

        return 0;
    }
    return -1;
}

int Genome::mutateDisableNode() {
    if (!nodeGenes.empty()) {
        auto nodeGene = select_randomly(nodeGenes.begin(), nodeGenes.end());

        nodeGene->setDisabled(!nodeGene->isDisabled());

        return 0;
    }
    return -1;
}

void Genome::apply() {
    for (auto &it: nodeGenes) {
        it.apply();
    }
    for (auto &it: edgeGenes) {
        it.apply();
    }
}

Genome Genome::crossbreed(const Genome &genome) {
    auto gen = std::bind(std::uniform_int_distribution<>(0, 1), std::default_random_engine());

    Genome child = Genome(network);

    int index1 = 0;
    int index2 = 0;
    while (index1 < edgeGenes.size() && index2 < genome.edgeGenes.size()) {
        if (edgeGenes[index1].getId() == genome.edgeGenes[index2].getId()) {
            if (gen()) {
                child.appendEdgeGene(edgeGenes[index1]);
            } else {
                child.appendEdgeGene(genome.edgeGenes[index2]);
            }
            index1++;
            index2++;
        } else if (edgeGenes[index1].getId() < genome.edgeGenes[index2].getId()) {
            child.appendEdgeGene(edgeGenes[index1]);
            index1++;
        } else {
            child.appendEdgeGene(genome.edgeGenes[index2]);
            index2++;
        }
    }

    while (index1 < edgeGenes.size()) {
        child.appendEdgeGene(edgeGenes[index1]);
        index1++;
    }

    while (index2 < genome.edgeGenes.size()) {
        child.appendEdgeGene(genome.edgeGenes[index2]);
        index2++;
    }

    return child;
}

double Genome::distance(const Genome &genome, int threshold, double c1, double c2, double c3) {

    int numDisjoint = 0;
    double weightDiff = 0;

    int index1 = 0;
    int index2 = 0;
    while (index1 < edgeGenes.size() && index2 < genome.edgeGenes.size()) {
        if (edgeGenes[index1].getId() == genome.edgeGenes[index2].getId()) {
            weightDiff += abs(edgeGenes[index1].getWeight() - genome.edgeGenes[index2].getWeight());
            index1++;
            index2++;
        } else if (edgeGenes[index1].getId() < genome.edgeGenes[index2].getId()) {
            numDisjoint++;
            index1++;
        } else {
            numDisjoint++;
            index2++;
        }
    }

    unsigned long numExcess = 0;
    if (index1 == edgeGenes.size()) {
        numExcess = genome.edgeGenes.size() - index2;
    } else {
        numExcess = edgeGenes.size() - index1;
    }

    unsigned long N = std::max(genome.edgeGenes.size(), edgeGenes.size());

    N = N < threshold ? 1 : N;

    return (c1 * numDisjoint / N) + (c2 * numExcess / N) + (c3 * weightDiff);
}

void Genome::appendNodeGene(const NodeGene &gene) {
    nodeGenes.emplace_back(gene);
}

void Genome::appendEdgeGene(const EdgeGene &gene) {
    edgeGenes.emplace_back(gene);
}

const std::vector<EdgeGene> &Genome::getEdgeGenes() const {
    return edgeGenes;
}

const std::vector<NodeGene> &Genome::getNodeGenes() const {
    return nodeGenes;
}
