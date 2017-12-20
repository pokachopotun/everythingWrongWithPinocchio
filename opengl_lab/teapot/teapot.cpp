#include <iostream>
#include "glut.h"


GLUquadricObj * theqw;

GLfloat lightposition[] = { 13, 0, -5, 0 };

void init() {
    glClearColor(0.1, 0.98, 0.3, 1);
    theqw = gluNewQuadric();
    //glEnable(GL_COLOR_MATERIAL);
    glLightfv(GL_LIGHT0, GL_POSITION, lightposition);
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_LIGHTING);
    glEnable(GL_LIGHT0);
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, 1);
}


void Display() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glRotatef(0.001, 0.001, 0.001, 0.001);
    glColor3f(255, 255, 0);
    glutSolidTeapot(0.3);
    glutPostRedisplay();
    glutSwapBuffers();
}

int main() {
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH);
    glutInitWindowSize(480, 480);
    glutInitWindowPosition(100, 100);
    glutCreateWindow("tmp");
    init();
    glutDisplayFunc(Display);
    glutMainLoop();
    return 0;
}

