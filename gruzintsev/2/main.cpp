#include <iostream>

using namespace std;

class MyClass {
public:
	MyClass(int val = 0) : val(val) {};
	MyClass(bool condition) : val(condition ? 10 : 15) {};
	int val;
};

int main() {
	bool condition = bool(rand() & 1 > 0);
	MyClass mc(condition);
	cout << mc.val << endl;	
	return 0;
}
