#include "glut.h"
GLUnurbsObj* nobj;




const int n = 5, k = 5;  

//constexpr int tmaxint = n - k + 2;
//constexpr int xsize = 2 * k + tmaxint - 1;
//GLfloat tmax = n - k + 2;

const int tmaxint = n + k;
const int xsize = tmaxint;

GLfloat tmax = static_cast<GLfloat>(tmaxint);

GLfloat tleft = k - 1, tright = n + 1, dt = 0.01;
GLfloat x[xsize] = {0};

void init(void) {
    if (false) {
        for (int i = 0; i < k; i++) {
            x[i] = static_cast<GLfloat>(0);
            x[xsize - 1 - i] = tmax;
        }
        for (int i = 1; i < tmaxint; i++) {
            x[i + k - 1] = static_cast<GLfloat>(i);
        }
    }
    else
    {
        for (int i = 0; i < xsize; i++) {
            x[i] = static_cast<GLfloat>(i);
        }
    }
}


GLfloat matrix[2 * n + 2][2 * k + 2];

void calc_matrix(GLfloat t)
{
    for (int i = 0; i <= 2 * n + 1; i++) {
        for (int j = 0; j <= 2 * k + 1; j++) {
            matrix[i][j] = 0;
        }
    }
    for (int i = 0; i <= 2 * n + 1; i++) {
        if (x[i] <= t && t < x[i + 1])
            matrix[i][1] = 1.0;
        else
            matrix[i][1] = 0.0;
    }
    for (int ki = 2; ki <= 2 * k + 1; ki++) {
        for (int i = 0; i <= 2 * n + 1; i++) {

                 if ((x[i + ki - 1] - x[i]) != 0)
                     matrix[i][ki] += (t - x[i]) * matrix[i][ki - 1] / (x[i + ki - 1] - x[i]);
                 if ((x[i + ki] - x[i + 1]) != 0)
                     matrix[i][ki] += (x[i + ki] - t) * matrix[i + 1][ki - 1] / (x[i + ki] - x[i + 1]);
        }
    }
}
//
//GLfloat N(int i, int k, GLfloat t) {
//
//    if (k == 1.0) {
//        if (x[i] <= t && t < x[i + 1])
//             return 1.0;
//        return 0.0;
//    }
//    
//    GLfloat left = 0, right = 0;
//     if ((x[i + k - 1] - x[i]) != 0)
//         left = (t - x[i]) * N(i, k - 1, t) / (x[i + k - 1] - x[i]);
//     if ((x[i + k] - x[i + 1]) != 0)
//         right = (x[i + k] - t) * N(i + 1, k - 1, t) / (x[i + k] - x[i + 1]);
//     GLfloat val = left + right;
//    return val;
//}

void DisplayCurve()
{
    //  glClear(GL_COLOR_BUFFER_BIT);
    //  glLineWidth(3);
    glClearColor(0.0, 0.0, 0.7, 1);
    glEnable(GL_DEPTH_TEST);

    GLfloat ctlarray[7][4] = {
        0.0, 0.0, 0.0, 1.0,
        0.1, 0.5, 0.0, 1.0,
        0.2, 0.0, 0.0, 1.0,
        0.3, 0.5, 0.0, 1.0,
        0.4, 0.0, 0.0, 1.0,
        0.5, 0.5, 0.0, 1.0,
        0.6, 0.0, 0.0, 1.0,
    };


    /*GLfloat knotW[] = { 0,0,1,1 };*/

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    //glRotatef(-0.1, -0.1, 0.1, 0.1);
    glColor3d(1, 0, 0);
    glPointSize(10);
    glBegin(GL_POINTS);
    glColor3d(1, 0, 0);
    for (GLfloat t = tleft; t <=  tright ; t += dt) {
        GLfloat xres = 0, yres = 0;
        calc_matrix(t);
        for (int i = 0; i <= n; i++) {
            GLfloat nik = matrix[i][k];
            xres += nik * ctlarray[i][0];
            yres += nik * ctlarray[i][1];
        }
        glVertex3d(xres, yres, 0);
    }
    glColor3d(0, 1, 0);
    for (int i = 0; i < n + 1; i++) {
        glVertex3d(ctlarray[i][0], ctlarray[i][1], 0);
    }
    glColor3d(1, 1, 0);
    for (GLfloat t = tleft; t <= tright; t += dt) {
        calc_matrix(t);
        for (int i = 0; i <= n; i++) {
                GLfloat nik = matrix[i][k];
                glVertex3d(t/5.0 - 0.5, nik/2.0 - 0.5, 0);
            }
        }
        
   
    glEnd();

    //glBegin(GL_POINTS);
    //    glColor3d(1, 0, 0);
    //    glVertex3d(0.5, 0.5, 0); // первая точка
    //    glVertex3d(0.75, 0.75, 0);   // вторая точка
    //    glVertex3d(0, 0, 0);
    //glEnd();
    //
    //gluBeginSurface(nobj);
    //gluNurbsSurface(nobj, 9, knotU, 4, knotW, 4, 7 * 4, &ctlarray[0][0][0], 2, 2, GL_MAP2_VERTEX_4);
    //gluEndSurface(nobj);

    glutPostRedisplay();
    glutSwapBuffers();
}

void main()
{
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH);
    glutInitWindowSize(300, 300);
    glutInitWindowPosition(100, 100);
    glutCreateWindow(" ");
    init();
    glutDisplayFunc(DisplayCurve);
    glutMainLoop();
}