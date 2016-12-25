#include "mathadditionals.h"
#include <stdexcept>

Matrix::Matrix(int height, int width, double val, bool diagonal)
    : std::vector< std::vector<double> >( height, vector<double>( width, diagonal ? 0 : val))
{

    rows_ = height;
    cols_ = width;
    if(diagonal)
    for(size_t i = 0; i < rows_; i++)
    {
        this->operator [](i)[i] = val;
    }
}

Matrix& Matrix::operator+=(const Matrix& rhs)
{
    for(size_t i = 0; i < rows(); i++)
    {
        for(size_t j = 0; j < cols(); j++)
        {
            this->operator [](i)[j] += rhs[i][j];
        }
    }
    return *this;
}

Matrix& Matrix::operator-=(const Matrix& rhs)
{
    for(size_t i = 0; i < rows(); i++)
    {
        for(size_t j = 0; j < cols(); j++)
        {
            this->operator [](i)[j] -= rhs[i][j];
        }
    }
    return *this;
}

Matrix Matrix::getInverse()
{
  Matrix a(*this);
  Matrix res(rows_, cols_, 1, true);
  for (int cur = 0; cur < rows_; cur++)
  {
      int maxid = cur;
      for (int row = cur; row < rows_; row++)
      {
          if (a[row][cur] > a[maxid][cur] || a[maxid][cur] == 0)
          {
              maxid = row;
          }
      }

      if (maxid != cur)
      {
          std::swap(a[maxid], a[cur]);
          std::swap(res[maxid], res[cur]);
      }
      for (int row = 0; row < rows_; row++)
      {
          if (row != cur)
          {
              double k = (a[row][cur] / a[cur][cur]);
              for (int col = 0; col < a.size(); col++)
              {
                  a[row][col] -= a[cur][col] * k;
                  res[row][col] -= res[cur][col] * k;
              }
          }
      }
      double cura = a[cur][cur];
      for (int col = 0; col < cols_; col++)
      {
          a[cur][col] /= cura;
          res[cur][col] /= cura;
      }
  }
  return res;
}

Matrix operator+(const Matrix& lhs, const Matrix& rhs)
{
    Matrix res(lhs);
    res+=rhs;
    return res;
}

Matrix operator-(const Matrix& lhs, const Matrix& rhs)
{
    Matrix res(lhs);
    res-=rhs;
    return res;
}

Matrix operator*(const Matrix& lhs, const Matrix& rhs)
{
    Matrix res(lhs.rows(), rhs.cols());
    for(size_t i = 0; i < lhs.rows();i++)
    {
        for(size_t k = 0 ; k < lhs.cols(); k++)
        {
            for(size_t j = 0; j < rhs.cols(); j++)
            {
                res[i][j] += lhs[i][k] * rhs[k][j];
            }
        }
    }
    return res;
}

std::istream& operator>>(std::istream& is, Matrix& mat)
{
    int rows, cols;
    is >> rows >> cols;
    mat = Matrix(rows, cols);
    for(int i = 0; i < rows; i++)
        for(int j = 0; j < cols; j++)
            is >> mat[i][j];
    return is;
}

std::ostream& operator<<(std::ostream& os, const Matrix& mat)
{
    for(int i = 0; i < mat.rows(); i++)
    {
        for(int j = 0;j < mat.cols(); j++)
        {
            os << mat[i][j] << ' ';
        }
        os << std::endl;
    }
    os<<std::endl;
    return os;
}

Polynom::Polynom(int len, double val) : vector<double>(len, val)
{
}

Polynom& Polynom::operator+=(const Polynom& rhs)
{
    for(size_t i =0 ; i < rhs.size(); i++)
    {
        this->operator [](i) += rhs[i];
    }
}

Polynom& Polynom::operator-=(const Polynom& rhs)
{
    for(size_t i =0 ; i < rhs.size(); i++)
    {
        this->operator [](i) -= rhs[i];
    }

}

double Polynom::getValue(double x)
{
    double res = 0;
    double px = 1;
    for(size_t i = 0; i < size(); i++)
    {
        res += px * operator [](i);
        px *= x;
    }
    return res;
}

Polynom operator+(const Polynom& lhs, const Polynom& rhs){
    Polynom res(std::max(lhs.size(), rhs.size()));
    res+=rhs;
    res+=lhs;
    return res;
}

Polynom operator-(const Polynom& lhs, const Polynom& rhs){
    Polynom res(std::max(lhs.size(), rhs.size()));
    res+=lhs;
    res-=rhs;
    return res;
}

Polynom operator*(const Polynom& lhs, const Polynom& rhs){
    Polynom res(lhs.size() + rhs.size(), 0);
    for(size_t i = 0; i < lhs.size(); i++)
    {
        for(size_t j = 0; j < rhs.size(); j++)
        {
            res[i + j] += lhs[i] * rhs[j];
        }
    }
    return res;
}

Polynom operator*(const double& lhs, const Polynom& rhs)
{
    Polynom res(rhs);
    for(size_t i = 0; i < rhs.size(); i++)
    {
        res[i] *= lhs;
    }
    return res;
}

Polynom operator*(const Polynom& lhs, const double& rhs)
{
    Polynom res(lhs);
    for(size_t i = 0; i < lhs.size(); i++)
    {
        res[i] *= rhs;
    }
    return res;
}

std::istream& operator>>(std::istream& is, Polynom& pol)
{
    int n;
    is >> n;
    pol = Polynom(n);
    for(size_t i = 0; i < n; i++)
    {
        is >> pol[i];
    }
    return is;
}

Polynom operator/(const Polynom& lhs, const double& rhs)
{
    Polynom res(lhs);
    for(size_t i = 0; i < lhs.size(); i++)
    {
        res[i] /= rhs;
    }
    return res;
}

std::ostream& operator<<(std::ostream& os, const Polynom& pol){
    for(size_t i = 0; i < pol.size(); i++)
    {
        os << pol[i] << ' ';
    }
    os << std::endl;
    return os;
}

double RationalFunction::getValue(double x)
{
    return num_.getValue(x)/denum_.getValue(x); /// needs fixing
}

RationalFunction operator+(const RationalFunction& lhs, const RationalFunction& rhs)
{
    Polynom n = lhs.num_ * rhs.denum_ + rhs.num_ * lhs.denum_;
    Polynom d = lhs.denum_ * rhs.denum_;
    return RationalFunction(n, d);
}

RationalFunction operator-(const RationalFunction& lhs, const RationalFunction& rhs)
{
    Polynom n = lhs.num_ * rhs.denum_ - rhs.num_ * lhs.denum_;
    Polynom d = lhs.denum_ * rhs.denum_;
    return RationalFunction(n, d);
}
RationalFunction operator*(const RationalFunction& lhs, const RationalFunction& rhs)
{
    Polynom n = lhs.num_ * rhs.num_;
    Polynom d = lhs.denum_ * rhs.denum_;
    return RationalFunction(n, d);
}
RationalFunction operator*(const double& lhs, const RationalFunction& rhs)
{
    Polynom n = rhs.num_ * lhs;
    Polynom d = rhs.denum_;
    return RationalFunction(n, d);
}

RationalFunction operator*(const RationalFunction& lhs, const double& rhs)
{
    Polynom n = lhs.num_ * rhs;
    Polynom d = lhs.denum_;
    return RationalFunction(n, d);
}

RationalFunction operator/(const RationalFunction& lhs, const RationalFunction& rhs)
{
    Polynom n = lhs.num_ * rhs.denum_;
    Polynom d = lhs.denum_ * rhs.num_;
    return RationalFunction(n, d);
}

std::ostream& operator<<(std::ostream& os, const RationalFunction& rf)
{
    os << rf.num_ << std::endl;
    os << rf.denum_ << std::endl;
    return os;
}

RationalFunction operator/(const RationalFunction& lhs, const double& rhs)
{
    Polynom n = lhs.num_ / rhs;
    Polynom d = lhs.denum_;
    return RationalFunction(n, d);
}



