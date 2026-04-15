#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    vector<string> siko = {"Beks", "Zhasik", "Tima"};
    bool siko_gay = false;

    int i = 0;
    while (!siko_gay && i < siko.size()) {
        cout << "Siko krasavchik" << endl;

        if (siko[i] == "Tima") {
            cout << "Siko absolute gay" << endl;
            return 0;
        }

        i += 1;
    }

    return 0;
}