#include <iostream>
#include <string>
#include <windows.h>
#include <algorithm>
#include <iterator> 
#include <cmath>
#include <set>
using namespace std;


void setUnion(set<int> setA, set<int> setB) {
    int countUnion = 0;
    set <int> setUnion;
    set_union(setA.begin(), setA.end(),
        setB.begin(), setB.end(),inserter(setUnion, setUnion.begin()));

    for (int i : setUnion) {
            if (-11 < i and i < 11) {
                cout << i << '\n';
        }

    }
}

int main() {
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    set<int> A;
    set<int> B;
    int x;

    // Ввод массивов
    cout << "Введите элементы множетсва A (заканчивается на 0)" << endl;
    while (cin >> x and x != 0) {
        A.insert(x);
    }

    cout << "Введите элементы множетсва B (заканчивается на 0)" << endl;
    while (cin >> x and x != 0) {
        B.insert(x);
    }

    cout << "----------\n";

    setUnion(A, B);

    return 0;
}