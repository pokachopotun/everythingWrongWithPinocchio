#include "mainwindow.h"
#include "ui_mainwindow.h"

#include "solution.h"
#include <iostream>
#include <fstream>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::doNewtonLike()
{
   using namespace  std;
   ifstream in("input.txt");

   int n;
   in >> n;
   vector<double> xin(n), fin(n);
   QVector<double> xi;
   QVector<double> fi;
   for(int i =0; i < n; i++)
   {
       in >> xin[i];
       xi.push_back(xin[i]);
       in >> fin[i];
       fi.push_back(fin[i]);
   }
   newtonLike newton(xin, fin, n/2);
   QVector<double> x;
   QVector<double> f;

   for(double i = xin[0]-0.1; i<=xin.back() + 0.1; i+=0.01)
   {
       x.push_back(i);
       f.push_back(newton.ans.getValue(i));
       if( abs( f.back() ) > 50)
       {
           x.pop_back();
           f.pop_back();
       }
   }
   ui->plot->xAxis->setLabel("x");
   ui->plot->yAxis->setLabel("y");
   ui->plot->addGraph();
   ui->plot->graph(0)->setPen(QPen(Qt::red));
   ui->plot->graph(0)->addData(x, f);
   ui->plot->addGraph();
   ui->plot->graph(1)->setPen(QPen(Qt::blue));
   ui->plot->graph(1)->setLineStyle(QCPGraph::lsNone);
   ui->plot->graph(1)->setScatterStyle(QCPScatterStyle(QCPScatterStyle::ssCircle, 5));
   ui->plot->graph(1)->addData(xi, fi);
   ui->plot->rescaleAxes();
   ui->plot->replot();
}
void MainWindow::doNevileLike()
{
    using namespace  std;
    ifstream in("input1.txt");
    int n;
    in >> n;
    vector<double> xin(n), fin(n);
    QVector<double> xi;
    QVector<double> fi;
    for(int i =0; i < n; i++)
    {
        in >> xin[i];
        xi.push_back(xin[i]);
        in >> fin[i];
        fi.push_back(fin[i]);
    }
    double point;
    in >> point;
    nevilleLike nl;
    QVector<double> x;
    QVector<double> f;
    for(double i = xin[0]-0.1; i<=xin.back() + 0.1; i+=0.01)
    {
        x.push_back(i);
        f.push_back(nl.getRes(xin,fin, 4, 4, i));
        if( abs( f.back() ) > 50)
        {
            x.pop_back();
            f.pop_back();
        }
    }
    ui->plot->xAxis->setLabel("x");
    ui->plot->yAxis->setLabel("y");
    ui->plot->addGraph();
    ui->plot->graph(0)->setPen(QPen(Qt::red));
    ui->plot->graph(0)->addData(x, f);
    ui->plot->addGraph();
    ui->plot->graph(1)->setPen(QPen(Qt::blue));
    ui->plot->graph(1)->setLineStyle(QCPGraph::lsNone);
    ui->plot->graph(1)->setScatterStyle(QCPScatterStyle(QCPScatterStyle::ssCircle, 5));
    ui->plot->graph(1)->addData(xi, fi);
    ui->plot->rescaleAxes();
    ui->plot->replot();

}

void MainWindow::on_newtonButton_clicked()
{
    ui->plot->clearGraphs();
    ui->plot->replot();
    doNewtonLike();
}

void MainWindow::on_nevileButton_clicked()
{
    ui->plot->clearGraphs();
    ui->plot->replot();
    doNevileLike();

}
