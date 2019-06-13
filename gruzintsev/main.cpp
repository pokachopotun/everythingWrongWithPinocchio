#include <iostream>
#include <sstream>
#include <map>
#include <vector>
#include <set>
#include <exception>

using namespace std;

class Rational {
public:
    Rational() {
        numerator = 0;
        denominator = 1;
        reduce();
    }

    Rational(int numerator, int denominator) {
        if (denominator == 0) {
            throw invalid_argument("Denominator should not be zero");
        }
        this->numerator = numerator;
        this->denominator = denominator;
        reduce();
    }

    int Numerator() const {
        return numerator;
    }

    int Denominator() const {
        return denominator;
    }

    Rational operator+(const Rational& other) {
        return Rational(
                this->Numerator() * other.Denominator() + this->Denominator() * other.Numerator(),
                this->Denominator() * other.Denominator()
        );
    }

    Rational operator-(const Rational& other) {
        return Rational(
                this->Numerator() * other.Denominator() - this->Denominator() * other.Numerator(),
                this->Denominator() * other.Denominator()
        );
    }

    Rational operator*(const Rational& other) {
        return Rational(
                this->Numerator() * other.Numerator(),
                this->Denominator() * other.Denominator()
        );
    }

    Rational operator/(const Rational& other) {
        if (other.Denominator() == 0) {
            throw std::domain_error("Division on zero");
        }
        return Rational(
                this->Numerator() * other.Denominator(),
                this->Denominator() * other.Numerator()
        );
    }


    bool operator==(const Rational& other) const {
        return numerator == other.Numerator() && denominator == other.Denominator();
    }

    friend ostream& operator<<(ostream& out, const Rational& rational);
    friend istream& operator>>(istream& in, Rational& rational);

    bool operator<(const Rational& other) const {
        if (this->Denominator() == other.Denominator()) {
            return this->Numerator() < other.Numerator();
        } else {
            return this->Numerator() * other.Denominator() < other.Numerator() * this->Denominator();
        }
    }

private:
    int numerator;
    int denominator;

    void reduce() {
        if (denominator < 0) {
            numerator *= -1;
            denominator *= -1;
        }

        int divisor = gcd(abs(numerator), denominator);
        if (divisor != 0) {
            numerator /= divisor;
            denominator /= divisor;
        }
    }

    int gcd(int a, int b) {
		return b == 0 ? a : gcd( b, a % b );
		if ( a < b ) {
			swap(a,b);
		}
        while (b != 0) {
            a %= b;
            swap(a, b);
        }
        return a;
    }
};

ostream& operator<<(ostream& out, const Rational& rational) {
    return out << rational.Numerator() << '/' << rational.Denominator();
}

istream& operator>>(istream& in, Rational& rational) {
    in >> rational.numerator;
    in.ignore(1);
    in >> rational.denominator;
    rational.reduce();

    return in;
}

int main() {
    // test case 1
    {
        const Rational r(3, 10);
        if (r.Numerator() != 3 || r.Denominator() != 10) {
            cout << "Rational(3, 10) != 3/10" << endl;
            return 1;
        }
    }

    {
        const Rational r(8, 12);
        if (r.Numerator() != 2 || r.Denominator() != 3) {
            cout << "Rational(8, 12) != 2/3" << endl;
            return 2;
        }
    }

    {
        const Rational r(-4, 6);
        if (r.Numerator() != -2 || r.Denominator() != 3) {
            cout << "Rational(-4, 6) != -2/3" << endl;
            return 3;
        }
    }

    {
        const Rational r(4, -6);
        if (r.Numerator() != -2 || r.Denominator() != 3) {
            cout << "Rational(4, -6) != -2/3" << endl;
            return 3;
        }
    }

    {
        const Rational r(0, 15);
        if (r.Numerator() != 0 || r.Denominator() != 1) {
            cout << "Rational(0, 15) != 0/1" << endl;
            return 4;
        }
    }

    {
        const Rational defaultConstructed;
        if (defaultConstructed.Numerator() != 0 || defaultConstructed.Denominator() != 1) {
            cout << "Rational() != 0/1" << endl;
            return 5;
        }
    }

    // test case 2
    {
        Rational r1(4, 6);
        Rational r2(2, 3);
        bool equal = r1 == r2;
        if (!equal) {
            cout << "4/6 != 2/3" << endl;
            return 1;
        }
    }

    {
        Rational a(2, 3);
        Rational b(4, 3);
        Rational c = a + b;
        bool equal = c == Rational(2, 1);
        if (!equal) {
            cout << "2/3 + 4/3 != 2" << endl;
            return 2;
        }
    }

    {
        Rational a(5, 7);
        Rational b(2, 9);
        Rational c = a - b;
        bool equal = c == Rational(31, 63);
        if (!equal) {
            cout << "5/7 - 2/9 != 31/63" << endl;
            return 3;
        }
    }

    // test case 3
    {
        Rational a(2, 3);
        Rational b(4, 3);
        Rational c = a * b;
        bool equal = c == Rational(8, 9);
        if (!equal) {
            cout << "2/3 * 4/3 != 8/9" << endl;
            return 1;
        }
    }

    {
        Rational a(5, 4);
        Rational b(15, 8);
        Rational c = a / b;
        bool equal = c == Rational(2, 3);
        if (!equal) {
            cout << "5/4 / 15/8 != 2/3" << endl;
            return 2;
        }
    }

    // test case 4
    {
        ostringstream output;
        output << Rational(-6, 8);
        if (output.str() != "-3/4") {
            cout << "Rational(-6, 8) should be written as \"-3/4\"" << endl;
            return 1;
        }
    }

    {
        istringstream input("5/7");
        Rational r;
        input >> r;
        bool equal = r == Rational(5, 7);
        if (!equal) {
            cout << "5/7 is incorrectly read as " << r << endl;
            return 2;
        }
    }

    {
        istringstream input("5/7 10/8");
        Rational r1, r2;
        input >> r1 >> r2;
        bool correct = r1 == Rational(5, 7) && r2 == Rational(5, 4);
        if (!correct) {
            cout << "Multiple values are read incorrectly: " << r1 << " " << r2 << endl;
            return 3;
        }

        input >> r1;
        input >> r2;
        correct = r1 == Rational(5, 7) && r2 == Rational(5, 4);
        if (!correct) {
            cout << "Read from empty stream shouldn't change arguments: " << r1 << " " << r2 << endl;
            return 4;
        }
    }

    // test case 5
    {
        const set<Rational> rs = {{1, 2}, {1, 25}, {3, 4}, {3, 4}, {1, 2}};
        if (rs.size() != 3) {
            cout << "Wrong amount of items in the set" << endl;
            return 1;
        }

        vector<Rational> v;
        for (auto x : rs) {
            v.push_back(x);
        }
        if (v != vector<Rational>{{1, 25}, {1, 2}, {3, 4}}) {
            cout << "Rationals comparison works incorrectly" << endl;
            return 2;
        }
    }

    {
        map<Rational, int> count;
        ++count[{1, 2}];
        ++count[{1, 2}];

        ++count[{2, 3}];

        if (count.size() != 2) {
            cout << "Wrong amount of items in the map" << endl;
            return 3;
        }
    }

    // test case 6
    {

        try {
            Rational r(1, 0);
            cout << "Doesn't throw in case of zero denominator" << endl;
            return 1;
        } catch (std::invalid_argument&) {
			cout << "test case 6 exception caught" << endl;
        }
    }
    {
        try {
            auto x = Rational(1, 2) / Rational(0, 1);
            cout << "Doesn't throw in case of division by zero" << endl;
            return 2;
        } catch (std::domain_error& e) {
            cout << "got exception 2" << endl;
        }
    }

    cout << "OK" << endl;
    return 0;
}

