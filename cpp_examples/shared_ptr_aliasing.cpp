#include <vector>
#include <iostream>
#include <memory>

using namespace std;

struct My {
    My(size_t size) : A(size) {
        for (size_t i = 0; i < size; ++i) {
            A[i] = static_cast<int>(i);
        }
    }
    vector<int> A;
};

int main() {
    shared_ptr<int> a;
    {
        auto ptr = make_shared<My>(10);
        a = shared_ptr<int>(ptr, &ptr->A[5]);
    }
    cout << *a << endl;
    return 0;
}

