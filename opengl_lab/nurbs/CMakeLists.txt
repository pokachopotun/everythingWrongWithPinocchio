project(nurbs)

include_directories(nurbs ${GLUT_INCLUDE})

add_executable(nurbs main.cpp freeglut/include/GL/glut.h mathadditionals.h mathadditionals.cpp)