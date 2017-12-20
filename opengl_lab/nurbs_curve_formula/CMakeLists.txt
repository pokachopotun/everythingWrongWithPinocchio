project(nurbs_curve_formula  CXX)

add_executable(nurbs_curve_formula nurbs_curve_formula.cpp)

#target_link_libraries(nurbs_curve_formula ${GLUT_LIBS})

include_directories(nurbs_curve_formula ${GLUT_INCLUDE})

install(TARGETS nurbs_curve_formula
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib/static)