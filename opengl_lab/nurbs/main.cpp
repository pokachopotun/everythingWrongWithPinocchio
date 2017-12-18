#define _USE_MATH_DEFINES
#include "freeglut/include/GL/glut.h" 
#include "math.h"
#include "mathadditionals.h"
GLUnurbsObj* nobj;

//void init() {
//
//	// Set the current clear color to black and the current drawing color to
//	// white.
//	glClearColor(0.0, 0.0, 0.0, 1.0);
//	glColor3f(1.0, 1.0, 1.0);
//
//	// Set the camera lens to have a 60 degree (vertical) field of view, an
//	// aspect ratio of 4/3, and have everything closer than 1 unit to the
//	// camera and greater than 40 units distant clipped away.
//	glMatrixMode(GL_PROJECTION);
//	glLoadIdentity();
//	gluPerspective(60.0, 4.0 / 3.0, 1, 40);
//
//	// Position camera at (4, 6, 5) looking at (0, 0, 0) with the vector
//	// <0, 1, 0> pointing upward.
//	glMatrixMode(GL_MODELVIEW);
//	glLoadIdentity();
//	gluLookAt(4, 6, 5, 0, 0, 0, 0, 1, 0);
//}

const int rcnt = 4;
double xi[rcnt];
double ti[rcnt];
const int k = 3;
Matrix Nmat(k, rcnt), NmatRev(rcnt, k), D(rcnt, 2), B(rcnt, 2);
int tmax = rcnt - k + 1;
const int knotWsize = k * 2 + rcnt - 1;
GLfloat knotW[knotWsize];


void init_knotw() {

	for (int i = 0; i < rcnt; i++) {
		knotW[i + k - 1] = i;
	}

	for (int i = 0; i < k; i++) {
		knotW[i] = 0;
		knotW[knotWsize - 1 - i] = rcnt;
	}
}


double dist(double x0, double y0, double x1, double y1) {
	return sqrt((x1 - x0) * (x1 - x0) + (y1 - y0)*(y1 - y0));
}

void init_ti() {
	ti[0] = 0;
	for (int i = 1; i < rcnt; i++) {
		 double d = dist(D[i][0], D[i][1], D[i - 1][0], D[i - 1][1]);
		ti[i] = ti[i - 1] + d;
	}
	//for (int i = 1; i < rcnt - 1; i++) {
	//	ti[i] /= ti[rcnt - 1];
	//}
}

double Nikt(int i, int k, double t) {
	if (k == 1) {
		if (ti[i - 1] <= t && t < ti[i]) {
			return 1.0;
		}
		else
			return 0.0;
	}
	double a = (t - ti[i - 1]) * Nikt(i, k - 1, t);
	double c = (ti[i + k - 2] - ti[i - 1]);
	
	double b = (ti[i + k - 1] - t) * Nikt(i + 1, k - 1, t);
	double d = (ti[i + k - 1] - ti[i]);
	if (c == 0.0) {
		a = 0;
	}
	else {
		a /= c;
	}
	if (d == 0.0) {
		b = 0;
	}
	else {
		b /= d;
	}
	return a + b;
}

void init_mat() {

	for (int i = 0; i < rcnt; i++) {
		D[i][0] = i * 2.0 * M_PI / rcnt;
		D[i][1] = cos(D[i][0]);
	}
	/*for (int i = 0; i < rcnt; i++) {
		D[i][0] /= D[rcnt - 1][0];
	}*/
	init_ti();
	for (int i = 0; i < rcnt; i++) {
		for (int j = 0; j < k; j++) {
			Nmat[j][i] = Nikt(i + 1, j + 1, ti[i]);
		}
	}
	Matrix NT(Nmat.cols(), Nmat.rows());
	for (int i = 0; i < Nmat.rows(); i++)
		for (int j = 0; j < Nmat.cols(); j++)
			NT[j][i] = Nmat[i][j];
	Matrix tmp = NT * Nmat;
	B =  tmp.getInverse() * NT * D;

}

void DisplaySurface()
{
	//	glClear(GL_COLOR_BUFFER_BIT);
	//	glLineWidth(3);4
	glClearColor(0.0, 0.0, 0.7, 1);
	GLUnurbsObj* nobj = gluNewNurbsRenderer();
	glEnable(GL_DEPTH_TEST);
	gluNurbsProperty(nobj, GLU_SAMPLING_TOLERANCE, 25.0);
	GLfloat one_direction[rcnt][4];
	for (int i = 0; i < rcnt; i++) {
		one_direction[i][0] = B[i][0];
		one_direction[i][1] = B[i][1];
		one_direction[i][2] = 0.0;
		one_direction[i][3] = 1.0;
	}


	const int N = 20;
	GLfloat ctlarray[N][rcnt][4];
	
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < rcnt; j++) {
			GLfloat c = cos(M_PI * 2.0 * static_cast<GLfloat>(i) / (N - 2));
			GLfloat s = sin(M_PI * 2.0 * static_cast<GLfloat>(i) / (N - 2)); 
			ctlarray[i][j][0] = one_direction[j][0] * c - one_direction[j][2] * s;
			ctlarray[i][j][1] = one_direction[j][1];
			ctlarray[i][j][2] = one_direction[j][0] * s + one_direction[j][2] * c;
			ctlarray[i][j][3] = one_direction[j][3];
		}
	}

	const int knotUsize = N - 4 + 1 + 6;
	GLfloat knotU[knotUsize];
	

	for (int i = 0; i < N; i++) {
		knotU[i + 3] = i;
	}

	for (int i = 0; i < 4; i++) {
		knotU[i] = 0;
		knotU[knotUsize - 1 - i] = N;
	}


	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glRotatef(0.5, -1, 0.5, 0.2);
	glColor3f(1, 0, 0);

	gluBeginSurface(nobj);
	glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
	gluNurbsSurface(nobj, knotUsize, knotU, knotWsize, knotW, rcnt * 4, 4, &ctlarray[0][0][0], 4, k, GL_MAP2_VERTEX_4);
	gluEndSurface(nobj);

	glEnd();

	glutPostRedisplay();
	glutSwapBuffers();
}

void main(int argcp, char *argv[])
{

	glutInit(&argcp, argv);
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH);
	glutInitWindowSize(300, 300);
	glutInitWindowPosition(100, 100);
	glutCreateWindow(" ");
	//init();
	//init_ti();
	init_knotw();
	init_mat();

	glEnable(GL_LIGHTING);
	glEnable(GL_LIGHT0);
	//glMatrixMode(GL_PROJECTION);
	GLfloat lightpos[] = { .5, 1., 1., 0. };
	glLightfv(GL_LIGHT0, GL_POSITION, lightpos);
	glutDisplayFunc(DisplaySurface);
	glutMainLoop();

}



 //This is a simple introductory program; its main window contains a static
 //picture of a torus.  The program illustrates viewing by choosing a camera
 //setup with gluLookAt(), which is conceptually simpler than transforming
 //objects to move into a predefined view volume.

//#ifdef __APPLE_CC__
//#include <GLUT/glut.h>
//#else
//#include "freeglut/include/GL/glut.h"
//#include "math.h"
//#endif
//
//// Clears the window and draws the torus.
//void display() {
//
//	glClear(GL_COLOR_BUFFER_BIT);
//
//	// Draw a white torus of outer radius 3, inner radius 0.5 with 15 stacks
//	// and 30 slices.
//	glColor3f(1.0, 1.0, 1.0);
//	glutWireTorus(0.5, 3, 15, 30);
//
//	// Draw a red x-axis, a green y-axis, and a blue z-axis.  Each of the
//	// axes are ten units long.
//	glBegin(GL_LINES);
//	glColor3f(1, 0, 0); glVertex3f(0, 0, 0); glVertex3f(10, 0, 0);
//	glColor3f(0, 1, 0); glVertex3f(0, 0, 0); glVertex3f(0, 10, 0);
//	glColor3f(0, 0, 1); glVertex3f(0, 0, 0); glVertex3f(0, 0, 10);
//	glEnd();
//
//	glFlush();
//}
//
//// Sets up global attributes like clear color and drawing color, and sets up
//// the desired projection and modelview matrices.
//void init() {
//
//	// Set the current clear color to black and the current drawing color to
//	// white.
//	glClearColor(0.0, 0.0, 0.0, 1.0);
//	glColor3f(1.0, 1.0, 1.0);
//
//	// Set the camera lens to have a 60 degree (vertical) field of view, an
//	// aspect ratio of 4/3, and have everything closer than 1 unit to the
//	// camera and greater than 40 units distant clipped away.
//	glMatrixMode(GL_PROJECTION);
//	glLoadIdentity();
//	gluPerspective(60.0, 4.0 / 3.0, 1, 40);
//
//	// Position camera at (4, 6, 5) looking at (0, 0, 0) with the vector
//	// <0, 1, 0> pointing upward.
//	glMatrixMode(GL_MODELVIEW);
//	glLoadIdentity();
//	gluLookAt(4, 6, 5, 0, 0, 0, 0, 1, 0);
//}
//
//// Initializes GLUT, the display mode, and main window; registers callbacks;
//// does application initialization; enters the main event loop.
//int main(int argc, char** argv) {
//	glutInit(&argc, argv);
//	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
//	glutInitWindowPosition(80, 80);
//	glutInitWindowSize(800, 600);
//	glutCreateWindow("A Simple Torus");
//	glutDisplayFunc(display);
//	init();
//	glutMainLoop();
//}