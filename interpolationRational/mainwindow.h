#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();
    void doNewtonLike();
    void doNevileLike();

private slots:
    void on_newtonButton_clicked();

    void on_nevileButton_clicked();

private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
