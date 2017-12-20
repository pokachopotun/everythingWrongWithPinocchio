#define _USE_MATH_DEFINES
#include "glut.h"
#include <math.h>
GLUnurbsObj* nobj;
GLfloat lightposition[] = { 13, 0, -5, 0 };
void init(void) {
    glClearColor(1, 1, 1, 1);
    nobj = gluNewNurbsRenderer();
    //gluNurbsProperty(nobj, GLU_SAMPLING_TOLERANCE, 25.0);
	glLightfv(GL_LIGHT0, GL_POSITION, lightposition);
	glEnable(GL_DEPTH_TEST);
	glEnable(GL_LIGHTING);
	glEnable(GL_LIGHT0);
	glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, 1);

}

bool flag;

void DisplaySurface()
{
	//  glClear(GL_COLOR_BUFFER_BIT);
	//  glLineWidth(3);
	//glClearColor(0.0, 0.0, 0.7, 1);
	//GLUnurbsObj* nobj = gluNewNurbsRenderer();
	//glEnable(GL_DEPTH_TEST);
	//gluNurbsProperty(nobj, GLU_SAMPLING_TOLERANCE, 25.0);

	GLfloat ctlarray[3][7][4] = {


		0.0, 0.0, 0.0, 1.0,
		0.0, 0.1, 0.1, 1.0,
		0.0, 0.0, 0.2, 1.0,
		0.0, 0.1, 0.3, 1.0,
		0.0, 0.0, 0.4, 1.0,
		0.0, 0.1, 0.5, 1.0,
		0.0, 0.0, 0.6, 1.0,

		0.0, 0.0, 0.0, 1.0,
		0.1, 0.1, 0.1, 1.0,
		0.2, 0.0, 0.2, 1.0,
		0.3, 0.1, 0.3, 1.0,
		0.4, 0.0, 0.4, 1.0,
		0.5, 0.1, 0.5, 1.0,
		0.6, 0.0, 0.6, 1.0,

		0.0, 0.0, 0.0, 1.0,
		0.1, 0.1, 0.1, 1.0,
		0.2, 0.0, 0.2, 1.0,
		0.3, 0.1, 0.3, 1.0,
		0.4, 0.0, 0.4, 1.0,
		0.5, 0.1, 0.5, 1.0,
		0.6, 0.0, 0.6, 1.0,

		//0.0, 0.0, 0.0, 1.0,
		//0.1, 0.1, 0.1, 1.0,
		//0.2, 0.0, 0.2, 1.0,
		//0.3, 0.1, 0.3, 1.0,
		//0.4, 0.0, 0.4, 1.0,
		//0.5, 0.1, 0.5, 1.0,
		//0.6, 0.0, 0.6, 1.0,

		//0.0, 0.0, 0.0, 1.0,
		//0.1, 0.1, 0.0, 1.0,
		//0.2, 0.0, 0.0, 1.0,
		//0.3, 0.1, 0.0, 1.0,
		//0.4, 0.0, 0.0, 1.0,
		//0.5, 0.1, 0.0, 1.0,
		//0.6, 0.0, 0.0, 1.0,
	};


	for (int i = 0; i < 7; i++) {
		ctlarray[2][i][0] *= static_cast<GLfloat>(sin(M_PI / 4));
		ctlarray[2][i][2] *= static_cast<GLfloat>(cos(M_PI / 4));
		ctlarray[1][i][0] *= static_cast<GLfloat>(sin(M_PI / 6));
		ctlarray[1][i][2] *= static_cast<GLfloat>(cos(M_PI / 6));
		//ctlarray[3][i][0] *= static_cast<GLfloat>(sin(M_PI / 3));
		//ctlarray[3][i][2] *= static_cast<GLfloat>(cos(M_PI / 3));
	}
	//glPointSize(500);
	//glColor3d(1, 0, 0);
	//glBegin(GL_POINTS);
	//for(int j = 0; j < 3; j++){
	//	for (int i = 0; i < 7; i++) {
	//		glVertex3d(ctlarray[j][i][0] , ctlarray[j][i][1], ctlarray[j][i][2]);
	//	}
	//}
	//glEnd();
	GLfloat knotU[] = { 0,0,0,0,1,2,3,4,5,6,6,6,6 };
	GLfloat knotW[] = { 0, 0, 1, 1, 2, 2};

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glRotatef(-0.1, 1.0, 1.0, 1.0);
    glColor3f(1.0, 0, 0);
    gluBeginSurface(nobj);
    gluNurbsSurface(nobj, 13, knotU, 6, knotW, 4, 7 * 4, &ctlarray[0][0][0], 4, 2, GL_MAP2_VERTEX_4);
    gluEndSurface(nobj);

    //glEnd();

    glutPostRedisplay();
    glutSwapBuffers();
}

void main()
{
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_DEPTH);
	//glEnable(GL_CULL_FACE);
    glutInitWindowSize(1000, 1000);
    glutInitWindowPosition(100, 100);
    glutCreateWindow("main");
    init();
    glutDisplayFunc(DisplaySurface);
    glutMainLoop();

}