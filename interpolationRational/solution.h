#ifndef SOLUTION_H
#define SOLUTION_H
#include <vector>
#include <mathadditionals/mathadditionals.h>

class newtonLike // for function itself calculation
{
public:
    newtonLike(const std::vector<double>& x, const std::vector<double>& f, int n)
    {
        Polynom num(1, f[0]);
        Polynom denum(1, 1);
        ans = RationalFunction(num, denum);
        Polynom num1(2, 1);
        num1[0] = -x[0];
        RationalFunction tmp(num1, denum);
        ans = ans + tmp/getNext(x, f, n, 1);
    }
    RationalFunction getRes()
    {
        return ans;
    }
    RationalFunction getNext(const std::vector<double>& x, const std::vector<double>& f, int n, int i)
    {
        if(i == 2 * n)
        {
            Polynom num(1, ( reciprocalDifference(0, i, x, f) - reciprocalDifference(0, i - 2 , x, f)));
            Polynom denum(1,1);
            return RationalFunction(num,denum);
        }

        Polynom num(1, reciprocalDifference(0, i, x, f) - reciprocalDifference(0, i - 2 , x, f));
        Polynom denum(1,1);
        Polynom num1(2, 1);
        num1[0] = -x[i];
        RationalFunction tmp(num1, denum);
        return RationalFunction(num, denum) + tmp/getNext(x,f, n, i + 1);
    }

    double reciprocalDifference(int l, int r, const std::vector<double> x, const std::vector<double>& f)
    {
        if(l > r)
            return 0;
        if(l == r)
            return f[l];
        if(l + 1 == r)
            return ( x[l] - x[r] ) / (f[l] - f[r]);
        return ( x[l] - x[r] ) / ( reciprocalDifference(l, r - 1, x, f) - reciprocalDifference(l + 1, r, x, f)) +
                reciprocalDifference(l + 1, r - 1, x, f);
    }
    RationalFunction ans;
};

class nevilleLike
{
public:
    double getRes(const std::vector<double>& x, const std::vector<double>& f, int i, int k, double x0)
    {
        if(k < 0)
            return 0;
        if(k == 0)
            return f[i];
        double num = getRes(x,f,i, k-1, x0)-getRes(x,f, i - 1, k - 1,x0);
        double a = (x0 - x[i - k])/(x0 - x[i]);
        double b = num / (getRes(x,f,i, k-1, x0)-getRes(x,f, i - 1, k - 2,x0));
        return getRes(x,f,i, k-1, x0) + num /(a * (1 - b) - 1);
    }
};

#endif // SOLUTION_H
