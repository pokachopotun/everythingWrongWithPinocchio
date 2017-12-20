#include "glut.h"
#include <cstdio>

GLUquadricObj * theqw;
GLenum mode;
GLuint hits = 0;
void drawsphera()
{
    GLfloat koort[][2] = { {100, 140}, {120, 120}, {140, 140}, {160, 80} };
    for (int i = 0; i < 4; i++) {
        switch (i) {
        case 0: glColor4f(1, 0, 0, 0.2); break;
        case 1: glColor4f(0, 1, 1, 0.4); break;
        case 2: glColor4f(0, 0, 1, 0.7); break;
        case 3: glColor4f(0, 1, 0, 0.9); break;
        default:
            return;
        }
        if (mode == GL_SELECT) glLoadName(i);
        glPushMatrix();
        glTranslatef(koort[i][0], koort[i][1], -50);
        gluSphere(theqw, 40, 50, 50);
        glPopMatrix();
    }
}

void init() {
    glClearColor(1.0, 1.0, 1.0, 1);
    GLfloat lightposition[] = { 0, 0, -100, 0 };
    theqw = gluNewQuadric();
    glEnable(GL_DEPTH_TEST);
    glLightfv(GL_LIGHT0, GL_POSITION, lightposition);
    glEnable(GL_LIGHTING);
    glEnable(GL_LIGHT0);
    glEnable(GL_COLOR_MATERIAL);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    mode = GL_RENDER;
}


void pick(int button, int state, int x, int y) {
    GLint viewport[4];
    GLuint selectBuf[16];
    if (button != GLUT_LEFT_BUTTON || state != GLUT_DOWN)
        return;

    glGetIntegerv(GL_VIEWPORT, viewport);
    glSelectBuffer(16, selectBuf);
    mode = GL_SELECT;
    glRenderMode(mode);
    glInitNames();
    glPushName(0);
    glMatrixMode(GL_PROJECTION);
    glPushMatrix();
    glLoadIdentity();
    gluPickMatrix((GLdouble)x, (GLdouble)y, 1.0, 1.0, viewport);
    glOrtho(0, 240, 0, 240, 10, 240);
    drawsphera();
    glMatrixMode(GL_PROJECTION);
    glPopMatrix();
    hits = 0;
    for (int i = 3; i < 16; i+=4) {
        hits += (GLuint)(selectBuf[i] != 3435973836);
    }
    mode = GL_RENDER;
    printf("%d\n", hits);
    glRenderMode(mode);
    glutSwapBuffers();
    glutPostRedisplay();
}
void Display() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glDepthMask(GL_FALSE);
    drawsphera();
    glDepthMask(GL_TRUE);
    glutPostRedisplay();
    glutSwapBuffers();
}

void reshape(int w, int h) {
    glViewport(0, 0, w, h);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0, 240, 240, 0, 10, 240);
    glMatrixMode(GL_MODELVIEW);
}

int main() {
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH);
    glutInitWindowSize(240, 240);
    glutInitWindowPosition(100, 100);
    glutCreateWindow(" ");
    init();
    glutMouseFunc(pick);
    glutReshapeFunc(reshape);
    glutDisplayFunc(Display);
    glutMainLoop();
    return 0;
}