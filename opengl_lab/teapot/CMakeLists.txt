project(teapot  CXX)

add_executable(teapot teapot.cpp)

#target_link_libraries(teapot ${GLUT_LIBS})

include_directories(teapot ${GLUT_INCLUDE})

install(TARGETS teapot
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib/static)