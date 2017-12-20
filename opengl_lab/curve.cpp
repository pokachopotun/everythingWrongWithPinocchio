#include <iostream>
#include "glut.h"
void DisplaySphere() {
    glClear(GL_COLOR_BUFFER_BIT);
    glColor3f(0, 1, 0);
    glPushMatrix();
    glTranslatef(0.001, 0, 0);
    glutWireSphere(1.0, 30, 30);
    glPopMatrix();
    glutPostRedisplay();
    glutSwapBuffers();
}


GLUnurbsObj * nobj;
GLfloat ctlarray[4][3] = { { -0.9, -0.8, 0.0 }
,{ -0.2, 0.8, 0.0 }
,{ 0.2, -0.5 , 0.0 }
,{ 0.9, 0.8, 0.0 }
};

void init() {
    glClearColor(1, 1, 1, 1);
    nobj = gluNewNurbsRenderer();
    gluNurbsProperty(nobj, GLU_SAMPLING_TOLERANCE, 25.0);
}

void Display() {
    GLfloat knot[] = { 0., 0., 0., 1. , 2., 2., 2. };
    glClear(GL_COLOR_BUFFER_BIT);
    glLineWidth(3.0);
    glColor3f(0, 0.3, 1);
    gluNurbsCurve(nobj, 7, knot, 3, &ctlarray[0][0], 3, GL_MAP1_VERTEX_3);
    glPointSize(4.0);
    glColor3f(0., 0., 1.);
    glBegin(GL_POINTS);
    for (int i = 0; i < 4; i++) {
        glVertex3f(ctlarray[i][0], ctlarray[i][1], ctlarray[i][2]);
    }
    glEnd();
    glFlush();
}

int main() {

    glutInitDisplayMode(GLUT_RGBA | GLUT_SINGLE);
    glutInitWindowSize(480, 480);
    glutInitWindowPosition(100, 100);
    glutCreateWindow("tmp");
    init();
    //glutDisplayFunc(DisplaySphere);
    glutDisplayFunc(Display);
    glutMainLoop();
    return 0;
}

