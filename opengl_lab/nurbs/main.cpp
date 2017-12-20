#define _USE_MATH_DEFINES
#include "GL/glut.h" 
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

//const double eps = 1e-6;
const int rcnt = 20;
const int n = 5;
 
GLfloat ti[rcnt];
const int k = 3;
Matrix Nmat(rcnt, n), D(rcnt, 2), B(n, 2);
const int tmax = n - k + 1;
const int knotWsize = k * 2 + tmax - 1;
GLfloat xi[knotWsize + 1];
GLfloat knotW[knotWsize];


void init_knotw() {

	for (int i = 0; i <= tmax; i++) {
		knotW[i + k - 1] = i;
	}

	for (int i = 0; i < k; i++) {
		knotW[i] = 0;
		knotW[knotWsize - 1 - i] = tmax;
	}
}


double dist(GLfloat x0, GLfloat y0, GLfloat x1, GLfloat y1) {
	return sqrt((x1 - x0) * (x1 - x0) + (y1 - y0)*(y1 - y0));
}


GLfloat Nikt(int i, int k1, GLfloat t) {
	if (k1 == 1) {
		if (xi[i] <= t && t <= xi[i + 1]) {
			return 1.0;
		}
		else
			return 0.0;
	}
	GLfloat a = (t - xi[i]) * Nikt(i, k1 - 1, t);
	GLfloat c = (xi[i + k1 - 1] - xi[i]);
	
	GLfloat b = (xi[i + k1] - t) * Nikt(i + 1, k1 - 1, t);
	GLfloat d = (xi[i + k1] - xi[i + 1]);
	GLfloat ans = 0;
	if (c != 0.0) {
		ans += a / c;
	}
	if(d != 0.0){
		ans += b / d;
	}
	return ans;
}

//GLfloat matrix[2 * n + 2][2 * k + 2];
//
//void calc_matrix(GLfloat t)
//{
//	for (int i = 0; i <= 2 * n + 1; i++) {
//		for (int j = 0; j <= 2 * k + 1; j++) {
//			matrix[i][j] = 0;
//		}
//	}
//	for (int i = 0; i <= 2 * n + 1; i++) {
//		if (ti[i] <= t && t < ti[i + 1])
//			matrix[i][1] = 1.0;
//		else
//			matrix[i][1] = 0.0;
//	}
//	for (int ki = 2; ki <= 2 * k + 1; ki++) {
//		for (int i = 0; i <= 2 * n + 1; i++) {
//
//			if ((ti[i + ki - 1] - ti[i]) != 0)
//				matrix[i][ki] += (t - ti[i]) * matrix[i][ki - 1] / (ti[i + ki - 1] - ti[i]);
//			if ((ti[i + ki] - ti[i + 1]) != 0)
//				matrix[i][ki] += (ti[i + ki] - t) * matrix[i + 1][ki - 1] / (ti[i + ki] - ti[i + 1]);
//		}
//	}
//}

void init_mat() {

	for (int i = 0; i < rcnt; i++) {
		D[i][0] = i * M_PI / 5;
		D[i][1] = sin(D[i][0]);
	}
	//D[0][0] = 0;
	//D[0][1] = 0;
	//D[1][0] = 1.5;
	//D[1][1] = 2;
	//D[2][0] = 3;
	//D[2][1] = 2.5;
	//D[3][0] = 4.5;
	//D[3][1] = 2;
	//D[4][0] = 6;
	//D[4][1] = 0;
	/*for (int i = 0; i < rcnt; i++) {
		D[i][0] /= D[rcnt - 1][0];
	}*/
	ti[0] = 0;
	for (int i = 1; i < rcnt; i++) {
		ti[i] = ti[i - 1] + dist(D[i][0], D[i][1], D[i - 1][0], D[i - 1][1]);
	}

	for (int i = 1; i <= knotWsize; i++) {
		xi[i] = ti[rcnt - 1] * static_cast<GLfloat>(knotW[i - 1]) / knotW[knotWsize - 1];
	}

	for (int i = 1; i <= n; i++) {
		for (int j = 1; j <= rcnt; j++) {
			Nmat[j - 1][i - 1] = Nikt(i, k, ti[j - 1]);
		}
	}
	//Nmat[4][4] = 1;
	Matrix NT(Nmat.cols(), Nmat.rows());
	for (int i = 0; i < Nmat.rows(); i++)
		for (int j = 0; j < Nmat.cols(); j++)
			NT[j][i] = Nmat[i][j];
	Matrix tmp = NT * Nmat;
	B =  tmp.getInverse() * NT * D;
	//B = Nmat.getInverse() * D;	
	//Matrix test = Nmat * Nmat.getInverse();
}

void DisplaySurface()
{
	//	glClear(GL_COLOR_BUFFER_BIT);
	//	glLineWidth(3);4
	glClearColor(0.0, 0.0, 0.7, 1);
	GLUnurbsObj* nobj = gluNewNurbsRenderer();
	glEnable(GL_DEPTH_TEST);
	gluNurbsProperty(nobj, GLU_SAMPLING_TOLERANCE, 25.0);
	GLfloat one_direction[n][4];
	for (int i = 0; i < n; i++) {
		one_direction[i][0] = B[i][0]/10;
		one_direction[i][1] = B[i][1]/10;
		one_direction[i][2] = 0.0;
		one_direction[i][3] = 1.0;
	}


	const int N = 20;
	GLfloat ctlarray[N][n][4];
	
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < n; j++) {
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
	gluNurbsSurface(nobj, knotUsize, knotU, knotWsize, knotW, n * 4, 4, &ctlarray[0][0][0], 4, k, GL_MAP2_VERTEX_4);
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