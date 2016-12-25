#-------------------------------------------------
#
# Project created by QtCreator 2016-12-26T00:07:05
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets printsupport

TARGET = interpolationRational
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    mathadditionals/mathadditionals.cpp \
    qcustomplot.cpp

HEADERS  += mainwindow.h \
    mathadditionals/mathadditionals.h \
    qcustomplot.h \
    solution.h

FORMS    += mainwindow.ui
