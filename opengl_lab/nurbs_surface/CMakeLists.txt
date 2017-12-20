project(nurbs_surface  CXX)

add_executable(nurbs_surface nurbs_surface.cpp)

include_directories(nurbs_surface ${GLUT_INCLUDE})