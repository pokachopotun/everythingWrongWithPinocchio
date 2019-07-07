#include <iostream>

using namespace std;

class MyClass {
public:
	MyClass(int val = 0) : val(val) {};
	int val;
};

int main() {
	bool condition = bool(rand() & 1 > 0);
	MyClass mc;
	
	if (condition) {
		mc = MyClass(10);
	} else {
		mc = MyClass(15);
	}
	cout << mc.val << endl;	
	return 0;
}
