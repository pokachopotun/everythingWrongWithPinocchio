project(lab_opengl  CXX)


#add_subdirectory(glut)

link_directories(${CMAKE_CURRENT_SOURCE_DIR}/glut)

set(GLUT_LIBS glut)

set(GLUT_INCLUDE ${CMAKE_CURRENT_SOURCE_DIR}/glut)

add_subdirectory(teapot)

add_subdirectory(3d_color)
add_subdirectory(nurbs_surface)
add_subdirectory(nurbs_curve_formula)