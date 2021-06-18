//
// Created by Leon Jungemeyer on 01.06.21.
//

#include <iostream>
#include <unordered_map>
#include "network/graph/include/Node.h"
#include "network/graph/include/InputNode.h"
#include "network/Network.h"
#include "Genome.h"

using namespace std;

int main() {

    shared_ptr<Network> net = make_shared<Network>(2, 2);

    auto genome = Genome(net);
    auto genome2 = Genome(net);

    for (int x = 0; x < 100; x++) {
        cout << "LOOPING" << endl;
        genome.mutateEdge(2);
        genome2.mutateEdge(-10);

        //genome.mutateNode(0);
        //genome2.mutateNode(0);
    }


    auto child = genome2.crossbreed(genome);

    for (int i = 0; i < child.getEdgeGenes().size(); i++) {
        cout << "child: " << child.getEdgeGenes()[i].getWeight() << endl;
    }


    /**
    cout << net.registerEdge(1, 4) << endl;
    cout << net.registerEdge(1, 4) << endl;
    //cout << net.registerEdge(3, 9) << endl;
    //cout << net.registerEdge(4, 9) << endl;

    net.computeDependencies();


    auto ids = net.registerNode(1, 4);
    cout << std::get<0>(ids) << ";" << std::get<1>(ids) << ";" << std::get<2>(ids) << endl;

    //ids = net.registerNode(1, 4);
    //cout << std::get<0>(ids) << ";" << std::get<1>(ids) << ";" << std::get<2>(ids) << endl;

    cout << "Compute" << std::endl;
    net.computeDependencies();

    cout << net.registerEdge(2, 0) << endl;

    vector<double> vec;
    vec.push_back(10);
    vec.push_back(0.2);
    vec.push_back(1.0);

    auto result = net.forward(vec);
    for (std::vector<double>::const_iterator i = result.begin(); i != result.end(); ++i) {
        std::cout << *i << ' ';
    }

    **/

    return 0;
}
