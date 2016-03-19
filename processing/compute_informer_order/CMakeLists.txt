project(Neutron)
cmake_minimum_required(VERSION 2.8.12)

include(conanbuildinfo.cmake)
conan_basic_setup()

add_executable(compute_informer_order main.cpp)
target_link_libraries(compute_informer_order ${CONAN_LIBS})
