#include <iostream>
#include <fstream>
#include "mathadditionals.h"

using namespace std;

int main(int argc, char *argv[])
{
    freopen("input.txt", "r", stdin);
    Matrix a, b;
    cin >> a >> b;
    cout << a * b;
    Polynom c ,d;
    cin >> c >> d;
    cout << c * d;
    return 0;
}
