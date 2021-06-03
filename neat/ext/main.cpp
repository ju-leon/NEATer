//
// Created by Leon Jungemeyer on 01.06.21.
//

#include <iostream>
#include <unordered_map>
#include "graph/include/Node.h"
#include "graph/include/InputNode.h"
#include "Network.h"

using namespace std;

int main() {

    Network net = Network(3, 3);


    cout << net.registerEdge(1, 4) << endl;
    cout << net.registerEdge(1, 4) << endl;
    //cout << net.registerEdge(3, 9) << endl;
    //cout << net.registerEdge(4, 9) << endl;

    net.computeFeedforward();

    auto ids = net.registerNode(1, 4);
    cout << std::get<0>(ids) << ";" << std::get<1>(ids) << ";" << std::get<2>(ids) << endl;

    //ids = net.registerNode(1, 4);
    //cout << std::get<0>(ids) << ";" << std::get<1>(ids) << ";" << std::get<2>(ids) << endl;

    cout << "Compute" << std::endl;
    net.computeFeedforward();

    cout << net.registerEdge(2, 5) << endl;


    return 0;
}
